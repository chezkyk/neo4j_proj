from flask import Blueprint, jsonify, request

transaction_srvice_bp = Blueprint('transaction_srvice', __name__, url_prefix='/api/v1/transactions')

@transaction_srvice_bp.route('/', methods=['POST'])
def create_transaction():
    return jsonify({'status': 'ok'})


@transaction_srvice_bp.route('/<string:id>', methods=['GET'])
def get_transaction_by_id(id):
    return jsonify({'status': 'ok'})


@transaction_srvice_bp.route('/search', methods=['GET'])
def get_transaction_by_search():
    return jsonify({'status': 'ok'})


