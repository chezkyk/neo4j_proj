from flask import Flask
from transaction_service_blueprint import transaction_srvice_bp

app = Flask(__name__)
app.register_blueprint(transaction_srvice_bp)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5001)