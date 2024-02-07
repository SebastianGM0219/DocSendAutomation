from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time



# Initialize the driver
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--disable-gpu')  # This flag is necessary in headless mode.
chrome_options.add_argument('--no-sandbox')  # This flag is also typically necessary in headless mode.
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')


service = Service(ChromeDriverManager().install(),options=chrome_options)
driver = webdriver.Chrome(service=service)

# Navigate to the website
driver.get("http://deck2pdf.com")

# Find the input field and enter the text "RRS"
input_field = driver.find_element(By.ID, 'docsendURL') # Replace 'input-field-id' with the actual ID of the input element
input_field.send_keys("https://docsend.com/view/mcy8h43sjjf5hchf")

# Find and click the convert button
convert_button = driver.find_element(By.CLASS_NAME, 'btn-primary')  # Using the class name to locate the "Convert" button
convert_button.click()

convert_button.find_element(By.ID, "docusendURL")
# Wait for the file to be ready for download
# This step is greatly dependent on how the website functions.
# You might need to wait for a certain element to be visible or check the status of the download.
timeout = 120

try:
    # Wait until the element appears with href attribute starting with '/tmp/' and ending with '.pdf'
    link_element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, '/tmp/') and contains(@href, '.pdf')]")
        )
    )
    
    # Click the link when it's available
    link_element.click()
except TimeoutException:
    print(f"Timeout occurred after {timeout} seconds while waiting for the PDF download link.")
except Exception as e:
    print(f"An exception occurred: {e}")
time.sleep(1000000)
driver.quit()