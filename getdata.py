import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_jpgs(url, base_url, visited):
    if url in visited:
        return
    visited.add(url)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return
    
    # Create a directory to save images if it doesn't exist
    os.makedirs('images', exist_ok=True)

    # Find and download all JPG images
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url and img_url.endswith('.jpg'):
            full_img_url = urljoin(base_url, img_url)
            try:
                img_data = requests.get(full_img_url).content
                img_name = os.path.basename(full_img_url)
                with open(f'images/{img_name}', 'wb') as f:
                    f.write(img_data)
                    print(f'Downloaded {img_name}')
            except requests.RequestException as e:
                print(f"Failed to download image {full_img_url}: {e}")
    
    # Recursively visit all links on the page
    for link in soup.find_all('a', href=True):
        full_link = urljoin(base_url, link['href'])
        if base_url in full_link:  # Ensure the link is within the same domain
            download_jpgs(full_link, base_url, visited)

def main():
    base_url = "http://www.spanishbeercoasters.es"
    visited = set()
    download_jpgs(base_url, base_url, visited)

if __name__ == "__main__":
    main()
