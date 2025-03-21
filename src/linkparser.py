import re

import requests
import tldextract


class LinkParser:
    __valid_domains = {
        # 'bsky.app': {
        #   'type': 'social',
        #   'replacement': 'bskyx.app'
        # },
        "instagram.com": {"type": "social", "replacement": "ddinstagram.com"},
        "bloomberg.com": {"type": "news"},
        "nytimes.com": {"type": "news"},
        "apple.news": {"type": "apple"},
        "theatlantic.com": {"type": "news"},
        "threads.net": {"type": "social", "replacement": "vxthreads.net"},
        "tiktok.com": {"type": "social", "replacement": "vxtiktok.com"},
        "twitter.com": {"type": "social", "replacement": "vxtwitter.com"},
        "washingtonpost.com": {"type": "news"},
        "wsj.com": {"type": "news"},
        "x.com": {"type": "social", "replacement": "vxtwitter.com"},
        "expressnews.com": {"type": "news"},
        "newsweek.com": {"type": "news"},
        "forbes.com": {"type": "news"},
        "haaretz.com": {"type": "news"},
        "latimes.com": {"type": "news"},
        "houstonchronicle.com": {"type": "news"},
        "stltoday.com": {"type": "news"},
    }

    def __init__(self, url) -> None:
        self.url = url
        self.extracted_url = tldextract.extract(url)

    def fix(self):
        # Check if it's a valid domain
        try:
            domain = self.extracted_url.registered_domain
            domainInfo = self.__valid_domains[domain]
        except Exception:
            return None

        # Execute the relevant replacement function and return
        if domainInfo["type"] == "social":
            return self.replace_social(domainInfo)
        elif domainInfo["type"] == "apple":
            return self.replace_apple()
        elif domainInfo["type"] == "news":
            if "unlocked_article_code" in self.url:
                return None
            else:
                return self.replace_news()

        return None

    def replace_social(self, domainInfo: object):
        """Social media link replacement"""
        fqdn = self.extracted_url.fqdn
        new_url = self.url.replace(fqdn, domainInfo["replacement"])
        return new_url

    def replace_news(self):
        """News link replacement"""
        new_url = f"https://archive.today/newest/{self.url}"
        return new_url

    def replace_apple(self):
        """Apple link replacement"""
        try:
            response = requests.get(self.url)
            if response.status_code != 200:
                return None
            content = response.text
        except Exception:
            return None
        match = re.search(r'<a\s+href="(https?://[^"]+)"', content)
        if not match:
            return None
        extracted_url = match.group(1)
        return f"https://archive.today/newest/{extracted_url}"
