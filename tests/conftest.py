"""
Shared fixtures for Playwright e2e tests.

This module provides common fixtures for testing the Dioxus application,
including browser setup and base URL configuration.
"""

import os

from playwright.sync_api import Page
import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Base URL for the Dioxus application.

    By default, assumes the app is running on localhost:8080.
    Can be overridden with the BASE_URL environment variable (useful for CI).
    To run tests, start the Dioxus server first:
        dx serve --platform web
    """
    return os.getenv("BASE_URL", "http://localhost:8080")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture
def page(page: Page, base_url: str) -> Page:
    """
    Provide a Playwright page fixture with the base URL configured.

    The page is automatically navigated to the base URL before each test.
    """
    page.goto(base_url)
    return page
