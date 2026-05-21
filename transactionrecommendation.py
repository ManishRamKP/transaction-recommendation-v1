import os
from flask import Flask, request, jsonify
import uuid
import json
import time
from datetime import datetime
import pandas as pd
import boto3
import requests  # to make HTTP requests to an external API

app = Flask(__name__)

# Load configuration from a JSON file
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# AWS Configurations
AWS_ACCESS_KEY_ID = config_data["aws"]["aws_access_key_id"]
AWS_SECRET_ACCESS_KEY = config_data["aws"]["aws_secret_access_key"]
REGION_NAME = config_data["aws"]["region_name"]
ATHENA_S3_OUTPUT = config_data["athena"]["s3_output_location"]

# Initialize a boto3 session
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

# Function to run Athena query
def run_athena_query(borrower_gst):
    client = session.client('athena', region_name=REGION_NAME)
    query = f"""
    SELECT 
    DATE AS inv_date,
    ptgstin, 
    ctin, 
    inv_no AS invoice_id, 
    taxval AS invoice_amount,
    lgl_nm
FROM 
    "prod-erp"."v_rpt_tally"
    WHERE 
    ptgstin = '{borrower_gst}'
    AND linkage_statuS= 'Unlinked'
    AND inv_delayin_dayS < 0
    AND inv_typ = 'Sales';

    """
    # print("Executing query:", query)
    # Execute the query
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'tally_data'},
        ResultConfiguration={'OutputLocation': ATHENA_S3_OUTPUT}
    )

    # Get the query execution ID
    query_execution_id = response['QueryExecutionId']
    for _ in range(10):
        query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']
        if query_execution_status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)  # Adjust sleep time as needed

    if query_execution_status == 'SUCCEEDED':
        result_data = client.get_query_results(QueryExecutionId=query_execution_id)
        column_names = [col['Label'] for col in result_data['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        rows = result_data['ResultSet']['Rows'][1:]  # Exclude column names

        data = []
        for row in rows:
            values = []
            for value in row['Data']:
                # Check if 'VarCharValue' exists; if not, append None or a default value
                if 'VarCharValue' in value:
                    values.append(value['VarCharValue'])
                else:
                    values.append(None)  # or some default value you see fit
            data.append(dict(zip(column_names, values)))

        return pd.DataFrame(data)
    else:
        print(f"Query failed: {query_status['QueryExecution']['Status']['StateChangeReason']}")
        return pd.DataFrame()
def compute_credit_score(borrower_gst, trader_gst, current_invoice_amount, ctin, invoice_id):
    api_url = "os.environ.get("CREDIT_SCORE_API_URL", "YOUR_CREDIT_SCORE_API_URL")"
    headers = { 'Authorization': 'Bearer ' + os.environ.get('API_BEARER_TOKEN', 'YOUR_BEARER_TOKEN')}
    additional_metrics = {
        "grn_present": False,
        "e_invoice_present": False,
        "e_way_bill_present": False,
        "trader_partner_confirmation": False
    }
    data = {
        "invoice_data": {
            "borrower_gst": borrower_gst,
            "trader_gst": trader_gst,
            "current_invoice_amount": current_invoice_amount
        },
        "additional_metrics": additional_metrics
    }
    try:

        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "base_score": result.get('base_score', 45.5),
                "credit_score": result.get('credit_score', 45.5),
                "request_id": result.get('request_id'),
                "timestamp": result.get('timestamp'),
                "highlights": result.get('highlights', []),
                "observations": result.get('observations', []),
                "final_verdict": result.get('final_verdict', "Insufficient data for verdict")
            }
        else:
            print(f"No data for ctin {ctin} and invoice_id {invoice_id}: {response.status_code}")
            return {"success": False}
    except requests.exceptions.RequestException as e:
        print(f"Request failed for ctin {ctin} and invoice_id {invoice_id}: {e}")
        return {"success": False}


# Function to calculate cumulative trade score
def calculate_cumulative_trade_score(df):
    if not df.empty and 'credit_score' in df.columns:
        df['credit_score'] = pd.to_numeric(df['credit_score'], errors='coerce')
        df['invoice_amount'] = pd.to_numeric(df['invoice_amount'], errors='coerce')
        return (df['credit_score'] * df['invoice_amount']).sum() / df['invoice_amount'].sum()
    return 45.5
@app.route('/transaction-recommendation', methods=['POST'])
def transaction_recommendation():
    data = request.json
    if not data:
        return jsonify({"error": "Request payload is missing."}), 400

    # Fetch 'total_amount' and 'borrower_gst' from request data
    total_amount_requested = data.get('total_amount')
    borrower_gst = data.get('borrower_gst')

    # Check for the presence of 'total_amount' and 'borrower_gst'
    if total_amount_requested is None or borrower_gst is None:
        return jsonify({"error": "Missing 'total_amount' or 'borrower_gst'."}), 400

    # Attempt to convert 'total_amount' to a float
    try:
        total_amount_requested = float(total_amount_requested)
    except ValueError:
        return jsonify({"error": "'total_amount' must be a number."}), 400

    # Check if 'borrower_gst' is a non-empty string
    if not isinstance(borrower_gst, str) or not borrower_gst.strip():
        return jsonify({"error": "'borrower_gst' must be a non-empty string."}), 400

    # Execute Athena query and process data
    try:
        df = run_athena_query(borrower_gst)
        if df.empty:
            return jsonify({"error": "No data returned from Athena query."}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to execute Athena query: {str(e)}"}), 500

    # Prepare the data
    df['invoice_amount'] = pd.to_numeric(df['invoice_amount'], errors='coerce').abs()
    df['inv_date'] = pd.to_datetime(df['inv_date'])
    df = df.sort_values(by=['inv_date', 'invoice_amount'], ascending=[True, True])

    accumulated_amount = 0.0
    selected_invoices = pd.DataFrame()
    for index, row in df.iterrows():
        invoice_amount = row['invoice_amount']
        if accumulated_amount + invoice_amount <= total_amount_requested:
            credit_details = compute_credit_score(row['ptgstin'], row['ctin'], invoice_amount, row['ctin'], row['invoice_id'])
            if credit_details["success"]:
                if credit_details["credit_score"] >= 30:
                    row['credit_details'] = credit_details
                    row['lgl_nm'] = row.get('lgl_nm')
                    selected_invoices = pd.concat([selected_invoices, pd.DataFrame([row]).reset_index(drop=True)], ignore_index=True)
                    accumulated_amount += invoice_amount
                else:
                    print(f"Skipping invoice {row['invoice_id']} with credit score {credit_details['credit_score']}")
        elif accumulated_amount < total_amount_requested and accumulated_amount + invoice_amount <= total_amount_requested * 1.10:
            credit_details = compute_credit_score(row['ptgstin'], row['ctin'], invoice_amount, row['ctin'], row['invoice_id'])
            if credit_details["success"]:
                if credit_details["credit_score"] >= 30:
                    row['credit_details'] = credit_details
                    row['lgl_nm'] = row.get('lgl_nm')
                    selected_invoices = pd.concat([selected_invoices, pd.DataFrame([row]).reset_index(drop=True)], ignore_index=True)
                    accumulated_amount += invoice_amount
                else:
                    print(f"Skipping invoice {row['invoice_id']} with credit score {credit_details['credit_score']}")
        if accumulated_amount >= total_amount_requested:
            break  # Stop if we've reached or exceeded the target amount

    # Calculate the cumulative trade score
    if 'credit_details' in selected_invoices.columns:
        selected_invoices['credit_score'] = selected_invoices['credit_details'].apply(lambda x: x['credit_score'])
        selected_invoices.sort_values(by='credit_score', ascending=False, inplace=True)
        cumulative_trade_score = calculate_cumulative_trade_score(selected_invoices)
    else:
        cumulative_trade_score = None

    # Construct the response
    request_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cumulative_assessment = {
        "cumulative_trade_score": round(cumulative_trade_score, 2) if cumulative_trade_score is not None else None,
        "request_id": request_id,
        "timestamp": timestamp,
        "total_amount_requested": total_amount_requested,
        "total_invoice_amount": accumulated_amount,
    }

    individual_assessment = []
    for _, row in selected_invoices.iterrows():
        credit_details = row['credit_details']
        assessment_detail = {
            "invoice_id": row['invoice_id'],
            "invoice_amount": row['invoice_amount'],
            "inv_date": row['inv_date'].strftime("%Y-%m-%d"),
            "ctin": row['ctin'],
            "lgl_nm": row['lgl_nm'],
            "assessment": {
                "request_id": request_id,
                "timestamp": timestamp,
                "base_score": credit_details['base_score'],
                "credit_score": credit_details['credit_score'],
                "highlights": credit_details['highlights'],
                "observations": credit_details['observations'],
                "final_verdict": credit_details['final_verdict']
            }
        }
        individual_assessment.append(assessment_detail)

    response = {
        "cumulative_assessment": cumulative_assessment,
        "individual_assessment": individual_assessment
    }
    print("transation recommendation-1",response)
    return jsonify(response)

def compute_credit_score_2(invoice_details, additional_metrics):
    api_url = "os.environ.get("CREDIT_SCORE_API_URL", "YOUR_CREDIT_SCORE_API_URL")"
    headers = {
        'Authorization': 'Bearer ' + os.environ.get('API_BEARER_TOKEN', 'YOUR_BEARER_TOKEN')  # Make sure to use the actual token here
    }
    # Prepare the payload excluding 'invoice_id' from the 'invoice_data'
    payload = {
        "invoice_data": {
            "borrower_gst": invoice_details.get("borrower_gst"),
            "trader_gst": invoice_details.get("trader_gst"),
            "current_invoice_amount": invoice_details.get("current_invoice_amount")
        },
        "additional_metrics": additional_metrics
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred
        return response.json()
    except requests.RequestException as e:
        print(f"Error calling the credit score API: {e}")
        return None  # Handle error scenario
@app.route('/transaction-recommendation-refine', methods=['POST'])
def transaction_recommendation_refine():
    data = request.json
    trxn_reco_refine = data.get('trxn_reco_refine', [])
    total_invoice_amount = 0
    individual_assessment = []

    for item in trxn_reco_refine:
        # Corrected extraction of 'invoice_details' and 'additional_metrics'
        invoice_details = item.get('invoice_data', {}).get('invoice_details', {})
        additional_metrics = item.get('invoice_data', {}).get('additional_metrics', {})
        # Fill in missing metrics with False as default
        for metric in ["grn_present", "e_invoice_present", "e_way_bill_present", "trader_partner_confirmation"]:
            additional_metrics.setdefault(metric, False)

        credit_score_data = compute_credit_score_2(invoice_details, additional_metrics)
        if credit_score_data:
            individual_assessment.append({
                "invoice_id": invoice_details.get("invoice_id"), 
                "invoice_date": invoice_details.get("invoice_date"), 
                "ctin": invoice_details.get("trader_gst"),
                "lgl_nm": invoice_details.get("lgl_nm"),
                "invoice_amount": invoice_details.get("current_invoice_amount"),
                "assessment": credit_score_data
            })
            total_invoice_amount += invoice_details.get("current_invoice_amount", 0)

    if individual_assessment:
        cumulative_trade_score = sum(assess["assessment"]["credit_score"] * assess["invoice_amount"] for assess in individual_assessment) / total_invoice_amount
    else:
        cumulative_trade_score = None

    cumulative_assessment = {
        "cumulative_trade_score": round(cumulative_trade_score, 2) if cumulative_trade_score is not None else None,
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_amount_requested": sum(item.get("invoice_amount", 0) for item in individual_assessment),
        "total_invoice_amount": total_invoice_amount
    }

    response = {
        "cumulative_assessment": cumulative_assessment,
        "individual_assessment": individual_assessment
    }
    print("transaction recommendation-2",response)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8113)
 