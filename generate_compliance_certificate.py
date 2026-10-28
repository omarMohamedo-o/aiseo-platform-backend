"""Generate high-resolution Executive AISEO / GEO Compliance Certificate (PDF + HTML).

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import asyncio
import os
from playwright.async_api import async_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
HTML_PATH = os.path.join(OUTPUT_DIR, "AISEO_GEO_Compliance_Certificate.html")
PDF_PATH = os.path.join(OUTPUT_DIR, "AISEO_GEO_Compliance_Certificate.pdf")

CERTIFICATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AISEO Platform - GEO Compliance & Brand Grounding Certificate</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {
    size: 1920px 1080px;
    margin: 0;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    width: 1920px;
    height: 1080px;
    background: #030712;
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .cert-frame {
    width: 1840px;
    height: 1000px;
    background: radial-gradient(circle at 50% 30%, #0b1329 0%, #030712 100%);
    border: 3px solid #d97706;
    outline: 16px solid #0f172a;
    box-shadow: 0 0 80px rgba(217, 119, 6, 0.25), inset 0 0 100px rgba(0, 0, 0, 0.8);
    position: relative;
    padding: 50px 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }

  /* Guilloche Corner Accents */
  .corner {
    position: absolute;
    width: 80px;
    height: 80px;
    border: 4px solid #f59e0b;
  }
  .top-left { top: 20px; left: 20px; border-right: none; border-bottom: none; }
  .top-right { top: 20px; right: 20px; border-left: none; border-bottom: none; }
  .bottom-left { bottom: 20px; left: 20px; border-right: none; border-top: none; }
  .bottom-right { bottom: 20px; right: 20px; border-left: none; border-top: none; }

  /* Header */
  .header {
    text-align: center;
    position: relative;
    z-index: 2;
  }
  .brand-logo {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: rgba(217, 119, 6, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.35);
    padding: 8px 24px;
    border-radius: 999px;
    margin-bottom: 16px;
  }
  .brand-logo span {
    font-size: 13px;
    letter-spacing: 4px;
    color: #f59e0b;
    font-weight: 700;
    text-transform: uppercase;
  }
  .cert-title {
    font-family: 'Cinzel', serif;
    font-size: 44px;
    font-weight: 900;
    letter-spacing: 6px;
    background: linear-gradient(135deg, #ffffff 0%, #fef3c7 50%, #f59e0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .cert-subtitle {
    font-size: 14px;
    letter-spacing: 5px;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 500;
  }

  /* Recipient Section */
  .recipient-section {
    text-align: center;
    margin: 20px 0;
    position: relative;
    z-index: 2;
  }
  .presented-to {
    font-size: 14px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 12px;
  }
  .recipient-name {
    font-family: 'Cinzel', serif;
    font-size: 52px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 3px;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  }
  .recipient-domain {
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    color: #38bdf8;
    margin-top: 6px;
    letter-spacing: 2px;
  }

  /* Citations Statement */
  .statement {
    text-align: center;
    max-width: 1200px;
    margin: 0 auto;
    font-size: 15px;
    line-height: 1.7;
    color: #cbd5e1;
    position: relative;
    z-index: 2;
  }
  .statement strong {
    color: #f8fafc;
  }

  /* Pillar Metrics Cards */
  .metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
    position: relative;
    z-index: 2;
  }
  .metric-card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(217, 119, 6, 0.3);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    backdrop-filter: blur(8px);
  }
  .metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 36px;
    font-weight: 700;
    color: #fbbf24;
    margin-bottom: 4px;
  }
  .metric-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #94a3b8;
    font-weight: 600;
  }
  .metric-status {
    font-size: 11px;
    color: #10b981;
    font-weight: 600;
    margin-top: 4px;
  }

  /* Signatures & Seal Footer */
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-top: 20px;
    border-top: 1px solid rgba(217, 119, 6, 0.25);
    position: relative;
    z-index: 2;
  }
  .sig-block {
    text-align: left;
  }
  .sig-title {
    font-size: 13px;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: 1px;
  }
  .sig-role {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 2px;
  }
  .sig-line {
    width: 220px;
    height: 1px;
    background: #475569;
    margin-bottom: 8px;
  }
  .sig-signature {
    font-family: 'Cinzel', serif;
    font-size: 20px;
    color: #f59e0b;
    margin-bottom: 4px;
    font-style: italic;
  }

  /* Gold Seal */
  .seal {
    width: 130px;
    height: 130px;
    border-radius: 50%;
    background: radial-gradient(circle, #f59e0b 0%, #b45309 80%, #78350f 100%);
    border: 4px double #fef3c7;
    box-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #ffffff;
    padding: 10px;
  }
  .seal-text-top {
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
  }
  .seal-star {
    font-size: 22px;
    color: #fef3c7;
    margin: 2px 0;
  }
  .seal-text-bottom {
    font-size: 8px;
    letter-spacing: 1.5px;
    font-weight: 600;
    text-transform: uppercase;
  }

  .meta-block {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #64748b;
    line-height: 1.6;
  }
  .meta-block span {
    color: #cbd5e1;
  }

  /* Watermark */
  .watermark {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-25deg);
    font-family: 'Cinzel', serif;
    font-size: 160px;
    font-weight: 900;
    color: rgba(255, 255, 255, 0.018);
    pointer-events: none;
    text-transform: uppercase;
    letter-spacing: 20px;
    z-index: 1;
    white-space: nowrap;
  }

  .copyright-bar {
    position: absolute;
    bottom: 8px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 10px;
    color: #475569;
    letter-spacing: 1.5px;
  }
</style>
</head>
<body>

<div class="cert-frame">
  <div class="corner top-left"></div>
  <div class="corner top-right"></div>
  <div class="corner bottom-left"></div>
  <div class="corner bottom-right"></div>

  <div class="watermark">AISEO VERIFIED</div>

  <!-- Header -->
  <div class="header">
    <div class="brand-logo">
      <span>AISEO GLOBAL STANDARDS BOARD · ISO/IEC 42001 ALIGNED</span>
    </div>
    <h1 class="cert-title">Certificate of GEO Excellence</h1>
    <p class="cert-subtitle">Generative Engine Optimization & Brand Grounding Credential</p>
  </div>

  <!-- Recipient -->
  <div class="recipient-section">
    <div class="presented-to">This credential is authenticated and awarded to</div>
    <div class="recipient-name">Enterprise Sovereign Domain</div>
    <div class="recipient-domain">https://enterprise-client.com</div>
  </div>

  <!-- Statement -->
  <div class="statement">
    Having successfully completed the multi-engine algorithmic audit across <strong>OpenAI ChatGPT-4o</strong>,
    <strong>Google Gemini 1.5</strong>, <strong>Anthropic Claude 3.5</strong>, and <strong>Perplexity AI</strong>,
    confirming verifiable brand citation presence, machine-readable structured knowledge graph compliance,
    and mathematical resistance against generative AI hallucinations.
  </div>

  <!-- Metrics Grid -->
  <div class="metrics-row">
    <div class="metric-card">
      <div class="metric-value">94.8%</div>
      <div class="metric-label">AI Visibility Index</div>
      <div class="metric-status">Top 1% Tier Worldwide</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">98.2%</div>
      <div class="metric-label">RAG Grounding Ratio</div>
      <div class="metric-status">Zero Critical Hallucinations</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">100%</div>
      <div class="metric-label">Schema.org Depth</div>
      <div class="metric-status">Direct Entity Resolution</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">0.96</div>
      <div class="metric-label">AEO Snippet Concordance</div>
      <div class="metric-status">Direct-Answer Featured</div>
    </div>
  </div>

  <!-- Footer with Signature, Seal, and Verification Digest -->
  <div class="footer">
    <div class="sig-block">
      <div class="sig-signature">Omar Mohamed</div>
      <div class="sig-line"></div>
      <div class="sig-title">Omar Mohamed (@omarMohamedo-o)</div>
      <div class="sig-role">Lead Architect & Chairman, AISEO Global Standards Board</div>
    </div>

    <div class="seal">
      <div class="seal-text-top">Certified</div>
      <div class="seal-star">★</div>
      <div class="seal-text-bottom">Platinum 2026</div>
    </div>

    <div class="meta-block">
      <div>CERTIFICATE ID: <span>GEO-CERT-2026-A87B2E49</span></div>
      <div>DIGEST: <span>SHA256:7F83B1657FF1FC53B92DC18148A1D65DFC2</span></div>
      <div>ISSUE DATE: <span>2026-10-26</span> · EXPIRES: <span>2027-10-26</span></div>
      <div>VALIDATION: <span>https://aiseo-platform.com/verify</span></div>
    </div>
  </div>

  <div class="copyright-bar">
    Copyright © 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved. Proprietary AISEO & GEO Visibility Scoring Architecture.
  </div>
</div>

</body>
</html>
"""


async def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(CERTIFICATE_HTML)
    print(f"Generated HTML certificate at: {HTML_PATH}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(f"file:///{os.path.abspath(HTML_PATH).replace(os.sep, '/')}", wait_until="networkidle")
        await page.pdf(
            path=PDF_PATH,
            width="1920px",
            height="1080px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()

    print(f"Generated PDF certificate at: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")


if __name__ == "__main__":
    asyncio.run(main())

