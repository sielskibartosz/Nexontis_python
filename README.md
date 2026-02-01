## Info for Recruiters
I wrote the tests in **Python**, as I have been testing in Python for the past few years.  
I also generated JavaScript code with the help of AI, but I decided to submit the **Python version**, because although I understand JavaScript, my coding skills in it without AI support are still at a basic level.
---
## Project Structure
| File / Folder        | Description                                                  |
|---------------------|--------------------------------------------------------------|
| `test_web.py`        | Automated web UI tests using Selenium and Allure            |
| `test_api.py`        | Automated API tests using `requests` and Allure             |
| `utils.py`           | Helper methods for Selenium tests                            |
| `requirements.txt`   | Python dependencies                                          |
| `allure-results/`    | Folder where Allure test results are stored                 |

## Requirements
- Python 3.10+ (recommended)
- All dependencies listed in `requirements.txt`
---
## Install Dependencies
1. **Create a virtual environment (optional but recommended):**
- python -m venv .venv
2. **Activate the virtual environment**
- Windows cmd:
.venv\Scripts\activate
- Mac/Linux:
source .venv/bin/activate
3. **Install required packages:**
- pip install -r requirements.txt
---
## Run Tests
1. **Run all tests:**
- pytest -v --alluredir=allure-results

2. **Run specific test files:**
- pytest test_web.py --alluredir=allure-results
- pytest test_api.py --alluredir=allure-results
---
## Generate and serve an Allure report:
- allure serve allure-results