import base64
import json
import os

import httpx
from playwright.async_api import async_playwright  # type: ignore


async def get_google_pagespeed_score(url: str, api_key: str | None = None) -> dict:
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=seo&category=performance"
    if api_key:
        api_url += f"&key={api_key}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(api_url)
            if response.status_code == 429:
                return {"seo": 0, "performance": 0, "rate_limited": True}
            
            data = response.json()
            categories = data.get("lighthouseResult", {}).get("categories", {})
            seo_score = int(categories.get("seo", {}).get("score", 0) * 100)
            perf_score = int(categories.get("performance", {}).get("score", 0) * 100)
            return {"seo": seo_score, "performance": perf_score, "rate_limited": False}
        except Exception:
            return {"seo": 0, "performance": 0, "rate_limited": False}

async def analyze_with_gemini_vision(screenshot_base64: str, gemini_api_key: str) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    
    prompt = """
    You are an expert AI Search Engine Optimization (AEO/GEO/GLMM) analyzer.
    Look at the provided screenshot of the website. Evaluate its layout, content hierarchy, readability, CTA prominence, and multimodal readiness.
    
    Return a valid JSON object strictly adhering to this format:
    {
        "aeo_score": 85,
        "geo_score": 75,
        "glmm_score": 80,
        "visual_insights": ["Insight 1", "Insight 2", "Insight 3"]
    }
    """
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inlineData": {
                        "mimeType": "image/jpeg",
                        "data": screenshot_base64
                    }
                }
            ]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(url, headers={"Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
            result_json = response.json()
            content_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(content_text)
        except Exception:
            return {"aeo_score": 0, "geo_score": 0, "glmm_score": 0, "visual_insights": []}

async def analyze_with_ollama_vision(screenshot_base64: str) -> dict | None:
    url = "http://localhost:11434/api/generate"
    prompt = """
    You are an expert UI/UX analyzer. Analyze this website screenshot's layout, readability, and visual structure.
    Output ONLY a raw JSON object matching this exact format, with no markdown, no backticks, and no extra text:
    {"aeo_score": 85, "geo_score": 75, "glmm_score": 80, "visual_insights": ["Insight 1"]}
    """
    
    payload = {
        "model": "moondream",
        "prompt": prompt,
        "images": [screenshot_base64],
        "stream": False,
        "format": "json"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result_json = response.json()
            return json.loads(result_json.get("response", "{}"))
        except Exception as e:
            print(f"Ollama vision failed: {e}")
            return None

async def run_visual_audit(url: str, google_api_key_override: str | None = None) -> dict:
    gemini_api_key = os.getenv("AISEO_LLM__GEMINI_API_KEY")
    google_api_key = google_api_key_override or os.getenv("GOOGLE_PAGESPEED_API_KEY")

    # 1. Google SEO
    google_scores = await get_google_pagespeed_score(url, google_api_key)
    
    # 2. Screenshot
    vision_scores = {"aeo_score": 0, "geo_score": 0, "glmm_score": 0, "visual_insights": []}
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            # Use a smaller viewport and disable full_page to drastically save Gemini vision quota
            page = await browser.new_page(viewport={"width": 1024, "height": 768})
            await page.goto(url, wait_until="networkidle", timeout=15000)
            screenshot_bytes = await page.screenshot(type="jpeg", quality=30, full_page=False)
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            await browser.close()
        
        # Try Ollama lightweight model first (100% free local)
        print("Attempting local Ollama vision analysis (moondream)...")
        ollama_scores = await analyze_with_ollama_vision(screenshot_base64)
        
        if ollama_scores:
            vision_scores = ollama_scores
            print("Successfully used Ollama!")
        elif gemini_api_key:
            print("Ollama failed or not installed. Falling back to Gemini Vision...")
            vision_scores = await analyze_with_gemini_vision(screenshot_base64, gemini_api_key)
    except Exception as e:
        print(f"Vision audit failed: {e}")

    return {
        "google_seo": google_scores["seo"],
        "google_perf": google_scores["performance"],
        "visual_aeo": vision_scores.get("aeo_score", 0),
        "visual_geo": vision_scores.get("geo_score", 0),
        "visual_glmm": vision_scores.get("glmm_score", 0),
        "visual_insights": vision_scores.get("visual_insights", [])
    }
