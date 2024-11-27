
class GraphAnalyzer:
    def __init__(self, driver):
        self.driver = driver

    def find_circular_patterns(self,min_amount=10_0000):
        with self.driver.session() as session:
            query = """
            MATCH path = (a:Account)-[:TRANSACTION*1..]->(a)
            WHERE ALL( r IN relationships(path) WHERE r.amount >= $min_amount)
            RETURN nodes(path) as accounts,
                   relationships(path) as transactions,
                   length(path) as cycle_length
            ORDER BY cycle_length
            LIMIT 10
            """

            result = session.run(query, {'min_amount': min_amount})

            patterns = []
            for record in result:
                pattern = {

                    'accounts': [node['id'] for node in record['accounts']],
                    'transactions': [
                        {
                            'amount': tx['amount'],
                            'currency': tx['currency'],
                            'timestamp': tx['timestamp']
                        } for tx in record['transactions']
                    ],
                    'cycle_length': record['cycle_length']
                }
                patterns.append(pattern)
                print("p is", pattern)
            print("patterns is in q", patterns)
            return patterns



    def calculate_metrics(self):
        return "calculate_metrics"

    def generate_network_visualization(self):
        return "generate_network_visualization"