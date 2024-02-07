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
import gridfs
import time

app = Flask(__name__)
mongo_client = MongoClient("your_mongodb_uri")
db = mongo_client["pdf_database"]
fs = gridfs.GridFS(db)

chrome_options = webdriver.ChromeOptions()

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    url_to_convert = data.get('url')
    if not url_to_convert:
        return jsonify({'error': 'No URL provided'}), 400

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("http://deck2pdf.com")
    
    input_field = driver.find_element(By.ID, 'docsendURL') # Replace 'input-field-id' with the actual ID of the input element
    input_field.send_keys(url_to_convert)

    convert_button = driver.find_element(By.CLASS_NAME, 'btn-primary')  # Using the class name to locate the "Convert" button
    convert_button.click()


    timeout = 120

    try:
        link_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/tmp/') and contains(@href, '.pdf')]")
            )
        )
        
        link_element.click()
    except TimeoutException:
        print(f"Timeout occurred after {timeout} seconds while waiting for the PDF download link.")
    except Exception as e:
        print(f"An exception occurred: {e}")
    time.sleep(1000000)

    with open("temp_folder/downloaded.pdf", "rb") as pdf_file:
        fs.put(pdf_file, filename="downloaded.pdf")
    
    driver.quit()
    return jsonify({'message': 'PDF converted and saved to MongoDB'}), 200

if __name__ == '__main__':
    app.run(debug=False)

