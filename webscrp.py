from playwright.sync_api import sync_playwright
import os
import requests

def get_pdfs():
    unique_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.cbsl.gov.lk/si/%E0%B7%83%E0%B6%82%E0%B6%9B%E0%B7%8A%E2%80%8D%E0%B6%BA%E0%B7%8F%E0%B6%AD%E0%B7%92/%E0%B6%86%E0%B6%BB%E0%B7%8A%E0%B6%AE%E0%B7%92%E0%B6%9A-%E0%B6%AF%E0%B6%BB%E0%B7%8A%E0%B7%81%E0%B6%9A/%E0%B6%B8%E0%B7%92%E0%B6%BD-%E0%B7%80%E0%B7%8F%E0%B6%BB%E0%B7%8A%E0%B6%AD%E0%B7%8F%E0%B7%80")
        publications = page.locator('.view-content').nth(2)
        anchors = publications.locator('a').all()
        for anchor in anchors:
            url = anchor.get_attribute('href')
            if url and url.endswith(".pdf"):
                
                if url.startswith('/'):
                    url = "https://www.cbsl.gov.lk" + url
                unique_urls.add(url)
        browser.close()

    return list(unique_urls)

def download_pdfs(pdf_urls, download_folder = "data"):
    """Downloads the given PDF URLs and saves them to an existing folder."""
    
    if not os.path.exists(download_folder):
        print(f"Warning: Folder '{download_folder}' does not exist. Creating it...")
        os.makedirs(download_folder)
    
    existing_files = set(os.listdir(download_folder))

    for url in pdf_urls:
        pdf_name = url.split("/")[-1] 
        pdf_path = os.path.join(download_folder, pdf_name)

        if pdf_name in existing_files:
            print(f"Skipping {pdf_name}, already downloaded.")
            continue

        print(f"Downloading: {url}...")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status() 
            
            with open(pdf_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Saved: {pdf_path}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")

