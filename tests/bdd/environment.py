from __future__ import annotations
import os
from selenium import webdriver
import shutil
from pathlib import Path
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def _find_chrome_binary() -> str | None:
    # Allow override via env
    env_bin = os.environ.get("CHROME_BIN")
    if env_bin and os.path.exists(env_bin):
        return env_bin
    # Common Windows locations
    candidates = [
        r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Google",
            "Chrome",
            "Application",
            "chrome.exe",
        ),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def _find_edge_binary() -> str | None:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _find_edge_driver_path() -> str | None:
    # 1) Explicit env
    env_path = os.environ.get("EDGE_DRIVER_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    # 2) On PATH
    which = shutil.which("msedgedriver") or shutil.which("msedgedriver.exe")
    if which:
        return which
    # 3) Common install locations (winget / manual)
    candidates = [
        Path(r"C:\\Program Files\\Microsoft\\EdgeWebDriver"),
        Path(r"C:\\Program Files (x86)\\Microsoft\\EdgeWebDriver"),
    ]
    for base in candidates:
        if base.exists():
            try:
                for p in base.rglob("msedgedriver.exe"):
                    return str(p)
            except Exception:
                pass
    return None


def before_all(context):
    # Default browser is Edge; set BROWSER=chrome to use Chrome instead.
    browser = os.environ.get("BROWSER", "edge").lower()

    if browser == "chrome":
        chrome_bin = _find_chrome_binary()
        copts = ChromeOptions()
        if os.environ.get("HEADFUL") != "1":
            copts.add_argument("--headless=new")
        copts.add_argument("--window-size=1280,900")
        copts.add_argument("--disable-gpu")
        copts.add_argument("--no-sandbox")
        copts.add_argument("--disable-dev-shm-usage")
        if chrome_bin:
            copts.binary_location = chrome_bin
        cservice = ChromeService(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(service=cservice, options=copts)
    else:
        edge_bin = os.environ.get("EDGE_BIN") or _find_edge_binary()
        if not edge_bin:
            raise RuntimeError(
                "Microsoft Edge tidak ditemukan. Install Edge atau set EDGE_BIN ke path msedge.exe."
            )
        eopts = EdgeOptions()
        if os.environ.get("HEADFUL") != "1":
            eopts.add_argument("--headless=new")
        eopts.add_argument("--window-size=1280,900")
        eopts.add_argument("--disable-gpu")
        eopts.add_argument("--no-sandbox")
        eopts.add_argument("--disable-dev-shm-usage")
        eopts.binary_location = edge_bin
        # Prefer Selenium Manager (no explicit driver path). It may work offline if a compatible driver exists on PATH.
        try:
            context.driver = webdriver.Edge(options=eopts)
        except Exception:
            # Offline fallback: try to discover a local msedgedriver
            driver_path = _find_edge_driver_path()
            if driver_path:
                eservice = EdgeService(driver_path)
                context.driver = webdriver.Edge(service=eservice, options=eopts)
            else:
                # Last resort: try webdriver-manager (requires internet on first run)
                eservice = EdgeService(EdgeChromiumDriverManager().install())
                context.driver = webdriver.Edge(service=eservice, options=eopts)

    context.base_url = os.environ.get("BASE_URL", "http://localhost:3000")


def after_all(context):
    try:
        context.driver.quit()
    except Exception:
        pass
