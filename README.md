# SauceDemo Automation Testing

This project was created to learn and practice web automation testing using Playwright and Pytest.

It demonstrates an end-to-end automation framework built with Python, Pytest, and Playwright, featuring reusable fixtures, 
utilities, assertions, HTML reporting, tracing, screenshots, parallel execution, and automated testing against the SauceDemo application.

## Testing Scope

This project demonstrates the following testing types:

| Testing Type | Coverage |
|-------------|----------|
| Functional Testing | Login, Logout, Inventory, Cart, Checkout |
| UI Testing | Product information, Product details, Navigation, Burger Menu |
| End-to-End (E2E) Testing | Complete user journey from Login → Checkout → Order Confirmation |
| Smoke Testing | Critical user flows using Pytest markers |
| Regression Testing | Full automation suite executed with all tests |

## Technologies

- Python 3.14
- Playwright
- Pytest
- Pytest HTML
- Pytest-xdist
- Black Formatter
- Git

## Project Structure

Automation-Testing/
│
├── tests/
├── reports/
├── downloads/
├── conftest.py
├── utils.py
├── pytest.ini
├── requirements.txt
└── README.md

## Features Tested
- Login Automation
- Cart Automation
- Checkout Automation
- Inventory Validation
- Product Details Validation
- Burger Menu Validation

### Authentication
- Login
- Invalid Login
- Logout

### Inventory
- Product information
- Product details
- Sorting
- Cart badge

### Cart
- Add to cart
- Remove from cart

### Checkout
- Successful checkout
- Invalid checkout
- Checkout navigation
- PDF order download

### Menu & Navigation
- Burger menu
- About
- All Items
- Reset App State

### External Links
- Twitter
- Facebook
- LinkedIn

## Installation

``terminal
git clone ...
cd Automation-Testing
pip install -r requirements.txt
playwright install

## CI/CD

This project uses GitHub Actions to automatically execute the test suite whenever code is pushed to the repository.

## Reports
After execution, HTML reports and Playwright traces are generated for debugging.

Generate an HTML report

```terminal
python -m pytest --html=reports/report.html --self-contained-html
```

View Playwright Trace

```terminal
playwright show-trace reports/trace.zip
```

Run all tests

```terminal
python -m pytest
```

Run smoke tests

```terminal
python -m pytest -m smoke
```

Run checkout tests

```terminal
python -m pytest -m checkout
```

Run tests in parallel

```terminal
python -m pytest -n auto
```

## Future Improvements

- Implement the Page Object Model (POM)
- Integrate GitHub Actions for CI/CD
- Expand test coverage
- Add API testing
- Add cross-browser execution
