# REST Server

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

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
    device_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    location = db.Column(db.String(20), unique=True)
    created = db.Column(db.String(20))

    def __init__(self, name, location, created):
        self.name = name
        self.location = location
        self.created = created

class DispenserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Float)
    volume_dispensed = db.Column(db.Float)
    fluid_level = db.Column(db.Float)
    ignored = db.Column(db.Boolean)
    datetime = db.Column(db.String(20))

    def __init__(self, distance, volume_dispensed, fluid_level, ignored, datetime):
        self.distance = distance
        self.volume_dispensed = volume_dispensed
        self.fluid_level = fluid_level
        self.ignored = ignored
        self.datetime = datetime

# Dispenser schema
class DispenserDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'distance', 'volume_dispensed', 'fluid_level', 'ignored', 'datetime')

# Dispenser Data schema
class DispenserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'created')

# init schemas
dispenser_data_schema = DispenserDataSchema()
dispensers_data_schema = DispenserDataSchema(many=True)

dispenser_schema = DispenserSchema()
dispensers_schema = DispenserSchema(many=True)

# register dispenser
@app.route('/dispenser/register', methods=['POST'])
def register_dispenser():
    device_id = request.json['device_id']
    name = request.json['name']
    location = request.json['location']
    created = request.json['created']

    # assign id
    if not device_id:
        print("unregistered device")
        new_dispenser = Dispenser(name, location, created)

    return dispenser_schema.jsonify(new_dispenser)

# add Dispenser Data
@app.route('/dispenser', methods=['POST'])
def add_dispenser_data():
    distance = request.json['distance']
    volume_dispensed = request.json['volume_dispensed']
    fluid_level = request.json['fluid_level']
    ignored = request.json['ignored']
    datetime = request.json['datetime']

    new_dispenser_data = DispenserData(distance, volume_dispensed, fluid_level, ignored, datetime)

    print(new_dispenser_data.fluid_level)

    db.session.add(new_dispenser_data)
    db.session.commit()

    return dispenser_data_schema.jsonify(new_dispenser_data)

# get all dispensers
@app.route('/dispensers', methods=['GET'])
def test():
    # get all dispenser data
    all_dispensers = DispenserData.query.all()

    # convert data to dictionary
    result = dispensers_data_schema.dump(all_dispensers)

    # convert to json and send
    return jsonify(result)

# run Server
if __name__ == '__main__':
    # ip 0.0.0.0 allows all devices on the network to connect
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)