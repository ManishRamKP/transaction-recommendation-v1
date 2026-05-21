# finflow-transaction-recommendation-v1

A Flask microservice that recommends the optimal set of invoices for financing based on a borrower's GST number and a requested total amount. Each recommended invoice is individually scored by the Credit Recommendation Engine (CRE) and returned with a cumulative trade score.

---

## Overview

This is **v1** of the Transaction Recommendation service. It:

1. Accepts a borrower GST and a total financing amount
2. Fetches the borrower's recent unlinked sales invoices from AWS Athena
3. Greedily selects invoices that cumulatively approach the requested amount
4. Scores each invoice via the CRE API (minimum credit score threshold: 30)
5. Returns a ranked individual assessment and a weighted cumulative trade score

Two endpoints are provided:

| Endpoint | Description |
|---|---|
| `POST /transaction-recommendation` | Auto-fetches invoices from Athena and scores them |
| `POST /transaction-recommendation-refine` | Accepts pre-selected invoices with additional metrics for refined scoring |

---

## Prerequisites

- Python 3.8+
- Docker
- AWS credentials with Athena + S3 access
- Access to a running CRE scoring API

---

## Configuration

All sensitive values are supplied via environment variables or `config.json`. **Never commit `config.json` with real values.**

### Environment variables

| Variable | Description |
|---|---|
| `CREDIT_SCORE_API_URL` | URL of the CRE compute_credit_score endpoint |
| `API_BEARER_TOKEN` | Bearer token for CRE API authentication |

```bash
export CREDIT_SCORE_API_URL=https://your-cre-api/compute_credit_score
export API_BEARER_TOKEN=your-bearer-token
```

### config.json (AWS / Athena)

```json
{
  "aws": {
    "aws_access_key_id": "YOUR_AWS_ACCESS_KEY_ID",
    "aws_secret_access_key": "YOUR_AWS_SECRET_ACCESS_KEY",
    "region_name": "ap-south-1",
    "bucket_name": "YOUR_S3_BUCKET_NAME"
  },
  "athena": {
    "s3_output_location": "s3://YOUR_S3_BUCKET_NAME/"
  }
}
```

---

## Running Locally

```bash
git clone https://github.com/your-org/finflow-transaction-recommendation-v1.git
cd finflow-transaction-recommendation-v1

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Set env vars
export CREDIT_SCORE_API_URL=https://your-cre-api/compute_credit_score
export API_BEARER_TOKEN=your-bearer-token

python transactionrecommendation.py
```

Service runs on `http://localhost:8113`.

---

## Docker Deployment

```bash
docker build -t trade-recommendation .
docker run -p 8113:8113 \
  -e CREDIT_SCORE_API_URL=https://your-cre-api/compute_credit_score \
  -e API_BEARER_TOKEN=your-bearer-token \
  trade-recommendation
```

---

## Kubernetes Deployment

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f loadbalancer.yaml
```

Update the image URI in `deployment.yaml` with your ECR/GCR path before applying.

| Resource | Type | Port |
|---|---|---|
| `finflow-tradereco` | Deployment | 8112 |
| `finflow-tradereco-service` | NodePort | 8112 → 30009 |
| `finflow-tradereco-service-loadbalancer` | LoadBalancer | 8112 |

---

## API Reference

### `POST /transaction-recommendation`

**Request**
```json
{
  "borrower_gst": "27XXXXXXXXXXXXX",
  "total_amount": 400000
}
```

**Response**
```json
{
  "cumulative_assessment": {
    "cumulative_trade_score": 45.43,
    "request_id": "uuid",
    "timestamp": "2024-01-04 12:31:59",
    "total_amount_requested": 400000.0,
    "total_invoice_amount": 401680.0
  },
  "individual_assessment": [
    {
      "invoice_id": "INV-001",
      "invoice_amount": 6400.0,
      "inv_date": "2023-12-09",
      "ctin": "29XXXXXXXXXXX",
      "assessment": {
        "credit_score": 61.8,
        "base_score": 61.8,
        "highlights": ["..."],
        "observations": ["..."],
        "final_verdict": "This transaction appears strongly favorable."
      }
    }
  ]
}
```

### `POST /transaction-recommendation-refine`

Accepts manually selected invoices with additional document metrics (GRN, e-invoice, e-way bill, trader confirmation) for a refined credit score.

**Request**
```json
{
  "trxn_reco_refine": [
    {
      "invoice_data": {
        "invoice_details": {
          "borrower_gst": "27XXXXXXXXXXXXX",
          "trader_gst": "29XXXXXXXXXXXXX",
          "current_invoice_amount": 50000,
          "invoice_id": "INV-001",
          "invoice_date": "2024-01-01",
          "lgl_nm": "Trader Legal Name"
        },
        "additional_metrics": {
          "grn_present": true,
          "e_invoice_present": false,
          "e_way_bill_present": true,
          "trader_partner_confirmation": false
        }
      }
    }
  ]
}
```

---

## Scoring Logic

- Invoices are fetched sorted by date and amount (ascending)
- Invoices are selected greedily until the `total_amount` is reached (with a 10% overflow tolerance)
- Invoices with a credit score below **30** are skipped
- The **cumulative trade score** is a weighted average: `Σ(credit_score × invoice_amount) / Σ(invoice_amount)`

---

## Related Services

This service is part of the FinFlow CRE suite:
- `finflow-cre-v11` — Core credit scoring engine
- `finflow-ekg-cre-metrics-v11` — Enterprise knowledge graph manager
- `finflow-transaction-recommendation-v1` — This service (invoice selection + scoring)

---

## Security Notes

- Never commit `config.json` with real AWS credentials
- Inject `API_BEARER_TOKEN` and `CREDIT_SCORE_API_URL` at runtime via environment variables or a secrets manager
- Rotate Bearer tokens regularly; treat them like passwords
