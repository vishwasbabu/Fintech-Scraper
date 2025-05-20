from __future__ import annotations

import json
import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

USER_AGENT = "Mozilla/5.0 (FintechScraper/1.0)"
DATA_DIR = os.path.join(os.path.dirname(__file__), "scraped_data")
TRACK_FILE = "downloaded.json"

app = FastAPI(title="Fintech Investor Materials")
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")


def list_companies() -> List[str]:
    if not os.path.exists(DATA_DIR):
        return []
    return sorted(d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d)))


def load_history(company: str) -> dict:
    path = os.path.join(DATA_DIR, company, TRACK_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def fetch_market_data(ticker: str) -> dict | None:
    if not ticker:
        return None
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        quote = data.get("quoteResponse", {}).get("result", [])
        if quote:
            q = quote[0]
            return {
                "price": q.get("regularMarketPrice"),
                "marketCap": q.get("marketCap"),
                "currency": q.get("currency"),
            }
    except Exception as e:
        print(f"Failed market data for {ticker}: {e}")
    return None


@app.get("/", response_class=HTMLResponse)
def index():
    companies = list_companies()
    items = "".join(
        f'<li><a href="/{c}">{c.replace("_", " ").title()}</a></li>' for c in companies
    )
    html = f"""
    <html>
    <body>
    <h1>Fintech Companies</h1>
    <ul>{items}</ul>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.get("/{company}", response_class=HTMLResponse)
def company_page(company: str):
    history = load_history(company)
    if history is None:
        raise HTTPException(status_code=404, detail="Company not found")
    files = [history[url] for url in history]
    files.sort()
    ticker = None
    meta_path = os.path.join(DATA_DIR, company, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            ticker = meta.get("ticker")
    stats = fetch_market_data(ticker) if ticker else None
    rows = "".join(f"<li><a href='/data/{company}/{f}'>{f}</a></li>" for f in files)
    stats_html = ""
    if stats:
        stats_html = (
            f"<p>Price: {stats['price']} {stats['currency']}<br>"
            f"Market Cap: {stats['marketCap']}</p>"
        )
    html = f"""
    <html><body>
    <h1>{company.replace('_',' ').title()}</h1>
    {stats_html}
    <ul>{rows}</ul>
    </body></html>
    """
    return HTMLResponse(html)
