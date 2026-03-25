from functools import lru_cache
import os
import xml.etree.ElementTree as ET

import requests


class AITPartnerClient:
    """https://support.archive-it.org/hc/en-us/articles/360032747311-Access-your-account-with-the-Archive-It-Partner-API"""

    PARTNER_API_BASE_URL = "https://partner.archive-it.org/api"

    def __init__(
        self,
        username: str = os.getenv("AIT_USERNAME"),
        password: str = os.getenv("AIT_PASSWORD"),
    ):
        self.session = requests.Session()
        if username and password:
            self.session.auth = (username, password)

    @lru_cache()
    def get(self, prefix, **kwargs):
        url = f"{self.PARTNER_API_BASE_URL}/{prefix}?limit=-1"
        for key, value in kwargs.items():
            url += f"&{key}={value}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


class AITOpensearchClient:
    """https://support.archive-it.org/hc/en-us/articles/208002246-Access-your-web-archives-with-OpenSearch"""

    OPENSEARCH_BASE_URL = "https://archive-it.org/search-master/opensearch"

    def __init__(self):
        pass

    @lru_cache()
    def search(
        self,
        collection_id: int,
        query: str,
        limit=20,
        offset=0,
    ) -> dict:
        response = requests.get(
            f"{self.OPENSEARCH_BASE_URL}?i={collection_id}&q={query}&p={offset}&n={limit}"
        )
        ns = {
            "wa": "http://web.archive.org/-/spec/opensearchrss/1.0/",
            "os": "http://a9.com/-/spec/opensearchrss/1.0/",
        }

        root = ET.fromstring(response.text)
        items = []
        for item in root.findall(".//item"):
            item = {
                "title": item.findtext("title", "").strip(),
                "link": item.findtext("link", "").strip(),
                "date": item.findtext("date", "").strip(),
                "description": item.findtext("description", "").strip(),
                "score": item.findtext("wa:score", namespaces=ns),
                "site": item.findtext("wa:site", namespaces=ns),
                "length": item.findtext("wa:length", namespaces=ns),
                "type": item.findtext("wa:type", namespaces=ns),
                "collection": item.findtext("wa:collection", namespaces=ns),
            }
            item["wayback_link"] = (
                f"https://wayback.archive-it.org/{collection_id}/{item['date']}/{item['link']}"
            )
            items.append(item)

        return {
            "total": int(
                root.findtext(".//os:totalResults", namespaces=ns, default="0")
            ),
            "offset": offset,
            "limit": limit,
            "items": items,
        }


class AITCDXClient:
    """https://support.archive-it.org/hc/en-us/articles/115001790023-Access-Archive-It-s-Wayback-index-with-the-CDX-C-API"""

    @lru_cache()
    def get(self, collection_id: int, url: str) -> list[dict]:
        response = requests.get(
            f"https://wayback.archive-it.org/{collection_id}/timemap/cdx?url={url}"
        )
        fields = [
            "surt_url",
            "timestamp",
            "original_url",
            "mime_type",
            "status_code",
            "digest",
            "redirect_url",
            "meta",
            "compressed_length",
            "offset",
            "warc_filename",
        ]
        records = []
        for line in response.content.strip().split(b"\n"):
            if line:
                values = line.decode("utf-8").split(" ", 10)
                records.append(dict(zip(fields, values)))
        return records


class AITWarcClient:
    """https://support.archive-it.org/hc/en-us/articles/360015225051-How-to-find-and-download-your-WARC-files-with-WASAPI"""

    def __init__(self, session):
        self.session = session

    @lru_cache()
    def get_collection_warcs(self, collection_id: int) -> dict:
        return self.session.get(
            f"https://warcs.archive-it.org/wasapi/v1/webdata?collection={collection_id}"
        ).json()

    @lru_cache()
    def get_crawl_warcs(self, crawl_id: int) -> dict:
        return self.session.get(
            f"https://warcs.archive-it.org/wasapi/v1/webdata?crawl={crawl_id}"
        ).json()


class AITCollection:
    def __init__(self, collection_id: int):
        self.collection_id = collection_id

        self._partner = AITPartnerClient()
        self._opensearch = AITOpensearchClient()
        self._cdx = AITCDXClient()
        self._warc = AITWarcClient(self._partner.session)

        self.data = self._load_collection()

    def _load_collection(self) -> dict:
        data = self._partner.get("collection", id=self.collection_id)[0]
        print(f"Loaded collection: {data['name']}, state: {data['state']}")
        return data

    def search(
        self,
        query: str,
        limit=20,
        offset=0,
    ):
        return self._opensearch.search(
            self.collection_id, query, limit=limit, offset=offset
        )

    def seeds(self):
        return self._partner.get(
            "seed",
            collection=self.collection_id,
            sort="created_date",
            limit=-1,
        )

    def crawls(self):
        return self._partner.get(
            "crawl_job",
            collection=self.collection_id,
            sort="original_start_date",
        )

    @property
    def last_crawl(self):
        crawls = self.crawls()
        if not crawls:
            return None
        return max(crawls, key=lambda c: c["original_start_date"])

    def crawl_report_hosts(self, crawl_id: int, offset=0, limit=1_000):
        hosts = self._partner.get(
            f"reports/host/{crawl_id}",
            format="json",
            offset=offset,
            limit=limit,
        )
        return {h["host"]: h for h in hosts}

    def crawl_report_seeds(self, crawl_id: int, offset=0, limit=1_000):
        hosts = self._partner.get(
            f"reports/seed/{crawl_id}",
            format="json",
            offset=offset,
            limit=limit,
        )
        return {h["seed"]: h for h in hosts}

    def cdx_for_url(self, url):
        return self._cdx.get(self.collection_id, url)

    def warcs(self, crawl_id: int | None = None) -> dict:
        if crawl_id:
            return self._warc.get_crawl_warcs(crawl_id)
        return self._warc.get_collection_warcs(self.collection_id)
