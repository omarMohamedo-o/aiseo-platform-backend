"""
Script to generate the enterprise AISEO / AEO / GEO Platform Solution Stages & Pipeline PDF deck.
Produces a 16-page widescreen (16:9) executive landscape PDF matching the Infomineo whitepaper style.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def generate_html() -> str:
    # 16 High-Impact Widescreen Executive Presentation Slides
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AISEO / AEO / GEO Platform — Solution Stages & Pipeline</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

@page {
  size: 960px 540px;
  margin: 0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

a {
  text-decoration: none !important;
  color: inherit;
}

html, body {
  margin: 0;
  padding: 0;
  background: #070B14;
  color: #E2E8F0;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

/* Slide Base Setup */
.slide {
  width: 960px;
  height: 540px;
  max-height: 540px;
  min-height: 540px;
  padding: 24px 36px 20px 36px;
  page-break-after: always;
  break-after: page;
  overflow: hidden;
  position: relative;
  background: #070B14;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.slide:last-child {
  page-break-after: avoid !important;
  break-after: avoid !important;
}

/* Slide Header */
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 10px;
  margin-bottom: 14px;
}
.header-left {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.tag-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #38BDF8;
  background: rgba(56, 189, 248, 0.1);
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid rgba(56, 189, 248, 0.25);
  width: fit-content;
}
.tag-badge.emerald {
  color: #34D399;
  background: rgba(52, 211, 153, 0.1);
  border-color: rgba(52, 211, 153, 0.25);
}
.tag-badge.purple {
  color: #C084FC;
  background: rgba(192, 132, 252, 0.1);
  border-color: rgba(192, 132, 252, 0.25);
}
.slide-title {
  font-size: 20px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.3px;
}
.slide-subtitle {
  font-size: 11px;
  color: #94A3B8;
  font-weight: 400;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.pill {
  font-size: 9px;
  font-weight: 600;
  padding: 4px 9px;
  border-radius: 9999px;
  background: #1E293B;
  color: #CBD5E1;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.pill.accent {
  background: linear-gradient(135deg, #0284C7, #0369A1);
  color: #FFFFFF;
  border: none;
}

/* Footer Row */
.footer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 8px;
  font-size: 10px;
  color: #64748B;
  margin-top: auto;
}
.footer-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.footer-brand {
  font-weight: 700;
  color: #94A3B8;
  letter-spacing: 0.5px;
}
.footer-right {
  display: flex;
  align-items: center;
  gap: 14px;
}
.page-number {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #38BDF8;
}

/* Cards & Grid Layouts */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  flex: 1;
}
.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  flex: 1;
}
.card {
  background: #0E1626;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 8px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  position: relative;
}
.card.highlight {
  border-color: rgba(56, 189, 248, 0.3);
  background: linear-gradient(180deg, #111D33 0%, #0E1626 100%);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.card-title {
  font-size: 13px;
  font-weight: 700;
  color: #F8FAFC;
}
.card-badge {
  font-size: 8.5px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
}
.badge-blue { background: rgba(56, 189, 248, 0.15); color: #38BDF8; }
.badge-green { background: rgba(52, 211, 153, 0.15); color: #34D399; }
.badge-purple { background: rgba(192, 132, 252, 0.15); color: #C084FC; }
.badge-amber { background: rgba(251, 191, 36, 0.15); color: #FBBF24; }

.bullet-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 10.5px;
  color: #CBD5E1;
  line-height: 1.4;
}
.bullet-list li {
  position: relative;
  padding-left: 14px;
}
.bullet-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #38BDF8;
  font-weight: bold;
}
.bullet-list.green li::before { color: #34D399; }
.bullet-list.purple li::before { color: #C084FC; }

.tool-tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 8px;
}
.tool-tag {
  background: #172339;
  border: 1px solid rgba(255, 255, 255, 0.09);
  padding: 3px 7px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  font-weight: 500;
  color: #38BDF8;
}

.data-flow-box {
  background: #080D18;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  padding: 8px 10px;
  margin-top: 8px;
  font-size: 9.5px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.data-flow-label {
  font-weight: 700;
  color: #94A3B8;
  text-transform: uppercase;
  font-size: 8px;
  letter-spacing: 0.8px;
}
.data-flow-val {
  color: #F1F5F9;
  font-family: 'JetBrains Mono', monospace;
  word-break: break-all;
}

/* Cover Slide Special Styling */
.cover-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding-right: 80px;
}
.cover-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.3);
  color: #38BDF8;
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 18px;
}
.cover-title {
  font-size: 40px;
  font-weight: 800;
  line-height: 1.1;
  background: linear-gradient(135deg, #FFFFFF 30%, #38BDF8 85%, #818CF8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 14px;
}
.cover-subtitle {
  font-size: 15px;
  color: #94A3B8;
  font-weight: 400;
  line-height: 1.5;
  max-width: 780px;
  margin-bottom: 26px;
}
.cover-stats-row {
  display: flex;
  gap: 20px;
  width: 100%;
}
.cover-stat-box {
  background: #0E1626;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 12px 18px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.cover-stat-num {
  font-size: 18px;
  font-weight: 800;
  color: #38BDF8;
}
.cover-stat-desc {
  font-size: 9.5px;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  font-weight: 600;
}

/* Pipeline Flow Blocks */
.pipeline-flow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 10px;
}
.pipe-step {
  background: #0E1626;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.pipe-step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  font-weight: 700;
  color: #38BDF8;
}
.pipe-step-title {
  font-size: 11px;
  font-weight: 700;
  color: #FFFFFF;
}
.pipe-step-desc {
  font-size: 9px;
  color: #94A3B8;
  line-height: 1.3;
}
.pipe-step-tools {
  font-size: 8px;
  color: #34D399;
  font-family: 'JetBrains Mono', monospace;
  margin-top: 2px;
}

/* Master Table Layout */
.tech-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9.5px;
  margin-top: 4px;
}
.tech-table th {
  background: #111D33;
  color: #94A3B8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  font-size: 8px;
  padding: 6px 10px;
  text-align: left;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.tech-table td {
  padding: 5.5px 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  color: #CBD5E1;
  background: #0B111E;
}
.tech-table tr:nth-child(even) td {
  background: #0E1626;
}
.tech-name {
  font-weight: 700;
  color: #38BDF8;
  font-family: 'JetBrains Mono', monospace;
}
.tech-category {
  font-weight: 600;
  color: #A78BFA;
}
</style>
</head>
<body>

<!-- SLIDE 1: COVER -->
<div class="slide">
  <div class="header-row" style="border-bottom: none; margin-bottom: 0;">
    <div class="header-left">
      <span class="tag-badge">AISEO SOLUTION BLUEPRINT • 2026</span>
    </div>
    <div class="header-right">
      <span class="pill accent">Clean Architecture</span>
      <span class="pill">FastAPI • MLflow • ONNX</span>
    </div>
  </div>

  <div class="cover-container">
    <div class="cover-badge">⚡ Enterprise AI Visibility Intelligence Platform</div>
    <h1 class="cover-title">AISEO / AEO / GEO Platform</h1>
    <p class="cover-subtitle">
      A comprehensive technical blueprint of our search visibility intelligence architecture:
      deconstructing all 10 core execution stages, deep technical mechanics, tool selections,
      and the end-to-end data pipeline that propels enterprise brands into definitive generative AI citations.
    </p>

    <div class="cover-stats-row">
      <div class="cover-stat-box">
        <div class="cover-stat-num">10 Stages</div>
        <div class="cover-stat-desc">End-to-End Pipeline</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">SEO • AEO • GEO</div>
        <div class="cover-stat-desc">Unified Visibility Scope</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">&lt; 15 ms</div>
        <div class="cover-stat-desc">ONNX Serving Latency</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">Hexagonal</div>
        <div class="cover-stat-desc">Decoupled Architecture</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Enterprise Generative Search Engine Optimization Series</span>
    </div>
    <div class="footer-right">
      <span>Confidential & Proprietary</span>
      <span class="page-number">01 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 2: THE 3 PILLARS (SEO vs AEO vs GEO) -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STRATEGIC PARADIGM</span>
      <div class="slide-title">The Three Pillars of Search Visibility</div>
      <div class="slide-subtitle">The fundamental paradigm shift from legacy 10-blue-links to generative AI synthesis and citations</div>
    </div>
    <div class="header-right">
      <span class="pill">Market Analysis</span>
      <span class="pill accent">Zero-Click AI Shift</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Pillar 1: SEO -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. SEO (Search Engines)</div>
        <span class="card-badge badge-blue">Traditional</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Primary Target:</strong> Google SERP, Microsoft Bing crawler index.</li>
        <li><strong>Core Mechanism:</strong> Crawls raw HTML, analyzes keyword density, H1/title tags, domain authority, and backlink graphs.</li>
        <li><strong>User Experience:</strong> User scrolls through 10 blue links, manually clicks domains, and navigates web pages.</li>
        <li><strong>Critical Vulnerability:</strong> Over 65% of searches now result in zero clicks as AI synthesizes the answer directly.</li>
      </ul>
      <div class="data-flow-box">
        <span class="data-flow-label">Key Metric</span>
        <span class="data-flow-val">SERP Rank Position #1 - #10 • CTR %</span>
      </div>
    </div>

    <!-- Pillar 2: AEO -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. AEO (Answer Engines)</div>
        <span class="card-badge badge-green">Direct Answers</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Primary Target:</strong> Google Featured Snippets, Voice Search (Siri, Alexa, Google Assistant).</li>
        <li><strong>Core Mechanism:</strong> Identifies direct, concise 40–60 word answer blocks, schema.org FAQ markup, and definition tables.</li>
        <li><strong>User Experience:</strong> Delivers single definitive answer instantly without requiring the user to navigate to the website.</li>
        <li><strong>Optimization Focus:</strong> Question-to-answer formatting, bulleted lists, and high factual information density.</li>
      </ul>
      <div class="data-flow-box">
        <span class="data-flow-label">Key Metric</span>
        <span class="data-flow-val">Snippet Capture % • Voice Readout Rate</span>
      </div>
    </div>

    <!-- Pillar 3: GEO -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. GEO (Generative Engines)</div>
        <span class="card-badge badge-purple">The New Frontier</span>
      </div>
      <ul class="bullet-list purple">
        <li><strong>Primary Target:</strong> ChatGPT (OpenAI), Google Gemini, Claude, Perplexity AI, and SearchGPT.</li>
        <li><strong>Core Mechanism:</strong> RAG retrieval, entity-relationship graphs, statistical authority, and citation readiness.</li>
        <li><strong>The Core Question:</strong> <em>"When an enterprise buyer asks an AI engine for a solution, does the model recommend and cite your brand?"</em></li>
        <li><strong>Platform Mission:</strong> Ensure your domain is the ground-truth cited source for generative responses.</li>
      </ul>
      <div class="data-flow-box" style="border-color: rgba(192, 132, 252, 0.3);">
        <span class="data-flow-label">Key Metric</span>
        <span class="data-flow-val" style="color: #C084FC;">Brand Mention Rate • Domain Citation URLs</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Section 1: Market & Strategic Foundation</span>
    </div>
    <div class="footer-right">
      <span>Confidential</span>
      <span class="page-number">02 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 3: MASTER PIPELINE ARCHITECTURE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">SYSTEM ARCHITECTURE</span>
      <div class="slide-title">Unified End-to-End Pipeline Blueprint</div>
      <div class="slide-subtitle">How a tenant URL flows through our decoupled 10-stage Clean Hexagonal Architecture</div>
    </div>
    <div class="header-right">
      <span class="pill">Hexagonal Architecture</span>
      <span class="pill accent">Ports & Adapters</span>
    </div>
  </div>

  <div class="pipeline-flow">
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 01</div>
      <div class="pipe-step-title">Ingest & Vault</div>
      <div class="pipe-step-desc">Tenant isolation, URL validation, and AES-256 encrypted provider keys.</div>
      <div class="pipe-step-tools">FastAPI • Pydantic • Fernet</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 02</div>
      <div class="pipe-step-title">Crawl & Traversal</div>
      <div class="pipe-step-desc">Sitemap discovery, robots.txt rules, and BFS link exploration.</div>
      <div class="pipe-step-tools">HTTPX • Playwright • BS4</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 03</div>
      <div class="pipe-step-title">Scrape & Structure</div>
      <div class="pipe-step-desc">Boilerplate noise removal, JSON-LD schema, and H1-H3 hierarchy.</div>
      <div class="pipe-step-tools">Trafilatura • lxml • HTML5</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 04</div>
      <div class="pipe-step-title">Chunk & Vectorize</div>
      <div class="pipe-step-desc">Recursive 800-token splitting and dense vector database indexing.</div>
      <div class="pipe-step-tools">OpenAI • pgvector • PostgreSQL</div>
    </div>
  </div>

  <div class="pipeline-flow">
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 05</div>
      <div class="pipe-step-title">ML Intent Serving</div>
      <div class="pipe-step-desc">Sub-10ms query intent categorization and technical signal evaluation.</div>
      <div class="pipe-step-tools">ONNX Runtime • MLflow • Scikit</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 06</div>
      <div class="pipe-step-title">Prompt & Question Lab</div>
      <div class="pipe-step-desc">Synthesizing multi-lens buyer persona queries (Awareness, Comparison).</div>
      <div class="pipe-step-tools">GPT-4o • Gemini 1.5 • Claude</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 07</div>
      <div class="pipe-step-title">Multi-Model Audit</div>
      <div class="pipe-step-desc">Parallel matrix execution across ChatGPT, Gemini, Claude & Perplexity.</div>
      <div class="pipe-step-tools">Async Matrix • Tenacity Retry</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 08</div>
      <div class="pipe-step-title">Score & Recommend</div>
      <div class="pipe-step-desc">Deterministic 0-100 GEO score, competitor gaps & automated report digest.</div>
      <div class="pipe-step-tools">Scorer • Celery • EmailPort</div>
    </div>
  </div>

  <div class="card" style="padding: 10px 14px; background: rgba(56, 189, 248, 0.05); border-color: rgba(56, 189, 248, 0.2);">
    <div style="font-size: 10.5px; color: #CBD5E1; line-height: 1.4;">
      <strong style="color: #38BDF8;">Architectural Guarantee:</strong> Domain logic remains completely decoupled from third-party vendor SDKs. Every external technology (OpenAI, Gemini, ONNX, PostgreSQL) is accessed exclusively through abstract <em>Ports</em> implemented by swappable <em>Adapters</em>.
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Section 2: System Architecture</span>
    </div>
    <div class="footer-right">
      <span>Pipeline v2.4</span>
      <span class="page-number">03 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 4: STAGE 01 - CRAWLING & DISCOVERY -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 01</span>
      <div class="slide-title">Domain Discovery & Intelligent Crawling</div>
      <div class="slide-subtitle">Autonomous topology discovery, link traversal, sitemap parsing, and robots compliance</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/crawler</span>
      <span class="pill accent">HttpxCrawler</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Mechanics & Logic</div>
        <span class="card-badge badge-blue">Discovery Engine</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Breadth-First Exploration:</strong> Concurrently maps internal links constrained strictly to target domain netloc.</li>
        <li><strong>Robots.txt & Sitemap Introspection:</strong> Fetches `/robots.txt` and `/sitemap.xml` in parallel to verify indexing rules and discover hidden deep URLs.</li>
        <li><strong>URL Sanitization:</strong> Normalizes paths, eliminates trailing slashes, strips tracking parameters (`utm_*`, `fbclid`), and prevents cycle traps.</li>
        <li><strong>JavaScript Hydration Fallback:</strong> Automatically delegates client-rendered Single Page Applications to headless browser sessions.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>HTTPX:</strong> Async HTTP/2 client enabling asynchronous I/O and connection pooling for 100+ concurrent requests.</li>
        <li><strong>Playwright:</strong> Headless Chromium runtime executing dynamic JavaScript (React, Next.js, Vue) that standard HTTP scrapers miss.</li>
        <li><strong>BeautifulSoup4:</strong> C-accelerated DOM anchor extraction (<code>&lt;a href&gt;</code>) with tolerant parsing for malformed web pages.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">httpx</span>
        <span class="tool-tag">playwright</span>
        <span class="tool-tag">beautifulsoup4</span>
        <span class="tool-tag">asyncio</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Input Parameters</span>
        <span class="data-flow-val">Url("https://example.com"), max_pages=100</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Contract</span>
        <span class="data-flow-val">list[Url], has_sitemap: bool, has_robots: bool</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Observed Throughput</span>
        <span class="data-flow-val">50 pages / 2.8 sec • Concurrency Semaphore: 6</span>
      </div>
      <ul class="bullet-list" style="margin-top: 8px;">
        <li>Guarantees strict tenant isolation; crawl manifests persist in history with execution timestamps.</li>
      </ul>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 01: Crawling & Topology Discovery</span>
    </div>
    <div class="footer-right">
      <span>CrawlerPort</span>
      <span class="page-number">04 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 5: STAGE 02 - BOILERPLATE REMOVAL & EXTRACTION -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 02</span>
      <div class="slide-title">Boilerplate Stripping & Clean Content Extraction</div>
      <div class="slide-subtitle">Purifying raw HTML into structured, high-signal semantic DOM trees for AI comprehension</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/scraper</span>
      <span class="pill accent">TrafilaturaScraper</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Mechanics & Logic</div>
        <span class="card-badge badge-blue">Text Purification</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Noise Elimination:</strong> Discards 60–75% of raw page weight by stripping navbars, footers, cookie banners, tracking tags, CSS, and ads.</li>
        <li><strong>Semantic Node Preservation:</strong> Preserves core headings (H1-H6), article paragraphs, bulleted lists, comparison tables, and blockquotes.</li>
        <li><strong>Metadata & Entity Extraction:</strong> Extracts JSON-LD Schema.org blocks, OpenGraph tags, meta titles, descriptions, and language codes.</li>
        <li><strong>Heading Hierarchy Tree:</strong> Constructs a nested outline of the document to evaluate logical topical depth.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Trafilatura:</strong> Industry-standard Python web scraper recognized for state-of-the-art precision in article body extraction.</li>
        <li><strong>lxml:</strong> Lightning-fast C parser providing native XPath and tree traversal with minimal memory footprint.</li>
        <li><strong>BeautifulSoup4:</strong> Specialized extraction for JSON-LD schema blocks, OpenGraph metadata, and structured microdata.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">trafilatura</span>
        <span class="tool-tag">lxml</span>
        <span class="tool-tag">beautifulsoup4</span>
        <span class="tool-tag">json-ld</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Input</span>
        <span class="data-flow-val">Raw HTML response stream from Stage 01</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Aggregate (StructuredContent)</span>
        <span class="data-flow-val">{ title, raw_text, headings: list[str], language, json_ld_schemas, characters_count }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Context Efficiency</span>
        <span class="data-flow-val">Payload reduction: ~68% • Zero hallucinations</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 02: Content Extraction & Structuring</span>
    </div>
    <div class="footer-right">
      <span>ScraperPort</span>
      <span class="page-number">05 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 6: STAGE 03 - CHUNKING & VECTOR STORAGE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 03</span>
      <div class="slide-title">Semantic Chunking & Vector Storage</div>
      <div class="slide-subtitle">Hierarchical semantic splitting and high-dimensional vector embeddings for similarity search</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/semantic</span>
      <span class="pill accent">PostgreSQL + pgvector</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Mechanics & Logic</div>
        <span class="card-badge badge-blue">Chunking Geometry</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Grammatical Boundary Splitting:</strong> Replaces naive character slicing with recursive splits on paragraphs (`\n\n`), sentences (`. `), and words.</li>
        <li><strong>Contextual Windowing:</strong> 800-token target chunk size with a 120-token sliding overlap window to preserve cross-sentence reasoning.</li>
        <li><strong>Embedding Generation:</strong> Transforms each clean chunk into a 1536-dimensional or 384-dimensional dense semantic vector.</li>
        <li><strong>HNSW Vector Indexing:</strong> Enables sub-millisecond approximate nearest neighbor (ANN) retrieval with cosine distance.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>RecursiveCharacterChunker:</strong> Custom domain chunker enforcing semantic coherence without truncating key business claims.</li>
        <li><strong>OpenAI text-embedding-3-small:</strong> High-density, cost-effective embeddings optimized for enterprise RAG retrieval.</li>
        <li><strong>Sentence-Transformers (bge-small):</strong> Open-source offline embedding adapter for air-gapped deployments.</li>
        <li><strong>PostgreSQL + pgvector:</strong> Eliminates external vector DB overhead by unifying relational metadata and vectors in one database.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">pgvector</span>
        <span class="tool-tag">text-embedding-3</span>
        <span class="tool-tag">postgresql</span>
        <span class="tool-tag">hnsw</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Input</span>
        <span class="data-flow-val">StructuredContent from Stage 02</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Schema</span>
        <span class="data-flow-val">list[Chunk]: { id, page_id, chunk_index, text, embedding: vector(1536) }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Retrieval Capability</span>
        <span class="data-flow-val">Semantic cosine similarity • Semantic deduplication</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 03: Semantic Chunking & Vector DB</span>
    </div>
    <div class="footer-right">
      <span>VectorStorePort</span>
      <span class="page-number">06 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 7: STAGE 04 - ML MODEL SERVING & INTENT -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 04</span>
      <div class="slide-title">ML Inference & Intent Classification</div>
      <div class="slide-subtitle">Sub-millisecond intent categorization via ONNX Runtime and MLflow MLOps lifecycle tracking</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/ml</span>
      <span class="pill accent">OnnxModelProvider</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Mechanics & Logic</div>
        <span class="card-badge badge-blue">Inference Engine</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Microsecond Latency:</strong> Replaces expensive 2-second LLM calls with optimized local neural and classical classifiers.</li>
        <li><strong>Intent Taxonomy:</strong> Classifies user search queries and page sections into 4 categories: <em>Commercial, Informational, Navigational, Transactional</em>.</li>
        <li><strong>Offline-to-Online Architecture:</strong> Models trained offline in MLflow, exported to `.onnx` binaries, and loaded strictly at runtime.</li>
        <li><strong>Deterministic Confidence Scores:</strong> Provides calibrated probability distribution across intent classes for explainability.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>ONNX Runtime:</strong> High-performance, cross-platform inference engine with CPU SIMD optimizations, achieving &lt; 5ms latency.</li>
        <li><strong>MLflow:</strong> Complete machine learning lifecycle tracking: hyperparameter sweeps, metric logging, and Model Registry artifact storage.</li>
        <li><strong>Scikit-Learn:</strong> Fast TF-IDF token vectorization and statistical classification pipelines.</li>
        <li><strong>OpenCV (Headless):</strong> Image layout parsing for visual layout signals without GUI dependencies.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">onnxruntime</span>
        <span class="tool-tag">mlflow</span>
        <span class="tool-tag">scikit-learn</span>
        <span class="tool-tag">opencv-headless</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Model Artifact</span>
        <span class="data-flow-val">models/intent_classifier_v1.onnx</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Prediction Contract</span>
        <span class="data-flow-val">Prediction(label="Commercial", confidence=0.962, latency_ms=3.4)</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Economic Advantage</span>
        <span class="data-flow-val">99.2% cost reduction vs invoking external LLM</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 04: Classical ML & Intent Serving</span>
    </div>
    <div class="footer-right">
      <span>ModelProviderPort</span>
      <span class="page-number">07 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 8: STAGE 05 - SYNTHETIC QUESTION LAB -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 05</span>
      <div class="slide-title">Synthetic Buyer Persona & Question Lab</div>
      <div class="slide-subtitle">Synthesizing multi-lens queries reflecting how real enterprise buyers query generative AI engines</div>
    </div>
    <div class="header-right">
      <span class="pill">application/analysis</span>
      <span class="pill accent">QuestionGenerator</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Mechanics & Logic</div>
        <span class="card-badge badge-blue">Query Synthesis</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Conversational Query Modeling:</strong> Enterprise buyers no longer type simple keywords; they formulate detailed, multi-step prompts.</li>
        <li><strong>Multi-Lens Prompt Generation:</strong> Synthesizes query sets through 4 distinct strategic buyer lenses:
          <br>• <em>Awareness:</em> "What are the top enterprise analytics platforms?"
          <br>• <em>Comparison:</em> "ExampleCorp vs CompetitorX pricing and security."
          <br>• <em>Technical AEO:</em> "Does ExampleCorp support SOC2 and custom APIs?"
          <br>• <em>Commercial:</em> "Best customer intelligence tool for banks."
        </li>
        <li><strong>Schema Enforcement:</strong> Pydantic models guarantee deduplicated, strictly typed question batches.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>QuestionGeneratorService:</strong> Orchestrates domain prompt construction and deduplication.</li>
        <li><strong>OpenAI GPT-4o:</strong> Primary high-reasoning query synthesizer with JSON mode for structured schema adherence.</li>
        <li><strong>Google Gemini 1.5 Flash:</strong> Secondary multi-lingual query generator offering diverse phrasing and natural buyer variance.</li>
        <li><strong>Pydantic v2:</strong> Validates `QuestionSet` models and enforces min/max length constraints.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">gpt-4o</span>
        <span class="tool-tag">gemini-1.5</span>
        <span class="tool-tag">pydantic-v2</span>
        <span class="tool-tag">prompt-lab</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Input</span>
        <span class="data-flow-val">{ topic, keywords: list[str], lens: "geo", count: 10, language: "en" }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Contract</span>
        <span class="data-flow-val">QuestionSet: { topic, questions: list[QuestionItem] }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Coverage Diversity</span>
        <span class="data-flow-val">100% unique intents • 0% keyword repetition</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 05: Synthetic Buyer Persona Lab</span>
    </div>
    <div class="footer-right">
      <span>IntelligencePort</span>
      <span class="page-number">08 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 9: STAGE 06 - MULTI-MODEL AI VISIBILITY MATRIX -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 06</span>
      <div class="slide-title">Multi-Model AI Visibility Execution Matrix</div>
      <div class="slide-subtitle">Live concurrent querying across ChatGPT, Gemini, Claude, and Perplexity with fault tolerance</div>
    </div>
    <div class="header-right">
      <span class="pill">application/analysis</span>
      <span class="pill accent">PromptExecutor</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Mechanics & Logic</div>
        <span class="card-badge badge-blue">Matrix Dispatch</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Cross-Ecosystem Audit:</strong> Concurrently tests brand presence across 4 major generative AI search engines.</li>
        <li><strong>Parallel Matrix Dispatch:</strong> Executes `[Questions] × [Providers]` asynchronously, minimizing overall audit duration.</li>
        <li><strong>Deterministic Resilience:</strong> Built-in circuit breakers, exponential backoff, and mock fallback handlers if external vendor APIs fail.</li>
        <li><strong>Error Normalization:</strong> Maps vendor rate limits and timeouts into unified `ProviderRateLimitError` and `ProviderTimeoutError`.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Providers & Adapters</div>
        <span class="card-badge badge-green">Supported Engines</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>OpenAI (GPT-4o):</strong> Simulates ChatGPT Plus & SearchGPT answer synthesis behavior.</li>
        <li><strong>Google Gemini (Gemini 1.5):</strong> Evaluates visibility in Google AI Overviews and Gemini conversational search.</li>
        <li><strong>Anthropic Claude:</strong> Provides an independent analytical baseline for neutral brand perception.</li>
        <li><strong>Perplexity AI (Sonar):</strong> Direct web-grounded live search testing with source link verification.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">openai</span>
        <span class="tool-tag">gemini</span>
        <span class="tool-tag">claude</span>
        <span class="tool-tag">perplexity</span>
        <span class="tool-tag">tenacity</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Request Payload</span>
        <span class="data-flow-val">{ providers: ["openai", "gemini"], questions: [...] }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Execution Response</span>
        <span class="data-flow-val">list[ProviderExecutionResult]: { provider, question, raw_response, latency_ms }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Resilience SLA</span>
        <span class="data-flow-val">100% uptime with graceful degradation</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 06: Multi-Model AI Execution Matrix</span>
    </div>
    <div class="footer-right">
      <span>LlmProviderPort</span>
      <span class="page-number">09 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 10: STAGE 07 - ANSWER AUDITING & CITATION EXTRACTION -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 07</span>
      <div class="slide-title">Answer Auditing, Citations & Competitor Intelligence</div>
      <div class="slide-subtitle">Deconstructing generative responses into brand mention, sentiment, citations, and competitor share</div>
    </div>
    <div class="header-right">
      <span class="pill">application/analysis</span>
      <span class="pill accent">AnswerAnalyzer</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Mechanics & Logic</div>
        <span class="card-badge badge-blue">Citation Auditing</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Brand Mention Extraction:</strong> Performs exact and fuzzy named entity matching to detect if the brand is acknowledged in answers.</li>
        <li><strong>Citation URL Parsing:</strong> Extracts inline markdown URLs, footnotes, and grounded search references pointing back to the website.</li>
        <li><strong>Sentiment & Tone Classification:</strong> Evaluates context surrounding brand mentions: <em>Positive, Neutral, or Negative</em>.</li>
        <li><strong>Competitor Infiltration:</strong> Detects rival companies mentioned in the same answer and calculates relative share-of-voice.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>AnswerAnalyzerService:</strong> High-speed parsing engine processing multi-model responses into structured metrics.</li>
        <li><strong>spaCy (en_core_web_sm):</strong> Industrial-strength NLP library executing Named Entity Recognition (NER) for organizations.</li>
        <li><strong>CompetitorDiscoveryService:</strong> Identifies competitive overlap and missing content areas cited by AI engines.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">spacy-ner</span>
        <span class="tool-tag">regex-url-parser</span>
        <span class="tool-tag">sentiment-engine</span>
        <span class="tool-tag">competitor-discovery</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Input</span>
        <span class="data-flow-val">brand: "ExampleCorp", items: list[ExecutionResult]</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output (AnswerAnalysisResult)</span>
        <span class="data-flow-val">{ brand_mentioned: bool, sentiment: "positive", extracted_citations: ["https://..."], competitors: [...] }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Business Value</span>
        <span class="data-flow-val">Proves exact ROI of generative visibility</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 07: Answer Auditing & Citation Parsing</span>
    </div>
    <div class="footer-right">
      <span>GeoAuditPort</span>
      <span class="page-number">10 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 11: STAGE 08 - UNIFIED GEO SCORING -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 08</span>
      <div class="slide-title">Unified GEO Visibility & Opportunity Scoring</div>
      <div class="slide-subtitle">Deterministic, mathematical, and explainable 0–100 visibility scores across 6 distinct sub-pillars</div>
    </div>
    <div class="header-right">
      <span class="pill">domain/scoring</span>
      <span class="pill accent">OpportunityScorer</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. The 6 Sub-Pillars</div>
        <span class="card-badge badge-blue">Weighted Formula</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Content Clarity (20%):</strong> Flesch-Kincaid readability, heading structure, and absence of marketing fluff.</li>
        <li><strong>Entity Coverage (20%):</strong> Depth of products, pricing, features, and target audience definitions.</li>
        <li><strong>AI Visibility (20%):</strong> Brand mention rate across multi-model query matrix.</li>
        <li><strong>Citation Readiness (15%):</strong> Presence of verifiable statistics, data tables, and FAQ schemas.</li>
        <li><strong>Competitive Share (15%):</strong> Brand dominance vs competitors in recommendation lists.</li>
        <li><strong>Technical SEO (10%):</strong> Robots.txt, sitemaps, canonicals, and SSL signals.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>OpportunityScorerService:</strong> Core domain calculation engine computing deterministic 0-100 scores.</li>
        <li><strong>technical_signals.py:</strong> Automated validator for title tag length, H1-H3 depth, schema markup, and robots.txt.</li>
        <li><strong>visual_scorer.py:</strong> Playwright + Multimodal Vision analysis evaluating layout clarity and mobile readiness.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">opportunity-scorer</span>
        <span class="tool-tag">technical-signals</span>
        <span class="tool-tag">visual-audit</span>
        <span class="tool-tag">radar-metrics</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Calculated Scores</span>
        <span class="data-flow-val">overall_visibility_score: 78 / 100<br>overall_opportunity_score: 82 / 100</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Pillar Breakdown (Example)</span>
        <span class="data-flow-val">Clarity: 88 | Entities: 79 | AI Visibility: 71<br>Citations: 63 | Competitors: 68 | Tech: 84</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Explainability</span>
        <span class="data-flow-val">100% deterministic • Zero black-box metrics</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 08: Unified Visibility Scoring</span>
    </div>
    <div class="footer-right">
      <span>ScoringPort</span>
      <span class="page-number">11 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 12: STAGE 09 - STRATEGIC RECOMMENDATIONS ENGINE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 09</span>
      <div class="slide-title">Prioritized Strategic Recommendations Engine</div>
      <div class="slide-subtitle">Translating diagnostic data into high-ROI engineering tasks and actionable content improvements</div>
    </div>
    <div class="header-right">
      <span class="pill">application/analysis</span>
      <span class="pill accent">RecommendationGenerator</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Prioritization Matrix</div>
        <span class="card-badge badge-blue">Impact vs Effort</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Quick Wins (Low Effort, High Impact):</strong> Implement missing FAQ JSON-LD schema; inject target keywords into H1 tags; unblock AI web crawlers (GPTBot, PerplexityBot) in robots.txt.</li>
        <li><strong>Content Architecture (Medium Effort, High Impact):</strong> Create dedicated "Brand vs Competitor" comparison tables; construct transparent pricing breakdown tiers.</li>
        <li><strong>Authority Building (High Effort, High Impact):</strong> Publish proprietary research studies; secure authoritative external citations; link entity graphs.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>RecommendationGeneratorService:</strong> Rule-based and LLM-assisted action planning engine.</li>
        <li><strong>Contextual Gap Analyzer:</strong> Cross-references discovered competitor citations to pinpoint exact unaddressed buyer questions.</li>
        <li><strong>Pydantic Action Models:</strong> Categorizes each recommendation with category, impact level, and specific implementation checklists.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">recommendation-engine</span>
        <span class="tool-tag">schema-generator</span>
        <span class="tool-tag">gap-analyzer</span>
        <span class="tool-tag">impact-matrix</span>
      </div>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Actionable Deliverables</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Aggregate</span>
        <span class="data-flow-val">list[AuditRecommendation]: { category: "Schema", impact: "High", title: "Missing FAQ Markup", action_items: [...] }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Engineering Ready</span>
        <span class="data-flow-val">Includes copy-paste JSON-LD Schema code & meta tag rewrites</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 09: Strategic Action Generation</span>
    </div>
    <div class="footer-right">
      <span>RecommendationPort</span>
      <span class="page-number">12 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 13: STAGE 10 - VAULT & AUTOMATED SCHEDULING -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 10</span>
      <div class="slide-title">Enterprise Tenant Vault & Automated Scheduled Reports</div>
      <div class="slide-subtitle">Multi-tenant cryptographic security, white-label PDF generation, and automated cron email digests</div>
    </div>
    <div class="header-right">
      <span class="pill">infrastructure/vault</span>
      <span class="pill accent">ReportGenerator</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Tenant Security Vault</div>
        <span class="card-badge badge-blue">Cryptographic Security</span>
      </div>
      <ul class="bullet-list">
        <li><strong>AES-256 Key Encryption:</strong> Client-provided API keys (OpenAI, Gemini, Serper) are encrypted using authenticated symmetric encryption (`Fernet`).</li>
        <li><strong>Tenant Isolation:</strong> Enforces tenant isolation on all vault queries via mandatory `X-Tenant-Id` header.</li>
        <li><strong>Zero Leakage:</strong> Raw credentials never hit application logs; masked in all API responses (`sk-proj-****`).</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. White-Label Branding</div>
        <span class="card-badge badge-green">Enterprise Customization</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Custom Agency Styling:</strong> Injects client logo, custom hex accent colors, corporate header, and confidential footer disclaimers.</li>
        <li><strong>Multi-Tone Summaries:</strong> Generates tailored narrative reports for 3 distinct executive personas:
          <br>• <em>Executive:</em> High-level ROI and market share.
          <br>• <em>Technical:</em> Schema, indexation, and signals.
          <br>• <em>Content-Strategy:</em> Comparison themes and topics.
        </li>
      </ul>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Automated Schedules</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <ul class="bullet-list purple">
        <li><strong>Cron Schedule Engine:</strong> Automated weekly or monthly scans (`0 9 * * 1`) executing end-to-end audits.</li>
        <li><strong>EmailPort & EmailAdapter:</strong> Asynchronous dispatch of branded PDF reports directly to stakeholder inboxes.</li>
      </ul>
      <div class="data-flow-box">
        <span class="data-flow-label">Schedule Contract</span>
        <span class="data-flow-val">{ name: "Monday Executive Digest", cron: "0 9 * * 1", recipient: "leadership@example.com" }</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Stage 10: Enterprise Vault & Delivery</span>
    </div>
    <div class="footer-right">
      <span>Vault & Delivery</span>
      <span class="page-number">13 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 14: MASTER TECHNOLOGY MATRIX -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">TECHNOLOGY MASTER MATRIX</span>
      <div class="slide-title">Complete Technology Stack & Architectural Rationale</div>
      <div class="slide-subtitle">Comprehensive breakdown of all tools, frameworks, and why each was architecturally chosen</div>
    </div>
    <div class="header-right">
      <span class="pill">Tech Stack Audit</span>
      <span class="pill accent">Production Verified</span>
    </div>
  </div>

  <table class="tech-table">
    <thead>
      <tr>
        <th style="width: 14%;">Layer</th>
        <th style="width: 20%;">Technology</th>
        <th style="width: 26%;">Primary Responsibility</th>
        <th style="width: 40%;">Architectural Justification</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="tech-category">Package Mgr</td>
        <td class="tech-name">uv (Rust)</td>
        <td>Dependency resolution & lockfiles</td>
        <td>100x faster than pip/poetry; creates deterministic virtual environments in milliseconds via uv.lock.</td>
      </tr>
      <tr>
        <td class="tech-category">Backend API</td>
        <td class="tech-name">FastAPI + Uvicorn</td>
        <td>Async REST endpoints & dependency DI</td>
        <td>High-throughput async/await, native OpenAPI/Swagger docs, and Pydantic request validation.</td>
      </tr>
      <tr>
        <td class="tech-category">Web Crawler</td>
        <td class="tech-name">HTTPX & Playwright</td>
        <td>High-concurrency link discovery & SPAs</td>
        <td>HTTPX handles high-speed async HTTP/2; Playwright handles dynamic JavaScript execution for client-side apps.</td>
      </tr>
      <tr>
        <td class="tech-category">Text Extraction</td>
        <td class="tech-name">Trafilatura & lxml</td>
        <td>Noise & boilerplate stripping</td>
        <td>Gold-standard precision in removing headers/footers/ads; isolates core article text with zero hallucinations.</td>
      </tr>
      <tr>
        <td class="tech-category">Vector DB</td>
        <td class="tech-name">PostgreSQL + pgvector</td>
        <td>Relational & vector embedding storage</td>
        <td>Unifies transactional tenant data and HNSW vector similarity search in a single database without extra vector DBs.</td>
      </tr>
      <tr>
        <td class="tech-category">ML Inference</td>
        <td class="tech-name">ONNX Runtime</td>
        <td>Sub-5ms query intent classification</td>
        <td>Decouples ML serving from heavy training frameworks; runs high-throughput inference on CPU with minimal memory.</td>
      </tr>
      <tr>
        <td class="tech-category">MLOps</td>
        <td class="tech-name">MLflow</td>
        <td>Experiment tracking & Model Registry</td>
        <td>Versioned datasets, hyperparameter sweeps, metric comparison, and verified model artifact staging.</td>
      </tr>
      <tr>
        <td class="tech-category">LLM Providers</td>
        <td class="tech-name">OpenAI, Gemini, Claude</td>
        <td>Synthetic prompt lab & visibility audit</td>
        <td>Multi-provider diversity prevents vendor lock-in; swappable via clean Hexagonal LlmProvider port interfaces.</td>
      </tr>
      <tr>
        <td class="tech-category">Security</td>
        <td class="tech-name">Fernet (AES-256)</td>
        <td>Multi-tenant encrypted API credential vault</td>
        <td>Guarantees cryptographic key isolation per tenant organization; zero leakage in application logs.</td>
      </tr>
    </tbody>
  </table>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Section 3: Technology Architecture</span>
    </div>
    <div class="footer-right">
      <span>Production Stack</span>
      <span class="page-number">14 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 15: CHALLENGES & RISK MITIGATION -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge purple">RISK MANAGEMENT</span>
      <div class="slide-title">Engineering Challenges & Production Mitigations</div>
      <div class="slide-subtitle">Overcoming non-determinism, anti-bot protections, rate limits, and multi-tenant security</div>
    </div>
    <div class="header-right">
      <span class="pill">SLA & Resilience</span>
      <span class="pill accent">Enterprise Ready</span>
    </div>
  </div>

  <div class="grid-2">
    <!-- Challenge 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. LLM Hallucinations & Non-Determinism</div>
        <span class="card-badge badge-amber">Reliability</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> Commercial LLMs can produce varied answers across runs or hallucinate citations that do not exist.</li>
        <li><strong>Platform Mitigation:</strong>
          <br>• Temperature locked to `0.2` for evaluation queries.
          <br>• Multi-run prompt matrix averaging across independent providers.
          <br>• Regex verification validating that extracted citation URLs resolve to live, crawled domain pages.
        </li>
      </ul>
    </div>

    <!-- Challenge 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Dynamic SPAs & Anti-Bot Protections</div>
        <span class="card-badge badge-amber">Extraction</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> React, Next.js, and Cloudflare-protected sites return empty HTML shells to basic HTTP crawlers.</li>
        <li><strong>Platform Mitigation:</strong>
          <br>• Automatic fallback from HTTPX to Playwright headless Chromium when hydration markers are detected.
          <br>• Realistic browser header rotations (User-Agent, Accept-Language, Sec-CH-UA).
          <br>• Domain-polite rate limiting and exponential backoff.
        </li>
      </ul>
    </div>

    <!-- Challenge 3 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">3. Vendor API Rate Limits & Cost Inflation</div>
        <span class="card-badge badge-amber">Cost & Scale</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> Executing multi-model scans across thousands of URLs can incur high API costs and 429 throttling.</li>
        <li><strong>Platform Mitigation:</strong>
          <br>• Asynchronous concurrency semaphores limit parallel vendor requests.
          <br>• ONNX Runtime local models handle classification locally (&lt; 5ms, $0 cost).
          <br>• Tenacity retry policies with randomized jitter prevent thundering herd spikes.
        </li>
      </ul>
    </div>

    <!-- Challenge 4 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">4. Multi-Tenant Data Leakage</div>
        <span class="card-badge badge-amber">Security</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> Competitors auditing the same industry must never access or cross-pollinate keyword datasets.</li>
        <li><strong>Platform Mitigation:</strong>
          <br>• Mandatory `X-Tenant-Id` header enforced at the API gateway layer.
          <br>• Domain aggregates enforce TenantId value objects across all operations.
          <br>• Database queries strictly filter by `tenant_id` at the repository layer.
        </li>
      </ul>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Section 4: Production Resilience</span>
    </div>
    <div class="footer-right">
      <span>Risk Mitigation</span>
      <span class="page-number">15 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 16: ROADMAP & NEXT HORIZONS -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">IMPLEMENTATION ROADMAP</span>
      <div class="slide-title">Roadmap, Delivery Milestones & Next Horizons</div>
      <div class="slide-subtitle">Continuous development alignment across the 15-phase platform evolution</div>
    </div>
    <div class="header-right">
      <span class="pill">Phase 1 - 15</span>
      <span class="pill accent">Enterprise Scaled</span>
    </div>
  </div>

  <div class="grid-3">
    <!-- Col 1 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">Completed Foundation</div>
        <span class="card-badge badge-green">Production Ready</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Clean Hexagonal Core:</strong> Domain aggregates, value objects, error hierarchies, and DI composition root.</li>
        <li><strong>Crawling & Extraction:</strong> Multi-page live crawler, Trafilatura boilerplate stripping, and technical signal detection.</li>
        <li><strong>ONNX Serving:</strong> Offline MLflow tracking and sub-millisecond intent classification serving.</li>
        <li><strong>Question & Visibility Lab:</strong> Multi-engine prompt execution across OpenAI, Gemini, and Perplexity.</li>
      </ul>
    </div>

    <!-- Col 2 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">Active Capabilities</div>
        <span class="card-badge badge-blue">Verified Active</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Deterministic GEO Scorer:</strong> 6-pillar weighted formula delivering explainable 0-100 visibility scores.</li>
        <li><strong>Strategic Recommendations:</strong> Impact vs Effort action prioritization with copy-paste Schema.org code.</li>
        <li><strong>Tenant Vault:</strong> AES-256 encrypted provider credential storage with strict tenant isolation.</li>
        <li><strong>White-Label Reports:</strong> Cron-scheduled email briefs with custom agency branding.</li>
      </ul>
    </div>

    <!-- Col 3 -->
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">Future Expansion</div>
        <span class="card-badge badge-purple">Next Horizons</span>
      </div>
      <ul class="bullet-list purple">
        <li><strong>Graph RAG & Entity Networks:</strong> Knowledge graph representation of brand entity relationships for deeper grounding.</li>
        <li><strong>Real-Time AI SERP Monitoring:</strong> Continuous webhooks triggering alerts when AI citations shift or drop.</li>
        <li><strong>Autonomous Fix PR Generation:</strong> Direct GitHub integration creating pull requests for missing schema and heading fixes.</li>
      </ul>
    </div>
  </div>

  <div class="card" style="padding: 10px 14px; background: rgba(56, 189, 248, 0.08); border-color: rgba(56, 189, 248, 0.25); margin-top: 8px;">
    <div style="font-size: 11px; color: #FFFFFF; display: flex; justify-content: space-between; align-items: center;">
      <span><strong>Enterprise Conclusion:</strong> Transition your organization from legacy search ranking to undisputed authority across the generative AI ecosystem.</span>
      <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #38BDF8; font-weight: 700;">AISEO PLATFORM v2.4</span>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM SPECIFICATION</span>
      <span>Conclusion & Implementation Roadmap</span>
    </div>
    <div class="footer-right">
      <span>Enterprise Edition</span>
      <span class="page-number">16 / 16</span>
    </div>
  </div>
</div>

</body>
</html>
"""
    return html


def build_pdf() -> None:
    html_content = generate_html()
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "AISEO_Platform_Solution_Stages_and_Pipeline.html"
    pdf_path = output_dir / "AISEO_Platform_Solution_Stages_and_Pipeline.pdf"

    html_path.write_text(html_content, encoding="utf-8")
    print(f"Generated HTML slide deck: {html_path.resolve()}")

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = None
    for ep in edge_paths:
        if os.path.exists(ep):
            edge_exe = ep
            break

    if not edge_exe:
        print("Error: Microsoft Edge executable not found.")
        sys.exit(1)

    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        str(html_path.resolve()),
    ]
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Edge process exited with code {result.returncode}")
        print("Stderr:", result.stderr)
        print("Stdout:", result.stdout)
    else:
        print("PDF compilation successful!")
        if pdf_path.exists():
            print(f"Generated PDF file: {pdf_path.resolve()} ({pdf_path.stat().st_size} bytes)")


if __name__ == "__main__":
    build_pdf()
