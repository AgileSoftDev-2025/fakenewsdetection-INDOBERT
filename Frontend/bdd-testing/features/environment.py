import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
    # Configure Chrome options (headless by default for CI/running without display)
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Use new headless mode when available
    try:
        options.add_argument("--headless=new")
    except Exception:
        options.add_argument("--headless")

    # Locate Chrome/Chromium binary: prefer CHROME_BINARY env, then common macOS paths
    def find_chrome_binary():
        env_path = os.environ.get("CHROME_BINARY")
        candidates = []
        if env_path:
            candidates.append(env_path)
        candidates.extend([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ])
        for p in candidates:
            if p and os.path.exists(p):
                return p
        return None

    chrome_bin = find_chrome_binary()
    if chrome_bin:
        options.binary_location = chrome_bin
    else:
        raise RuntimeError(
            "Chrome binary not found. Install Google Chrome (brew install --cask google-chrome) "
            "or Chromium, or set the CHROME_BINARY environment variable to the browser binary path."
        )

    # Create Chrome service using webdriver-manager to auto-download driver
    service = Service(ChromeDriverManager().install())

    # Create browser and store on context
    context.browser = webdriver.Chrome(service=service, options=options)

def after_all(context):
    # Close browser if it was created
    if hasattr(context, "browser") and context.browser:
        try:
            context.browser.quit()
        except Exception:
            pass
