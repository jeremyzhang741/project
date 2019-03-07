import requests
from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_bootstrap import Bootstrap
from flask_restplus import reqparse, Api, Resource
from rank import *
from prediction import *
from comments import *
from matching_function import *
import json



app = Flask(__name__)
api = Api(app, title='wine prediction system')
parser = reqparse.RequestParser()
parser.add_argument('Country', type=str)
parser.add_argument('Variety', type=str)
parser.add_argument('Winery', type=str)

@api.route('/main/value')
class prediction(Resource):
    @api.expect(parser, validate=True)
    def post(self):
        args = parser.parse_args(request)
        country = args.get('Country')
        variety = args.get('Variety')
        winery = args.get('Winery')
        price = prediction(country,variety,winery)
        recomm = recommendation(country,variety,winery)
        return {'price':price,'data':recomm}, 200

@api.route('/main/rank')
class rank(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('country', type=str)
        parser.add_argument('variety', type=str)
        parser.add_argument('price', type=str)
        parser.add_argument('top', type=str)
        args = parser.parse_args()
        top = args.get('top')
        top = int(top)
        country = args.get('country')
        variety = args.get('variety')
        price = args.get('price')
        result = ranked(country, variety, price, top)
        return jsonify(result), 200

@api.route('/main/show')
class show(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        name = args.get('name')
        data = show_reviews(name)
        return jsonify(data), 200

@api.route('/main/add')
class add(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('comments', type=str)
        parser.add_argument('points', type=str)
        args = parser.parse_args()
        name = args.get('name')
        comments = args.get('comments')
        points = args.get('points')
        points = int(points)
        data = add_reviews(name,comments,points)
        return jsonify(data), 200

@api.route('/main/match')
class match(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('palate', type=str, action='append')
        parser.add_argument('flavor', type=str, action='append')
        parser.add_argument('type',type=str)
        args = parser.parse_args()
        palate = args.get('palate')
        flavor = args.get('flavor')
        type = args.get('type')
        #print(palate)
        #print(flavor)
        li=palate+flavor
        data = matching_function(type,li)
        return jsonify(data), 200



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)

