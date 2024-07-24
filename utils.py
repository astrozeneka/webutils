
from time import sleep
from selenium.webdriver.common.by import By
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

def get_driver():
    #s = Service(ChromeDriverManager(version="117.0", latest_release_url="dsf").install())

    #s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    #options.browser_version = "117"
    # ถ้าอยากจะใช้ local chrome executable
    #options.binary_location = "../bin/chromedriver"


    if os.environ.get('MODE')=='headless': # Headless or headful
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    if os.environ.get('WINDOW_SIZE'):
        options.add_argument(f"--window-size={os.environ.get('WINDOW_SIZE')}")
    options.add_argument('--user-data-dir=data-dir')
    # driver = webdriver.Chrome(service=s, options=options)
    service = Service()
    # options.binary_location = "/Users/astrozeneka/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_mobile_driver():
    #s = Service(ChromeDriverManager(version="88.0", latest_release_url="dsf").install())
    s = ChromeDriverManager(version="88.0")
    options = webdriver.ChromeOptions()

    # Set mobile emulation options
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 10; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    if os.environ.get('MODE') == 'headless':  # Headless or headful
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=s, options=options)
    return driver

def element_exists(css_selector, regexp, driver):
    browser = driver
    elts = browser.execute_script(f"return document.querySelectorAll('{css_selector}')")
    cmp = re.compile(regexp)
    for elt in elts:
        if cmp.match(elt.text):
            return True
    return False

def send_keys(css_selector, text, driver):
    driver.find_element(By.CSS_SELECTOR, css_selector).send_keys(text)

def click(css_selector, driver):
    driver.execute_script(f"""
    let elt = document.querySelector('{css_selector}')
    elt.click()
    """)
    # driver.find_element(By.CSS_SELECTOR, css_selector).click()

def click_submit(css_selector, driver):
    click(css_selector, driver)
    sleep(0.5)

def click_by_text(css_selector, text, driver, case_sensitive=False):
    if case_sensitive:
        driver.execute_script(f"""
        let elts = document.querySelectorAll('{css_selector}')
    elts.forEach((elt)=>{{
      if(elt.innerText.includes(`{text}`))
          elt.click()
    }})""")
    else:
        driver.execute_script(f"""
        let elts = document.querySelectorAll('{css_selector}')
    elts.forEach((elt)=>{{
        if(elt.innerText.toLowerCase().includes(`{text.lower()}`))
            elt.click()
    }})""")
    sleep(0.2)

def has_text(css_selector, text, driver, case_sensitive=False):
    if case_sensitive:
        return driver.execute_script(f"""
        let elts = document.querySelectorAll('{css_selector}')
    let output = false;
    elts.forEach((elt)=>{{
    if(elt.innerText.includes("{text}")){{
    output = true;
    return
    }}
    }})
    return output""")
    else:
        return driver.execute_script(f"""
        let elts = document.querySelectorAll('{css_selector}')
    let output = false;
    elts.forEach((elt)=>{{
    if(elt.innerText.toLowerCase().includes("{text.lower()}")){{
    output = true;
    return
    }}
    }})
    return output""")

# Experimental feature has_text using regexp
def has_text_regexp(css_selector, regexp, driver):
    return driver.execute_script(f"""
    let elts = document.querySelectorAll('{css_selector}')
    let output = false;
    let cmp = new RegExp('{regexp}')
    elts.forEach((elt)=>{{
    if(cmp.test(elt.innerText)){{
    output = true;
    return
    }}
    }})
    return output""")


def get_selection_option_values(css_selector, driver):
    return driver.execute_script(f"""
    output=[]
let opts=document.querySelectorAll('{css_selector}>option')
opts.forEach(opt=>output.push(opt.value))
return output""")


def set_select_value(css_selector, value, driver):
    from selenium.webdriver.support.ui import Select
    #driver.execute_script(f"""let elt = document.querySelector('{css_selector}')
    #elt.value = '{value}'""")
    s = Select(driver.find_element(By.CSS_SELECTOR, css_selector))
    s.select_by_value(value)


def navigate(url, driver):
    driver.get(url)
    sleep(0.5)


def input_value(css_selector, driver):
    return driver.execute_script(f"return document.querySelector('{css_selector}').value")

def navigate_by_text(css_selector, text, driver):
    click_by_text(css_selector, text, driver)
    sleep(0.5)

def clear_input(css_selector, driver):
    elt = driver.find_element(By.CSS_SELECTOR, css_selector)
    elt.clear()
    elt.send_keys(" \b")

def set_server_time(time, driver):
    navigate(f"http://localhost:3001/api/v1/fakeTime/set?time={time}", driver)

def fill_input(driver, css_selector, value):
    try:
        elt = driver.find_element(By.CSS_SELECTOR, css_selector)
        elt.send_keys(value)
    except Exception as e:
        print(e)
        return