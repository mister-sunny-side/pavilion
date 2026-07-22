"""
E2E validation tests for the Pavilion Dioxus blog.

These tests validate that the core app functionality is working:
- Home page loads and displays content
- Navigation between Home and Blog routes works
- App is interactive and hydrated
- Blog route params render correctly

To run these tests:
1. Start the Dioxus server: dx serve --platform web
2. Run tests: uv run pytest tests/test_dioxus_app.py
"""

import re
from urllib.parse import urljoin

from playwright.sync_api import Page, expect


def build_url(base_url: str, path: str = "") -> str:
    """
    Normalize and join the base URL with a relative path.
    Ensures consistent trailing slashes and works when the base URL includes a subpath.
    """
    normalized_base = base_url.rstrip("/") + "/"
    normalized_path = path.lstrip("/")
    return urljoin(normalized_base, normalized_path)


def test_home_page_loads_and_displays_content(page: Page):
    """Test that the home page loads successfully and displays content."""
    page.wait_for_load_state("networkidle")

    body = page.locator("body")
    expect(body).to_be_visible()

    navbar = page.locator("#navbar")
    expect(navbar).to_be_visible()

    hero = page.locator("#hero")
    expect(hero).to_be_visible()

    echo = page.locator("#echo")
    expect(echo).to_be_visible()


def test_home_page_learn_dioxus_link_works(page: Page):
    """Test that the Learn Dioxus hero link is present and navigates correctly."""
    page.wait_for_load_state("networkidle")

    learn_link = page.locator("#hero #links").get_by_role("link", name="Learn Dioxus")
    expect(learn_link).to_be_visible()
    expect(learn_link).to_have_attribute("href", "https://dioxuslabs.com/learn/0.7/")

    learn_link.click()
    page.wait_for_url("https://dioxuslabs.com/learn/0.7/**", timeout=15_000)
    expect(page).to_have_url(re.compile(r"https://dioxuslabs\.com/learn/0\.7/?"))


def test_navbar_navigation_works(page: Page, base_url: str):
    """Test that Home and Blog links in the navbar work correctly."""
    page.wait_for_load_state("networkidle")

    home_link = page.locator("#navbar").get_by_role("link", name="Home")
    blog_link = page.locator("#navbar").get_by_role("link", name="Blog")
    expect(home_link).to_be_visible()
    expect(blog_link).to_be_visible()

    blog_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "blog/1"))

    heading = page.get_by_role("heading", name="This is blog #1!")
    expect(heading).to_be_visible()

    home_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url))
    expect(page.locator("#hero")).to_be_visible()


def test_blog_route_works(page: Page, base_url: str):
    """Test that navigating directly to a blog route works."""
    page.goto(build_url(base_url, "blog/42"))
    page.wait_for_load_state("networkidle")

    expect(page).to_have_url(build_url(base_url, "blog/42"))
    expect(page.locator("#blog")).to_be_visible()
    expect(page.get_by_role("heading", name="This is blog #42!")).to_be_visible()


def test_blog_prev_next_navigation(page: Page, base_url: str):
    """Test that Previous/Next links on the blog page update the route."""
    page.goto(build_url(base_url, "blog/1"))
    page.wait_for_load_state("networkidle")

    page.get_by_role("link", name="Next").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "blog/2"))
    expect(page.get_by_role("heading", name="This is blog #2!")).to_be_visible()

    page.get_by_role("link", name="Previous").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "blog/1"))


def test_app_is_fully_hydrated(page: Page, base_url: str):
    """Test that the Dioxus app has fully hydrated and is interactive."""
    page.wait_for_load_state("networkidle")

    body = page.locator("body")
    expect(body).to_be_visible()

    page.locator("#navbar").get_by_role("link", name="Blog").click()
    page.wait_for_load_state("networkidle")

    expect(page.locator("#navbar")).to_be_visible()
    expect(page).to_have_url(build_url(base_url, "blog/1"))


def test_echo_server_function(page: Page):
    """Test that the fullstack echo server function responds to input."""
    page.wait_for_load_state("networkidle")

    echo_input = page.locator("#echo input")
    expect(echo_input).to_be_visible()

    echo_input.fill("pavilion")
    expect(page.locator("#echo").get_by_text("Server echoed:")).to_be_visible(timeout=10_000)
    expect(page.locator("#echo").get_by_text("pavilion")).to_be_visible()
