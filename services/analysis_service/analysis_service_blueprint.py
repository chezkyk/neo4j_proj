from flask import Blueprint, jsonify, request, json, send_file

from analysis_repository import GraphAnalyzer
from config import neo4j_driver, redis_client

analysis_service_bp = Blueprint('analysis_service', __name__, url_prefix='/api/v1/analysis')


@analysis_service_bp.route('/patterns', methods=['GET'])
def get_patterns():
    min_amount = float(request.args.get('min_amount', 10000))
    max_depth = int(request.args.get('max_depth', 4))

    try:
        analyzer = GraphAnalyzer(neo4j_driver)
        patterns = analyzer.find_circular_patterns(min_amount, max_depth)

        # Cache the results
        cache_key = f'patterns_{min_amount}_{max_depth}'
        redis_client.setex(
            cache_key,
            3600,  # Cache for 1 hour
            json.dumps(f'{patterns}')
        )

        return jsonify(patterns), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_service_bp.route('/metrics', methods=['GET'])
def get_metrics():
    timeframe = int(request.args.get('timeframe_hours', 24))
    cache_key = f'metrics_{timeframe}'

    # Try to get from cache
    cached_metrics = redis_client.get(cache_key)
    if cached_metrics:
        return jsonify(json.loads(cached_metrics)), 200

    try:
        analyzer = GraphAnalyzer(neo4j_driver)
        metrics = analyzer.calculate_metrics(timeframe)

        # Cache the results
        redis_client.setex(
            cache_key,
            300,  # Cache for 5 minutes
            json.dumps(metrics)
        )

        return jsonify(metrics), 200

    except Exception as e:
        print(f'error in get_metrics: {e}')
        return jsonify({'error': str(e)}), 500


@analysis_service_bp.route('/visualization', methods=['GET'])
def get_visualization():
    min_amount = float(request.args.get('min_amount', 50000))

    try:
        analyzer = GraphAnalyzer(neo4j_driver)
        buf = analyzer.generate_network_visualization(min_amount)

        return send_file(
            buf,
            mimetype='image/png',
            as_attachment=True,
            download_name='network_visualization.png'
        )

    except Exception as e:
        print(f'error in get_visualization: {e}')
        return jsonify({'error': str(e)}), 500
