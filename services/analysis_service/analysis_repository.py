from datetime import datetime, timedelta
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import io

class GraphAnalyzer:
    def __init__(self, driver):
        self.driver = driver

    def find_circular_patterns(self, min_amount=10000, max_depth=4):
        with self.driver.session() as session:
            query = """
            MATCH path = (a:Account)-[:TRANSACTION*1..%d]->(a)
            WHERE ALL(r IN relationships(path) WHERE r.amount >= $min_amount)
            RETURN nodes(path) as accounts,
                   relationships(path) as transactions,
                   length(path) as cycle_length
            ORDER BY cycle_length
            LIMIT 10
            """ % max_depth

            result = session.run(query, {'min_amount': min_amount})

            patterns = []
            for record in result:
                pattern = {
                    'accounts': [node['id'] for node in record['accounts']],
                    'transactions': [{
                        'amount': tx['amount'],
                        'currency': tx['currency'],
                        'timestamp': f'{tx["timestamp"]}'
                    } for tx in record['transactions']],
                    'cycle_length': record['cycle_length']
                }
                patterns.append(pattern)

            return patterns



    def calculate_metrics(self,timeframe_hours=24):
        with self.driver.session() as session:
            query = """
            MATCH (source)-[t:TRANSACTION]->(target)
            WHERE t.timestamp >= datetime($start_time)
            RETURN count(t) as total_transactions,
                   sum(t.amount) as total_amount,
                   avg(t.amount) as avg_amount,
                   collect(t.amount) as amounts
            """

            start_time = (datetime.now() - timedelta(hours=timeframe_hours)).isoformat()
            result = session.run(query, {'start_time': start_time})
            record = result.single()

            amounts = pd.Series(record['amounts'])
            metrics = {
                'total_transactions': record['total_transactions'],
                'total_amount': record['total_amount'],
                'avg_amount': record['avg_amount'],
                'std_dev': amounts.std(),
                'percentiles': {
                    '25': amounts.quantile(0.25),
                    '50': amounts.quantile(0.50),
                    '75': amounts.quantile(0.75),
                    '90': amounts.quantile(0.90)
                }
            }

            return metrics

    def generate_network_visualization(self, min_amount=50000):
        with self.driver.session() as session:
            query = """
            MATCH (source)-[t:TRANSACTION]->(target)
            WHERE t.amount >= $min_amount
            RETURN source.id as source,
                   target.id as target,
                   t.amount as amount
            LIMIT 100
            """

            result = session.run(query, {'min_amount': min_amount})

            G = nx.DiGraph()
            for record in result:
                G.add_edge(
                    record['source'],
                    record['target'],
                    weight=record['amount']
                )

            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(G)
            nx.draw(
                G, pos,
                with_labels=True,
                node_color='lightblue',
                node_size=500,
                arrowsize=20,
                font_size=8
            )

            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            plt.close()

            return buf
