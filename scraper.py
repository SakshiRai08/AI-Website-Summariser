import requests
from bs4 import BeautifulSoup

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_website_contents(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, headers=HEADER, timeout=15)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Could not fetch the website. Error: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No title found"

    for tag in soup(["script", "style", "nav", "footer", "button"]):
        tag.decompose()  # Remove script and style tags

    text = soup.get_text(separator="\n", strip=True)
    return f"Title: {title}\n\nContent:\n{text[:10000]}"  # Limit to first 10,000 characters