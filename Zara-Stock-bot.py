from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email ayarları
def send_email(stock_message):
    sender_email = "sender@gmail.com"
    receiver_email = "example@outlook.com"
    password = "********" #This must be Google's app password after enabling "Two-Step Verification"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Zara Stock Update"

    message.attach(MIMEText(stock_message, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

IsAvailable = False

# Selenium options
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def check_stock():
    global IsAvailable
    url = "https://www.zara.com/tr/tr/cizgili-ve-mansetli-ince-ceket-p02010769.html?v1=345248126&v2=2210105" #This is a example
    driver.get(url)

    time.sleep(5)  #Waiting time for the page to load

    try:
        size_elements = driver.find_elements(By.CSS_SELECTOR, "li.size-selector-list__item")
        stock_message = ""

        for size_element in size_elements:
            size_text = size_element.find_element(By.CSS_SELECTOR, "div.product-size-info__main-label").text
            if "XS" in size_text or "S" in size_text: #You can change this with your size(s)
                if "size-selector-list__item--out-of-stock" not in size_element.get_attribute("class"):
                    stock_message += f"{size_text} clothes size is in stock!"

        if stock_message:
            send_email(stock_message)
            print(stock_message)
            IsAvailable = True
        else:
            print("The requested sizes are out of stock.")
    except Exception as e:
        print("Error:", e)

while not IsAvailable:
    check_stock()
    if not IsAvailable:
        time.sleep(300)  #Wait 5 minute and check again

driver.quit()