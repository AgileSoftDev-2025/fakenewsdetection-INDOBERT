# BDD Quick Reference Card

## ⚡ Quick Commands

### Setup (One Time)
```powershell
cd tests\bdd
python -m venv .testenv
.testenv\Scripts\Activate.ps1
pip install behave selenium webdriver-manager python-docx
```

### Run Tests
```powershell
# Activate environment
.testenv\Scripts\Activate.ps1

# Set driver (optional)
$env:EDGE_DRIVER_PATH = "C:\path\to\msedgedriver.exe"

# Run tests
behave features\check_news.feature
```

## 🎯 Common Commands

| Command | Purpose |
|---------|---------|
| `behave` | Run all tests |
| `behave features\check_news.feature` | Run specific feature |
| `behave --no-capture` | Show print output |
| `behave -n "scenario name"` | Run specific scenario |
| `$env:HEADFUL="1"; behave` | Show browser window |
| `behave --dry-run` | Syntax check only |
| `behave --tags=@smoke` | Run tagged tests |

## 🔧 Environment Variables

```powershell
$env:BASE_URL = "http://localhost:3000"
$env:BROWSER = "edge"                    # or "chrome"
$env:HEADFUL = "1"                       # Show browser
$env:EDGE_DRIVER_PATH = "C:\path\..."
```

## ✅ Pre-Test Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Virtual environment activated (.testenv)
- [ ] Edge driver path set (if needed)

## 📝 Quick Test

```powershell
# Test 1: Check servers
curl http://localhost:8000/health
curl http://localhost:3000

# Test 2: Run BDD
behave features\check_news.feature --no-capture
```

## 🐛 Quick Fixes

**Backend not running:**
```powershell
cd Backend\fastapi-app
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Frontend not running:**
```powershell
cd Frontend\nextjs-app
npm run dev
```

**Driver error:**
```powershell
$env:EDGE_DRIVER_PATH = "C:\Users\epeto\Downloads\edgedriver_win32 (1)\msedgedriver.exe"
```

## 📊 Expected Output

```
Feature: Check news validity

  Scenario: User checks a valid news via text          ... passed
  Scenario: User checks a valid news via document      ... passed

2 scenarios (2 passed)
8 steps (8 passed)
0m15.234s
```

## 🎓 Tips

- Use `--no-capture` to see debug output
- Use `HEADFUL=1` to debug visually
- Start backend & frontend BEFORE running tests
- Check BDD_TESTING_GUIDE.md for detailed help
