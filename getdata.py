import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def download_jpgs(base_url):
    visited = set()
    queue = deque([base_url])
    
    while queue:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            continue
        
        # Download JPG images
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
                except FileNotFoundError:
                    print("Failed to download image")
                    pass
                
        # Add new links to the queue
        for link in soup.find_all('a', href=True):
            full_link = urljoin(base_url, link['href'])
            if base_url in full_link and full_link not in visited:
                queue.append(full_link)

def main():
    base_url = "http://www.spanishbeercoasters.es"
    download_jpgs(base_url)

if __name__ == "__main__":
    main()
