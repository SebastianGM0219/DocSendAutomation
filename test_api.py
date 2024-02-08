from flask import Flask, Response, request, jsonify
from bson.objectid import ObjectId
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from bson.json_util import dumps
import gridfs
import time
import os
import webbrowser

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        url_to_convert = data.get('url')
        
        # Add input validation here if needed
        
        # Your PDF conversion logic here
        
        # Assuming PDF conversion is successful
        # Send the success response to the front-end
        return jsonify({'message': 'PDF converted successfully!'}), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred during the PDF conversion: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
