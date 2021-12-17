from flask.json import jsonify
from flask_restful import Resource
import pandas as pd



def hotelAPi(checkin_day, checkin_month, checkin_year, checkout_day, checkout_month, checkout_year):
    days = abs(checkout_day - checkin_day)
    month = abs(checkout_day - checkin_day)
    yr = abs(checkout_day - checkin_day)
    total = (days+month+yr)/2
    df = pd.read_csv('hotels.csv')
    def spiltx(x):
        if 'km' in x:
            x = x.split('km')
            x = float(x[0])*1000
        else:
            x = x.split('m')
            x = x[0]
        return int(x)
    def format_price(x,total,lam):
        p = x.split("₹")[-1].split(',')
        rt = float(''.join(p))
        x = int(rt+total*lam)
        x = str(x)
        x = "₹ " + x[:-3] + ","+x[-3:]
        return x
    def money_numX(x):
        p = x.split("₹")[-1].split(',')
        rt = int(''.join(p))
        return rt
    df.money = df.money.apply(lambda x:format_price(x,total,0.2))
    df['distanceM'] = df.distance.apply(spiltx)
    df['money_num'] = df.money.apply(money_numX)
    return [df.T.to_dict()[i] for i in df.T.to_dict()]


class HotelApi(Resource):
    def get(self, checkin_day, checkin_month, checkin_year, checkout_day, checkout_month, checkout_year):
        hoteldata = hotelAPi(checkin_day, checkin_month,
                             checkin_year, checkout_day, checkout_month, checkout_year)
        return jsonify({"data": hoteldata})
