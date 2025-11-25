"""
BDD Testing Runner for Windows
Usage: python run_tests.py [option]
"""

import sys
import subprocess
import requests
from pathlib import Path

# Colors for Windows terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_colored(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.END}")

def check_backend():
    """Check if backend is running"""
    print_colored("[1/3] Checking backend...", Colors.YELLOW)
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print_colored("✓ Backend is running", Colors.GREEN)
            return True
        else:
            print_colored(f"✗ Backend returned status {response.status_code}", Colors.RED)
            return False
    except Exception as e:
        print_colored("✗ Backend is NOT running", Colors.RED)
        print("\nPlease start backend first:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        return False

def check_frontend():
    """Check if frontend is running"""
    print_colored("[2/3] Checking frontend...", Colors.YELLOW)
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print_colored("✓ Frontend is running", Colors.GREEN)
        return True
    except Exception as e:
        print_colored("✗ Frontend is NOT running", Colors.RED)
        print("\nPlease start frontend first:")
        print("  cd frontend/nextjs-app")
        print("  npm run dev")
        return False

def create_screenshots_dir():
    """Create screenshots directory if not exists"""
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)

def run_behave(args):
    """Run behave with specified arguments"""
    # Use python -m behave for Windows compatibility
    cmd = [sys.executable, "-m", "behave"] + args
    print_colored(f"\nRunning: {' '.join(cmd)}", Colors.BLUE)
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as e:
        print_colored(f"Error running behave: {e}", Colors.RED)
        return 1

def main():
    print()
    print_colored("╔════════════════════════════════════════════╗", Colors.BLUE)
    print_colored("║  FakeNews Detection - BDD Testing Suite  ║", Colors.BLUE)
    print_colored("╚════════════════════════════════════════════╝", Colors.BLUE)
    print()

    # Check prerequisites
    if not check_backend():
        sys.exit(1)
    
    if not check_frontend():
        sys.exit(1)

    # Create screenshots directory
    create_screenshots_dir()

    # Parse command line arguments
    print_colored("[3/3] Running tests...", Colors.YELLOW)
    print()

    if len(sys.argv) < 2:
        option = "all"
    else:
        option = sys.argv[1].lower()

    # Run tests based on option
    behave_args = []
    
    if option == "smoke":
        print_colored("Running smoke tests...", Colors.BLUE)
        behave_args = ["--tags=@smoke", "--format=progress"]
    
    elif option == "critical":
        print_colored("Running critical tests...", Colors.BLUE)
        behave_args = ["--tags=@critical", "--format=progress"]
    
    elif option == "happy":
        print_colored("Running happy path tests...", Colors.BLUE)
        behave_args = ["--tags=@happy-path", "--format=progress"]
    
    elif option == "edge":
        print_colored("Running edge case tests...", Colors.BLUE)
        behave_args = ["--tags=@edge-case", "--format=progress"]
    
    elif option == "ui":
        print_colored("Running UI tests...", Colors.BLUE)
        behave_args = ["--tags=@ui", "--format=progress"]
    
    elif option == "integration":
        print_colored("Running integration tests...", Colors.BLUE)
        behave_args = ["--tags=@integration", "--format=progress"]
    
    elif option == "security":
        print_colored("Running security tests...", Colors.BLUE)
        behave_args = ["--tags=@security", "--format=progress"]
    
    elif option == "verbose":
        print_colored("Running all tests (verbose)...", Colors.BLUE)
        behave_args = ["--verbose", "--no-capture", "--no-capture-stderr"]
    
    elif option == "dry":
        print_colored("Dry run (showing scenarios without executing)...", Colors.BLUE)
        behave_args = ["--dry-run", "--no-summary", "--format=plain"]
    
    elif option == "list":
        print_colored("Listing all scenarios...", Colors.BLUE)
        behave_args = ["--dry-run", "--no-summary", "--format=steps"]
    
    elif option == "feature":
        if len(sys.argv) < 3:
            print_colored("Error: Please specify feature name", Colors.RED)
            print("Usage: python run_tests.py feature <feature_name>")
            sys.exit(1)
        feature_name = sys.argv[2]
        print_colored(f"Running feature: {feature_name}", Colors.BLUE)
        behave_args = [f"features/{feature_name}.feature"]
    
    elif option == "scenario":
        if len(sys.argv) < 3:
            print_colored("Error: Please specify scenario name", Colors.RED)
            print("Usage: python run_tests.py scenario '<scenario_name>'")
            sys.exit(1)
        scenario_name = sys.argv[2]
        print_colored(f"Running scenario: {scenario_name}", Colors.BLUE)
        behave_args = ["--name", scenario_name]
    
    elif option == "report":
        print_colored("Running tests and generating report...", Colors.BLUE)
        behave_args = ["--junit", "--junit-directory", "reports/"]
    
    elif option in ["help", "-h", "--help"]:
        print_help()
        sys.exit(0)
    
    else:
        print_colored("Running all tests...", Colors.BLUE)
        behave_args = []

    # Execute behave
    exit_code = run_behave(behave_args)

    # Print results
    print()
    print("=" * 60)
    if exit_code == 0:
        print_colored("✓ All tests passed!", Colors.GREEN)
    else:
        print_colored("✗ Some tests failed", Colors.RED)
        print("\nCheck screenshots/ directory for failure screenshots")
    print("=" * 60)
    print()

    sys.exit(exit_code)

def print_help():
    """Print help message"""
    print("Usage: python run_tests.py [option]")
    print()
    print("Options:")
    print("  smoke       Run smoke tests only (@smoke)")
    print("  critical    Run critical tests (@critical)")
    print("  happy       Run happy path tests (@happy-path)")
    print("  edge        Run edge case tests (@edge-case)")
    print("  ui          Run UI tests (@ui)")
    print("  integration Run integration tests (@integration)")
    print("  security    Run security tests (@security)")
    print("  verbose     Run all tests with verbose output")
    print("  dry         Dry run (show scenarios without executing)")
    print("  list        List all scenarios")
    print("  feature     Run specific feature file")
    print("  scenario    Run specific scenario by name")
    print("  report      Generate test reports (JUnit)")
    print("  help        Show this help message")
    print()
    print("Examples:")
    print("  python run_tests.py smoke")
    print("  python run_tests.py feature share_detection")
    print("  python run_tests.py scenario 'User berhasil membuat share link'")

if __name__ == "__main__":
    main()