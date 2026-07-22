"""
E2E validation tests for the Pavilion Dioxus blog.

These tests validate that the core app functionality is working:
- Me tab loads as the default page
- Navigation between Me, Dialogue, and Misc tabs works
- Dialogue lists links to blog posts
- Blog route params render correctly
- App is interactive and hydrated

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


def test_me_tab_loads_and_displays_content(page: Page):
    """Test that the default Me tab loads successfully and displays content."""
    page.wait_for_load_state("networkidle")

    body = page.locator("body")
    expect(body).to_be_visible()

    navbar = page.locator("#navbar")
    expect(navbar).to_be_visible()
    expect(navbar.get_by_role("link", name="Me")).to_be_visible()
    expect(navbar.get_by_role("link", name="Dialogue")).to_be_visible()
    expect(navbar.get_by_role("link", name="Misc")).to_be_visible()

    expect(page.locator("#me")).to_be_visible()
    expect(page.locator("#hero")).to_be_visible()
    expect(page.locator("#echo")).to_be_visible()


def test_home_page_learn_dioxus_link_works(page: Page):
    """Test that the Learn Dioxus hero link is present and navigates correctly."""
    page.wait_for_load_state("networkidle")

    learn_link = page.locator("#hero #links").get_by_role("link", name="Learn Dioxus")
    expect(learn_link).to_be_visible()
    expect(learn_link).to_have_attribute("href", "https://dioxuslabs.com/learn/0.7/")

    learn_link.click()
    page.wait_for_url("https://dioxuslabs.com/learn/0.7/**", timeout=15_000)
    expect(page).to_have_url(re.compile(r"https://dioxuslabs\.com/learn/0\.7/?"))


def test_navbar_tabs_navigate(page: Page, base_url: str):
    """Test that Me, Dialogue, and Misc tabs navigate correctly."""
    page.wait_for_load_state("networkidle")

    navbar = page.locator("#navbar")
    me_link = navbar.get_by_role("link", name="Me")
    dialogue_link = navbar.get_by_role("link", name="Dialogue")
    misc_link = navbar.get_by_role("link", name="Misc")

    dialogue_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "dialogue"))
    expect(page.locator("#dialogue")).to_be_visible()
    expect(page.get_by_role("heading", name="Dialogue")).to_be_visible()

    misc_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "misc"))
    expect(page.locator("#misc")).to_be_attached()

    me_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url))
    expect(page.locator("#me")).to_be_visible()
    expect(page.locator("#hero")).to_be_visible()


def test_dialogue_lists_blog_post_links(page: Page, base_url: str):
    """Test that Dialogue shows post links and opens a blog post."""
    page.goto(build_url(base_url, "dialogue"))
    page.wait_for_load_state("networkidle")

    posts = page.locator("#dialogue-posts")
    expect(posts).to_be_visible()
    expect(posts.get_by_role("link", name="Hello, Pavilion")).to_be_visible()
    expect(posts.get_by_role("link", name="Notes from the workshop")).to_be_visible()
    expect(posts.get_by_role("link", name="Small and fast")).to_be_visible()

    posts.get_by_role("link", name="Hello, Pavilion").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "blog/1"))
    expect(page.get_by_role("heading", name="This is blog #1!")).to_be_visible()


def test_misc_tab_is_empty(page: Page, base_url: str):
    """Test that the Misc tab renders an empty placeholder page."""
    page.goto(build_url(base_url, "misc"))
    page.wait_for_load_state("networkidle")

    misc = page.locator("#misc")
    expect(misc).to_be_attached()
    expect(misc).to_be_empty()


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

    page.locator("#navbar").get_by_role("link", name="Dialogue").click()
    page.wait_for_load_state("networkidle")

    expect(page.locator("#navbar")).to_be_visible()
    expect(page).to_have_url(build_url(base_url, "dialogue"))


def test_echo_server_function(page: Page):
    """Test that the fullstack echo server function responds to input."""
    page.wait_for_load_state("networkidle")

    echo_input = page.locator("#echo input")
    expect(echo_input).to_be_visible()

    echo_input.fill("pavilion")
    expect(page.locator("#echo").get_by_text("Server echoed:")).to_be_visible(timeout=10_000)
    expect(page.locator("#echo").get_by_text("pavilion")).to_be_visible()
