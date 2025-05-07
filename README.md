# OrangeHRM Automation

This project is a test automation framework for the OrangeHRM application using Selenium and Pytest.

## Prerequisites

Before running the tests, ensure you have the following installed:

1. Python 3.7 or higher
2. Google Chrome browser
3. ChromeDriver (automatically managed by `chromedriver-autoinstaller`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kaushan23/Orange-HRM-Test-Automation.git
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Running the Tests

1. To run all tests:
   ```bash
    pytest TestCases/test_orange_hrm.py
   ```

2. To generate an HTML report after all tests are completed and save it in the `Reports` folder with a timestamp:
   ```bash
   # Step 1: Generate the timestamp
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

   # Step 2: Run the test with the generated report name
        pytest TestCases/test_orange_hrm.py --html="Reports/report_$timestamp.html"
   ```

3. To suppress warnings while generating the report:
   ```bash
   # Step 1: Generate the timestamp
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

   # Step 2: Run the test with the generated report name
        pytest TestCases/test_orange_hrm.py --html="Reports/report_$timestamp.html" --disable-warnings
   ```
## Screenshots

- Screenshots are saved in the `Screenshots` directory under a subfolder for each test run.

## Project Structure

```
test-automation/
├── PageObjects/           # Contains page object models for different pages
├── Reports/               # Stores test execution reports
├── Screenshots/           # Stores screenshots taken during test execution
├── TestCases/             # Contains test case scripts
├── conftest.py            # Pytest configuration and fixtures
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
```

## Notes

- Ensure the Chrome browser version matches the ChromeDriver version managed by `chromedriver-autoinstaller`.
- Use the `--disable-warnings` flag with pytest to suppress warnings:
  ```bash
  pytest --disable-warnings
  ```

## License

This project is licensed under the MIT License.
