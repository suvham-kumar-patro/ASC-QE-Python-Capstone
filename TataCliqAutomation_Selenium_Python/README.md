# Converted Selenium project (Java -> Python pytest)

This project was auto-converted from a Java Selenium TestNG project to a Python + pytest project.
Location: `/mnt/data/TataCliqAutomation_converted_python`

## Requirements
Install dependencies (preferably in a virtualenv):
```
pip install -r requirements.txt
```

## Run tests
From project root (in PyCharm open this folder as project) you can run:
```
pytest -q --html=report.html
```

Notes:
- The converted tests use `webdriver-manager` to auto-download ChromeDriver.
- Some XPath/CSS selectors were ported as best-effort. You may need to update locators in `tests/test_tatacliq.py` to match the current website structure.
- OTP flows often require manual input; tests will skip with message if OTP/manual interaction is necessary.
