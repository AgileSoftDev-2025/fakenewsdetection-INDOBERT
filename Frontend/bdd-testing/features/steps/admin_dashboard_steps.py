from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I am on "Admin Homepage"')
def step_on_admin_homepage(context):
    context.browser.get("http://localhost:3001/")

@then('I should see "Total Pengecekan"')
def step_see_total_pengecekan(context):
    WebDriverWait(context.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Total Pengecekan')]")))
    assert "Total Pengecekan" in context.browser.page_source

@then('I should see "Hoax Terdeteksi"')
def step_see_hoax_terdeteksi(context):
    assert "Hoax Terdeteksi" in context.browser.page_source

@then('I should see "Sistem Overview"')
def step_see_sistem_overview(context):
    assert "Sistem Overview" in context.browser.page_source

@then('I should see "Update Model"')
def step_see_update_model(context):
    assert "Update Model" in context.browser.page_source

@then('I should see "Aksi Admin"')
def step_see_aksi_admin(context):
    assert "Aksi Admin" in context.browser.page_source