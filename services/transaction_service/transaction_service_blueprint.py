from datetime import datetime

from flask import Blueprint, jsonify, request, json

from config import neo4j_driver, redis_client
from transaction_repository import TransactionRepository

transaction_srvice_bp = Blueprint('transaction_srvice', __name__, url_prefix='/api/v1/transactions')

@transaction_srvice_bp.route('/', methods=['POST'])
def create_transaction():
    data = request.json
    required_fields = ['source_id', 'target_id', 'amount','timestamp', 'currency']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        repo = TransactionRepository(neo4j_driver)
        transaction_id = repo.create_transaction(data)

        redis_client.lpush(
            'recent_transactions',
            json.dumps({**data, 'transaction_id': transaction_id})
        )
        redis_client.ltrim('recent_transactions', 0, 999)

        return jsonify({
            'status': 'success',
            'transaction_id': transaction_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_srvice_bp.route('/<transaction_id>', methods=['GET'])
def get_transaction_by_id(transaction_id):
    try:
        repo = TransactionRepository(neo4j_driver)
        transaction = repo.get_transaction(transaction_id)

        if transaction:
            return jsonify(transaction), 200
        return jsonify({'error': 'Transaction not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_srvice_bp.route('/search', methods=['GET'])
def search_transaction_by_date_and_min_amount():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_amount = request.args.get('min_amount')

    try:
        repo = TransactionRepository(neo4j_driver)
        transactions = repo.search_transactions(start_date, end_date, min_amount)
        return jsonify(transactions), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



