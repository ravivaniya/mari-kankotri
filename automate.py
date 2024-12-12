import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Folder Path containing the PDF files
PDF_FOLDER = "/Users/ravivaniya/Developer/mari-kankotri/output_invites"

# Delay settings
WAIT_TIME = 30

# Function to initialize the WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./whatsapp_profile")  # Save WhatsApp session
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to send a message and attach a file
def send_message(driver, mobile_number, user_name, file_path):
    try:
        # Open WhatsApp Web chat
        url = f"https://web.whatsapp.com/send?phone={mobile_number}&text=Hi%20{user_name}!%20This%20is%20automated%20message%20pls%20ignore%20this."
        driver.get(url)
        time.sleep(60)  # Wait for the chat to load

        # Locate the attachment button
        attach_button = driver.find_element(By.XPATH, "//span[@data-icon='plus']")
        attach_button.click()
        time.sleep(15)

        # Upload the PDF file
        file_input = driver.find_element(By.XPATH, "//input[@accept='*']")
        file_input.send_keys(file_path)
        time.sleep(60)  # Wait for the file to upload

        # Click the send button
        send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
        send_button.click()
        time.sleep(10)  # Wait for the message to be sent

        print(f"Message sent to {mobile_number} {user_name}")
    except Exception as e:
        print(f"Failed to send message to {mobile_number}: {e}")

# Main Logic
if __name__ == "__main__":
    # Initialize WebDriver
    driver = init_driver()

    # Wait for the user to scan the QR code
    print("Please scan the QR code to log in to WhatsApp Web.")
    driver.get("https://web.whatsapp.com/")
    time.sleep(60)

    for file_name in os.listdir(PDF_FOLDER):
        if file_name.endswith(".pdf"):
            # Extract mobile number and user name from file name
            parts = file_name.replace(".pdf", "").split("_")
            if len(parts) == 2:
                mobile_number, user_name = parts
                pdf_path = os.path.join(PDF_FOLDER, file_name)

                # Send the message and PDF
                send_message(driver, mobile_number, user_name, pdf_path)

                # Wait before processing the next user
                time.sleep(WAIT_TIME)
            else:
                print(f"Invalid file name format: {file_name}")

    # Close the WebDriver
    driver.quit()
