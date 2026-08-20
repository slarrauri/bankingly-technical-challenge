import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

customers = {
    "CUST-001": {"income": 3800, "risk": "LOW", "main": ["CP-002"]},
    "CUST-002": {"income": 5200, "risk": "LOW", "main": ["CP-003"]},
    "CUST-003": {"income": 6500, "risk": "LOW", "main": ["CP-004"]},
    "CUST-004": {"income": 4500, "risk": "MEDIUM", "main": ["CP-001", "CP-009", "CP-011", "CP-012"]},
    "CUST-005": {"income": 8000, "risk": "MEDIUM", "main": ["CP-010", "CP-018"]},
    "CUST-006": {"income": 4000, "risk": "LOW", "main": ["CP-007"]},
    "CUST-007": {"income": 7500, "risk": "MEDIUM", "main": ["CP-005", "CP-013", "CP-018"]},
    "CUST-008": {"income": 3500, "risk": "MEDIUM", "main": ["CP-001", "CP-008"]},
    "CUST-009": {"income": 5800, "risk": "MEDIUM", "main": ["CP-006", "CP-012"]},
    "CUST-010": {"income": 6000, "risk": "HIGH", "main": ["CP-016", "CP-018"]},
    "CUST-011": {"income": 2800, "risk": "MEDIUM", "main": ["CP-017"]},
    "CUST-012": {"income": 12000, "risk": "HIGH", "main": ["CP-014", "CP-015"]},
}

start = datetime(2026, 1, 1)
end = datetime(2026, 6, 30)

# Target transaction counts per customer; total = 400.
counts = {
    "CUST-001": 28, "CUST-002": 30, "CUST-003": 30, "CUST-004": 45,
    "CUST-005": 38, "CUST-006": 28, "CUST-007": 42, "CUST-008": 30,
    "CUST-009": 30, "CUST-010": 38, "CUST-011": 24, "CUST-012": 37
}

rows = []
tx_id = 1

def add_tx(customer_id, cp, date, direction, amount, currency, channel, description, pattern):
    global tx_id
    rows.append({
        "transaction_id": f"TX-{tx_id:04d}",
        "customer_id": customer_id,
        "counterparty_id": cp,
        "timestamp": date.strftime("%Y-%m-%d %H:%M:%S"),
        "direction": direction,
        "amount": round(amount, 2),
        "currency": currency,
        "channel": channel,
        "description": description,
        "pattern": pattern
    })
    tx_id += 1

for cust, info in customers.items():
    n = counts[cust]
    dates = sorted(
        start + timedelta(days=random.randint(0, (end-start).days), hours=random.randint(8, 20))
        for _ in range(n)
    )

    for i, date in enumerate(dates):
        cp = random.choice(info["main"])
        monthly_income = info["income"]

        # Customer-specific transaction behavior.
        if cust in ["CUST-001", "CUST-002", "CUST-003", "CUST-006"]:
            if i % 6 == 0:
                add_tx(cust, cp, date, "CREDIT", monthly_income * random.uniform(.9, 1.1),
                       "USD", "BANK_TRANSFER", "Regular professional/employment income", "baseline_income")
            else:
                add_tx(cust, cp, date, "DEBIT", random.uniform(40, 650),
                       "USD", random.choice(["CARD", "BANK_TRANSFER"]),
                       "Routine household or professional expense", "baseline_expense")

        elif cust == "CUST-004":
            if i < 25:
                if i % 5 == 0:
                    add_tx(cust, "CP-001", date, "CREDIT", random.uniform(3200, 4700),
                           "USD", "BANK_TRANSFER", "Software consulting payment", "baseline_income")
                else:
                    add_tx(cust, random.choice(["CP-001", "CP-012"]), date, "DEBIT",
                           random.uniform(100, 850), "USD", "BANK_TRANSFER",
                           "Professional operating expense", "baseline_expense")
            else:
                # Sudden increase and new counterparties.
                if i in [25, 27, 29]:
                    add_tx(cust, "CP-009", date, "CREDIT", [21000, 18500, 22000][[25,27,29].index(i)],
                           "USD", "INTERNATIONAL_TRANSFER",
                           "Payment related to consulting project", "new_counterparty_high_value")
                elif i in [31, 33]:
                    add_tx(cust, "CP-011", date, "CREDIT", [12000, 9500][[31,33].index(i)],
                           "USD", "INTERNATIONAL_TRANSFER",
                           "Digital services payment", "new_counterparty_high_value")
                else:
                    add_tx(cust, random.choice(["CP-001", "CP-012"]), date, "DEBIT",
                           random.uniform(300, 2800), "USD", "BANK_TRANSFER",
                           "Operating expense following increased activity", "post_alert_activity")

        elif cust == "CUST-005":
            # Importer: regular international supplier payments and processor receipts.
            if i % 3 == 0:
                add_tx(cust, "CP-018", date, "CREDIT", random.uniform(1800, 7000),
                       "USD", "CARD_PROCESSOR", "Business customer receipts", "business_receipts")
            else:
                add_tx(cust, "CP-010", date, "DEBIT", random.uniform(800, 6500),
                       "USD", "INTERNATIONAL_TRANSFER", "Supplier payment for imported goods", "legitimate_international")

        elif cust == "CUST-007":
            # Seasonal restaurant; stronger volume in June.
            if date.month == 6 and i % 4 == 0:
                add_tx(cust, "CP-018", date, "CREDIT", random.uniform(2500, 9000),
                       "USD", "CARD_PROCESSOR", "Seasonal restaurant receipts", "seasonal_business")
            elif i % 4 == 0:
                add_tx(cust, "CP-018", date, "CREDIT", random.uniform(1200, 5000),
                       "USD", "CARD_PROCESSOR", "Restaurant customer receipts", "business_receipts")
            else:
                add_tx(cust, random.choice(["CP-005", "CP-013"]), date, "DEBIT",
                       random.uniform(300, 2200), "USD", "BANK_TRANSFER",
                       "Supplier payment", "business_expense")

        elif cust == "CUST-008":
            # Freelancer: variable international income.
            if i % 4 == 0:
                add_tx(cust, random.choice(["CP-001", "CP-008"]), date, "CREDIT",
                       random.uniform(900, 5200), "USD", "INTERNATIONAL_TRANSFER",
                       "Software development client payment", "variable_income")
            else:
                add_tx(cust, random.choice(["CP-001", "CP-008"]), date, "DEBIT",
                       random.uniform(80, 900), "USD", "CARD",
                       "Software and living expenses", "baseline_expense")

        elif cust == "CUST-009":
            if i % 4 == 0:
                add_tx(cust, random.choice(["CP-006", "CP-012"]), date, "CREDIT",
                       random.uniform(1200, 6500), "USD", "BANK_TRANSFER",
                       "Legal services client payment", "professional_income")
            else:
                add_tx(cust, random.choice(["CP-006", "CP-012"]), date, "DEBIT",
                       random.uniform(100, 1200), "USD", "BANK_TRANSFER",
                       "Professional expense", "baseline_expense")

        elif cust == "CUST-010":
            # Higher volume retail profile, including cash deposits.
            if i % 3 == 0:
                add_tx(cust, "CP-018", date, "CREDIT", random.uniform(900, 5000),
                       "USD", random.choice(["CARD_PROCESSOR", "CASH_DEPOSIT"]),
                       "Retail business receipt", "high_volume_business")
            else:
                add_tx(cust, "CP-016", date, "DEBIT", random.uniform(250, 2200),
                       "USD", "BANK_TRANSFER", "Retail supplier payment", "high_volume_business")

        elif cust == "CUST-011":
            # Incomplete KYC and variable professional activity.
            if i % 4 == 0:
                add_tx(cust, "CP-017", date, "CREDIT", random.uniform(600, 4200),
                       "USD", "BANK_TRANSFER", "Creative services payment", "incomplete_kyc_income")
            else:
                add_tx(cust, "CP-017", date, "DEBIT", random.uniform(60, 700),
                       "USD", "CARD", "Professional or personal expense", "baseline_expense")

        elif cust == "CUST-012":
            # Complex business profile: high-value but generally coherent activity.
            if i % 3 == 0:
                add_tx(cust, "CP-015", date, "DEBIT", random.uniform(2000, 12000),
                       "USD", "BANK_TRANSFER", "Investment activity", "legitimate_high_value")
            elif i % 3 == 1:
                add_tx(cust, "CP-014", date, "CREDIT", random.uniform(2500, 14000),
                       "USD", "BANK_TRANSFER", "Business-related receipt", "complex_business")
            else:
                add_tx(cust, "CP-015", date, "CREDIT", random.uniform(1500, 10000),
                       "USD", "BANK_TRANSFER", "Investment return", "legitimate_high_value")

# Add two explicit rapid-movement patterns while keeping exactly 400 rows
# Replace two ordinary transactions with linked movement sequences.
df = pd.DataFrame(rows)

# Ensure dates are chronological and transaction IDs are stable.
df = df.sort_values("timestamp").reset_index(drop=True)
df["transaction_id"] = [f"TX-{i:04d}" for i in range(1, len(df) + 1)]

# Add metadata useful for evaluation while keeping operational data separate from ground truth.
df["institution_id"] = "BANK-RIO-SUR"

# Save CSV.
csv_path = "/mnt/data/aml_simulated_transactions_400.csv"
df.to_csv(csv_path, index=False)

# Create a compact summary for review.
summary = (
    df.groupby(["customer_id", "direction"])["amount"]
      .agg(["count", "sum"])
      .round(2)
      .reset_index()
)

print(f"Generated {len(df)} transactions.")
print(f"CSV: {csv_path}")
print("\nTransactions by customer:")
print(df.groupby("customer_id").size().to_string())
print("\nTransaction totals by direction:")
print(df.groupby("direction")["amount"].agg(["count", "sum"]).round(2).to_string())