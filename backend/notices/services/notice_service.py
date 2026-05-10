import requests
from bs4 import BeautifulSoup
from sqlmodel import Session, func, select
import urllib3
from notices.models.notice import Notice
from notices.schemas.notice import NoticeCreate
from datetime import datetime, timezone

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_notices_initial() -> list[NoticeCreate]:
    base_url = "https://iost.tu.edu.np/notices"
    headers = {"User-Agent": "Mozilla/5.0"}
    all_notices = []
    url = base_url

    while url:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        for notice in soup.find_all("div", class_="recent-post-wrapper"):
            
            date = notice.find("span", class_="nep_date").text.strip()
            title = notice.find("h5").text.strip()
            link = notice.find("a")["href"]
            notice_number = int(link.split("/")[-1])
            print(f"scraping notice {notice_number}")

            all_notices.append(NoticeCreate(
                date=parse_notice_date(date),
                title=title,
                link=link,
                notice_number=notice_number,
            ))

        next_button = soup.find("a", rel="next")
        url = next_button["href"] if next_button else None

    print(f"\nTotal notices scraped: {len(all_notices)}")
    return all_notices

def scrape_notices(session) -> list[NoticeCreate]:
    base_url = "https://iost.tu.edu.np/notices"
    headers = {"User-Agent": "Mozilla/5.0"}
    all_notices = []
    url = base_url

    latest_notice_number = session.exec(
        select(func.max(Notice.notice_number))
    ).one()

    while url:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        for notice in soup.find_all("div", class_="recent-post-wrapper"):
            
            date = notice.find("span", class_="nep_date").text.strip()
            title = notice.find("h5").text.strip()
            link = notice.find("a")["href"]
            notice_number = int(link.split("/")[-1])
            print(f"scraping notice {notice_number}")
            if notice_number <= latest_notice_number:
                print(f"\nTotal notices scraped: {len(all_notices)}")
                if len(all_notices) == 0:
                    print("database uptodate")
                return all_notices

            all_notices.append(NoticeCreate(
                date=parse_notice_date(date),
                title=title,
                link=link,
                notice_number=notice_number,
            ))

        next_button = soup.find("a", rel="next")
        url = next_button["href"] if next_button else None

    print(f"\nTotal notices scraped: {len(all_notices)}")
    return all_notices
    
    


def create_notice(session, data: NoticeCreate) -> Notice:
    notice = Notice(**data.model_dump())
    session.add(notice)
    session.commit()
    session.refresh(notice)
    return notice


def seed_notices(session):
    if is_notice_table_empty(session):
        notices = scrape_notices_initial()
    else:
        notices = scrape_notices(session)
    for data in notices:
        create_notice(session, data)
    print(f"Inserted {len(notices)} notices into the database.")
    return len(notices)  # return count

def parse_notice_date(date_str: str) -> datetime:
    """Convert scraped date string '2026-04-29' to timezone-aware datetime."""
    return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

def is_notice_table_empty(session: Session) -> bool:
    return session.exec(select(Notice).limit(1)).first() is None