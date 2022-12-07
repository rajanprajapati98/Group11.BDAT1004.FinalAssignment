import flask
from flask import Flask
from flask_cors import CORS, cross_origin

from utils import get_acquisition_data_collection

app = Flask(__name__)
cors = CORS(app)



@app.route('/api/v1/countries', methods=['GET'])
@cross_origin()
def get_all_countries():
    acquisition_dc = get_acquisition_data_collection()
    all_countries_result = acquisition_dc.find({}, {'_id': False})
    return flask.jsonify([item for item in all_countries_result])


@app.route('/api/v1/countries/<int:start_country_id>/<int:end_country_id>', methods=['GET'])
@cross_origin()
def get_counties_from_to_in_range(start_country_id, end_country_id):
    acquisition_dc = get_acquisition_data_collection()
    countries_result = acquisition_dc.find({'country_id': {'$gte': start_country_id, '$lte': end_country_id}}, {'_id': False})
    return flask.jsonify([item for item in countries_result])


@app.route('/api/v1/country/<int:country_id>', methods=['GET'])
@cross_origin()
def get_country_by_country_id(country_id):
    acquisition_dc = get_acquisition_data_collection()
    country_result = acquisition_dc.find_one({'country_id': country_id}, {'_id': False})
    return flask.jsonify(country_result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
