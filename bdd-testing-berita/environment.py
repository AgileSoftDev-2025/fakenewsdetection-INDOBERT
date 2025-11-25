"""
Behave environment setup for BDD testing
Handles Selenium WebDriver and test context
"""

import os
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests


def before_all(context):
    """
    Setup yang dijalankan sebelum semua test
    """
    # Configuration
    context.base_url = os.getenv('BASE_URL', 'http://localhost:3000')
    context.api_url = os.getenv('API_URL', 'http://localhost:8000')
    context.timeout = 10
    
    # Create screenshots directory
    screenshots_dir = Path('screenshots')
    if screenshots_dir.exists():
        shutil.rmtree(screenshots_dir)
    screenshots_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*60)
    print("🚀 Starting BDD Testing Suite")
    print("="*60)
    print(f"📍 Frontend URL: {context.base_url}")
    print(f"📍 Backend API: {context.api_url}")
    
    # Check if backend is running
    try:
        response = requests.get(f"{context.api_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running")
        else:
            print(f"⚠️  Backend returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Backend is not accessible: {e}")
        print("💡 Please start backend with: uvicorn app.main:app --reload")
        exit(1)
    
    print("="*60 + "\n")


def before_scenario(context, scenario):
    """
    Setup yang dijalankan sebelum setiap scenario
    Inisialisasi browser baru untuk setiap scenario
    """
    print(f"\n📝 Scenario: {scenario.name}")
    
    # Chrome options
    chrome_options = Options()
    
    # Headless mode untuk CI/CD (uncomment jika perlu)
    # chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-notifications')
    
    # Enable clipboard access
    chrome_options.add_experimental_option('prefs', {
        'profile.default_content_setting_values.clipboard': 1,
        'profile.default_content_setting_values.notifications': 2
    })
    
    # Disable automation flags (to avoid detection)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set implicit wait
        context.driver.implicitly_wait(context.timeout)
        
        # Maximize window
        context.driver.maximize_window()
        
        # Initialize context variables
        context.result_id = None
        context.share_url = None
        context.analysis_data = {}
        
        print("✅ Browser initialized")
        
    except Exception as e:
        print(f"❌ Failed to initialize browser: {e}")
        raise


def after_scenario(context, scenario):
    """
    Cleanup yang dijalankan setelah setiap scenario
    """
    # Take screenshot jika scenario gagal
    if scenario.status == 'failed':
        timestamp = scenario.name.replace(' ', '_').replace('/', '_')
        screenshot_name = f'screenshots/FAILED_{timestamp}.png'
        
        try:
            context.driver.save_screenshot(screenshot_name)
            print(f'📸 Screenshot saved: {screenshot_name}')
        except Exception as e:
            print(f'⚠️  Could not save screenshot: {e}')
    
    # Close browser
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
            print("✅ Browser closed")
        except Exception as e:
            print(f"Error closing browser: {e}")
    
    # Print scenario status
    if scenario.status == 'passed':
        print(f"Scenario PASSED\n")
    else:
        print(f"Scenario FAILED\n")


def after_feature(context, feature):
    """
    Cleanup setelah feature selesai
    """
    print(f"\n{'='*60}")
    print(f"Feature completed: {feature.name}")
    print(f"{'='*60}\n")


def after_all(context):
    """
    Cleanup yang dijalankan setelah semua test selesai
    """
    print("\n" + "="*60)
    print("All BDD Tests Completed")
    print("="*60 + "\n")