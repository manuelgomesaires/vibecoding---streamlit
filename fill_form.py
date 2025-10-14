import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def fill_input_by_label(driver, label_text: str, value: str) -> None:
    # Find form question block containing the label text
    blocks = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
    for block in blocks:
        if label_text.lower() in block.text.lower():
            # Try to find an input or textarea inside this block
            inputs = block.find_elements(By.CSS_SELECTOR, 'input, textarea')
            if inputs:
                elem = inputs[0]
                elem.clear()
                elem.send_keys(value)
                return
    # If not found, do nothing (field may be optional)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python fill_form.py <google_form_url>")
        sys.exit(1)

    form_url = sys.argv[1]

    # Optional CLI args: url name email address phone comments
    name = sys.argv[2] if len(sys.argv) > 2 else "Ada Lovelace"
    email = sys.argv[3] if len(sys.argv) > 3 else "ada@example.com"
    address = sys.argv[4] if len(sys.argv) > 4 else "10 Downing Street, London"
    phone = sys.argv[5] if len(sys.argv) > 5 else "+44 20 7946 0958"
    comments = sys.argv[6] if len(sys.argv) > 6 else "Automated submission from Selenium."

    # Launch Chrome with automatic driver installation
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        driver.get(form_url)
        time.sleep(2)

        # Values (can be overridden via CLI args)
        fill_input_by_label(driver, "Name", name)
        fill_input_by_label(driver, "Email", email)
        fill_input_by_label(driver, "Address", address)
        fill_input_by_label(driver, "Phone number", phone)
        fill_input_by_label(driver, "Comments", comments)

        # Submit
        buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
        for btn in buttons:
            if "submit" in btn.text.lower():
                btn.click()
                break

        time.sleep(3)
        print("Form submitted (if all required fields were filled).")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
