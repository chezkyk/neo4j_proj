from flask import Flask

from analysis_service_blueprint import analysis_service_bp

app = Flask(__name__)
app.register_blueprint(analysis_service_bp)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5002)