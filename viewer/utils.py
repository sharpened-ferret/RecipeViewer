from selenium import webdriver

# Backup scraper for sites that require JavaScript to load
def backupScraper(url):
    driver = webdriver.Firefox()
    driver.get(url)
    page = driver.page_source
    driver.quit()
    return page
