import pytest
import re
from playwright.sync_api import expect
from utils import login


@pytest.mark.regression
@pytest.mark.inventory
class TestInventory:

    def test_inventory_information(self, logged_in_page):

        products = logged_in_page.locator(".inventory_item")

        assert products.count() == 6

        for i in range(products.count()):
            product = products.nth(i)

            expect(product.locator(".inventory_item_name")).to_be_visible()
            expect(product.locator(".inventory_item_desc")).to_be_visible()
            expect(product.locator(".inventory_item_price")).to_be_visible()
            expect(product.locator("img")).to_be_visible()
            expect(product.get_by_role("button")).to_be_visible()

    def test_inventory_sorting(self, logged_in_page):

        expect(logged_in_page.get_by_text("Products")).to_be_visible()

        # Low to High
        logged_in_page.get_by_role("combobox").select_option("lohi")
        prices = logged_in_page.locator(".inventory_item_price").all_text_contents()
        prices = [float(price.strip("$")) for price in prices]
        assert prices == sorted(prices)

        # High to Low
        logged_in_page.get_by_role("combobox").select_option("hilo")
        prices = logged_in_page.locator(".inventory_item_price").all_text_contents()
        prices = [float(price.strip("$")) for price in prices]
        assert prices == sorted(prices, reverse=True)

        # Sort A to Z
        logged_in_page.get_by_role("combobox").select_option("az")
        names = logged_in_page.locator(".inventory_item_name").all_text_contents()
        names = [name.strip() for name in names]
        assert names == sorted(names)

        # Sort Z to A
        logged_in_page.get_by_role("combobox").select_option("za")
        names = logged_in_page.locator(".inventory_item_name").all_text_contents()
        names = [name.strip() for name in names]
        assert names == sorted(names, reverse=True)
