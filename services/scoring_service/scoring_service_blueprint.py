from flask import Blueprint, jsonify

scoring_service_bp = Blueprint('scoring_service', __name__, url_prefix='/api/v1')


@scoring_service_bp.route('/risk-score/<string:entity_id>', methods=["GET"])
def get_risk_score(entity_id):
    return jsonify({'status': 'ok'})

@scoring_service_bp.route('/blacklist', methods=["POST"])
def blacklist():
    return jsonify({'status': 'ok'})

@scoring_service_bp.route('/risk-metrics', methods=["GET"])
def get_risk_metrics():
    return jsonify({'status': 'ok'})