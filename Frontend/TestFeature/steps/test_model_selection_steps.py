from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EDGE_DRIVER_PATH = r"C:\Users\CrowBell\Downloads\edgedriver_win64\msedgedriver.exe"

# Utility: Wait for element with timeout
def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

@given('I open the ListModelAI page')
def step_open_page(context):
    logger.info("Opening ListModelAI page using EdgeDriver...")
    service = EdgeService(EDGE_DRIVER_PATH)
    context.driver = Edge(service=service)
    context.driver.get("http://localhost:5173/")
    context.driver.maximize_window()
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    logger.info("✅ Page loaded successfully.")

@when('I click on "{button_text}" button of "{model_name}"')
def step_click_model_button(context, button_text, model_name):
    logger.info(f"Clicking '{button_text}' for {model_name}...")

    # Find all model cards by locating divs that contain an <h2>
    cards = context.driver.find_elements(By.XPATH, "//div[h2]")

    logger.info(f"Found {len(cards)} cards on the page.")
    for i, card in enumerate(cards):
        title = card.find_element(By.TAG_NAME, "h2").text.strip()
        btns = card.find_elements(By.TAG_NAME, "button")
        logger.info(f"Card {i+1} title: {title}, Buttons: {[b.text for b in btns]}")

        if model_name.lower() in title.lower():
            for btn in btns:
                if button_text.lower() in btn.text.lower():
                    btn.click()
                    logger.info(f"✅ Clicked '{button_text}' on {model_name}")
                    time.sleep(1)
                    return
    raise AssertionError(f"Button '{button_text}' for '{model_name}' not found.")

@then('I should see a toast message "{expected_message}"')
def step_check_toast_message(context, expected_message):
    logger.info(f"Checking toast for message: {expected_message}")
    try:
        # Wait for the toast container to appear
        toast = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//div[contains(@class, 'toast') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{expected_message.lower()}')]"
            ))
        )
        logger.info(f"✅ Toast found with message: {toast.text}")
        assert expected_message.lower() in toast.text.lower(), (
            f"Expected '{expected_message}', but got '{toast.text}'"
        )
        # Keep it visible long enough for manual confirmation (optional)
        time.sleep(1)
    except Exception as e:
        logger.error(f"❌ Toast not found or incorrect: {e}")
        # Screenshot for debugging (optional)
        context.driver.save_screenshot("toast_error.png")
        raise AssertionError(f"Toast message '{expected_message}' not found or mismatched.")

@given('"{model_name}" is already active')
def step_model_already_active(context, model_name):
    step_open_page(context)
    step_click_model_button(context, "Aktifkan", model_name)
    time.sleep(1)

@then('the model card should show "Aktif"')
def step_card_should_show_active(context):
    logger.info("Checking that active badge appears...")
    badge = WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Aktif')]"))
    )
    assert badge, "❌ Badge 'Aktif' not found."
    logger.info("✅ Active badge found.")

@then('the model card should not show "Aktif"')
def step_card_should_not_show_active(context):
    logger.info("Checking that active badge disappears...")
    time.sleep(1)
    badges = context.driver.find_elements(By.XPATH, "//span[contains(text(), 'Aktif')]")
    assert len(badges) == 0, "❌ Badge 'Aktif' still visible."
    logger.info("✅ Active badge no longer visible.")
