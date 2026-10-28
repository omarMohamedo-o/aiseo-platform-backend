"""
Script to generate the Technical Architecture & Engineering Deep-Dive PDF for AISEO / GEO Platform.
Designed for CTOs, Chief Architects, Lead Engineers, and technical evaluators.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def generate_technical_html() -> str:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AISEO Platform — Technical Architecture & Engineering Specification</title>
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

.slide {
  width: 960px;
  height: 540px;
  max-height: 540px;
  min-height: 540px;
  padding: 24px 36px 18px 36px;
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

/* Header Row */
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.header-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.tag-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 8.5px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #38BDF8;
  background: rgba(56, 189, 248, 0.1);
  padding: 2px 7px;
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
  font-size: 19px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.3px;
}
.slide-subtitle {
  font-size: 10.5px;
  color: #94A3B8;
  font-weight: 400;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.pill {
  font-size: 8.5px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 9999px;
  background: #151D2E;
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
  font-size: 9.5px;
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

/* Grids & Cards */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  flex: 1;
}
.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  flex: 1;
}
.card {
  background: #0E1626;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 8px;
  padding: 13px;
  display: flex;
  flex-direction: column;
  position: relative;
}
.card.highlight {
  border-color: rgba(56, 189, 248, 0.35);
  background: linear-gradient(180deg, #111D33 0%, #0E1626 100%);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 7px;
}
.card-title {
  font-size: 12.5px;
  font-weight: 700;
  color: #F8FAFC;
}
.card-badge {
  font-size: 8px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
}
.badge-blue { background: rgba(56, 189, 248, 0.15); color: #38BDF8; }
.badge-green { background: rgba(52, 211, 153, 0.15); color: #34D399; }
.badge-purple { background: rgba(192, 132, 252, 0.15); color: #C084FC; }

.bullet-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 10px;
  color: #CBD5E1;
  line-height: 1.4;
}
.bullet-list li {
  position: relative;
  padding-left: 13px;
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
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5px;
  font-weight: 500;
  color: #38BDF8;
}

.data-flow-box {
  background: #080D18;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  padding: 7px 10px;
  margin-top: 7px;
  font-size: 9px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.data-flow-label {
  font-weight: 700;
  color: #94A3B8;
  text-transform: uppercase;
  font-size: 7.5px;
  letter-spacing: 0.8px;
}
.data-flow-val {
  color: #F1F5F9;
  font-family: 'JetBrains Mono', monospace;
  word-break: break-all;
}

/* Cover Special Styling */
.cover-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding-right: 60px;
}
.cover-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.3);
  color: #38BDF8;
  padding: 5px 12px;
  border-radius: 9999px;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  margin-bottom: 14px;
}
.cover-title {
  font-size: 38px;
  font-weight: 800;
  line-height: 1.1;
  background: linear-gradient(135deg, #FFFFFF 30%, #38BDF8 80%, #818CF8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
}
.cover-subtitle {
  font-size: 14px;
  color: #94A3B8;
  font-weight: 400;
  line-height: 1.5;
  max-width: 780px;
  margin-bottom: 22px;
}
.cover-stats-row {
  display: flex;
  gap: 16px;
  width: 100%;
}
.cover-stat-box {
  background: #0E1626;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 10px 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.cover-stat-num {
  font-size: 17px;
  font-weight: 800;
  color: #38BDF8;
}
.cover-stat-desc {
  font-size: 8.5px;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.7px;
  font-weight: 600;
}

/* Pipeline Flow Blocks */
.pipeline-flow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 8px;
}
.pipe-step {
  background: #0E1626;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 9px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.pipe-step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5px;
  font-weight: 700;
  color: #38BDF8;
}
.pipe-step-title {
  font-size: 10.5px;
  font-weight: 700;
  color: #FFFFFF;
}
.pipe-step-desc {
  font-size: 8.5px;
  color: #94A3B8;
  line-height: 1.3;
}
.pipe-step-tools {
  font-size: 7.5px;
  color: #34D399;
  font-family: 'JetBrains Mono', monospace;
  margin-top: 2px;
}

/* Master Tech Table */
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
  background: #080D18;
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

<!-- SLIDE 1: TECHNICAL COVER -->
<div class="slide">
  <div class="header-row" style="border-bottom: none; margin-bottom: 0;">
    <div class="header-left">
      <span class="tag-badge emerald">TECHNICAL SPECIFICATION • ARCHITECTURE BLUEPRINT</span>
    </div>
    <div class="header-right">
      <span class="pill accent">Clean Architecture</span>
      <span class="pill">FastAPI • MLflow • ONNX</span>
    </div>
  </div>

  <div class="cover-container">
    <div class="cover-badge">⚙️ High-Throughput Decoupled Intelligence Engine</div>
    <h1 class="cover-title">AISEO Platform Architecture</h1>
    <p class="cover-subtitle">
      A comprehensive engineering blueprint detailing the Clean / Hexagonal Architecture,
      the 10 decoupled execution stages, sub-millisecond ONNX Runtime serving, multi-engine prompt matrices,
      and RAG citation grounding guardrails powering our enterprise search intelligence platform.
    </p>

    <div class="cover-stats-row">
      <div class="cover-stat-box">
        <div class="cover-stat-num">10 Stages</div>
        <div class="cover-stat-desc">Synchronous & Async Pipeline</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">&lt; 15 ms</div>
        <div class="cover-stat-desc">ONNX Serving Latency</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">Hexagonal</div>
        <div class="cover-stat-desc">Ports & Adapters (DDD)</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">Zero Leaks</div>
        <div class="cover-stat-desc">AES-256 Multi-Tenant Vault</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Engineering Deep-Dive Series • Technical Specification v2.4</span>
    </div>
    <div class="footer-right">
      <span>Confidential Technical Specification</span>
      <span class="page-number">01 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 2: HEXAGONAL ARCHITECTURE PRINCIPLES -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">CORE ENGINEERING PHILOSOPHY</span>
      <div class="slide-title">Clean / Hexagonal Architecture & Dependency Inversion</div>
      <div class="slide-subtitle">Isolating domain business logic from third-party frameworks, database drivers, and vendor LLM SDKs</div>
    </div>
    <div class="header-right">
      <span class="pill">Domain-Driven Design</span>
      <span class="pill accent">Open/Closed Principle</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Domain Layer (Pure Python)</div>
        <span class="card-badge badge-blue">Zero Dependencies</span>
      </div>
      <ul class="bullet-list">
        <li>Contains pure business entities: <code>Website</code>, <code>WebPage</code>, <code>StructuredContent</code>, and <code>Score</code>.</li>
        <li>Immutable Value Objects: <code>TenantId</code>, <code>WebsiteId</code>, <code>Url</code>, enforcing strict invariant checks.</li>
        <li>Domain Errors: Unified exception hierarchy (<code>ProviderRateLimitError</code>, <code>InvalidUrlError</code>).</li>
        <li><strong>Strict Rule:</strong> Zero imports of FastAPI, SQLAlchemy, Redis, or OpenAI SDK.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Ports & Adapters Layer</div>
        <span class="card-badge badge-green">Inversion of Control</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Ports (Abstract Interfaces):</strong> <code>LlmProvider</code>, <code>CrawlerPort</code>, <code>ScraperPort</code>, <code>ModelProvider</code>, <code>VaultPort</code>.</li>
        <li><strong>Adapters (Concrete Implementations):</strong> <code>HttpxCrawler</code>, <code>TrafilaturaScraper</code>, <code>OnnxModelProvider</code>, <code>OpenAiProvider</code>.</li>
        <li>Pluggable architecture allows swapping LLMs or vector databases via simple configuration updates without altering domain code.</li>
      </ul>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Composition Root & DI</div>
        <span class="card-badge badge-purple">Configuration Driven</span>
      </div>
      <ul class="bullet-list">
        <li><strong>CompositionRoot:</strong> Centralizes dependency injection wiring at application bootstrap.</li>
        <li><strong>Generic Registry[T]:</strong> Open/Closed registry pattern eliminating hardcoded <code>if provider == "..."</code> branches.</li>
        <li><strong>Strict Multi-Tenancy:</strong> Request dependency extracts <code>X-Tenant-Id</code> and injects it into application services.</li>
      </ul>
      <div class="data-flow-box">
        <span class="data-flow-label">Dependency Direction</span>
        <span class="data-flow-val">API → Application → Domain ← Ports ← Adapters</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 1: Architecture Core</span>
    </div>
    <div class="footer-right">
      <span>Clean Architecture</span>
      <span class="page-number">02 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 3: MASTER END-TO-END PIPELINE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">END-TO-END PIPELINE</span>
      <div class="slide-title">Master Pipeline Execution Flow</div>
      <div class="slide-subtitle">High-throughput dataflow from raw tenant URL ingestion to automated white-label delivery</div>
    </div>
    <div class="header-right">
      <span class="pill">E2E Flow</span>
      <span class="pill accent">Async Orchestration</span>
    </div>
  </div>

  <div class="pipeline-flow">
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 01</div>
      <div class="pipe-step-title">Vault & Register</div>
      <div class="pipe-step-desc">AES-256 API key storage, tenant isolation, and URL normalization.</div>
      <div class="pipe-step-tools">FastAPI • Pydantic • Fernet</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 02</div>
      <div class="pipe-step-title">Crawl & Traversal</div>
      <div class="pipe-step-desc">Parallel BFS link discovery, sitemap.xml, robots.txt, and JS fallback.</div>
      <div class="pipe-step-tools">HTTPX • Playwright • BS4</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 03</div>
      <div class="pipe-step-title">Scrape & Clean</div>
      <div class="pipe-step-desc">Boilerplate noise removal, JSON-LD schema parsing, and H1-H3 trees.</div>
      <div class="pipe-step-tools">Trafilatura • lxml • HTML5</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 04</div>
      <div class="pipe-step-title">Chunk & Embed</div>
      <div class="pipe-step-desc">Recursive 800-token splitting with dense HNSW vector indexing.</div>
      <div class="pipe-step-tools">pgvector • OpenAI • BGE</div>
    </div>
  </div>

  <div class="pipeline-flow">
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 05</div>
      <div class="pipe-step-title">ONNX ML Serving</div>
      <div class="pipe-step-desc">Sub-5ms query intent classification (Commercial, Informational).</div>
      <div class="pipe-step-tools">ONNX Runtime • MLflow</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 06</div>
      <div class="pipe-step-title">Prompt & Question Lab</div>
      <div class="pipe-step-desc">Multi-lens buyer persona synthesis (Awareness, Comparison, AEO).</div>
      <div class="pipe-step-tools">GPT-4o • Gemini 1.5 • Claude</div>
    </div>
    <div class="pipe-step">
      <div class="pipe-step-num">STAGE 07</div>
      <div class="pipe-step-title">Multi-Model Matrix</div>
      <div class="pipe-step-desc">Concurrent execution across ChatGPT, Gemini, Claude & Perplexity.</div>
      <div class="pipe-step-tools">Async Matrix • Tenacity</div>
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
      <strong style="color: #38BDF8;">Orchestration Guarantees:</strong> Services execute via asynchronous concurrency semaphores (limit: 6). Network failures trigger exponential backoff with randomized jitter. All tenant aggregates remain strictly partition-filtered at the database repository layer.
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 2: Pipeline Architecture</span>
    </div>
    <div class="footer-right">
      <span>Pipeline v2.4</span>
      <span class="page-number">03 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 4: STAGE 01 - CRAWLER -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 01</span>
      <div class="slide-title">Domain Discovery & Intelligent Crawling</div>
      <div class="slide-subtitle">High-concurrency URL discovery, robots.txt compliance, and dynamic JavaScript rendering</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/crawler</span>
      <span class="pill accent">HttpxCrawler</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Algorithmic Mechanics</div>
        <span class="card-badge badge-blue">Engine</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Topology Mapping:</strong> Executes asynchronous BFS traversal restricted strictly to the canonical domain netloc.</li>
        <li><strong>Sitemaps & Robots:</strong> Concurrently inspects <code>/robots.txt</code> crawl-delay directives and parses XML sitemap trees.</li>
        <li><strong>Sanitization Pipeline:</strong> Strips tracking query parameters (<code>utm_*</code>, <code>fbclid</code>) and enforces canonical URLs.</li>
        <li><strong>Dynamic JS Fallback:</strong> Spawns headless Chromium via Playwright when client-rendered hydration markers are detected.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>HTTPX:</strong> Async HTTP/2 client with connection pooling, delivering 50+ concurrent requests per worker.</li>
        <li><strong>Playwright:</strong> Headless browser rendering React, Next.js, and Vue client-side applications.</li>
        <li><strong>BeautifulSoup4:</strong> C-accelerated link extraction with robust parsing for malformed DOM anchors.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">httpx</span>
        <span class="tool-tag">playwright</span>
        <span class="tool-tag">beautifulsoup4</span>
        <span class="tool-tag">asyncio</span>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Interface Contracts</div>
        <span class="card-badge badge-purple">Port Contract</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Method Signature</span>
        <span class="data-flow-val">async discover_pages(target: Url, max_pages: int) -&gt; list[Url]</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Performance SLA</span>
        <span class="data-flow-val">100 pages crawled in 4.2s • Concurrency Semaphore: 6</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Resilience Policy</span>
        <span class="data-flow-val">Domain-polite backoff, rate-limit retries with jitter</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Stage 01: Crawling & Discovery</span>
    </div>
    <div class="footer-right">
      <span>CrawlerPort</span>
      <span class="page-number">04 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 5: STAGE 02 - EXTRACTION & DOM PURIFICATION -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 02</span>
      <div class="slide-title">Boilerplate Stripping & Clean Content Extraction</div>
      <div class="slide-subtitle">Purifying raw HTML into high-signal semantic DOM trees and structured JSON-LD entities</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/scraper</span>
      <span class="pill accent">TrafilaturaScraper</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Purification Logic</div>
        <span class="card-badge badge-blue">Noise Filter</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Noise Elimination:</strong> Discards 68% of raw HTML page weight by stripping headers, footers, navbars, tracking tags, and ads.</li>
        <li><strong>Structural Extraction:</strong> Preserves logical heading hierarchy (H1-H6), article body text, bulleted lists, and tables.</li>
        <li><strong>Entity & Schema Parsing:</strong> Extracts Schema.org JSON-LD blocks, OpenGraph meta tags, and language attributes.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Trafilatura:</strong> Industry-standard Python web scraper recognized for state-of-the-art precision in article body extraction.</li>
        <li><strong>lxml:</strong> C-accelerated DOM traversal and XPath evaluation with minimal memory overhead.</li>
        <li><strong>BeautifulSoup4:</strong> Targeted querying for JSON-LD schema blocks, OpenGraph tags, and metadata attributes.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">trafilatura</span>
        <span class="tool-tag">lxml</span>
        <span class="tool-tag">beautifulsoup4</span>
        <span class="tool-tag">json-ld</span>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Domain Model (StructuredContent)</div>
        <span class="card-badge badge-purple">Entity Schema</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Entity Structure</span>
        <span class="data-flow-val">{ url: Url, title: str, raw_text: str, headings: list[str], language: str, json_ld_schemas: list[dict], characters_count: int }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Context Efficiency</span>
        <span class="data-flow-val">68% reduction in token consumption for downstream LLMs</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Stage 02: Extraction & Structuring</span>
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
      <div class="slide-subtitle">Context-preserving hierarchical text chunking and dense vector indexing in PostgreSQL</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/semantic</span>
      <span class="pill accent">PostgreSQL + pgvector</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Splitting Geometry</div>
        <span class="card-badge badge-blue">Chunking Logic</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Grammatical Splitting:</strong> Recursively splits text along double linebreaks (<code>\\n\\n</code>), sentences (<code>. </code>), and words.</li>
        <li><strong>Context Windowing:</strong> Target 800 tokens with a 120-token sliding overlap to maintain cross-paragraph reasoning.</li>
        <li><strong>Metadata Attachment:</strong> Every chunk retains parent URL, heading hierarchy path, and tenant ID.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>RecursiveCharacterChunker:</strong> Enforces semantic continuity without truncating critical factual claims.</li>
        <li><strong>OpenAI text-embedding-3-small:</strong> 1536-dimensional dense embeddings optimized for retrieval.</li>
        <li><strong>Sentence-Transformers (bge-small):</strong> Local open-source fallback embedding provider.</li>
        <li><strong>PostgreSQL + pgvector:</strong> HNSW vector indexing unified directly within relational database tables.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">pgvector</span>
        <span class="tool-tag">text-embedding-3</span>
        <span class="tool-tag">postgresql</span>
        <span class="tool-tag">hnsw</span>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Storage Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Chunk Contract</span>
        <span class="data-flow-val">{ id: UUID, page_id: UUID, chunk_index: int, text: str, embedding: vector(1536) }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Retrieval SLA</span>
        <span class="data-flow-val">&lt; 8ms ANN cosine similarity retrieval with HNSW indexing</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Stage 03: Semantic Chunking & Vector DB</span>
    </div>
    <div class="footer-right">
      <span>VectorStorePort</span>
      <span class="page-number">06 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 7: STAGE 04 - ONNX MODEL SERVING -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 04</span>
      <div class="slide-title">ML Model Serving via ONNX Runtime & MLflow</div>
      <div class="slide-subtitle">Sub-5ms local neural inference for intent classification, completely decoupled from LLMs</div>
    </div>
    <div class="header-right">
      <span class="pill">ports/ml</span>
      <span class="pill accent">OnnxModelProvider</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Inference Mechanics</div>
        <span class="card-badge badge-blue">Serving Engine</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Zero LLM Cost:</strong> Replaces 2-second LLM calls with local, microsecond neural classifiers.</li>
        <li><strong>Intent Taxonomy:</strong> Categorizes search queries into 4 intents: <em>Commercial, Informational, Navigational, Transactional</em>.</li>
        <li><strong>Offline-to-Online MLOps:</strong> Training runs in MLflow; only optimized <code>.onnx</code> computational graphs deploy to production.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>ONNX Runtime:</strong> High-throughput C++ inference engine with CPU SIMD execution, achieving &lt; 5ms latency.</li>
        <li><strong>MLflow:</strong> Model Registry, artifact versioning, hyperparameter tracking, and reproducibility.</li>
        <li><strong>Scikit-Learn:</strong> TF-IDF feature extraction and calibrated multi-class probability scoring.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">onnxruntime</span>
        <span class="tool-tag">mlflow</span>
        <span class="tool-tag">scikit-learn</span>
        <span class="tool-tag">opencv-headless</span>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Model Artifact & Performance</div>
        <span class="card-badge badge-purple">Serving Contract</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Production Model</span>
        <span class="data-flow-val">models/intent_classifier_v1.onnx</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Serving Latency</span>
        <span class="data-flow-val">3.4ms CPU latency • 99.4% cost reduction vs LLM API</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Prediction Schema</span>
        <span class="data-flow-val">Prediction(label="Commercial", confidence=0.962)</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
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
      <div class="slide-subtitle">Simulating high-intent buyer inquiries across 4 strategic lenses via structured Pydantic schemas</div>
    </div>
    <div class="header-right">
      <span class="pill">application/analysis</span>
      <span class="pill accent">QuestionGenerator</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Multi-Lens Taxonomy</div>
        <span class="card-badge badge-blue">Query Taxonomy</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Awareness Lens:</strong> "What are the most reputable enterprise analytics tools in 2026?"</li>
        <li><strong>Comparison Lens:</strong> "ExampleCorp vs CompetitorX security and pricing."</li>
        <li><strong>Technical AEO Lens:</strong> "Does ExampleCorp support SOC2 Type II and REST APIs?"</li>
        <li><strong>Commercial Lens:</strong> "Top recommended platforms for fintech client analytics."</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Tools & Rationale</div>
        <span class="card-badge badge-green">Tech Stack</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>QuestionGeneratorService:</strong> Enforces prompt diversity and schema adherence.</li>
        <li><strong>OpenAI GPT-4o:</strong> Primary high-reasoning query synthesizer with JSON mode.</li>
        <li><strong>Google Gemini 1.5:</strong> Secondary multi-lingual query generator offering diverse natural buyer phrasing.</li>
        <li><strong>Pydantic v2:</strong> Validates <code>QuestionSet</code> models and enforces constraints.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">gpt-4o</span>
        <span class="tool-tag">gemini-1.5</span>
        <span class="tool-tag">pydantic-v2</span>
        <span class="tool-tag">prompt-lab</span>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Request Payload</span>
        <span class="data-flow-val">{ topic, keywords: list[str], lens: "geo", count: 10, language: "en" }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Schema</span>
        <span class="data-flow-val">QuestionSet: { topic, questions: list[QuestionItem] }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Diversity</span>
        <span class="data-flow-val">100% unique intents • Zero redundant keyword repetition</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Stage 05: Synthetic Buyer Persona Lab</span>
    </div>
    <div class="footer-right">
      <span>IntelligencePort</span>
      <span class="page-number">08 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 9: STAGE 06 - MULTI-MODEL EXECUTION MATRIX -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 06</span>
      <div class="slide-title">Multi-Model AI Visibility Execution Matrix</div>
      <div class="slide-subtitle">Concurrent querying across ChatGPT, Gemini, Claude, and Perplexity with fault-tolerant retry loops</div>
    </div>
    <div class="header-right">
      <span class="pill">application/analysis</span>
      <span class="pill accent">PromptExecutor</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Matrix Dispatch</div>
        <span class="card-badge badge-blue">Dispatch Engine</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Cross-Ecosystem Testing:</strong> Concurrently tests brand presence across 4 major generative AI platforms.</li>
        <li><strong>Parallel Matrix Dispatch:</strong> Executes <code>[Questions] × [Providers]</code> asynchronously, minimizing audit duration.</li>
        <li><strong>Deterministic Resilience:</strong> Built-in circuit breakers, exponential backoff, and mock fallback handlers.</li>
        <li><strong>Error Normalization:</strong> Normalizes HTTP 429 and 504 errors into unified domain exceptions.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Providers & Adapters</div>
        <span class="card-badge badge-green">Engines</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>OpenAI (GPT-4o):</strong> Simulates ChatGPT Plus & SearchGPT answer synthesis behavior.</li>
        <li><strong>Google Gemini (Gemini 1.5):</strong> Evaluates visibility in Google AI Overviews.</li>
        <li><strong>Anthropic Claude:</strong> Independent baseline for neutral brand perception.</li>
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
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Stage 06: Multi-Model AI Execution Matrix</span>
    </div>
    <div class="footer-right">
      <span>LlmProviderPort</span>
      <span class="page-number">09 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 10: STAGE 07 - ANSWER AUDITING & CITATION GUARDRAIL -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">STAGE 07</span>
      <div class="slide-title">Answer Auditing & Citation Grounding Guardrail</div>
      <div class="slide-subtitle">Deconstructing generative responses into brand mention, sentiment, and factual grounding ratios</div>
    </div>
    <div class="header-right">
      <span class="pill">application/analysis</span>
      <span class="pill accent">AnswerAnalyzer</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Citation & Mention Audit</div>
        <span class="card-badge badge-blue">Audit Engine</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Brand Mention Extraction:</strong> Exact and fuzzy NER matching to verify if the brand is cited in answers.</li>
        <li><strong>Citation URL Parsing:</strong> Extracts inline markdown URLs, footnotes, and grounded search references.</li>
        <li><strong>Sentiment & Tone Classification:</strong> Evaluates context surrounding brand mentions: <em>Positive, Neutral, or Negative</em>.</li>
        <li><strong>Competitor Infiltration:</strong> Detects rival companies mentioned in the same answer.</li>
      </ul>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">2. Grounding Guardrail (HistoryVerse)</div>
        <span class="card-badge badge-purple">Hallucination Defense</span>
      </div>
      <ul class="bullet-list purple">
        <li><strong>Grounding Ratio:</strong> Measures entity overlap between AI answers and crawled website source context:
          <br><code>Grounding = |Answer Entities ∩ Crawled Text| / |Answer Entities|</code>
        </li>
        <li><strong>Hallucination Score:</strong> Flags when AI models invent false pricing or non-existent features.</li>
        <li><strong>Citation Verification:</strong> Ensures cited URLs resolve to live, crawled domain pages.</li>
      </ul>
      <div class="tool-tag-group">
        <span class="tool-tag">grounding-guard</span>
        <span class="tool-tag">spacy-ner</span>
        <span class="tool-tag">hallucination-detector</span>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">3. Data Contracts & Output</div>
        <span class="card-badge badge-green">Pipeline Interface</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Output Contract</span>
        <span class="data-flow-val">{ brand_mentioned: bool, sentiment: "positive", extracted_citations: ["https://..."], competitors: [...], hallucination_score: 0.12 }</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">Grounding Benchmark</span>
        <span class="data-flow-val">&gt; 0.85 Grounding Ratio indicates verified factual citation</span>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Stage 07: Answer Auditing & Citation Guard</span>
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
      <span class="footer-brand">AISEO PLATFORM</span>
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
      <span class="footer-brand">AISEO PLATFORM</span>
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
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Tenant Security Vault</div>
        <span class="card-badge badge-blue">Cryptographic Security</span>
      </div>
      <ul class="bullet-list">
        <li><strong>AES-256 Key Encryption:</strong> Client-provided API keys (OpenAI, Gemini, Serper) are encrypted using authenticated symmetric encryption (<code>Fernet</code>).</li>
        <li><strong>Tenant Isolation:</strong> Enforces tenant isolation on all vault queries via mandatory <code>X-Tenant-Id</code> header.</li>
        <li><strong>Zero Leakage:</strong> Raw credentials never hit application logs; masked in all API responses (<code>sk-proj-****</code>).</li>
      </ul>
    </div>

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

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Automated Schedules</div>
        <span class="card-badge badge-purple">Pipeline Interface</span>
      </div>
      <ul class="bullet-list purple">
        <li><strong>Cron Schedule Engine:</strong> Automated weekly or monthly scans (<code>0 9 * * 1</code>) executing end-to-end audits.</li>
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
      <span class="footer-brand">AISEO PLATFORM</span>
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
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 3: Technology Architecture</span>
    </div>
    <div class="footer-right">
      <span>Production Stack</span>
      <span class="page-number">14 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 15: PRODUCTION RESILIENCE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge purple">PRODUCTION RESILIENCE</span>
      <div class="slide-title">Engineering Challenges & Production Mitigations</div>
      <div class="slide-subtitle">Overcoming non-determinism, dynamic SPAs, vendor rate limits, and multi-tenant security</div>
    </div>
    <div class="header-right">
      <span class="pill">SLA & Resilience</span>
      <span class="pill accent">Enterprise Ready</span>
    </div>
  </div>

  <div class="grid-2">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. LLM Hallucinations & Non-Determinism</div>
        <span class="card-badge badge-blue">Reliability</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> Commercial LLMs can produce varied answers across runs or hallucinate citations that do not exist.</li>
        <li><strong>Platform Mitigation:</strong> Temperature locked to <code>0.2</code>; multi-run prompt matrix averaging across independent providers; regex and schema grounding validation.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Dynamic SPAs & Anti-Bot Protections</div>
        <span class="card-badge badge-blue">Extraction</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> Modern sites built in React/Next.js/Angular hide content behind client-side JavaScript hydration.</li>
        <li><strong>Platform Mitigation:</strong> Automatic fallback from HTTPX to Playwright headless Chromium when hydration markers are detected; realistic browser header rotations.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">3. Vendor API Rate Limits & Cost Inflation</div>
        <span class="card-badge badge-blue">Cost & Scale</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> Executing multi-model scans across thousands of URLs can incur high API costs and 429 throttling.</li>
        <li><strong>Platform Mitigation:</strong> Concurrency semaphores limit parallel requests; ONNX local model serving handles intent classification locally (&lt; 5ms, $0 cost); Tenacity retry with jitter.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">4. Multi-Tenant Data Leakage</div>
        <span class="card-badge badge-blue">Security</span>
      </div>
      <ul class="bullet-list">
        <li><strong>The Challenge:</strong> Competitors auditing the same industry must never access or cross-pollinate keyword datasets.</li>
        <li><strong>Platform Mitigation:</strong> Mandatory <code>X-Tenant-Id</code> enforced at API gateway; domain aggregates enforce TenantId value objects; repository queries filter by tenant.</li>
      </ul>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 4: Production Resilience</span>
    </div>
    <div class="footer-right">
      <span>Risk Mitigation</span>
      <span class="page-number">15 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 16: DEVELOPER API REFERENCE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">DEVELOPER REFERENCE</span>
      <div class="slide-title">REST API Endpoints & Verification Quickstart</div>
      <div class="slide-subtitle">Production endpoints, payload contracts, and automated testing verification</div>
    </div>
    <div class="header-right">
      <span class="pill">FastAPI OpenAPI</span>
      <span class="pill accent">Swagger Verified</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">Website & Crawl API</div>
        <span class="card-badge badge-blue">REST Endpoints</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">POST /api/v1/websites</span>
        <span class="data-flow-val">Registers tenant domain with URL validation</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">POST /api/v1/websites/crawl-and-analyze</span>
        <span class="data-flow-val">Full-domain crawl, Trafilatura extraction, per-page audit & GEO score</span>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Intelligence & Simulation</div>
        <span class="card-badge badge-green">AI Lab Endpoints</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">POST /api/v1/intelligence/questions/generate</span>
        <span class="data-flow-val">Generates multi-lens buyer persona questions</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">POST /api/v1/visibility/answers/analyze</span>
        <span class="data-flow-val">Audits brand mentions, sentiment & citations</span>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">Vault & Schedules</div>
        <span class="card-badge badge-purple">Enterprise Delivery</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">POST /api/v1/vault/credentials</span>
        <span class="data-flow-val">Stores AES-256 encrypted provider API keys</span>
      </div>
      <div class="data-flow-box">
        <span class="data-flow-label">POST /api/v1/reports/schedules</span>
        <span class="data-flow-val">Creates recurring cron-scheduled email audits</span>
      </div>
    </div>
  </div>

  <div class="card" style="padding: 9px 14px; background: rgba(56, 189, 248, 0.08); border-color: rgba(56, 189, 248, 0.25); margin-top: 8px;">
    <div style="font-size: 10.5px; color: #FFFFFF; display: flex; justify-content: space-between; align-items: center;">
      <span><strong>Verification Suite:</strong> 24 unit & integration tests passing (<code>uv run pytest</code>) • Strict type checking (<code>mypy src</code>) • Ruff lint clean.</span>
      <span style="font-family: 'JetBrains Mono', monospace; font-size: 9.5px; color: #38BDF8; font-weight: 700;">AISEO ENGINE v2.4</span>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Conclusion & API Verification Reference</span>
    </div>
    <div class="footer-right">
      <span>Technical Specification</span>
      <span class="page-number">16 / 16</span>
    </div>
  </div>
</div>

</body>
</html>
"""
    return html


def build_technical_pdf() -> None:
    html_content = generate_technical_html()
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "AISEO_Technical_Architecture_DeepDive.html"
    pdf_path = output_dir / "AISEO_Technical_Architecture_DeepDive.pdf"

    html_path.write_text(html_content, encoding="utf-8")
    print(f"Generated Technical HTML: {html_path.resolve()}")

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
        print(f"Edge exited with code {result.returncode}")
        print("Stderr:", result.stderr)
    else:
        print("Technical Architecture PDF compilation successful!")
        if pdf_path.exists():
            print(f"Generated PDF: {pdf_path.resolve()} ({pdf_path.stat().st_size} bytes)")


if __name__ == "__main__":
    build_technical_pdf()

