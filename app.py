from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    time = db.Column(db.DateTime)
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    devices = Device.query.all()
    print(devices)
    return render_template('index.html', devices=devices)

@app.route('/device/<int:device_id>')
def device_details(device_id):
    device_data = Data.query.filter_by(device_id=device_id).order_by(Data.time).all()
    return render_template('device_details.html', device_id=device_id, device_data=device_data)

@app.route('/graph/<int:device_id>')
def graph(device_id):
    device_data = Data.query.filter_by(device_id=device_id).order_by(Data.time).all()
    formatted_device_data = [{
        'time': data.time.strftime("%Y-%m-%d %H:%M:%S"),
        'W_Temp1': data.W_Temp1,
        'W_Temp2': data.W_Temp2,
        'W_Temp3': data.W_Temp3,
        'W_Temp4': data.W_Temp4,
        'W_Temp5': data.W_Temp5,
        'W_Temp6': data.W_Temp6,
        'B_Temp1': data.B_Temp1,
        'B_Temp2': data.B_Temp2,
        'Vib1': data.Vib1,
        'Vib2': data.Vib2
    } for data in device_data]

    return render_template('graph.html', device_data=formatted_device_data)

@app.route('/api/store_data', methods=['POST'])
def store_data():
    access_token = request.headers.get('Token')
    if access_token not in tokens:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data_json = request.json
        device_id = data_json.get('device_id')

        # Check if the 'time' and 'date' keys are present and not None
        time_str = data_json.get('time')
        if time_str is not None:
            time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        else:
            time = None  # Set time to None if 'time' is not provided

        date_str = data_json.get('date')
        if date_str is not None:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            date = None  # Set date to None if 'date' is not provided

        new_data = Data(
            device_id=device_id,
            time=time,
            date=date,
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
