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
from flask_cors import CORS
from flask import Response, stream_with_context
from bson.json_util import dumps
import time
import os

app = Flask(__name__)
CORS(app)
#cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app, resources={r"/convert": {"origins": "*"}})
mongo_client = MongoClient("mongodb+srv://adinbo:ElectionsApp2023@cluster0.etzh8ey.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["pdfdatabase"]
# fs = gridfs.GridFS(db)
collection = db["pdf"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# @app.route("/")
# def hello_world():
#  return "Hello World!"


@app.route('/test/', methods= ['POST'])
# @cross_origin()
def hello_world():
  return "#hello world#!!!!"

@app.route('/')
# @cross_origin()
def hello_world1():
  return "#hello world without url#!!!!"
        

     
def test_db_connection():
    print("test_db_connection")
    try:
        client = MongoClient("mongodb+srv://adinbo:ElectionsApp2023@cluster0.etzh8ey.mongodb.net/?retryWrites=true&w=majority")
        db1 = client.pdfdatabase  # Access the pdfdatabase  
        # Check if the connection is successful by accessing a collection
        pdf_collection = db1.pdf
        print( "Successfully connected to database!")
        return pdf_collection
    
    except Exception as e:
        return f"Failed to connect to the database: {e}"
    
# @app.route('/download/<pdf_id>', methods=['GET'])
# def download_pdf(pdf_id):
#     pdf_collection = test_db_connection()

#     try:
#         pdf_data = pdf_collection.find_one({"_id": ObjectId(pdf_id)})
#         if not pdf_data:
#             return jsonify({'error': 'File not found'}), 404
#         return Response(pdf_data['content'], mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename={}.pdf'.format(pdf_id)})
#     except Exception as e:  
#         return jsonify({'error': str(e)}), 500


@app.route('/download/<pdf_id>', methods=['GET'])
def download_pdf(pdf_id):
    pdf_collection = test_db_connection()
    try:
        pdf_data = pdf_collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf_data:
            return jsonify({'error': 'File not found'}), 404

        def generate():
            yield pdf_data['content']
        return Response(stream_with_context(generate()), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename={}.pdf'.format(pdf_id)})
    except Exception as e:  
        return jsonify({'error': str(e)}), 500
    
@app.route('/convert', methods=['POST'])
def convert():
    
    try:
        data = request.get_json()  # Use get_json to extract JSON data from the request
        url_to_convert = data.get('url')
        pdf_collection = test_db_connection()
        # pdf_collection.insert_one({"file_data": "binary_data"})

        if not url_to_convert:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Add the code for PDF conversion using Selenium
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("http://deck2pdf.com")
        
        input_field = driver.find_element(By.ID, 'docsendURL')
        input_field.send_keys(url_to_convert)

        convert_button = driver.find_element(By.CLASS_NAME, 'btn-primary')
        convert_button.click()


        timeout = 1200
        link_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/tmp/') and contains(@href, '.pdf')]")
            )
        )
        link_element.click()
        
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        seen_files = set()  # A set to keep track   of processed files

        time.sleep(2)  # A slight delay to ensure the file is downloaded.

        pdf_id = None
        while True:
            time.sleep(0.1)  # Poll every second
            for filename in os.listdir(downloads_folder):
                if filename.endswith('.pdf') and filename not in seen_files:
                    file_path = os.path.join(downloads_folder, filename)
                    with open(file_path, "rb") as pdf_file:
                        binary_data = pdf_file.read()
                        pdf_inserted = pdf_collection.insert_one({"url": url_to_convert, "content": binary_data})
                        pdf_id = pdf_inserted.inserted_id
                    os.remove(file_path)  # Optionally remove the file after processing                    
                    break
                    # pdf_inserted = pdf_collection.insert_one({"url": url_to_convert, "content": binary_data})
            if pdf_id is not None: 
                print(pdf_id)
                print("Success")
                return jsonify({'message': 'PDF converted and saved to MongoDB', 'pdf_id': str(pdf_id)}), 200                          
                break
        
        print("Sucess")
        return jsonify({'message': 'PDF converted and saved to MongoDB'}), 200
            # return jsonify({'message': 'PDF converted and saved to MongoDB', 'pdf_id': str(pdf_id)}), 200



                    # print(f"Success: {filename} opened and data inserted successfully")

        # pdf_collection.insert_one({"file_data": "binary_data"})
    except TimeoutException:
        print(f"Timeout occurred after {timeout} seconds while waiting for the PDF download link.")
        return jsonify({'error': 'Timeout occurred while waiting for the PDF download link.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    # finally:
    #     # Keep the window open for inspection before quitting
    #     input("Press Enter to close the browser...")
        
    #     driver.quit()
if __name__ == '__main__':
    app.run(debug=True)
