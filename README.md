# TACQ Project Lab

The objective of this project is to automate the testing of the website [Ecomus](https://automation-portal-bootcamp.vercel.app) in order to identify bugs and other potential issues.

The testing process involves evaluating the behaviour of different sections of the website:

* Home Page – The website's entry point, which provides access to the various other sections.

* Registration Page – Handles user registration, an account is required to make a purchase.

* Login Page – Handles user login using their account credentials.

* Product Page – Handles product display and selection, including all the different product variations (size, color, etc).

* Checkout Page – Handles the purchase process and order placement.

Each page has its own user flow and the combination of them represent the general user experience. For example, a customer navigating the site, registering, logging in, browsing products, adding items to the cart, and completing a purchase.

## Project Structure

The project's folder structure is as follows:

```
├── config
│   └── config.py
├── pages
│   ├── (page POMs)
│   └── components
│       └── (component POMs)
├── pytest.ini
├── requirements.txt
├── planning
│   └── (Test explanation for the POMs)
├── tests
│   ├── conftest.py
│   └── (test files)
    └── test_data
        └── (Files with JSON, CSV and data)
```

* `pages`: Contains the Page Object Models (POMs) for the website's pages and components. These POMs encapsulate page-specific interactions, making our tests modular and maintainable.

* `tests`: Contains the project's test files, where we define automated test cases for each page.

* `utils`: Contains shared utilities, such as `api_helper.py`, which manages test data via API calls to ensure consistency across all tests.

* `config`: Stores configuration variables in the `config.py` file, including the website's base URL (`https://automation-portal-bootcamp.vercel.app`) and test user credentials (`{"email": "team2@taqc.com", "password": "team2"}`).

## Technologies

Our testing framework is built on [Playwright](https://playwright.dev/python/), [pytest](https://docs.pytest.org/en/stable/), and [Python](https://www.python.org), with [Page Object Models (POMs)](https://playwright.dev/python/docs/pom) as a core organizational principle:

* [Python](https://www.python.org): A high-level, interpreted programming language known for its simplicity and readability.

* [Playwright](https://playwright.dev/python/): A powerful tool for browser automation, allowing us to simulate user interactions like clicking buttons, filling forms, and navigating pages across all flows.

* [POMs](https://playwright.dev/python/docs/pom): Each page in our e-commerce site has a corresponding POM class, encapsulating its elements and actions. This makes our test scripts cleaner and easier to maintain, as we reuse page interactions across multiple tests.

* [pytest](https://docs.pytest.org/en/stable/): Our test runner, which organizes and executes our test cases, supporting features like parameterization to test multiple scenarios efficiently.

![Static Badge](https://img.shields.io/badge/3.13.2-yellow?style=for-the-badge&logo=python&label=Python) ![Playwright](https://img.shields.io/badge/1.51.0-%232EAD33?style=for-the-badge&logo=playwright&label=Playwright&logoColor=white&color=orange) ![Static Badge](https://img.shields.io/badge/8.3.5-blue?style=for-the-badge&logo=pytest&label=Pytest)

## Installation

1. Create a virtual enviroment

```bash
python -m venv .venv
```

2. Install the project's dependencies with [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

## Usage

1. Enable the virtual environment

```bash
source .venv/bin/activate
```

2. Run the tests with [pytest](https://docs.pytest.org/en/stable/)

To run tests, invoke pytest from the project's root. Here are some example commands:

```bash
# run all tests
pytest
# run a specific test file
pytest ./tests/test_name.py
# run a specific test function
pytest ./tests/test_name.py::test_function
```

This project runs all tests in headless mode by default. It is possible to run the tests in headed mode by passing the option `--no-headless` to pytest:

```bash
# run in headed mode
pytest --no-headless
```

Generate a test report in XML by passing the option `--junit-xml=example_report.xml`

```bash
# generate XML test report
pytest --junit-xml=example_report.xml
```

For more options, check [pytest's usage documentation](https://docs.pytest.org/en/stable/how-to/usage.html) (or invoke pytest with the `--help` option)