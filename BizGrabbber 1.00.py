import os
import re
import csv
import time
import random
import contextlib
import concurrent.futures
import urllib.parse as up
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

BANNER_ASCII = (
    "██████╗ ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ \n"
    "██╔══██╗██║╚══███╔╝██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗\n"
    "██████╔╝██║  ███╔╝ ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝\n"
    "██╔══██╗██║ ███╔╝  ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗\n"
    "██████╔╝██║███████╗╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║\n"
    "╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CARDINAL = ["north", "south", "east", "west", "central", "downtown", "uptown", "midtown"]
NEAR_SYN = ["in", "near", "around", "inside", "across", "within"]

MAX_RESULTS = 500
MAX_WORKERS = 20
REQUEST_TIMEOUT = 60


def print_banner() -> None:
    print(f"{RED}{BANNER_ASCII}{RESET}")
    subtitle = f"{BLUE}B U S I N E S S   I N F O   E X T R A C T O R{RESET}"
    version = f"{RED}Version 1.00{RESET}"
    print(f"{subtitle:<70}{version}")
    print("By Joshua M Clatney - Ethical Pentesting Enthusiast\n")


def build_terms(b: str, c: str, r: str) -> list[str]:
    core = [f"{b} {k} {c} {r}" for k in NEAR_SYN]
    combos = [f"{b} {k} {c} {r}" for k in CARDINAL]
    deep = [f"{b} in {x} {c} {r}" for x in CARDINAL] + [
        f"{b} near {x} {c} {r}" for x in CARDINAL
    ]
    return (core + combos + deep)[:64]


def start_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--log-level=3")
    service = Service(ChromeDriverManager().install(), log_output=os.devnull)
    with open(os.devnull, "w") as devnull, contextlib.redirect_stderr(devnull), contextlib.redirect_stdout(
        devnull
    ):
        return webdriver.Chrome(service=service, options=opts)


def scrape_maps(driver: webdriver.Chrome, q: str, delay: int = 4) -> set[str]:
    driver.get(f"https://www.google.com/maps/search/{up.quote_plus(q)}")
    time.sleep(delay + random.uniform(0.5, 1.5))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return {
        a["href"].split("&")[0]
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("http")
        and "google." not in a["href"]
        and "maps" not in a["href"]
    }


def extract_site_info(session: requests.Session, url: str) -> dict[str, str] | None:
    try:
        r = session.get(url, timeout=REQUEST_TIMEOUT)
    except Exception:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else up.urlparse(url).netloc
    emails = "; ".join(sorted({e.lower() for e in EMAIL_RE.findall(r.text)}))
    return {"Business Name": title, "URL": url, "Email": emails}


def main() -> None:
    print_banner()
    b = input("Enter industry: ").strip()
    c = input("Enter city: ").strip()
    r = input("Enter region: ").strip()

    print("Searching...")
    terms = build_terms(b, c, r)
    driver = start_driver()
    sites = set()
    for t_ in terms:
        sites.update(scrape_maps(driver, t_))
    driver.quit()

    cleaned = [s.rstrip("/").lower() for s in sites if len(up.urlparse(s).netloc) > 3]

    records = []
    seen_url: set[str] = set()

    with requests.Session() as session, concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        future_to_url = {executor.submit(extract_site_info, session, url): url for url in cleaned}
        for future in concurrent.futures.as_completed(future_to_url):
            if len(records) == MAX_RESULTS:
                break
            info = future.result()
            if info and info["URL"] not in seen_url:
                records.append(info)
                seen_url.add(info["URL"])

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    fp = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"web-extraction-{ts}.csv")
    with open(fp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Business Name", "URL", "Email"])
        w.writeheader()
        w.writerows(records)

    print(f"Generated {len(records)} record(s) → {fp}")


if __name__ == "__main__":
    main()

#Created by Joshua M Clatney - Ethical Pentesting Enthusiast
#Clats Legal & Reliable Radio Solutions