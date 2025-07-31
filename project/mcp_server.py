from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name = "ProductsScraper",
    host="0.0.0.0",  
    port=8000
)


@mcp.tool(description="Scrapes 10 top-rated products (4 stars and above) from Daraz.pk based on the search query. Returns title, price, and product link.")
def get_daraz_products(query):
    url = f"https://www.daraz.pk/catalog/?q={query}&rating=4"

    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # Wait for JS to load

    product_divs = driver.find_elements(By.CSS_SELECTOR, '[data-qa-locator="product-item"]')
    
    results = []
    for div in product_divs[:10]:
        try:
            title_elem = div.find_element(By.CSS_SELECTOR, 'div.RfADt a')
            price_elem = div.find_element(By.CSS_SELECTOR, 'span.ooOxS')
            
            title = title_elem.get_attribute("title").strip()
            price_str = price_elem.text.replace("Rs.", "").replace(",", "").strip()
            price = float(price_str)
            link = title_elem.get_attribute("href")
            if link.startswith("//"):
                link = "https:" + link

            results.append({
                "title": title,
                "price": price,
                "link": link
            })
        except Exception as e:
            continue
    
    driver.quit()
    return results


@mcp.tool(description="Scrapes product listings from Telemart.pk based on search query. Extracts top 10 items with name, price, and link.")
def get_telemart_products(query):
    url = f"https://telemart.pk/search?query={query}"

    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.bg-white.relative.cursor-pointer'))
    )

    product_divs = driver.find_elements(By.CSS_SELECTOR, 'div.bg-white.relative.cursor-pointer')
    
    results = []
    for div in product_divs[:10]:
        try:
            link_elem = div.find_element(By.TAG_NAME, 'a')
            title_elem = div.find_element(By.CSS_SELECTOR, 'h4')
            price_elem = div.find_element(By.CSS_SELECTOR, 'span.text-green-600')
            
            title = title_elem.text.strip()
            price_str = price_elem.text.replace("Rs.", "").replace(",", "").strip()
            price = float(price_str)
            
            link = link_elem.get_attribute("href")
            if link.startswith("/"):
                link = "https://telemart.pk" + link

            results.append({
                "title": title,
                "price": price,
                "link": link
            })
        except Exception as e:
            continue
    
    driver.quit()
    return results



@mcp.tool(description="Scrapes search results from iShopping.pk. Returns up to 10 products with their title, price, and URL.")
def get_ishopping_products(query):
    url = f"https://www.ishopping.pk/catalogsearch/result/?q={query}"

    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-item-info'))
    )

    product_items = driver.find_elements(By.CSS_SELECTOR, 'div.product-item-info')

    results = []
    for index, item in enumerate(product_items[:10]): # Limit to first 10 products
        try:
            # Extract title and link
            title_elem = item.find_element(By.CSS_SELECTOR, 'a.product-item-link')
            title = title_elem.text.strip()
            link = title_elem.get_attribute("href")

            price_wrapper = item.find_element(By.CSS_SELECTOR, 'span.price-wrapper')
            price_str = price_wrapper.get_attribute("data-price-amount")

            if not price_str:
                print(f"Product {index + 1}: No price found. Skipping.")
                continue

            price = float(price_str)

            results.append({
                "title": title,
                "price": price,
                "link": link
            })
        except Exception as e:
            print("Error parsing item:", e)
            continue

    driver.quit()
    return results




if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")