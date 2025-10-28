from __future__ import annotations
import time
from pathlib import Path
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _resolve_path(path_str: str) -> str:
    """Resolve special paths used in scenarios to actual files.
    If path is "/path/valid_news.docx", create a temp DOCX with sample text and return its path.
    Otherwise, treat as absolute or workspace-relative path.
    """
    if path_str == "/path/valid_news.docx":
        try:
            from docx import Document  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "python-docx is required for document scenario. Install it in test env."
            ) from e
        tmp_dir = Path("tests/fixtures")
        tmp_dir.mkdir(parents=True, exist_ok=True)
        fpath = tmp_dir / "valid_news.docx"
        if not fpath.exists():
            doc = Document()
            doc.add_paragraph("The government officially announces a national holiday")
            doc.save(fpath)
        return str(fpath.resolve())

    p = Path(path_str)
    if p.exists():
        return str(p.resolve())
    # Try workspace-relative
    wrk = Path.cwd() / path_str
    if wrk.exists():
        return str(wrk.resolve())
    raise FileNotFoundError(f"Test file not found: {path_str}")


@given('I am on "check-news page"')
def step_open_home(context):
    context.driver.get(context.base_url + "/")


@when('I fill in "{field}" with "{text}"')
def step_fill_text(context, field: str, text: str):
    # we only support news_text for now
    if field != "news_text":
        raise AssertionError(f"Unsupported field: {field}")
    el = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="news_text"]'))
    )
    el.clear()
    el.send_keys(text)


@when('I attach the file "{path}" to "{field}"')
def step_attach_file(context, path: str, field: str):
    if field != "news_file":
        raise AssertionError(f"Unsupported field: {field}")
    # Switch to File tab by clicking button label "File"
    try:
        btn = context.driver.find_element(
            By.XPATH, "//button[normalize-space()='File']"
        )
        btn.click()
        time.sleep(0.2)
    except Exception:
        pass
    file_input = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="news_file"]'))
    )
    # Make hidden input visible so Selenium can send_keys
    context.driver.execute_script(
        "arguments[0].classList.remove('hidden'); arguments[0].style.display='block';",
        file_input,
    )
    real_path = _resolve_path(path)
    file_input.send_keys(real_path)


@when('I press "{label}"')
def step_press_button(context, label: str):
    # Prefer data-testid for stability
    try:
        btn = context.driver.find_element(By.CSS_SELECTOR, '[data-testid="check"]')
    except Exception:
        # Fallback by button text
        btn = context.driver.find_element(By.XPATH, f"//button[contains(., '{label}')]")
    btn.click()


@then('I should see "Valid/Hoax"')
def step_should_see_result(context):
    # Wait until navigation to results or result rendered
    WebDriverWait(context.driver, 30).until(
        lambda d: any(
            term in d.page_source
            for term in ["Valid", "valid", "Hoax", "hoax", "Hoaks", "Bukan Hoaks"]
        )
    )
