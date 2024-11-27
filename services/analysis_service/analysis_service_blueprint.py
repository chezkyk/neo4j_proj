from flask import Blueprint, jsonify, request, json

from analysis_repository import GraphAnalyzer
from config import neo4j_driver, redis_client

analysis_service_bp = Blueprint('analysis_service', __name__, url_prefix='/api/v1/analysis')

@analysis_service_bp.route('/patterns', methods=['GET'])
def get_patterns():
    min_amount = request.args.get('min_amount', 10_000)

    try:
        cached_result = redis_client.get(f'patterns_{min_amount}')
        if cached_result:
            return jsonify(json.loads(cached_result)), 200

        analyzer = GraphAnalyzer(neo4j_driver)
        patterns = analyzer.find_circular_patterns(min_amount)
        print("patterns",patterns)
        # cache the results
        cache_key = f'patterns_{min_amount}'

        redis_client.setex(
            cache_key,
            3600,  # 1 hour,
            json.dumps(f'patterns')
        )

        return jsonify(patterns), 200


    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@analysis_service_bp.route('/metrics', methods=['GET'])
def get_metrics():
    repo = GraphAnalyzer(neo4j_driver)
    metrics = repo.calculate_metrics()
    return jsonify({'ok': metrics})

@analysis_service_bp.route('/visualization', methods=['GET'])
def get_visualization():
    repo = GraphAnalyzer(neo4j_driver)
    visualization = repo.generate_network_visualization()
    return jsonify({'ok': visualization})

