## Info for info for recruiters
I wrote the tests in Python because I have been testing in Python for the past few years. I also generated the code in JavaScript with the help of ai, but I decided to submit the Python version, as while I understand JavaScript, my coding skills in it without AI support are still at a basic level.
# Install dependencies
## create virtual environment (optional but recommended)
python -m venv .venv
## activate it (Windows)
.venv\Scripts\activate
## activate it (Mac/Linux)
source .venv/bin/activate
## install dependencies
pip install -r requirements.txt

# Run tests
## run all web tests
pytest test_web.py --alluredir=allure-results
pytest test_api.py --alluredir=allure-results

# View test reports
allure serve allure-results