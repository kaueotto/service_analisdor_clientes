from flask import Flask, jsonify, request

from controllers.users import Users
from data import models
from security import security

# poetry run flask --app src/service.py --debug run

app = Flask(__name__)


@app.route('/cadastro', methods=['POST'])
def cadastro():

    data = request.get_json()
    try:
        user = Users(data)
        token = user.new_user()
        return jsonify({'mensagem': token}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
