from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from json.decoder import JSONDecodeError
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load tokens from tokens.json
with open('tokens.json') as file:
    tokens_data = json.load(file)
tokens = tokens_data.get("tokens", [])

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    description = db.Column(db.String)
    customer_id = db.Column(db.Integer)
    agent_id = db.Column(db.Integer)
    technition_id = db.Column(db.Integer)
    created_at = db.Column(DateTime, default=datetime.utcnow)

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    time = db.Column(DateTime)
    date = db.Column(db.String)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    W_Temp1 = db.Column(db.Float)
    W_Temp2 = db.Column(db.Float)
    W_Temp3 = db.Column(db.Float)
    W_Temp4 = db.Column(db.Float)
    W_Temp5 = db.Column(db.Float)
    W_Temp6 = db.Column(db.Float)
    B_Temp1 = db.Column(db.Float)
    B_Temp2 = db.Column(db.Float)
    Vib1 = db.Column(db.Float)
    Vib2 = db.Column(db.Float)
    created_at = db.Column(DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    devices = Device.query.all()
    return render_template('index.html', devices=devices)

@app.route('/device/<int:device_id>')
def device_details(device_id):
    device_data = Data.query.filter_by(device_id=device_id).order_by(Data.time).all()
    return render_template('device_details.html', device_id=device_id, device_data=device_data)

@app.route('/graph/<int:device_id>')
def graph(device_id):
    device_data = Data.query.filter_by(device_id=device_id).order_by(Data.time).all()
    return render_template('graph.html', device_data=device_data)

@app.route('/api/store_data', methods=['POST'])
def store_data():
    access_token = request.headers.get('Token')
    if access_token not in tokens:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data_json = request.json
        new_data = Data(
            device_id=data_json.get('device_id'),
            time=datetime.strptime(data_json.get('time'), "%Y-%m-%dT%H:%M:%SZ"),
            date=datetime.strptime(data_json.get('date'), "%Y-%m-%d").date(),
            event_id=data_json.get('event_id'),
            W_Temp1=data_json.get('W_Temp1'),
            W_Temp2=data_json.get('W_Temp2'),
            W_Temp3=data_json.get('W_Temp3'),
            W_Temp4=data_json.get('W_Temp4'),
            W_Temp5=data_json.get('W_Temp5'),
            W_Temp6=data_json.get('W_Temp6'),
            B_Temp1=data_json.get('B_Temp1'),
            B_Temp2=data_json.get('B_Temp2'),
            Vib1=data_json.get('Vib1'),
            Vib2=data_json.get('Vib2')
        )

        db.session.add(new_data)
        db.session.commit()

        return jsonify({"success": "Data stored successfully"}), 200

    except (JSONDecodeError, SQLAlchemyError, IntegrityError, ValueError) as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

