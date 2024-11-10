from restack_ai.function import function, log
import requests
from bs4 import BeautifulSoup
import requests

@function.defn(name="crawl_website")
async def crawl_website():
    try:
        url = "http://127.0.0.1:47334/api/projects/mindsdb/knowledge_bases/govt_benefit"
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "knowledge_base": {
                "urls": [
                    "https://home.treasury.gov/",
                    "https://childcare.gov/",
                    "https://studentaid.gov/",
                    "https://www.dhs.gov",
                    "https://www.hhs.gov",
                    "https://22007apply.gov/",
                    "https://www.usa.gov",
                    "https://studentaid.gov",
                    "https://www.grants.gov/",
                    "https://www.healthcare.gov",
                    "https://www.dol.gov/",
                    "https://www.opm.gov/",
                    "https://www.cms.gov/",
                    "https://www.bls.gov/",
                    "https://www.fns.usda.gov/",
                    "https://www.nutrition.gov",
                    "https://www.hud.gov",
                    "https://www.rd.usda.gov",
                    "https://www.ssa.gov/",
                    "https://www.va.gov/",
                    "https://otda.ny.gov/",
                    "https://www.benefits.va.gov",
                    "https://benefits.va.gov/",
                    "https://www.va.gov/",
                ],
                "limit": 100,
                "crawl_depth": 5,
            }
        }


        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses


    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        log.error("crawl_website function failed", error=e)
        raise e
