import time
import json
from datetime import datetime
from webbrowser import BackgroundBrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException
from pymongo import MongoClient
import requests
from selenium import *
from flask import Flask, render_template, jsonify
import threading
import certifi
import urllib.parse

password = urllib.parse.quote_plus("Akash@1906")

try:
    client = MongoClient(
        f'mongodb+srv://akash:{password}@cluster0.zl2ck.mongodb.net/?retryWrites=true&w=majority',
        serverSelectionTimeoutMS=10000,
        tls=True,
        tlsCAFile=certifi.where(),
        connectTimeoutMS=30000,
        socketTimeoutMS=30000
    )
    db = client['twitter_trends']
    collection = db['trending_topics']
except Exception as e:
    print(f"MongoDB connection error: {e}")

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-features=NetworkService')
    options.add_argument('--dns-prefetch-disable')
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    return driver

def login_to_twitter(driver):
    try:
        driver.get("https://twitter.com/login")
        time.sleep(15)  

        wait = WebDriverWait(driver, 30)
        
        username_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='username']")))
        username_input.clear()
        time.sleep(2)
        username_input.send_keys("ghosh_akas16422")
        time.sleep(2)
        username_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='current-password']")))
        password_input.clear()
        time.sleep(2)
        password_input.send_keys("Akash@1906")
        time.sleep(2)
        password_input.send_keys(Keys.RETURN)
        time.sleep(15) 
    except Exception as e:
        print(f"Error during login: {e}")
        raise

def click_explore_button(driver):
    try:
        time.sleep(10)  
        driver.execute_script("""
            document.querySelector('[data-testid="AppTabBar_Explore_Link"]').click();
        """)
        time.sleep(10)
    except Exception as e:
        print(f"Error clicking explore: {e}")
        raise

def get_trending_topics(driver):
    trends = []
    wait = WebDriverWait(driver, 30)
    
    try:
        time.sleep(15)  
        
        try:
            trend_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="trendItem"]')
            if not trend_elements:
                trend_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="trend"]')
        except:
            trend_elements = []

        if not trend_elements:
            trend_elements = driver.find_elements(By.CSS_SELECTOR, 'div[style*="position: relative"] > div > span')

        for element in trend_elements[:5]:
            try:
                trend_text = ''
                try:
                    trend_text = element.get_attribute('textContent')
                except:
                    try:
                        trend_text = element.text
                    except:
                        continue

                trend_text = trend_text.strip()
                if trend_text and trend_text != "undefined" and not trend_text.isdigit():
                    if 'K' not in trend_text and 'M' not in trend_text:  
                        trends.append(trend_text)
            except:
                continue

        if not trends:
            trend_texts = driver.execute_script("""
                return Array.from(document.querySelectorAll('div[style*="position: relative"] > div > span'))
                    .map(el => el.textContent)
                    .filter(text => text && text.trim() && !text.includes('K') && !text.includes('M'))
                    .slice(0, 5);
            """)
            trends.extend([t.strip() for t in trend_texts if t and t.strip() != "undefined"])

        trends = [t for t in trends if t and t != "undefined"][:5]
        
        if not trends:
            print("No valid trends found after all attempts")
            
    except Exception as e:
        print(f"Error in trend extraction: {e}")
    
    return trends

def save_to_mongodb(trends, ip):
    try:
        unique_id = str(datetime.now().timestamp())
        data = {
            "_id": unique_id,
            "trends": trends if trends else [],
            "datetime": datetime.now(),
            "ip_address": ip if ip else "IP Unavailable",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        collection.insert_one(data)
        return data
    except Exception as e:
        print(f"MongoDB Error: {e}")
        return {
            "trends": trends if trends else [],
            "ip_address": ip if ip else "IP Unavailable",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": str(e)
        }

def main():
    driver = None
    try:
        driver = get_driver()
        login_to_twitter(driver)
        click_explore_button(driver)

        trends = []
        max_attempts = 3
        for attempt in range(max_attempts):
            trends = get_trending_topics(driver)
            if trends:
                break
            time.sleep(5)
        
        try:
            ip = requests.get('http://ip-api.com/json/', timeout=5).json().get('query', 'IP Unavailable')
        except:
            ip = 'IP Unavailable'
            
        return {
            "trends": trends if trends else [],
            "ip_address": ip
        }

    except Exception as e:
        print(f"Error in main function: {e}")
        return {
            "trends": [],
            "ip_address": "IP Unavailable"
        }
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    try:
        result = main()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "trends": [],
            "ip_address": "IP Unavailable"
        })

if __name__ == '__main__':
    app.run(debug=True)