# BDD Testing Guide - Fake News Detection

Panduan lengkap untuk menjalankan BDD (Behavior-Driven Development) testing menggunakan Behave dan Selenium.

## 📋 Prerequisites

1. **Backend Server** harus berjalan di `http://localhost:8000`
2. **Frontend Server** harus berjalan di `http://localhost:3000`
3. **Microsoft Edge Browser** terinstall (atau Chrome dengan konfigurasi tambahan)
4. **Edge WebDriver** (msedgedriver.exe) sudah didownload

## 🚀 Quick Start

### 1. Aktifkan Virtual Environment

```powershell
cd tests\bdd
.testenv\Scripts\Activate.ps1
```

Anda akan melihat `(.testenv)` di prompt terminal.

### 2. Set Edge Driver Path (Optional)

Jika Edge driver tidak ada di PATH system, set manual:

```powershell
$env:EDGE_DRIVER_PATH = "C:\Users\epeto\Downloads\edgedriver_win32 (1)\msedgedriver.exe"
```

Ganti dengan path driver Anda yang sebenarnya.

### 3. Jalankan Test

**Jalankan semua test:**
```powershell
behave features\check_news.feature
```

**Jalankan dengan verbose output:**
```powershell
behave features\check_news.feature --no-capture
```

**Jalankan scenario tertentu:**
```powershell
behave features\check_news.feature -n "User checks a valid news via text"
```

**Jalankan dengan browser visible (non-headless):**
```powershell
$env:HEADFUL = "1"
behave features\check_news.feature
```

## 📊 Expected Output

### Successful Test Run:
```
Feature: Check news validity

  Scenario: User checks a valid news via text
    Given I am on "check-news page"              ... passed
    When I fill in "news_text" with "..."        ... passed
    And I press "Check"                          ... passed
    Then I should see "Valid/Hoax"               ... passed

  Scenario: User checks a valid news via document
    Given I am on "check-news page"              ... passed
    When I attach the file "..." to "news_file"  ... passed
    And I press "Check"                          ... passed
    Then I should see "Valid/Hoax"               ... passed

2 scenarios (2 passed)
8 steps (8 passed)
0m15.234s
```

## 🔧 Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `BASE_URL` | http://localhost:3000 | Frontend URL |
| `BROWSER` | edge | Browser to use (edge/chrome) |
| `HEADFUL` | 0 | Show browser? 1=yes, 0=headless |
| `EDGE_DRIVER_PATH` | auto-detect | Path to msedgedriver.exe |
| `EDGE_BIN` | auto-detect | Path to msedge.exe |

**Example:**
```powershell
$env:BASE_URL = "http://localhost:3000"
$env:HEADFUL = "1"
$env:EDGE_DRIVER_PATH = "C:\WebDrivers\msedgedriver.exe"
behave features\check_news.feature
```

## 📁 BDD Project Structure

```
tests/bdd/
├── features/
│   └── check_news.feature      # Gherkin scenarios
├── steps/
│   └── check_news_steps.py     # Step definitions
├── environment.py              # Behave hooks & setup
├── .testenv/                   # Virtual environment
└── requirements-test.txt       # Dependencies
```

## 📝 Test Scenarios

### Scenario 1: Text Input
- User masuk ke home page
- User input teks berita
- User klik tombol "Analisis Berita"
- System menampilkan hasil (Valid/Hoax)

### Scenario 2: Document Upload
- User masuk ke home page
- User switch ke tab "File"
- User upload dokumen DOCX
- User klik tombol "Analisis Berita"
- System menampilkan hasil (Valid/Hoax)

## 🐛 Troubleshooting

### Issue: "Edge binary not found"
**Solution:**
```powershell
# Set path manual
$env:EDGE_BIN = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

### Issue: "WebDriver not found"
**Solution:**
1. Download Edge WebDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
2. Extract msedgedriver.exe
3. Set path:
```powershell
$env:EDGE_DRIVER_PATH = "C:\path\to\msedgedriver.exe"
```

### Issue: "Connection refused" ke localhost:3000
**Solution:**
```powershell
# Start frontend di terminal terpisah
cd Frontend\nextjs-app
npm run dev
```

### Issue: "Cannot connect to localhost:8000"
**Solution:**
```powershell
# Start backend di terminal terpisah
cd Backend\fastapi-app
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### Issue: Test timeout atau lambat
**Solution:**
- Pastikan backend dan frontend sudah ready sebelum run test
- Tingkatkan timeout di step definitions jika perlu
- Check network/firewall tidak blocking localhost

### Issue: Element not found
**Solution:**
- Pastikan frontend memiliki attribute `data-testid`
- Check di browser bahwa element ada dengan DevTools
- Tunggu element muncul dengan WebDriverWait

## 🎯 Writing New Tests

### 1. Tambahkan Scenario di Feature File

```gherkin
Scenario: User checks news from URL
  Given I am on "check-news page"
  When I fill in "news_url" with "https://example.com/news"
  And I press "Check"
  Then I should see "Valid/Hoax"
```

### 2. Implementasi Step Definitions

```python
@when('I fill in "{field_id}" with "{value}"')
def step_fill_field(context, field_id, value):
    element = context.driver.find_element(By.CSS_SELECTOR, f'[data-testid="{field_id}"]')
    element.send_keys(value)
```

## 📚 Behave Commands Reference

```powershell
# Run all features
behave

# Run specific feature
behave features\check_news.feature

# Run with tags
behave --tags=@smoke

# Run specific scenario by name
behave -n "scenario name"

# Dry run (syntax check)
behave --dry-run

# Show step definitions
behave --steps-catalog

# Generate report
behave --junit --junit-directory reports/
```

## 🔍 Debugging Tips

### 1. Lihat Browser Execution
```powershell
$env:HEADFUL = "1"
behave features\check_news.feature
```

### 2. Print Debug Info
Edit `check_news_steps.py` tambahkan:
```python
print(f"Current URL: {context.driver.current_url}")
print(f"Page title: {context.driver.title}")
```

### 3. Pause Execution
Tambahkan di step definitions:
```python
import time
time.sleep(5)  # Pause 5 detik
```

### 4. Screenshot on Failure
Edit `environment.py`:
```python
def after_step(context, step):
    if step.status == "failed":
        context.driver.save_screenshot(f"failure_{step.name}.png")
```

## 🌐 CI/CD Integration

### GitHub Actions Example:
```yaml
name: BDD Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd tests/bdd
          python -m venv .testenv
          .testenv\Scripts\Activate.ps1
          pip install -r ../requirements-test.txt
      - name: Start Backend
        run: |
          cd Backend/fastapi-app
          uvicorn app.main:app &
      - name: Start Frontend
        run: |
          cd Frontend/nextjs-app
          npm install
          npm run dev &
      - name: Run BDD Tests
        run: |
          cd tests/bdd
          behave features\check_news.feature
```

## 📖 Additional Resources

- **Behave Documentation:** https://behave.readthedocs.io/
- **Selenium Python:** https://selenium-python.readthedocs.io/
- **Gherkin Syntax:** https://cucumber.io/docs/gherkin/reference/
- **Edge WebDriver:** https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

## 🎓 Best Practices

1. **Keep scenarios focused** - One scenario = One behavior
2. **Use meaningful names** - Describe what, not how
3. **Keep steps reusable** - Write generic step definitions
4. **Clean up after tests** - Close browsers, delete temp files
5. **Run tests regularly** - Integrate with CI/CD
6. **Update tests with features** - Keep tests synchronized with app changes
