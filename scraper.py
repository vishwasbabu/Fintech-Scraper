# coding: utf-8
"""Scraper for Fintech investor materials.

Downloads investor materials for all listed companies
and stores them under scraped_data/<company>.
Tracks downloaded URLs to avoid duplicates.

This script uses only the Python standard library.
"""

from __future__ import annotations

import os
import json
import time
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)
USER_AGENT = "Mozilla/5.0 (FintechScraper/1.0)"
HEADERS = {"User-Agent": USER_AGENT}


DATA_DIR = os.path.join(os.path.dirname(__file__), "scraped_data")
TRACK_FILE = "downloaded.json"

COMPANIES = [
    {
        "name": "Dave Inc.",
        "ticker": "DAVE",
        "ir": "https://investors.dave.com/",
    },
    {
        "name": "SoFi Technologies",
        "ticker": "SOFI",
        "ir": "https://investors.sofi.com/",
    },
    {
        "name": "Upstart Holdings",
        "ticker": "UPST",
        "ir": "https://ir.upstart.com/",
    },
    {
        "name": "LendingClub Corp.",
        "ticker": "LC",
        "ir": "https://ir.lendingclub.com/",
    },
    {
        "name": "Affirm Holdings",
        "ticker": "AFRM",
        "ir": "https://investors.affirm.com/",
    },
    {
        "name": "Block Inc.",
        "ticker": "SQ",
        "ir": "https://investors.block.xyz/",
    },
    {
        "name": "PayPal Holdings",
        "ticker": "PYPL",
        "ir": "https://investor.pypl.com/",
    },
    {
        "name": "Robinhood Markets",
        "ticker": "HOOD",
        "ir": "https://investors.robinhood.com/",
    },
    {
        "name": "Coinbase Global",
        "ticker": "COIN",
        "ir": "https://investor.coinbase.com/",
    },
    {
        "name": "Varo Bank",
        "ticker": None,
        "ir": "https://www.varomoney.com",
    },
    {
        "name": "Chime",
        "ticker": None,
        "ir": "https://www.chime.com",
    },
    {
        "name": "Stripe",
        "ticker": None,
        "ir": "https://stripe.com",
    },
    {
        "name": "Brex",
        "ticker": None,
        "ir": "https://www.brex.com",
    },
    {
        "name": "Plaid",
        "ticker": None,
        "ir": "https://plaid.com",
    },
    {
        "name": "Marqeta",
        "ticker": "MQ",
        "ir": "https://investors.marqeta.com/",
    },
    {
        "name": "Ramp",
        "ticker": None,
        "ir": "https://ramp.com",
    },
    {
        "name": "Current",
        "ticker": None,
        "ir": "https://current.com",
    },
    {
        "name": "Upgrade",
        "ticker": None,
        "ir": "https://upgrade.com",
    },
    {
        "name": "Adyen",
        "ticker": "ADYEN",
        "ir": "https://investors.adyen.com/",
    },
    {
        "name": "Nu Holdings (Nubank)",
        "ticker": "NU",
        "ir": "https://investors.nu/",
    },
    {
        "name": "Wise plc",
        "ticker": "WISE",
        "ir": "https://wise.com/investors",
    },
    {
        "name": "Revolut",
        "ticker": None,
        "ir": "https://www.revolut.com",
    },
    {
        "name": "Monzo",
        "ticker": None,
        "ir": "https://monzo.com",
    },
    {
        "name": "Starling Bank",
        "ticker": None,
        "ir": "https://www.starlingbank.com",
    },
    {
        "name": "N26",
        "ticker": None,
        "ir": "https://n26.com",
    },
]


class LinkParser(HTMLParser):
    """Minimal HTML parser to extract links to likely investor files."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = None
        for attr, val in attrs:
            if attr == "href":
                href = val
                break
        if href and any(href.lower().endswith(ext) for ext in [
            ".pdf", ".zip", ".ppt", ".pptx", ".xls", ".xlsx"
        ]):
            self.links.append(href)


def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        logger.debug(f"Creating directory {path}")
        os.makedirs(path)


def load_history(company_dir: str) -> dict:
    track_path = os.path.join(company_dir, TRACK_FILE)
    if os.path.exists(track_path):
        logger.debug(f"Loading history from {track_path}")
        with open(track_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(company_dir: str, history: dict) -> None:
    track_path = os.path.join(company_dir, TRACK_FILE)
    logger.debug(f"Saving history to {track_path}")
    with open(track_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def download_file(url: str, dest: str) -> None:
    logger.debug(f"Downloading {url} -> {dest}")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as out:
        data = resp.read()
        logger.debug(f"Writing {len(data)} bytes")
        out.write(data)


def push_to_chatgpt(path: str) -> None:
    """Placeholder for pushing files to custom ChatGPT."""
    logger.info(f"[CHATGPT] Would push {path}")


def scrape_company(company: dict) -> None:
    name = company["name"]
    ir_url = company["ir"]
    logger.info(f"Scraping {name}: {ir_url}")
    company_slug = name.lower().replace(" ", "_")
    company_dir = os.path.join(DATA_DIR, company_slug)
    ensure_dir(company_dir)
    logger.debug(f"Company directory: {company_dir}")
    # store metadata with ticker so UI can show market stats
    meta_path = os.path.join(company_dir, "metadata.json")
    meta = {"name": name, "ticker": company.get("ticker")}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f)
    history = load_history(company_dir)

    try:
        logger.debug(f"Requesting IR page {ir_url}")
        req = urllib.request.Request(ir_url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        logger.debug(f"Downloaded {len(html)} bytes from {ir_url}")
    except Exception as e:
        logger.error(f"Failed to download {ir_url}: {e}")
        return

    parser = LinkParser()
    parser.feed(html)
    logger.debug(f"Found {len(parser.links)} links on IR page")

    new_links = []
    for link in parser.links:
        abs_url = urljoin(ir_url, link)
        if abs_url in history:
            logger.debug(f"Skipping already downloaded {abs_url}")
            continue
        filename = os.path.basename(urlparse(abs_url).path)
        if not filename:
            continue
        dest_path = os.path.join(company_dir, filename)
        try:
            logger.info(f"  downloading {abs_url}")
            download_file(abs_url, dest_path)
            history[abs_url] = filename
            new_links.append(dest_path)
        except Exception as e:
            logger.error(f"  failed {abs_url}: {e}")

    if new_links:
        save_history(company_dir, history)
        for path in new_links:
            push_to_chatgpt(path)


def scrape_all() -> None:
    logger.info("Starting scrape of all companies")
    ensure_dir(DATA_DIR)
    for company in COMPANIES:
        scrape_company(company)


def schedule_daily() -> None:
    while True:
        scrape_all()
        logger.info("Sleeping for 24h...")
        time.sleep(60 * 60 * 24)


if __name__ == "__main__":
    logger.info("Running scraper once")
    scrape_all()
