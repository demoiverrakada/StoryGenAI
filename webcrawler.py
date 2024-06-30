import requests
from bs4 import BeautifulSoup
import os
import time
import random

# Function to fetch page content
def fetch_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract story URLs from page content
def extract_story_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    story_meta_tags = soup.find_all('meta', {'about': True})

    story_urls = [meta['about'] for meta in story_meta_tags]
    return story_urls

# Function to extract story content from story page
def extract_story_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    story_div = soup.find('div', class_='panel article aa_eQ')

    if not story_div:
        print("Story content not found.")
        return None

    paragraphs = story_div.find_all('p')
    story_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
    return story_text.strip()

# Function to save story content to file
def save_story_to_file(story_content, filename, directory):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(story_content)

# Main function
def main():
    # Directory to save stories
    save_directory = '/kaggle/working/stories'
    os.makedirs(save_directory, exist_ok=True)

    # Fetching URLs from tags pages
    base_url = 'https://tags.literotica.com/dirty%20talk/?page='
    all_story_urls = []

    for page_number in range(1, 34):
        url = base_url + str(page_number)
        page_content = fetch_page_content(url)

        if page_content:
            story_urls = extract_story_urls(page_content)
            all_story_urls.extend(story_urls)
            print(f"Fetched {len(story_urls)} story URLs from {url}")
        else:
            print(f"Failed to fetch URLs from {url}")

    print(f"Total {len(all_story_urls)} story URLs fetched.")

    # Fetching and saving story content
    for index, story_url in enumerate(all_story_urls, start=1):
        print(f"Fetching story {index}/{len(all_story_urls)}...")
        story_content = fetch_page_content(story_url)

        if story_content:
            story_text = extract_story_content(story_content)
            if story_text:
                # Generate a filename based on the story title or URL
                story_title = story_url.split('/')[-1]  # Get the last part of the URL as the title
                filename = f"story_{index}_{story_title}.txt"
                save_story_to_file(story_text, filename, save_directory)
                print(f"Story saved to {os.path.join(save_directory, filename)}")

                # Add a random delay before fetching the next story
                time.sleep(random.uniform(2, 5))
        else:
            print(f"Failed to fetch story content from {story_url}")

if __name__ == '__main__':
    main()
