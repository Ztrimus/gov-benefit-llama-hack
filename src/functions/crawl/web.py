"""
-----------------------------------------------------------------------
File: workflows/tp.py
Creation Time: Nov 9th, 2024, 6:51 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
"""

import time
import os
import re
import tempfile
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse
from pinecone import Pinecone, ServerlessSpec

# set up parser
parser = LlamaParse(
    api_key=os.environ["LLAMA_CLOUD_API_KEY"], result_type="markdown"
)  # "markdown" and "text" are available
file_extractor = {".pdf": parser}

# Initialize Pinecone and set up index
visited_urls = set()
INDEX_NAME = "gov-benefits"
API_KEY = os.getenv("PINECONE_API_KEY")
MAX_VISITED_URL = 5
MAX_DOCUMENTS = 96


def initialize_pinecone_index():
    pc = Pinecone(api_key=API_KEY)
    if INDEX_NAME not in [index["name"] for index in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024,  # Replace with your model dimensions
            metric="cosine",  # Replace with your model metric
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return pc


def parse_pdf(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "downloaded_file.pdf")
        try:
            # Download PDF
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(response.content)

            # Process PDF with SimpleDirectoryReader
            documents = SimpleDirectoryReader(
                input_dir=temp_dir, file_extractor=file_extractor
            ).load_data([pdf_path])
            return documents
        except Exception as e:
            print(f"Failed to read PDF {url}: {e}")
            return []


def crawl(url, max_depth, current_depth=0):
    if (
        current_depth > max_depth
        or url in visited_urls
        or len(visited_urls) > MAX_VISITED_URL
    ):
        return []

    print(f"Crawling: {url} at depth {current_depth}")
    visited_urls.add(url)
    web_content_list = set()

    # Fetch and clean content using SimpleWebPageReader
    try:
        if url.endswith(".pdf"):
            documents = parse_pdf(url)
        else:
            documents = SimpleWebPageReader(html_to_text=True).load_data([url])
        for doc in documents:
            if doc.text.strip():
                cleaned_text = clean_text(doc.text)
                print(f"Content from {url}: {cleaned_text}")
                for line in cleaned_text.split("\n"):
                    web_content_list.add(line)
    except Exception as e:
        print(f"Failed to read page {url}: {e}")

    # Parse links and recurse if within the same domain
    try:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        all_links_in_page = set(
            [link["href"] for link in soup.find_all("a", href=True)]
        )
        for href in all_links_in_page:
            if href.startswith("#") or href == "/":
                continue
            link = urljoin(url, href)
            if is_same_domain(url, link) and link not in visited_urls:
                web_content_list.union(crawl(link, max_depth, current_depth + 1))
    except requests.RequestException as e:
        print(f"Error fetching links from {url}: {e}")

    return web_content_list


def is_same_domain(base_url, new_url):
    return urlparse(base_url).netloc == urlparse(new_url).netloc


def clean_text(text):
    # Remove non-ASCII characters and extra whitespace
    lines = text.splitlines()
    cleaned_lines = [re.sub(r"[^\x00-\x7F]+", "", line).strip() for line in lines]
    return "\n".join(filter(None, cleaned_lines))


def create_vector_embedding(pc, data):
    embeddings = []
    for i in range(0, len(data), MAX_DOCUMENTS):
        embedding = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=data[i : i + MAX_DOCUMENTS],
            parameters={"input_type": "passage", "truncate": "END"},
        )
        embeddings.extend(embedding)
    return embeddings


def upsert_data(pc, data, embeddings):
    # Wait for the index to be ready
    while not pc.describe_index(INDEX_NAME).status.get("ready", False):
        time.sleep(1)

    index = pc.Index(INDEX_NAME)
    vectors = [
        {"id": f"{time.time()}_{i}", "values": e["values"], "metadata": {"text": d}}
        for i, (d, e) in enumerate(zip(data, embeddings))
    ]
    index.upsert(vectors=vectors, namespace="ns1")
    return index


def get_matching_embedding(pc, query: str):
    index = pc.Index(INDEX_NAME)
    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"},
    )
    results = index.query(
        namespace="ns1",
        vector=embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True,
    )
    return results


def main():
    pc = initialize_pinecone_index()
    start_urls = [
        "https://benefits.va.gov/benefits/",
        # "https://childcare.gov/",
        # "https://studentaid.gov",
        # "https://www.healthcare.gov",
        # "https://home.treasury.gov/",
        # "https://studentaid.gov/",
        # "https://www.dhs.gov",
        # "https://www.hhs.gov",
        # "https://22007apply.gov/",
        # "https://www.usa.gov",
        # "https://www.grants.gov/",
        # "https://www.dol.gov/",
        # "https://www.opm.gov/",
        # "https://www.cms.gov/",
        # "https://www.bls.gov/",
        # "https://www.fns.usda.gov/",
        # "https://www.nutrition.gov",
        # "https://www.hud.gov",
        # "https://www.rd.usda.gov",
        # "https://www.ssa.gov/",
        # "https://www.va.gov/",
        # "https://otda.ny.gov/",
        # "https://www.benefits.va.gov",
        # "https://www.va.gov/",
    ]

    # Crawling the web and creating embeddings
    web_crawl_data = []
    for url in start_urls:
        web_crawl_data.extend(crawl(url, max_depth=2))

    if web_crawl_data:
        embeddings = create_vector_embedding(pc, web_crawl_data)
        upsert_data(pc, web_crawl_data, embeddings)
    else:
        print("No data crawled.")

    query = "What kind of benefits veterans have from government?"
    results = get_matching_embedding(pc, query)


if __name__ == "__main__":
    main()
