import pytest
from config.config import BASE_URL
from playwright.async_api import expect

@pytest.mark.asyncio(loop_scope = "module")
async def test_session(browser, session, session_ui):
    sessions = {
        "api_login": session,
        "ui_login": session_ui
    }
    errors = []

    context = await browser.new_context()
    for type, session in sessions.items():
        await context.add_cookies(session)
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/my-account")
        try:
            await expect(page).to_have_url(f"{BASE_URL}/my-account")
        except AssertionError:
            errors.append(type)
        await page.close()
        await context.clear_cookies()

    assert not errors, f"Sessions with errors: {errors}"
