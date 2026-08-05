import pytest
import re
import os
from playwright.sync_api import sync_playwright, expect
from datetime import datetime
from utils import login


@pytest.fixture
def page():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
        )

        context = browser.new_context()

        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
        )

        page = context.new_page()

        yield page

        context.tracing.stop(path="reports/trace.zip")

        context.close()
        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield
    report = outcome.get_result()

    if report.failed:

        page = item.funcargs.get("page")

        if page:
            page.screenshot(path=f"reports/{item.name}.png")


@pytest.fixture
def logged_in_page(page):
    login(page, "standard_user", "secret_sauce")
    expect(page).to_have_url(re.compile(r".*inventory\.html"))

    return page


@pytest.fixture
def backpack_in_cart(logged_in_page):

    logged_in_page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(logged_in_page.locator('[data-test="shopping-cart-badge"]')).to_have_text(
        "1"
    )

    return logged_in_page


@pytest.fixture
def cart_page(backpack_in_cart):

    backpack_in_cart.locator('[data-test="shopping-cart-link"]').click()
    expect(backpack_in_cart).to_have_url(re.compile(r".*cart\.html"))
    expect(backpack_in_cart.get_by_text("Sauce Labs Backpack")).to_be_visible()

    return backpack_in_cart


@pytest.fixture
def checkout_page(cart_page):

    cart_page.locator('[data-test="checkout"]').click()
    expect(cart_page).to_have_url(re.compile(r".*checkout-step-one\.html"))
    expect(cart_page.get_by_text("Checkout: Your Information")).to_be_visible()

    return cart_page


@pytest.fixture
def checkout_overview(checkout_page):

    checkout_page.get_by_placeholder("First Name").fill("John")
    checkout_page.get_by_placeholder("Last Name").fill("Newman")
    checkout_page.get_by_placeholder("Postal Code").fill("3658")
    checkout_page.get_by_role("button", name="Continue").click()
    expect(checkout_page).to_have_url(re.compile(r".*checkout-step-two\.html"))

    return checkout_page


@pytest.fixture
def successful_checkout(checkout_overview):

    checkout_overview.get_by_role("button", name="Finish").click()
    expect(checkout_overview).to_have_url(re.compile(r".*checkout-complete\.html"))

    return checkout_overview


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page:

            screenshots_dir = "Reports/Screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_path = os.path.join(
                screenshots_dir,
                f"{item.name}_{timestamp}.png"
            )

            page.screenshot(path=screenshot_path)
