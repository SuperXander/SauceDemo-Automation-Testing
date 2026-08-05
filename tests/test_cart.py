import pytest
import re
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.cart
def test_add_to_cart(backpack_in_cart):

    expect(
        backpack_in_cart.locator('[data-test="remove-sauce-labs-backpack"]')
    ).to_be_visible()
    backpack_in_cart.locator('[data-test="shopping-cart-link"]').click()
    expect(backpack_in_cart).to_have_url(re.compile(r".*cart\.html"))
    expect(backpack_in_cart.get_by_text("Sauce Labs Backpack")).to_be_visible()


@pytest.mark.regression
@pytest.mark.cart
def test_remove_from_cart(backpack_in_cart):

    expect(backpack_in_cart).to_have_url(re.compile(r".*inventory\.html"))
    backpack_in_cart.locator('[data-test="remove-sauce-labs-backpack"]').click()
    expect(backpack_in_cart.locator('[data-test="shopping-cart-badge"]')).to_have_count(
        0
    )
    backpack_in_cart.locator('[data-test="shopping-cart-link"]').click()
    expect(backpack_in_cart).to_have_url(re.compile(r".*cart\.html"))
    expect(backpack_in_cart.get_by_text("Sauce Labs Backpack")).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.cart
def test_cart_badge(logged_in_page):

    expect(logged_in_page.locator(".shopping_cart_badge")).not_to_be_visible()

    logged_in_page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")

    logged_in_page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("2")

    logged_in_page.locator("[data-test='remove-sauce-labs-backpack']").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")

    logged_in_page.locator("[data-test='remove-sauce-labs-bike-light']").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).not_to_be_visible()


@pytest.mark.navigation
def test_continue_shopping(logged_in_page):

    logged_in_page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    logged_in_page.locator("[data-test='shopping-cart-link']").click()
    expect(logged_in_page).to_have_url(re.compile(r".*cart\.html"))
    expect(logged_in_page.get_by_text("Sauce Labs Backpack")).to_be_visible()

    logged_in_page.get_by_role("button", name="Continue Shopping").click()
    expect(logged_in_page).to_have_url(re.compile(r".*inventory\.html"))
