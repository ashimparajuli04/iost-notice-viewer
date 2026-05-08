import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://iost.tu.edu.np/notices"
headers = {"User-Agent": "Mozilla/5.0"}

all_notices = []
url = base_url  # Start from the first page

for _ in range(2):
    print(f"Scraping: {url}")
    response = requests.get(url, headers=headers, verify= False)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract notices on this page
    notices = soup.find_all("div", class_="recent-post-wrapper")
    for notice in notices:
        date = notice.find("span", class_="nep_date").text.strip()
        title = notice.find("h5").text.strip()
        link = notice.find("a")["href"]
        notice_number = int(link.split("/")[-1])
        all_notices.append({"date": date, "title": title, "link": link, "notice_number": notice_number})

    # Find the "Next" button link
    next_button = soup.find("a", rel="next")
    if next_button:
        url = next_button["href"]  # Move to next page
    else:
        url = None  # No more pages, stop the loop

print(f"\nTotal notices scraped: {len(all_notices)}")
for n in all_notices:
    print(n)