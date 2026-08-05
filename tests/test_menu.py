import pytest
import re
from playwright.sync_api import expect
from utils import login


@pytest.mark.regression
@pytest.mark.menu
def test_menu(logged_in_page):

    expect(logged_in_page.get_by_role("button", name="Open Menu")).to_be_visible()
    logged_in_page.get_by_role("button", name="Open Menu").click()

    expect(logged_in_page.get_by_role("link", name="All Items")).to_be_visible()
    expect(logged_in_page.get_by_role("link", name="About")).to_be_visible()
    expect(logged_in_page.get_by_role("link", name="Logout")).to_be_visible()
    expect(logged_in_page.get_by_role("link", name="Reset App State")).to_be_visible()


@pytest.mark.regression
@pytest.mark.menu
def test_about(logged_in_page):

    logged_in_page.get_by_role("button", name="Open Menu").click()

    about = logged_in_page.get_by_role("link", name="About")

    expect(about).to_be_visible()
    expect(about).to_have_attribute("href", "https://saucelabs.com/")

    about.click()

    expect(logged_in_page).to_have_url(re.compile(r".*saucelabs\.com.*"))


@pytest.mark.navigation
def test_all_items(logged_in_page):

    logged_in_page.get_by_text("Sauce Labs Backpack").click()
    expect(logged_in_page).to_have_url(re.compile(r".*inventory-item\.html"))
    logged_in_page.get_by_role("button", name="Open Menu").click()
    logged_in_page.get_by_role("link", name="All Items").click()
    expect(logged_in_page).to_have_url(re.compile(r".*inventory\.html"))


@pytest.mark.regression
@pytest.mark.menu
def test_reset_app_state(logged_in_page):

    logged_in_page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")
    logged_in_page.get_by_role("button", name="Open Menu").click()
    logged_in_page.get_by_role("link", name="Reset App State").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).not_to_be_visible()
