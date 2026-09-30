"""Utility to extract real technical SEO signals from raw HTML content.

Checks for Schema.org, OpenGraph, headings, FAQ, meta tags, etc.
Used to compute visibility scores based on actual page signals, not formulas.
"""
from __future__ import annotations

import json
import re
from typing import Any

import httpx
from bs4 import BeautifulSoup


def extract_technical_signals(html: str, full_text: str = "", brand: str = "") -> dict[str, Any]:
    """Extract real technical SEO and AEO signals from HTML content.

    Returns a dict of boolean flags and counts for each signal.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Schema.org JSON-LD
    schema_scripts = soup.find_all("script", type="application/ld+json")
    schema_types: list[str] = []
    for script in schema_scripts:
        try:
            data = json.loads(script.string or "")
            if isinstance(data, dict):
                schema_types.append(data.get("@type", "Unknown"))
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        schema_types.append(item.get("@type", "Unknown"))
        except Exception:
            pass
    has_schema_org = len(schema_scripts) > 0

    # OpenGraph
    og_tags = soup.find_all("meta", attrs={"property": re.compile(r"^og:")})
    has_opengraph = len(og_tags) > 0

    # Twitter Cards
    twitter_tags = soup.find_all("meta", attrs={"name": re.compile(r"^twitter:")})
    has_twitter_cards = len(twitter_tags) > 0

    # Meta Description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    has_meta_description = meta_desc is not None and bool(str(meta_desc.get("content", "") or "").strip())
    meta_description_text = ""
    if meta_desc:
        raw = meta_desc.get("content") or ""
        meta_description_text = (" ".join(raw) if isinstance(raw, list) else raw).strip()
    # Canonical URL
    canonical = soup.find("link", rel="canonical")
    has_canonical = canonical is not None

    # Viewport (mobile-friendly)
    viewport = soup.find("meta", attrs={"name": "viewport"})
    has_viewport = viewport is not None

    # HTML lang attribute
    html_tag = soup.find("html")
    has_lang_attr = html_tag is not None and bool(html_tag.get("lang"))

    # Heading hierarchy
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")
    h3_tags = soup.find_all("h3")
    has_h1 = len(h1_tags) > 0
    has_heading_hierarchy = has_h1 and len(h2_tags) > 0

    # FAQ content detection
    has_faq_schema = any("FAQ" in t for t in schema_types)
    
    # Extract all text and find questions (short sentences ending with ?)
    text_nodes = soup.find_all(string=True)
    questions = []
    for text in text_nodes:
        cleaned = text.strip()
        if cleaned.endswith("?") and len(cleaned) < 150 and len(cleaned) > 10:
            questions.append(cleaned)
            
    details_elements = soup.find_all("details")
    # Also check if 'faq' or 'frequently asked questions' is in the text
    has_faq_title = re.search(r'frequently asked questions|faq\b', soup.get_text(strip=True), re.IGNORECASE) is not None
    
    has_faq_content = has_faq_schema or len(questions) >= 2 or len(details_elements) >= 2 or (has_faq_title and len(questions) >= 1)
    
    faq_headings_count = len(questions)

    # Image alt text
    images = soup.find_all("img")
    images_with_alt = [img for img in images if str(img.get("alt", "") or "").strip()]
    has_alt_text = len(images) == 0 or (len(images_with_alt) / max(len(images), 1)) > 0.5

    # Brand in first 100 chars
    brand_in_first_100 = brand.lower() in full_text[:100].lower() if brand and full_text else False

    # Internal links count
    internal_links = [a for a in soup.find_all("a", href=True) if not str(a["href"]).startswith(("http", "mailto", "tel", "#", "javascript"))]

    # Content word count
    word_count = len(full_text.split()) if full_text else 0

    return {
        "has_schema_org": has_schema_org,
        "schema_types": schema_types,
        "has_opengraph": has_opengraph,
        "og_tags_count": len(og_tags),
        "has_twitter_cards": has_twitter_cards,
        "has_meta_description": has_meta_description,
        "meta_description_text": meta_description_text,
        "has_canonical": has_canonical,
        "has_viewport": has_viewport,
        "has_lang_attr": has_lang_attr,
        "has_h1": has_h1,
        "h1_count": len(h1_tags),
        "h2_count": len(h2_tags),
        "h3_count": len(h3_tags),
        "has_heading_hierarchy": has_heading_hierarchy,
        "has_faq_content": has_faq_content,
        "faq_headings_count": faq_headings_count,
        "has_alt_text": has_alt_text,
        "images_count": len(images),
        "images_with_alt_count": len(images_with_alt),
        "brand_in_first_100_chars": brand_in_first_100,
        "internal_links_count": len(internal_links),
        "word_count": word_count,
    }


def compute_visibility_score(signals: dict[str, Any]) -> dict[str, int]:
    """Compute specific readiness scores (0-100) based on real technical signals.
    
    Breaks down scores into SEO, AEO, GEO, and GLMM readiness.
    """
    word_count = signals.get("word_count", 0)

    # 1. SEO (Search Engine Optimization)
    seo_points = 0
    seo_max = 35
    if signals.get("has_h1", False): seo_points += 5
    if signals.get("has_meta_description", False): seo_points += 5
    if signals.get("has_canonical", False): seo_points += 5
    if signals.get("has_viewport", False): seo_points += 5
    if signals.get("has_sitemap", False): seo_points += 5
    if signals.get("has_robots_txt", False): seo_points += 5
    if signals.get("has_alt_text", False): seo_points += 5
    seo_score = int((seo_points / seo_max) * 100) if seo_max > 0 else 0

    # 2. AEO (Answer Engine Optimization)
    aeo_points = 0
    aeo_max = 30
    if signals.get("has_faq_content", False): aeo_points += 10
    if signals.get("has_schema_org", False): aeo_points += 10
    if signals.get("has_heading_hierarchy", False): aeo_points += 10
    aeo_score = int((aeo_points / aeo_max) * 100) if aeo_max > 0 else 0

    # 3. GEO (Generative Engine Optimization)
    geo_points = 0
    geo_max = 25
    if signals.get("brand_in_first_100_chars", False): geo_points += 10
    if signals.get("has_schema_org", False): geo_points += 5  # Shared with AEO
    if word_count > 1000: geo_points += 10
    elif word_count > 500: geo_points += 5
    geo_score = int((geo_points / geo_max) * 100) if geo_max > 0 else 0

    # 4. GLMM (Generative Large Multimodal Model)
    glmm_points = 0
    glmm_max = 25
    if signals.get("has_opengraph", False): glmm_points += 10
    if signals.get("has_twitter_cards", False): glmm_points += 5
    if signals.get("has_alt_text", False): glmm_points += 5
    if signals.get("has_lang_attr", False): glmm_points += 5
    glmm_score = int((glmm_points / glmm_max) * 100) if glmm_max > 0 else 0

    # Overall Visibility (Average of all 4)
    overall = int((seo_score + aeo_score + geo_score + glmm_score) / 4)

    return {
        "seo_score": seo_score,
        "aeo_score": aeo_score,
        "geo_score": geo_score,
        "glmm_score": glmm_score,
        "overall": overall
    }


async def check_sitemap_exists(domain: str, timeout: float = 5.0) -> bool:
    """Check if a sitemap.xml exists on the domain."""
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            resp = await client.head(f"https://{domain}/sitemap.xml")
            return resp.status_code == 200
    except Exception:
        return False


async def check_robots_txt_exists(domain: str, timeout: float = 5.0) -> bool:
    """Check if a robots.txt exists on the domain."""
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            resp = await client.head(f"https://{domain}/robots.txt")
            return resp.status_code == 200
    except Exception:
        return False
