"""
E2E validation tests for the Pavilion Dioxus blog.

These tests validate that the core app functionality is working:
- Default ("Hello") page loads and displays content
- Navigation between Hello, Dialogue, and Random works
- App is interactive and hydrated
- Dialogue lists build-time markdown posts and opens them
- Navbar is a side rail on desktop and a top bar on mobile

To run these tests:
1. Start the Dioxus server: dx serve --platform web
2. Run tests: uv run pytest tests/test_dioxus_app.py
"""

import re
from urllib.parse import urljoin

from playwright.sync_api import Page, expect

# Keep in sync with `@media (max-width: 48rem)` in assets/styling/navbar.css
MOBILE_BREAKPOINT_PX = 768
DESKTOP_VIEWPORT = {"width": 1280, "height": 720}
MOBILE_VIEWPORT = {"width": 390, "height": 844}


def build_url(base_url: str, path: str = "") -> str:
    """
    Normalize and join the base URL with a relative path.
    Ensures consistent trailing slashes and works when the base URL includes a subpath.
    """
    normalized_base = base_url.rstrip("/") + "/"
    normalized_path = path.lstrip("/")
    return urljoin(normalized_base, normalized_path)


def test_hello_page_loads_as_default(page: Page, base_url: str):
    """Test that the default route loads the hello page successfully."""
    page.wait_for_load_state("networkidle")

    body = page.locator("body")
    expect(body).to_be_visible()

    navbar = page.locator("#navbar")
    expect(navbar).to_be_visible()

    expect(page).to_have_url(build_url(base_url))
    expect(page.locator("#hello")).to_be_visible()
    expect(page.get_by_role("heading", name="Sam Miller")).to_be_visible()
    expect(page.locator("#hello").get_by_text("Hello Folks!", exact=False)).to_be_visible()


def test_navbar_navigation_works(page: Page, base_url: str):
    """Test that navbar links navigate to Hello, Dialogue, and Random."""
    page.wait_for_load_state("networkidle")

    navbar = page.locator("#navbar")
    hello_link = navbar.get_by_role("link", name="Hello")
    dialogue_link = navbar.get_by_role("link", name="Dialogue")
    random_link = navbar.get_by_role("link", name="Random")

    expect(hello_link).to_be_visible()
    expect(dialogue_link).to_be_visible()
    expect(random_link).to_be_visible()
    expect(navbar.get_by_role("link", name="Home")).to_have_count(0)

    dialogue_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r".*/dialogue/?$"))
    expect(page.locator("#dialogue")).to_be_visible()

    random_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url, "random"))
    expect(page.locator("#random")).to_be_visible()

    hello_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url))
    expect(page.locator("#hello")).to_be_visible()


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


def test_random_route(page: Page, base_url: str):
    """Test direct navigation to the Random page and server-generated number."""
    page.goto(build_url(base_url, "random"))
    page.wait_for_load_state("networkidle")
    expect(page.locator("#random")).to_be_visible()
    expect(page.get_by_role("heading", name="Random")).to_be_visible()

    number = page.locator("#random-number")
    expect(number).to_be_visible(timeout=15000)
    value = int(number.inner_text())
    assert 0 <= value < 1_000_000

    roll_button = page.locator("#random-roll")
    expect(roll_button).to_be_visible()
    first_value = value
    roll_button.click()
    page.wait_for_function(
        f"() => document.querySelector('#random-number')?.textContent.trim() !== '{first_value}'",
        timeout=15000,
    )
    second_value = int(number.inner_text())
    assert 0 <= second_value < 1_000_000


def test_app_is_fully_hydrated(page: Page, base_url: str):
    """Test that the Dioxus app has fully hydrated and is interactive."""
    page.wait_for_load_state("networkidle")

    body = page.locator("body")
    expect(body).to_be_visible()

    page.locator("#navbar").get_by_role("link", name="Dialogue").click()
    page.wait_for_load_state("networkidle")

    expect(page.locator("#navbar")).to_be_visible()
    expect(page).to_have_url(re.compile(r".*/dialogue/?$"))


def test_navbar_is_side_rail_on_desktop(page: Page):
    """On wide viewports the navbar is a vertical rail beside the content."""
    page.set_viewport_size(DESKTOP_VIEWPORT)
    page.wait_for_load_state("networkidle")

    navbar = page.locator("#navbar")
    expect(navbar).to_be_visible()

    flex_direction = navbar.evaluate("el => getComputedStyle(el).flexDirection")
    assert flex_direction == "column"

    hello = navbar.get_by_role("link", name="Hello").bounding_box()
    dialogue = navbar.get_by_role("link", name="Dialogue").bounding_box()
    page_column = page.locator(".page").first.bounding_box()
    assert hello is not None
    assert dialogue is not None
    assert page_column is not None

    # Links stack vertically in one column.
    assert hello["y"] < dialogue["y"]
    assert abs(hello["x"] - dialogue["x"]) < 8

    # Rail sits to the left of the centered content column.
    assert hello["x"] + hello["width"] <= page_column["x"] + 1


def test_navbar_is_top_bar_on_mobile(page: Page):
    """On narrow viewports the navbar becomes a horizontal top bar."""
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.wait_for_load_state("networkidle")

    navbar = page.locator("#navbar")
    expect(navbar).to_be_visible()

    flex_direction = navbar.evaluate("el => getComputedStyle(el).flexDirection")
    assert flex_direction == "row"

    hello = navbar.get_by_role("link", name="Hello").bounding_box()
    dialogue = navbar.get_by_role("link", name="Dialogue").bounding_box()
    nav_box = navbar.bounding_box()
    content = page.locator("#content").bounding_box()
    assert hello is not None
    assert dialogue is not None
    assert nav_box is not None
    assert content is not None

    # Links sit in a horizontal row.
    assert hello["x"] < dialogue["x"]
    assert abs(hello["y"] - dialogue["y"]) < 8

    # Bar sits above the content.
    assert nav_box["y"] + nav_box["height"] <= content["y"] + 1


def test_navbar_layout_switches_across_breakpoint(page: Page):
    """Navbar orientation flips when crossing the mobile breakpoint."""
    page.wait_for_load_state("networkidle")
    navbar = page.locator("#navbar")

    page.set_viewport_size({"width": MOBILE_BREAKPOINT_PX + 1, "height": 800})
    assert navbar.evaluate("el => getComputedStyle(el).flexDirection") == "column"

    page.set_viewport_size({"width": MOBILE_BREAKPOINT_PX, "height": 800})
    assert navbar.evaluate("el => getComputedStyle(el).flexDirection") == "row"


def test_navbar_navigation_works_on_mobile(page: Page, base_url: str):
    """Top-bar links remain interactive on mobile viewports."""
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.wait_for_load_state("networkidle")

    navbar = page.locator("#navbar")
    navbar.get_by_role("link", name="Dialogue").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r".*/dialogue/?$"))
    expect(page.locator("#dialogue")).to_be_visible()

    navbar.get_by_role("link", name="Hello").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(build_url(base_url))
    expect(page.locator("#hello")).to_be_visible()
