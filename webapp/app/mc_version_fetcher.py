import requests
from bs4 import BeautifulSoup
import re
from packaging.version import Version
from typing import List, Tuple

def get_minecraft_versions() -> Tuple[List[str], List[str]]:
    """
    Fetches all Java Edition release versions from Mojang's official manifest,
    and all Bedrock Edition release versions by scraping the wiki.
    """

    java_versions: List[str] = []
    bedrock_versions: List[str] = []

    # -------------------------------
    # 1. Java Editions from Mojang
    # -------------------------------
    try:
        java_manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        r = requests.get(java_manifest_url, timeout=10)
        r.raise_for_status()
        manifest = r.json()
        java_versions = [v["id"] for v in manifest["versions"] if v["type"] == "release"]
    except Exception as e:
        print(f"Failed to fetch Java versions: {e}")

    # -------------------------------
    # 2. Bedrock Editions from Wiki
    # -------------------------------
    bedrock_versions: List[str] = []
    wiki_url = "https://minecraft.wiki/w/Bedrock_Edition_version_history/Development_versions"
    try:
        r = requests.get(wiki_url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # find headings like "### 1.21.90" in the page
        headings = soup.select("h3, h2")
        candidates = set()
        for h in headings:
            text = h.get_text(strip=True)
            # simple check: version patterns like "1.21.90"
            parts = text.split()
            if parts:
                v = parts[0]
                # must have at least one dot
                if v.count('.') >= 1:
                    candidates.add(v)

        # parse and sort semantically
        def version_key(v):
            try:
                return Version(v)
            except:
                return Version("0.0.0")  # fallback for non-standard versions

        sorted_versions = sorted(candidates, key=version_key, reverse=True)
        bedrock_versions = sorted_versions

    except Exception as e:
        print("Failed to fetch Bedrock versions:", e)

    return java_versions, bedrock_versions