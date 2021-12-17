from flask_restful import Resource
import requests
from flask import jsonify



def get_movieList(api_key):
    data = requests.get('https://api.themoviedb.org/3/trending/all/day?api_key='+api_key)
    return data.json()


class MovieDB(Resource):
    def get(self):
        api_key = '38f5b3c12b04920fbe5fd093187951af'
        data = get_movieList(api_key)
        return jsonify(data)
