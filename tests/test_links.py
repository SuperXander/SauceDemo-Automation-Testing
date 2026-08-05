import pytest
import re
from playwright.sync_api import expect


@pytest.mark.regression
@pytest.mark.links
class TestSocialLinks:

    def test_twitter_link(self, logged_in_page):

        twitter = logged_in_page.get_by_role("link", name="Twitter")
        expect(twitter).to_be_visible()
        expect(twitter).to_have_attribute("href", "https://twitter.com/saucelabs")

        with logged_in_page.context.expect_page() as new_page_info:
            twitter.click()

        twitter_page = new_page_info.value
        twitter_page.wait_for_load_state()

        expect(twitter_page).to_have_url(re.compile(r".*x\.com.*"))

        twitter_page.close()

    def test_facebook_link(self, logged_in_page):

        facebook = logged_in_page.get_by_role("link", name="Facebook")
        expect(facebook).to_be_visible()
        expect(facebook).to_have_attribute("href", "https://www.facebook.com/saucelabs")

        with logged_in_page.context.expect_page() as new_page_info:
            facebook.click()

        facebook_page = new_page_info.value
        facebook_page.wait_for_load_state()

        expect(facebook_page).to_have_url(re.compile(r".*facebook\.com.*"))

        facebook_page.close()

    def test_linkedin_link(self, logged_in_page):

        linkedin = logged_in_page.get_by_role("link", name="LinkedIn")
        expect(linkedin).to_be_visible()
        expect(linkedin).to_have_attribute(
            "href", "https://www.linkedin.com/company/sauce-labs/"
        )

        with logged_in_page.context.expect_page() as new_page_info:
            linkedin.click()

        linkedin_page = new_page_info.value
        linkedin_page.wait_for_load_state()

        expect(linkedin_page).to_have_url(re.compile(r".*linkedin\.com.*"))

        linkedin_page.close()
