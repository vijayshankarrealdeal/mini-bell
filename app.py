from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from get_airport_status import GetAirportBorad, GetDetailStatus
#files import
from get_flight import GetFlights
from hotel import HotelApi
from moviedb import MovieDB
from shopping_nationl import Shopping


app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(GetFlights,"/getflights/<string:orgin>/<string:destination>/<string:date>/<int:adults>/<int:children>/<int:infants>")
api.add_resource(MovieDB,"/getlatestmovies/")
api.add_resource(Shopping,"/getshoping/<string:type_of_shop>")
api.add_resource(GetAirportBorad,"/getflightstatus/")
api.add_resource(GetDetailStatus,"/moreflightstatus/<string:link>")
api.add_resource(HotelApi,"/gethotel/<int:checkin_day>/<int:checkin_month>/<int:checkin_year>/<int:checkout_day>/<int:checkout_month>/<int:checkout_year>")

if __name__ == '__main__':
    app.run(debug=True)