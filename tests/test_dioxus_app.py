"""
E2E validation tests for the Pavilion Dioxus blog.

These tests validate that the core app functionality is working:
- Home page loads and displays content
- Navigation between Home, Dialogue, Matter, and Random works
- App is interactive and hydrated
- Dialogue lists build-time markdown posts and opens them

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
    """Test that navbar links navigate to Dialogue, Matter, Random, and Home."""
    page.wait_for_load_state("networkidle")

    navbar = page.locator("#navbar")
    home_link = navbar.get_by_role("link", name="Home")
    dialogue_link = navbar.get_by_role("link", name="Dialogue")
    matter_link = navbar.get_by_role("link", name="Matter")
    random_link = navbar.get_by_role("link", name="Random")

    expect(home_link).to_be_visible()
    expect(dialogue_link).to_be_visible()
    expect(matter_link).to_be_visible()
    expect(random_link).to_be_visible()

    dialogue_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r".*/dialogue/?$"))
    expect(page.locator("#dialogue")).to_be_visible()

    matter_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "matter"))
    expect(page.locator("#matter")).to_be_visible()

    random_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "random"))
    expect(page.locator("#random")).to_be_visible()

    home_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url))
    expect(page.locator("#hero")).to_be_visible()


def test_dialogue_lists_and_opens_posts(page: Page, base_url: str):
    """Test that Dialogue lists markdown posts and opens the welcome post."""
    page.goto(build_url(base_url, "dialogue"))
    page.wait_for_load_state("networkidle")

    expect(page.locator("#dialogue")).to_be_visible()
    welcome_link = page.locator("#dialogue").get_by_role("link", name="Welcome")
    expect(welcome_link).to_be_visible()

    welcome_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r".*/dialogue/welcome/?$"))
    expect(page.locator("#dialogue-post")).to_be_visible()
    expect(page.get_by_role("heading", name="Welcome")).to_be_visible()

    page.locator("#dialogue-post").get_by_role("link", name="Back to dialogue").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r".*/dialogue/?$"))


def test_matter_and_random_routes(page: Page, base_url: str):
    """Test direct navigation to Matter and Random pages."""
    page.goto(build_url(base_url, "matter"))
    page.wait_for_load_state("networkidle")
    expect(page.locator("#matter")).to_be_visible()
    expect(page.get_by_role("heading", name="Matter")).to_be_visible()

    page.goto(build_url(base_url, "random"))
    page.wait_for_load_state("networkidle")
    expect(page.locator("#random")).to_be_visible()
    expect(page.get_by_role("heading", name="Random")).to_be_visible()


def test_app_is_fully_hydrated(page: Page, base_url: str):
    """Test that the Dioxus app has fully hydrated and is interactive."""
    page.wait_for_load_state("networkidle")

    body = page.locator("body")
    expect(body).to_be_visible()

    page.locator("#navbar").get_by_role("link", name="Dialogue").click()
    page.wait_for_load_state("networkidle")

    expect(page.locator("#navbar")).to_be_visible()
    expect(page).to_have_url(re.compile(r".*/dialogue/?$"))


def test_echo_server_function(page: Page):
    """Test that the fullstack echo server function responds to input."""
    page.wait_for_load_state("networkidle")

    echo_input = page.locator("#echo input")
    expect(echo_input).to_be_visible()

    echo_input.fill("pavilion")
    expect(page.locator("#echo").get_by_text("Server echoed:")).to_be_visible(timeout=10_000)
    expect(page.locator("#echo").get_by_text("pavilion")).to_be_visible()
