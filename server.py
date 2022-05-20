from itertools import product
from flask import Flask, request, jsonify
from scraper import Scraper
server = Flask(__name__)

@server.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@server.route('/api/flipkart/<product>', methods=['GET'])
def get_flipkart_data(product):
    url = f'https://www.flipkart.com/search?q={product}&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY&page=1'
    return jsonify(Scraper(url).get_flipkart_data())

@server.route('/api/amazon/<product>', methods=['GET'])
def get_amazon_data(product):
    url = f'https://www.amazon.in/s?k={product}'
    return jsonify(Scraper(url).get_amazon_data())

@server.route('/api/myntra/<product>', methods=['GET'])
def get_myntra_data(product):
    url = f'https://www.myntra.com/iphone'
    return jsonify(Scraper(url).get_myntra_data())

@server.route('/api/nykaa/<product>', methods=['GET'])
def get_nykaa_data(product):
    url = f'https://www.nykaa.com/search/result/?q={product}&root=search'
    return jsonify(Scraper(url).get_nykaa_data())