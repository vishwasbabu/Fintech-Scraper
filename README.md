# Fintech-Scraper

Utilities for downloading investor materials from various Fintech companies.

---

# 📈 Publicly Listed U.S. Digital Banks & Fintech Companies

| Company               | Ticker Symbol | Exchange | Investor Relations Page                                     |
| --------------------- | ------------- | -------- | ----------------------------------------------------------- |
| **Dave Inc.**         | `DAVE`        | NASDAQ   | [investors.dave.com](https://investors.dave.com/)           |
| **SoFi Technologies** | `SOFI`        | NASDAQ   | [investors.sofi.com](https://investors.sofi.com/)           |
| **Upstart Holdings**  | `UPST`        | NASDAQ   | [ir.upstart.com](https://ir.upstart.com/)                   |
| **LendingClub Corp.** | `LC`          | NYSE     | [ir.lendingclub.com](https://ir.lendingclub.com/)           |
| **Affirm Holdings**   | `AFRM`        | NASDAQ   | [investors.affirm.com](https://investors.affirm.com/)       |
| **Block Inc.**        | `SQ`          | NYSE     | [investors.block.xyz](https://investors.block.xyz/)         |
| **PayPal Holdings**   | `PYPL`        | NASDAQ   | [investor.pypl.com](https://investor.pypl.com/)             |
| **Robinhood Markets** | `HOOD`        | NASDAQ   | [investors.robinhood.com](https://investors.robinhood.com/) |
| **Coinbase Global**   | `COIN`        | NASDAQ   | [investor.coinbase.com](https://investor.coinbase.com/)     |

---

# 🔒 Major Private U.S. Fintech Companies & Neobanks

| Company       | Status              | Website/Investor Relations Page                         |
| ------------- | ------------------- | ------------------------------------------------------- |
| **Varo Bank** | Private             | [varomoney.com](https://www.varomoney.com)              |
| **Chime**     | Private (IPO filed) | [chime.com](https://www.chime.com)                      |
| **Stripe**    | Private             | [stripe.com](https://stripe.com)                        |
| **Brex**      | Private             | [brex.com](https://www.brex.com)                        |
| **Plaid**     | Private             | [plaid.com](https://plaid.com)                          |
| **Marqeta**   | `MQ` (Public)       | [investors.marqeta.com](https://investors.marqeta.com/) |
| **Ramp**      | Private             | [ramp.com](https://ramp.com)                            |
| **Current**   | Private             | [current.com](https://current.com)                      |
| **Upgrade**   | Private             | [upgrade.com](https://upgrade.com)                      |

---

# 🌍 International Fintech Companies & Neobanks

| Company                  | Ticker Symbol | Exchange           | Investor Relations Page                             |
| ------------------------ | ------------- | ------------------ | --------------------------------------------------- |
| **Adyen**                | `ADYEN`       | Euronext Amsterdam | [investors.adyen.com](https://investors.adyen.com/) |
| **Nu Holdings (Nubank)** | `NU`          | NYSE               | [investors.nu](https://investors.nu/)               |
| **Wise plc**             | `WISE`        | LSE                | [wise.com/investors](https://wise.com/investors)    |
| **Revolut**              | - (Private)   | -                  | [revolut.com](https://www.revolut.com)              |
| **Monzo**                | - (Private)   | -                  | [monzo.com](https://monzo.com)                      |
| **Starling Bank**        | - (Private)   | -                  | [starlingbank.com](https://www.starlingbank.com)    |
| **N26**                  | - (Private)   | -                  | [n26.com](https://n26.com)                          |

---






## Usage

1. Run the scraper to download investor materials:

```bash
python3 scraper.py
```

This creates a `scraped_data/` directory with one subfolder per company. Run the script periodically (e.g. using cron) or invoke `schedule_daily()` to keep the data up to date.

2. Start the web UI:

```bash
uvicorn app:app --reload --port 8000
```

Open `http://localhost:8000/` in a browser to browse available companies and their files. Market data for public tickers is fetched from Yahoo Finance.

Note: the `push_to_chatgpt` function in `scraper.py` is a placeholder for pushing downloaded files to a custom ChatGPT instance.
