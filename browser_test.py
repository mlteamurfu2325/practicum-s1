from playwright.sync_api import Playwright, sync_playwright, expect


def test_element_appearance(page):
    page.goto("http://62.68.146.208:8501/")
    page.get_by_test_id("stSelectbox").locator("div").filter(has_text="С Вашего устройства").nth(2).click()
    page.get_by_text("С YouTube").click()
    page.get_by_placeholder("Ссылка формата https://www.").click()
    page.get_by_placeholder("Ссылка формата https://www.").fill("https://www.youtube.com/watch?v=m9NhYYg8jBo")
    page.locator("section").click()
    page.get_by_role("button", name="📺 Скачать файл с YouTube").click()
    page.get_by_role("button", name="🏁 Запустить транскрибирование!").click()
    
    locator = page.locator("span:has-text('📖 Текст без временны́х меток:')")
    expect(locator).to_be_visible(timeout=300000)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    test_element_appearance(page)
    
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
