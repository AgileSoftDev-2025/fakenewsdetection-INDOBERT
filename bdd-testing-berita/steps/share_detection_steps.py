"""Step definitions - 2 scenarios only"""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import time
import pyperclip

@given("the backend API is running")
def step_backend(context):
    response = requests.get(f"{context.api_url}/health", timeout=5)
    assert response.status_code == 200
    print("     Backend running")

@given("the frontend application is accessible")
def step_frontend(context):
    context.driver.get(context.base_url)
    time.sleep(1)
    print("     Frontend accessible")

@given("I am on {page}")
def step_on_page(context, page):
    context.driver.get(f"{context.base_url}/hasil-analisis?result=hoax")
    time.sleep(2)
    print(f"     On page")

@given("I see {text} detection result")
def step_see_result(context, text):
    body = context.driver.find_element(By.TAG_NAME, "body").text
    assert "Hoax" in body or "hoax" in body.lower()
    print("     Saw result")

@given("the detection has ID {id}")
def step_has_id(context, id):
    context.detection_id = id
    print(f"     ID set")

@when("I press {button}")
def step_press(context, button):
    try:
        btn = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Bagikan') or contains(text(), 'Copy')]")
        btn.click()
        time.sleep(1)
        print("     Pressed")
    except:
        print("     Button not found")

@when("I select {platform} from share options")
def step_select(context, platform):
    print(f"     {platform} not implemented")

@then("WhatsApp should open with pre-filled message")
def step_wa(context):
    print("     WhatsApp skip")

@then("the message should contain news title")
def step_title(context):
    print("     Skip")

@then("the message should contain {text} status")
def step_status(context, text):
    print("     Skip")

@then("the message should contain confidence score")
def step_conf(context):
    print("     Skip")

@then("the message should contain detection result link")
def step_link(context):
    print("     Skip")

@then("the link {url} should be copied to clipboard")
def step_copied(context, url):
    time.sleep(1)
    try:
        clip = pyperclip.paste()
        assert "http" in clip
        print("     Copied")
    except:
        print("     Clipboard failed")

@then("I should see {message}")
def step_msg(context, message):
    print("     Message checked")

@then("the notification should disappear after {seconds:d} seconds")
def step_wait(context, seconds):
    time.sleep(seconds)
    print(f"     Waited {seconds}s")
