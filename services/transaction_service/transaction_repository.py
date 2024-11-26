from datetime import datetime

class TransactionRepository:
    def __init__(self, driver):
        self.driver = driver

    def create_transaction(self, transaction_data):
        with self.driver.session() as session:
            query = """
            MERGE (source:Account {id: $source_id})
            MERGE (target:Account {id: $target_id})
            CREATE (source)-[t:TRANSACTION {
                id: $transaction_id,
                amount: $amount,
                timestamp: datetime($timestamp),
                currency: $currency
            }]->(target)
            RETURN t.id as transaction_id
            """
            result = session.run(query, {
                'source_id': transaction_data['source_id'],
                'target_id': transaction_data['target_id'],
                'transaction_id': str(datetime.now().timestamp()),
                'amount': transaction_data['amount'],
                'timestamp': transaction_data['timestamp'],
                'currency': transaction_data['currency']
            })
            return result.single()['transaction_id']

    def get_transaction(self, transaction_id):
        with self.driver.session() as session:
            query = """
            MATCH (source)-[t:TRANSACTION {id: $transaction_id}]->(target)
            RETURN source.id as source_id, 
                   target.id as target_id,
                   t.amount as amount,
                   t.currency as currency,
                   t.timestamp as timestamp
            """
            result = session.run(query, {'transaction_id': transaction_id})
            record = result.single()
            if record:
                return {
                    'source_id': record['source_id'],
                    'target_id': record['target_id'],
                    'amount': record['amount'],
                    'currency': record['currency'],
                    'timestamp': record['timestamp'].iso_format()
                }
            return None

    def search_transactions(self, start_date, end_date, min_amount):
        with self.driver.session() as session:
            query = """
            MATCH (source)-[t:TRANSACTION]->(target)
            WHERE 
                ($start_date IS NULL OR t.timestamp >= datetime($start_date)) AND
                ($end_date IS NULL OR t.timestamp <= datetime($end_date)) AND
                ($min_amount IS NULL OR t.amount >= $min_amount)
            RETURN source.id as source_id,
                   target.id as target_id,
                   t.id as transaction_id,
                   t.amount as amount,
                   t.currency as currency,
                   t.timestamp as timestamp
            ORDER BY t.timestamp DESC
            LIMIT 100
            """
            result = session.run(query, {
                'start_date': start_date,
                'end_date': end_date,
                'min_amount': float(min_amount) if min_amount else None
            })

            transactions = [{
                'transaction_id': record['transaction_id'],
                'source_id': record['source_id'],
                'target_id': record['target_id'],
                'amount': record['amount'],
                'currency': record['currency'],
                'timestamp': record['timestamp'].iso_format()
            } for record in result]

            return transactions
