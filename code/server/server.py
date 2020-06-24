# REST Server

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from waitress import serve
# init app
app = Flask(__name__)

# database configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://janesh:password@localhost/testdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

class Dispenser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    location = db.Column(db.String(20))
    created = db.Column(db.String(20))
    device_id = db.Column(db.Integer, unique=True)

    def __init__(self, name, location, created, device_id):
        self.name = name
        self.location = location
        self.created = created
        self.device_id = device_id

class DispenserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Float)
    volume_dispensed = db.Column(db.Float)
    fluid_level = db.Column(db.Float)
    ignored = db.Column(db.Boolean)
    datetime = db.Column(db.String(20))
    device_id = db.Column(db.Integer)

    def __init__(self, distance, volume_dispensed, fluid_level, ignored, datetime, device_id):
        self.distance = distance
        self.volume_dispensed = volume_dispensed
        self.fluid_level = fluid_level
        self.ignored = ignored
        self.datetime = datetime
        self.device_id = device_id

# Dispenser schema
class DispenserDataSchema(ma.Schema):
    class Meta:
        fields = ('id','distance', 'volume_dispensed', 'fluid_level', 'ignored', 'datetime', 'device_id')

# Dispenser Data schema
class DispenserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'created', 'device_id')

# init schemas
dispenser_data_schema = DispenserDataSchema()
dispensers_data_schema = DispenserDataSchema(many=True)

dispenser_schema = DispenserSchema()
dispensers_schema = DispenserSchema(many=True)

# register dispenser
@app.route('/api/dispenser/register', methods=['POST'])
def register_dispenser():
    name = request.json['name']
    location = request.json['location']
    created = request.json['created']
    device_id = request.json['device_id']

    # assign id if null or id is not registered
    if not device_id or not check_id(device_id):
        device_id = generate_new_id()
        name = "Dispenser" + str(device_id)

        new_dispenser = Dispenser(name, location, created, device_id)
        
        try:
            db.session.add(new_dispenser)
            db.session.commit()
        except:
            return {"message": "Duplicate value, name and/or location already exists"}, 400
        
        # send back updated config
        return {
            "device_id": device_id,
            "name": name,
            "location": location,
            "created": created
            }, 201

    else:
        return {"message": "device id is already registered"}, 400

def generate_new_id():
    dispensers = Dispenser.query.all()

    if dispensers:
        id_list = []
        for dispenser in dispensers:
            id_list.append(dispenser.device_id)
        
        return max(id_list) + 1

    else:
        return 1

def check_id(device_id):
    dispenser = Dispenser.query.filter_by(device_id=device_id).first()
    if dispenser: 
        return dispenser.device_id == device_id

    return False

# add Dispenser Data
@app.route('/api/dispenser/data', methods=['POST'])
def add_dispenser_data():
    device_id = request.json['device_id']

    # check if id is registered
    if not check_id(device_id):
        return {"message": "device id is not registered"}, 404

    distance = request.json['distance']
    volume_dispensed = request.json['volume_dispensed']
    fluid_level = request.json['fluid_level']
    ignored = request.json['ignored']
    datetime = request.json['datetime']

    new_dispenser_data = DispenserData(distance, volume_dispensed, fluid_level, ignored, datetime, device_id)

    db.session.add(new_dispenser_data)
    db.session.commit()

    return "OK", 201

# get all dispensers data
@app.route('/api/dispenser/data/all', methods=['GET'])
def get_all_dispensers_data():
    # get all dispenser data
    all_dispensers_data = DispenserData.query.all()

    # convert data to dictionary
    result = dispensers_data_schema.dump(all_dispensers_data)

    # convert to json and send
    return jsonify(result)

# get single dispensers data
@app.route('/api/dispenser/data/<device_id>', methods=['GET'])
def get_dispenser_data(device_id):
    # get dispenser data
    dispenser_data = DispenserData.query.filter_by(device_id=device_id).all()

    if dispenser_data:
        # convert data to dictionary
        result = dispensers_data_schema.dump(dispenser_data)

        # convert to json and send
        return jsonify(result)

    else:
        return {"message": "device id is not registered"}, 404

# get all dispensers
@app.route('/api/dispenser/all', methods=['GET'])
def get_all_dispensers():
    # get all dispenser data
    all_dispensers = Dispenser.query.all()

    # convert data to dictionary
    result = dispensers_schema.dump(all_dispensers)

    # convert to json and send
    return jsonify(result)

# get single dispenser
@app.route('/api/dispenser/<device_id>', methods=['GET'])
def get_dispenser(device_id):
    # get dispenser
    dispenser = Dispenser.query.filter_by(device_id=device_id).first()

    if dispenser:
        # convert data to dictionary
        result = dispenser_schema.dump(dispenser)

        # convert to json and send
        return jsonify(result)

    else:
        return {"message": "device id is not registered"}, 404

def delete(items):
    for item in items:
        db.session.delete(item)

# delete dispenser and associated data
@app.route('/api/dispenser/delete/<device_id>', methods=['Delete'])
def delete_dispenser(device_id):
    # get dispenser with given device_id
    dispenser = Dispenser.query.filter_by(device_id=device_id).all()

    # get all dispenser data for a given device_id
    dispenser_data = DispenserData.query.filter_by(device_id=device_id).all()

    if dispenser and dispenser_data:

        # delete dispenser
        delete(dispenser)

        # delete dispenser data
        delete(dispenser_data)

        # commit changes to databse
        db.session.commit()

        return {"message": "device with id " + device_id + " and all associated data successfully deleted"}, 200
    
    else:
        return {"message": "device id is not registered"}, 404

@app.before_request
def before_request_func():
    print(request.method, request.url, request.remote_addr, request.endpoint)

# run Server
if __name__ == '__main__':
    # ip 0.0.0.0 allows all devices on the network to connect
    serve(app, host='0.0.0.0', port=8080, url_scheme='https')