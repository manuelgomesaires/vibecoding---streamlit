import csv
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else "https://people.bamboohr.com/careers"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        driver.get(url)
        # Wait for initial content or network settle
        WebDriverWait(driver, 15).until(
            EC.any_of(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/jobs/"]')),
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/careers/"]')),
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class*="job" i], [data-automation*="job" i]'))
            )
        )

        # Scroll to load more (handles infinite scroll/lazy load)
        last_height = driver.execute_script("return document.body.scrollHeight")
        stable_rounds = 0
        for _ in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                stable_rounds += 1
                if stable_rounds >= 2:
                    break
            else:
                stable_rounds = 0
            last_height = new_height

        jobs = []
        # BambooHR careers pages usually render job cards/rows with anchor links
        cards = driver.find_elements(
            By.CSS_SELECTOR,
            'a[href*="/jobs/"], a[href*="/careers/"], a[class*="job" i], [role="link"][class*="job" i]'
        )
        seen = set()
        for a in cards:
            href = a.get_attribute('href') or ''
            if not href or href in seen:
                continue
            seen.add(href)

            # Title heuristics: text content, aria-label, or nested heading element
            title = a.text.strip() or (a.get_attribute('aria-label') or '').strip()
            if not title:
                try:
                    h = a.find_element(By.CSS_SELECTOR, 'h1, h2, h3, .job-title, [class*="title" i]')
                    title = h.text.strip()
                except Exception:
                    title = ''

            # Location heuristics: sibling or descendant with 'location' in class/text
            location = ''
            try:
                loc_el = a.find_element(By.XPATH, './/*[contains(@class, "location") or contains(translate(normalize-space(.), "LOCATION", "location"), "location")]')
                location = loc_el.text.strip()
            except Exception:
                try:
                    parent = a.find_element(By.XPATH, './..')
                    loc_el2 = parent.find_element(By.XPATH, './/*[contains(@class, "location") or contains(translate(normalize-space(.), "LOCATION", "location"), "location")]')
                    location = loc_el2.text.strip()
                except Exception:
                    location = ''

            jobs.append({
                'title': title,
                'location': location,
                'link': href,
            })

        with open('jobs.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'location', 'link'])
            writer.writeheader()
            writer.writerows(jobs)

        print(f"Saved {len(jobs)} jobs to jobs.csv")

    finally:
        driver.quit()


if __name__ == '__main__':
    main()


