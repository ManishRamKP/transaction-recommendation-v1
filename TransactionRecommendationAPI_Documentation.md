
# Transaction Recommendation API Overview

This API provides a strategic tool for financial analysis, offering personalized transaction recommendations. It is designed to help financial analysts and credit managers make informed decisions by evaluating and recommending invoices that cumulatively match a specified total amount. The focus is on optimizing the selection of recent invoices (raised in the last 30 days) to closely align with the client's financial request, facilitating efficient and targeted financial planning.

## Key Features

- **Invoice Selection:** Recommends a collection of invoices whose combined total approaches the requested amount, optimizing for financial efficiency and strategic value.
- **Recent Transactions:** Focuses on invoices raised in the last 30 days, ensuring recommendations are based on the most current financial activities.
- **Credit Assessment:** Each recommended invoice comes with a detailed credit assessment, including a credit score and a final verdict on the transaction's favorability. This assessment is enriched with highlights and observations to provide a comprehensive understanding of the financial implications.

## Basic Input and Output Example

### Input

The API expects a JSON payload with the total amount requested and the borrower's GST number.

```json
{
  "input": [
    {
      "total_amount": 400000,
      "borrower_gst": "36AAIFP3688H1ZS"
    }
  ]
}
```

### Output

The API responds with a JSON payload that includes a cumulative assessment and individual assessments for each recommended transaction. Each transaction is selected based on its alignment with the requested total amount and its recentness, with a preference for invoices raised in the last 30 days.

```json
{
  "output": [
    {
    "cumulative_assessment": {
        "cumulative_trade_score": 45.43,
        "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
        "timestamp": "2024-01-04 12:31:59",
        "total_amount_requested": 400000.0,
        "total_invoice_amount": 401680.0
    },
    "individual_assessment": [
        {
            "assessment": {
                "base_score":61.8,
                "credit_score": 61.8,
                "final_verdict": "This transaction appears strongly favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "29AATFS5544G1ZK",
            "inv_date": "2023-12-09",
            "invoice_amount": 6400.0,
            "invoice_id": "PT-4573-2023-24"
        },
        {
            "assessment": {
                "base_score":60.45,
                "credit_score": 60.45,
                "final_verdict": "This transaction appears strongly favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "37AAMCS2557B1ZB",
            "inv_date": "2023-12-14",
            "invoice_amount": 15000.0,
            "invoice_id": "PT-4700-2023-24"
        },
        {
            "assessment": {
                "base_score":56.58,
                "credit_score": 56.58,
                "final_verdict": "This transaction appears strongly favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "Infrequent transactions may suggest sporadic or inconsistent business dealings."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "36AAMFR4245E1Z5",
            "inv_date": "2023-12-11",
            "invoice_amount": 6000.0,
            "invoice_id": "PT-4594-2023-24"
        },
        {
            "assessment": {
                "base_score":55.3,
                "credit_score": 55.63,
                "final_verdict": "This transaction appears strongly favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "29AATFS5544G1ZK",
            "inv_date": "2023-12-19",
            "invoice_amount": 22000.0,
            "invoice_id": "PT-4781-2023-24"
        },
        {
            "assessment": {
                "base_score":55.16,
                "credit_score": 55.16,
                "final_verdict": "This transaction appears strongly favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "36AGHPM2768A1ZI",
            "inv_date": "2023-12-22",
            "invoice_amount": 5400.0,
            "invoice_id": "PT-4849-2023-24"
        },
        {
            "assessment": {
                "base_score":54.36,
                "credit_score": 54.36,
                "final_verdict": "This transaction appears strongly favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "37AABCG4489R1ZQ",
            "inv_date": "2023-12-14",
            "invoice_amount": 5100.0,
            "invoice_id": "PT-4695-2023-24"
        },
        {
            "assessment": {
                "base_score":53.07,
                "credit_score": 53.07,
                "final_verdict": "This transaction appears strongly favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "36AAATP3833E1ZQ",
            "inv_date": "2023-12-23",
            "invoice_amount": 33000.0,
            "invoice_id": "PT-4883-2023-24"
        },
        {
            "assessment": {
                "base_score":49.4,
                "credit_score": 49.4,
                "final_verdict": "This transaction seems generally favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "37AACCN4041K1ZG",
            "inv_date": "2023-12-26",
            "invoice_amount": 52440.0,
            "invoice_id": "PT-4913-2023-24"
        },
        {
            "assessment": {
                "base_score":49.22,
                "credit_score": 49.22,
                "final_verdict": "This transaction seems generally favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "36AABCA7322F1Z1",
            "inv_date": "2023-12-20",
            "invoice_amount": 45600.0,
            "invoice_id": "PT-4816-2023-24"
        },
        {
            "assessment": {
                "base_score":47.56,
                "credit_score": 47.56,
                "final_verdict": "This transaction seems generally favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "36AAATP3833E1ZQ",
            "inv_date": "2023-12-08",
            "invoice_amount": 56250.0,
            "invoice_id": "PT-4532-2023-24"
        },
        {
            "assessment": {
                "base_score":43.75,
                "credit_score": 43.75,
                "final_verdict": "This transaction seems generally favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The transaction size deviates from typical patterns, suggesting potential irregularities."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "37AAQCS4714G2Z1",
            "inv_date": "2023-12-26",
            "invoice_amount": 39900.0,
            "invoice_id": "PT-4911-2023-24"
        },
        {
            "assessment": {
                "base_score":42.29,
                "credit_score": 42.29,
                "final_verdict": "This transaction seems generally favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "32AAFFC5911M2ZI",
            "inv_date": "2023-12-26",
            "invoice_amount": 11550.0,
            "invoice_id": "PT-4899-2023-24"
        },
        {
            "assessment": {
                "base_score":40.72,
                "credit_score": 40.72,
                "final_verdict": "This transaction seems generally favorable. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The company's operational history signifies market experience and stability."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "37AANFN4254C1Z9",
            "inv_date": "2023-12-16",
            "invoice_amount": 6840.0,
            "invoice_id": "PT-4731-2023-24"
        },
        {
            "assessment": {
                "base_score":36.91,
                "credit_score": 36.91,
                "final_verdict": "This transaction presents a neutral standpoint. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The transaction size aligns favorably with our expectations based on historical trends.",
                    "Regular transactions between the parties indicate a robust business relationship.",
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement."
                ],
                "observations": [
                    "The company's relatively recent entry into the market may come with navigational challenges."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "37AAICN1643F1ZJ",
            "inv_date": "2023-12-16",
            "invoice_amount": 4680.0,
            "invoice_id": "PT-4744-2023-24"
        },
        {
            "assessment": {
                "base_score":31.24,
                "credit_score": 31.24,
                "final_verdict": "This transaction presents a neutral standpoint. Overall, the indicators suggest a good potential for financing.",
                "highlights": [
                    "The borrower showcases commendable financial discipline and compliance.",
                    "The trader involved has a commendable track record of financial responsibility.",
                    "Recent transaction activities suggest a growth trajectory or a significant business engagement.",
                    "The company's operational history signifies market experience and stability."
                ],
                "observations": [
                    "The transaction size deviates from typical patterns, suggesting potential irregularities.",
                    "Infrequent transactions may suggest sporadic or inconsistent business dealings."
                ],
                "request_id": "612ac32c-b64f-47c3-981b-157ff729629f",
                "timestamp": "2024-01-04 12:31:59"
            },
            "ctin": "36AADCH7188N1ZV",
            "inv_date": "2023-12-20",
            "invoice_amount": 91520.0,
            "invoice_id": "PT-4817-2023-24"
        }
    ]
}
]
}
```


## Data Fetching with SQL Query

The application fetches invoice data based on specific criteria to ensure that recommendations are both relevant and timely. This is accomplished by executing a SQL query against an AWS Athena database. The query selects invoices based on the borrower's GST number, ensuring they are unlinked, related to sales, and raised within the last 30 days. Here is the SQL query used:

```sql
SELECT 
    DATE AS inv_date,
    ptgstin, 
    ctin, 
    inv_no AS invoice_id, 
    taxval AS invoice_amount
FROM 
    "tally_data"."v_rpt_tally"
WHERE 
    ptgstin = '{borrower_gst}'
    AND linkage_status = 'Unlinked'
    AND inv_delayin_days < 0
    AND inv_typ = 'Sales';
```

This query is a crucial part of the application's backend logic, ensuring that the data used for making recommendations is both accurate and up to date. By focusing on specific criteria like unlinked sales invoices that were issued recently, the application can provide recommendations that are highly relevant to the borrower's current financial situation.


## Docker Setup

### Dockerfile Overview

To containerize the Transaction Recommendation API, a Dockerfile is utilized. This Dockerfile sets up a Python environment, installs necessary dependencies, and runs the Flask application in a container. Here is an overview of the Dockerfile used:

```Dockerfile
# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=trade_reco.py

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8113 available to the world outside this container
EXPOSE 8113

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8113"]
```

### Building and Running the Container

1. **Build the Docker Image:**
   ```
   docker build -t tradereco .
   ```

2. **Run the Container:**
   ```
   docker run -p 8113:8113 tradereco
   ```

## Conclusion

The Transaction Recommendation API stands out as a pivotal tool for financial institutions, leveraging recent transaction data to offer actionable insights and recommendations. By focusing on the latest 30 days of invoice activities, it ensures that the recommendations are timely and reflect the current financial landscape, providing a solid foundation for financial decision-making.
