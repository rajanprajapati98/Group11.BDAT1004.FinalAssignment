from flask_pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def get_acquisition_data_collection():
    mongoDbUrl = 'mongodb+srv://rajan_prajapati:rajanrajan@finalproject.6467p3n.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(
        mongoDbUrl,
        username='rajan_prajapati', password='rajanrajan')
    try:
        visualize_project_database = client.get_database('visualize_project')
        acquisition_data_collection = visualize_project_database.get_collection('acquisition_data')
        return acquisition_data_collection
    except ConnectionFailure:
        print("*** visualize project database is failed to connect at this moment ***")
