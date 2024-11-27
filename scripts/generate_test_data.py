import random
import json
from datetime import datetime, timedelta
import requests

class TestDataGenerator:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.account_ids = [f"ACC_{i:04d}" for i in range(100)]
        self.currencies = ["USD", "EUR", "GBP"]

    def generate_normal_transaction(self):
        """Generate a normal-looking transaction with a timestamp"""
        source = random.choice(self.account_ids)
        target = random.choice([acc for acc in self.account_ids if acc != source])

        # Generate a random timestamp within the last 30 days
        timestamp = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()

        return {
            "source_id": source,
            "target_id": target,
            "amount": round(random.uniform(1000, 50000), 2),
            "currency": random.choice(self.currencies),
            "timestamp": timestamp
        }

    def generate_suspicious_pattern(self):
        """Generate a circular pattern of transactions with timestamps"""
        # Select 3-4 accounts for the circle
        accounts = random.sample(self.account_ids, random.randint(3, 4))
        transactions = []

        # Create circular transactions with similar amounts and timestamps
        base_amount = random.uniform(20000, 100000)
        base_date = datetime.now() - timedelta(days=random.randint(0, 30))

        for i in range(len(accounts)):
            source = accounts[i]
            target = accounts[(i + 1) % len(accounts)]

            # Vary the amount slightly to make it less obvious
            amount = base_amount * random.uniform(0.95, 1.05)

            # Vary the timestamp slightly
            timestamp = (base_date + timedelta(hours=i * random.uniform(1, 5))).isoformat()

            transactions.append({
                "source_id": source,
                "target_id": target,
                "amount": round(amount, 2),
                "currency": random.choice(self.currencies),
                "timestamp": timestamp
            })

        return transactions

    def generate_dataset(self, num_normal=1000, num_suspicious=5):
        """Generate a full dataset with both normal and suspicious transactions"""
        all_transactions = []

        # Generate normal transactions
        for _ in range(num_normal):
            all_transactions.append(self.generate_normal_transaction())

        # Generate suspicious patterns
        for _ in range(num_suspicious):
            all_transactions.extend(self.generate_suspicious_pattern())

        # Shuffle transactions
        random.shuffle(all_transactions)

        return all_transactions

    def send_transactions(self, transactions):
        """Send transactions to the API"""
        results = []
        for tx in transactions:
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/transactions/",
                    json=tx
                )
                results.append({
                    'transaction': tx,
                    'status': response.status_code,
                    'response': response.json()
                })
            except Exception as e:
                results.append({
                    'transaction': tx,
                    'status': 'error',
                    'error': str(e)
                })
        return results


if __name__ == "__main__":
    generator = TestDataGenerator()

    # Generate test dataset
    transactions = generator.generate_dataset()

    # Save to file
    with open('test_transactions.json', 'w') as f:
        json.dump(transactions, f, indent=2)

    # Optionally send to API
    results = generator.send_transactions(transactions)

    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
