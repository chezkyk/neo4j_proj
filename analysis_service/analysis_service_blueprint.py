from flask import Blueprint, jsonify

analysis_service_bp = Blueprint('analysis_service', __name__, url_prefix='/api/v1/analysis')

@analysis_service_bp.route('/patterns', methods=['GET'])
def get_patterns():
    return jsonify({'status': 'ok'})

@analysis_service_bp.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify({'status': 'ok'})

@analysis_service_bp.route('/visualization', methods=['GET'])
def get_visualization():
    return jsonify({'status': 'ok'})

