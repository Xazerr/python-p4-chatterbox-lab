from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    try:
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201
    except KeyError:
        return make_response({'error': 'Missing required fields'}, 400)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if message:
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
            db.session.commit()
            return jsonify(message.to_dict()), 200
        else:
            return make_response({'error': 'Missing body field'}, 400)
    return make_response({'error': 'Message not found'}, 404)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return {}, 204
    return make_response({'error': 'Message not found'}, 404)

if __name__ == '__main__':
    app.run(port=5555)

