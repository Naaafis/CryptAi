import os
import requests
import time
from lxml import html
from sentiment_layer.utils.fetchers.base_news_fetcher import BaseNewsFetcher
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SECFetcher(BaseNewsFetcher):
    def __init__(self, tickers: list[str], filing_type: str = "10-K", amount: int = 3):
        """
        :param tickers: List of stock ticker symbols to fetch SEC filings for.
        :param filing_type: Type of SEC filing to retrieve (e.g., "10-K", "10-Q").
        :param amount: Number of filings to fetch per ticker.
        """
        self.tickers = tickers
        self.filing_type = filing_type
        self.amount = amount

    def _get_session(self) -> requests.Session:
        """Creates a requests session with the appropriate headers for SEC EDGAR."""
        email = os.getenv("SEC_API_EMAIL", "your-email@example.com")

        if not email or "@" not in email:
            raise ValueError("SEC API requires a valid email in the User-Agent header.")

        session = requests.Session()
        session.headers.update({
            "User-Agent": f"Nafis Abeer {email}",
            "Accept-Encoding": "gzip, deflate",
        })
        return session

    def _get_cik(self, ticker: str) -> str:
        """Fetch the company's CIK (Central Index Key) from SEC EDGAR."""
        url = "https://www.sec.gov/files/company_tickers.json"
        session = self._get_session()

        print(f"\n[SECFetcher] Requesting CIK for {ticker} from {url}...")

        try:
            response = session.get(url)
            print(f"[SECFetcher] Response Status: {response.status_code}")

            if response.status_code != 200:
                print(f"[SECFetcher] Failed to fetch CIK for {ticker}: {response.status_code}\nResponse: {response.text}")
                return None

            cik_data = response.json()
            cik_lookup = {}
            for key, entry in cik_data.items():
                if isinstance(entry, dict) and "ticker" in entry and "cik_str" in entry:
                    cik_lookup[entry["ticker"].upper()] = entry["cik_str"]

            cik = cik_lookup.get(ticker.upper())
            if cik:
                print(f"[SECFetcher] Found CIK for {ticker}: {cik}")
                return str(cik).zfill(10)  # Format CIK with leading zeros
            else:
                print(f"[SECFetcher] CIK not found for {ticker}.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"[SECFetcher] Request error while fetching CIK for {ticker}: {e}")
            return None

    def _extract_sections(self, filing_url: str) -> dict:
        """Extract sections from the SEC filing document."""
        session = self._get_session()
        try:
            response = session.get(filing_url)
            if response.status_code != 200:
                print(f"[SECFetcher] Error fetching filing document: {response.status_code}")
                return {"Error": "Unable to fetch filing document."}

            tree = html.fromstring(response.content)

            sections = {}
            headers = tree.xpath("//div[contains(@class, 'formGrouping')]//div[contains(@class, 'infoHead')]")
            texts = tree.xpath("//div[contains(@class, 'formGrouping')]//div[contains(@class, 'info')]")

            for header, text in zip(headers, texts):
                section_name = header.text_content().strip()
                section_content = text.text_content().strip()
                sections[section_name] = section_content

            return sections

        except requests.exceptions.RequestException as e:
            print(f"[SECFetcher] Error extracting sections from filing: {e}")
            return {"Error": "Request failed while extracting sections."}

    def fetch(self) -> list[dict]:
        """
        Fetch SEC filings for the given tickers.

        :return: List of dictionaries containing SEC filing details.
        """
        results = []
        session = self._get_session()

        for ticker in self.tickers:
            try:
                cik = self._get_cik(ticker)
                if not cik:
                    continue

                filing_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
                time.sleep(1)
                response = session.get(filing_url)

                if response.status_code != 200:
                    print(f"[SECFetcher] Error fetching filings for {ticker}: {response.status_code}")
                    continue

                filing_data = response.json()
                filings = filing_data.get("filings", {}).get("recent", {})
                if not filings:
                    print(f"[SECFetcher] No recent filings found for {ticker}.")
                    continue

                for idx, accession_no in enumerate(filings["accessionNumber"][:self.amount]):
                    form_type = filings["form"][idx]
                    filing_date = filings["filingDate"][idx]
                    filing_year = filing_date.split("-")[0] if filing_date else "Unknown"

                    sec_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no.replace('-', '')}/{accession_no}-index.html"

                    print(f"[SECFetcher] Found FORM {form_type} filing for {ticker} on {filing_date}")

                    # Extract sections from filing document
                    sections = self._extract_sections(sec_url)

                    results.append({
                        "ticker": ticker,
                        "filing_type": form_type,
                        "filing_date": filing_date,
                        "filing_year": filing_year,
                        "filing_url": sec_url,
                        "sections": sections
                    })

            except requests.exceptions.RequestException as e:
                print(f"[SECFetcher] HTTP error while fetching SEC filings for {ticker}: {e}")
            except Exception as e:
                print(f"[SECFetcher] Unexpected error fetching SEC filings for {ticker}: {e}")

        return results
