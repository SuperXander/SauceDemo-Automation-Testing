import re
import pytest
from playwright.sync_api import expect
from utils import login


@pytest.mark.smoke
@pytest.mark.authentication
class TestAuthentication:

    def test_login(self, logged_in_page):

        expect(logged_in_page).to_have_url(re.compile(r".*inventory\.html"))
        expect(logged_in_page.get_by_text("Products")).to_be_visible()

        expect(
            logged_in_page.locator('[data-test="shopping-cart-link"]')
        ).to_be_visible()

    def test_logout(self, logged_in_page):

        logged_in_page.get_by_role("button", name="Open Menu").click()
        logged_in_page.locator('[data-test="logout-sidebar-link"]').click()
        expect(logged_in_page).to_have_url(re.compile(r".*saucedemo\.com/?$"))
        expect(logged_in_page.locator('[data-test="login-button"]')).to_be_visible()


@pytest.mark.authentication
class TestInvalidLoginTests:

    def test_invalid_password(self, page):

        login(page, "standard_user", "invalid_password")

        expect(page.locator('[data-test="error"]')).to_be_visible()
        expect(page.locator('[data-test="error"]')).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )

    def test_invalid_username(self, page):

        login(page, "invalid_username", "secret_sauce")

        expect(page.locator('[data-test="error"]')).to_be_visible()
        expect(page.locator('[data-test="error"]')).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )

    def test_invalid_username_and_password(self, page):

        login(page, "invalid_username", "invalid_password")

        expect(page.locator('[data-test="error"]')).to_be_visible()
        expect(page.locator('[data-test="error"]')).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )
