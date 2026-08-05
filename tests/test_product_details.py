import pytest
import re
from playwright.sync_api import expect


@pytest.mark.navigation
def test_product_details_navigation(logged_in_page):

    logged_in_page.get_by_text("Sauce Labs Backpack").click()

    expect(logged_in_page).to_have_url(re.compile(r".*inventory-item\.html"))

    logged_in_page.get_by_role("button", name="Back to products").click()

    expect(logged_in_page).to_have_url(re.compile(r".*inventory\.html"))

    logged_in_page.get_by_alt_text("Sauce Labs Backpack").click()

    expect(logged_in_page).to_have_url(re.compile(r".*inventory-item\.html"))

    logged_in_page.get_by_role("button", name="Back to products").click()

    expect(logged_in_page).to_have_url(re.compile(r".*inventory\.html"))


pytest.mark.regression


@pytest.mark.inventory
def test_product_details_information(logged_in_page):

    products = logged_in_page.locator(".inventory_item")

    for i in range(products.count()):

        product = products.nth(i)

    expected_name = product.locator(".inventory_item_name").text_content().strip()
    expected_price = product.locator(".inventory_item_price").text_content()
    expected_description = product.locator(".inventory_item_desc").text_content()

    product.locator(".inventory_item_name").click()

    expect(logged_in_page).to_have_url(re.compile(r".*inventory-item\.html"))

    expect(logged_in_page.locator(".inventory_details_name")).to_have_text(
        expected_name
    )

    expect(logged_in_page.locator(".inventory_details_price")).to_have_text(
        expected_price
    )

    expect(logged_in_page.locator(".inventory_details_desc")).to_have_text(
        expected_description
    )

    expect(logged_in_page.locator(".inventory_details_img")).to_be_visible()

    expect(logged_in_page.locator(".inventory_details_img")).to_have_attribute(
        "alt",
        expected_name,
    )

    logged_in_page.get_by_role("button", name="Back to products").click()

    expect(logged_in_page).to_have_url(re.compile(r".*inventory\.html"))
