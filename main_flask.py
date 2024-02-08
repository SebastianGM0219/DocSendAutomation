from flask import Flask, request, jsonify
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
mongo_client = MongoClient("mongodb+srv://adinbo:ElectionsApp2023@cluster0.etzh8ey.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["pdfdatabase"]
# fs = gridfs.GridFS(db)
collection = db["pdf"]

chrome_options = webdriver.ChromeOptions()

def test_db_connection():
    print("test_db_connection")
    try:
        # Attempt to connect to MongoDB Atlas
        client = MongoClient("mongodb+srv://adinbo:ElectionsApp2023@cluster0.etzh8ey.mongodb.net/?retryWrites=true&w=majority")
        # client.server_info()  # This line will raise an exception if the connection is not successful
        db1 = client.pdfdatabase  # Access the pdfdatabase
        # Check if the connection is successful by accessing a collection
        pdf_collection = db1.pdf
        # pdf_documents = pdf_collection.find({})
        # pdf_json = dumps(pdf_documents)
        # print(pdf_json)

        print( "Successfully connected to database!")
        return pdf_collection
    
    except Exception as e:
        return f"Failed to connect to the database: {e}"
    
@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()  # Use get_json to extract JSON data from the request
        url_to_convert = data.get('url')

        # connection_status = test_db_connection()
        pdf_collection = test_db_connection()
        pdf_collection.insert_one({"file_data": "binary_data"})

        print("fool")
        print(url_to_convert)
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
        
        # Add the code to save the PDF to MongoDB using gridfs
        # with open("downloads/mcy8h43sjjf5hchf.pdf", "rb") as pdf_file:
        #     fs.put(pdf_file, filename="downloaded.pdf")

        pdf_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'mcy8h43sjjf5hchf.pdf')
        try:
            with open(pdf_path, "rb") as pdf_file:
                binary_data = pdf_file.read()
                print("opened")
                webbrowser.open(pdf_path)
                pdf_collection.insert_one({"url": "RRS", "content": binary_data})
            print("Success: File opened and data inserted successfully")
        except Exception as e:
            print("Error: " + str(e))

        # pdf_collection.insert_one({"url": url_to_convert, "content": pdf_content})
        # Insert the PDF file as binary data into the collection
        # collection.insert_one({"file_data": "binary_data"})
        pdf_collection.insert_one({"file_data": "binary_data"})

        return jsonify({'message': 'PDF converted and saved to MongoDB'}), 200
    except TimeoutException:
        print(f"Timeout occurred after {timeout} seconds while waiting for the PDF download link.")
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        # Keep the window open for inspection before quitting
        input("Press Enter to close the browser...")
        driver.quit()
if __name__ == '__main__':
    app.run(debug=False)
