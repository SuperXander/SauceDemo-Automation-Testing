import pytest
import re
from playwright.sync_api import expect
from utils import login
from pathlib import Path


@pytest.mark.smoke
@pytest.mark.checkout
class TestSuccessfulCheckout:

    def test_checkout(self, checkout_page):

        checkout_page.get_by_placeholder("First Name").fill("John")
        checkout_page.get_by_placeholder("Last Name").fill("Newman")
        checkout_page.get_by_placeholder("Postal Code").fill("3658")
        checkout_page.get_by_role("button", name="Continue").click()

        # Checkout Overview Page
        expect(checkout_page).to_have_url(re.compile(r".*checkout-step-two\.html"))
        expect(checkout_page.get_by_text("Checkout: Overview")).to_be_visible()
        expect(checkout_page.get_by_text("Sauce Labs Backpack")).to_be_visible()
        checkout_page.get_by_role("button", name="Finish").click()

        # Checkout Complete Page
        expect(checkout_page).to_have_url(re.compile(r".*checkout-complete\.html"))
        expect(checkout_page.get_by_text("Checkout: Complete!")).to_be_visible()
        expect(checkout_page.get_by_text("Thank you for your order!")).to_be_visible()

    def test_download(self, successful_checkout):

        with successful_checkout.expect_download() as download_info:
            successful_checkout.locator('[data-test="generate-pdf-order"]').click()

        download = download_info.value

        download_path = Path("downloads")
        download_path.mkdir(exist_ok=True)

        file_path = download_path / download.suggested_filename

        download.save_as(file_path)

        assert file_path.exists()


@pytest.mark.regression
@pytest.mark.checkout
@pytest.mark.navigation
class TestCheckoutCancel:

    def test_cancel_checkout_information(self, checkout_page):

        checkout_page.get_by_role("button", name="Cancel").click()
        expect(checkout_page).to_have_url(re.compile(r".*cart\.html"))
        checkout_page.get_by_role("button", name="Continue Shopping").click()
        expect(checkout_page).to_have_url(re.compile(r".*inventory\.html"))

    def test_cancel_checkout_overview(self, checkout_overview):

        checkout_overview.get_by_role("button", name="Cancel").click()
        expect(checkout_overview).to_have_url(re.compile(r".*inventory\.html"))


@pytest.mark.regression
@pytest.mark.checkout
class TestInvalidCheckout:

    def test_empty_firstname(self, checkout_page):

        checkout_page.get_by_placeholder("Last Name").fill("Newman")
        checkout_page.get_by_placeholder("Postal Code").fill("3658")
        checkout_page.get_by_role("button", name="Continue").click()
        expect(checkout_page.locator('[data-test="error"]')).to_have_text(
            "Error: First Name is required"
        )

    def test_empty_lastname(self, checkout_page):

        checkout_page.get_by_placeholder("First Name").fill("John")
        checkout_page.get_by_placeholder("Postal Code").fill("3658")
        checkout_page.get_by_role("button", name="Continue").click()
        expect(checkout_page.locator('[data-test="error"]')).to_have_text(
            "Error: Last Name is required"
        )

    def test_empty_postal_code(self, checkout_page):

        checkout_page.get_by_placeholder("First Name").fill("John")
        checkout_page.get_by_placeholder("Last Name").fill("Newman")
        checkout_page.get_by_role("button", name="Continue").click()
        expect(checkout_page.locator('[data-test="error"]')).to_have_text(
            "Error: Postal Code is required"
        )
