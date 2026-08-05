import re
from playwright.sync_api import Page, expect, sync_playwright 

def login(page: Page, username, password):

        page.goto("https://saucedemo.com")
        expect(page).to_have_title("Swag Labs")
        page.get_by_placeholder("Username").fill(username)
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Login").click()