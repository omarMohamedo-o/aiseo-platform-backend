"""
Script to generate the Enterprise Client Sales Pitch Deck PDF for AISEO / GEO Platform.
Designed for prospective clients, CMOs, CEOs, and agency partners to sell the solution.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def generate_sales_html() -> str:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AISEO Platform — Enterprise Client Sales & Product Pitch</title>
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
  background: #060913;
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
  background: #060913;
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
.tag-badge.gold {
  color: #FBBF24;
  background: rgba(251, 191, 36, 0.1);
  border-color: rgba(251, 191, 36, 0.25);
}
.tag-badge.emerald {
  color: #34D399;
  background: rgba(52, 211, 153, 0.1);
  border-color: rgba(52, 211, 153, 0.25);
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
.pill.gold-accent {
  background: linear-gradient(135deg, #D97706, #B45309);
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
.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  flex: 1;
}
.card {
  background: #0C1220;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 8px;
  padding: 13px;
  display: flex;
  flex-direction: column;
  position: relative;
}
.card.highlight {
  border-color: rgba(56, 189, 248, 0.35);
  background: linear-gradient(180deg, #101A2E 0%, #0C1220 100%);
}
.card.gold-highlight {
  border-color: rgba(251, 191, 36, 0.35);
  background: linear-gradient(180deg, #1A1710 0%, #0C1220 100%);
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
.badge-gold { background: rgba(251, 191, 36, 0.15); color: #FBBF24; }
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
.bullet-list.gold li::before { color: #FBBF24; }
.bullet-list.green li::before { color: #34D399; }

.stat-box {
  background: #080D18;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  padding: 8px 10px;
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.stat-box-num {
  font-size: 16px;
  font-weight: 800;
  color: #38BDF8;
}
.stat-box-desc {
  font-size: 8px;
  color: #94A3B8;
  text-transform: uppercase;
  letter-spacing: 0.7px;
  font-weight: 600;
}

/* Cover Styling */
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
  background: #0C1220;
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

/* Master Table */
.sales-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9.5px;
  margin-top: 4px;
}
.sales-table th {
  background: #101A2E;
  color: #94A3B8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  font-size: 8px;
  padding: 6px 10px;
  text-align: left;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.sales-table td {
  padding: 6px 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  color: #CBD5E1;
  background: #080D18;
}
.sales-table tr:nth-child(even) td {
  background: #0C1220;
}
</style>
</head>
<body>

<!-- SLIDE 1: SALES COVER -->
<div class="slide">
  <div class="header-row" style="border-bottom: none; margin-bottom: 0;">
    <div class="header-left">
      <span class="tag-badge gold">CLIENT PITCH DECK • EXECUTIVE EDITION</span>
    </div>
    <div class="header-right">
      <span class="pill gold-accent">Commercial Brief</span>
      <span class="pill">2026 AI Search Strategy</span>
    </div>
  </div>

  <div class="cover-container">
    <div class="cover-badge">🚀 Dominate Generative AI Search & Citations</div>
    <h1 class="cover-title">The Generative Search Revolution</h1>
    <p class="cover-subtitle">
      Over 65% of customer journeys now bypass traditional search results and ask ChatGPT, Google Gemini, and Perplexity directly.
      Our <strong>AISEO Platform</strong> guarantees your enterprise brand is recognized, favorably recommended, and cited as the authoritative source by generative AI.
    </p>

    <div class="cover-stats-row">
      <div class="cover-stat-box">
        <div class="cover-stat-num">65%+</div>
        <div class="cover-stat-desc">Zero-Click AI Searches</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">3.4×</div>
        <div class="cover-stat-desc">Higher Buyer Intent via AI</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">4 Engines</div>
        <div class="cover-stat-desc">ChatGPT • Gemini • Claude • Perplexity</div>
      </div>
      <div class="cover-stat-box">
        <div class="cover-stat-num">30 Days</div>
        <div class="cover-stat-desc">Measurable Citation Uplift</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Enterprise Generative Search Optimization • Client Pitch Series</span>
    </div>
    <div class="footer-right">
      <span>Confidential Presentation</span>
      <span class="page-number">01 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 2: THE BUSINESS PROBLEM -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">THE MARKET CRISIS</span>
      <div class="slide-title">Why Legacy SEO is Failing Enterprise Brands</div>
      <div class="slide-subtitle">Traditional ranking strategies no longer capture high-value buyers who search with generative AI</div>
    </div>
    <div class="header-right">
      <span class="pill">Problem Analysis</span>
      <span class="pill accent">The Zero-Click Shift</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. The Death of 10 Blue Links</div>
        <span class="card-badge badge-blue">Shift</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Zero-Click Reality:</strong> Google AI Overviews and ChatGPT answer complex questions directly. Users no longer scroll through ten search results.</li>
        <li><strong>Organic Traffic Bleed:</strong> Even brands ranking #1 on traditional Google are losing up to 40% of organic search clicks to synthesized AI answers.</li>
        <li><strong>Wasted Ad Spend:</strong> High-intent buyers ask AI for unbiased comparisons rather than clicking sponsored search ads.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">65.2%</div>
        <div class="stat-box-desc">Searches conclude without visiting any website</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Invisible to Generative Engines</div>
        <span class="card-badge badge-gold">Risk</span>
      </div>
      <ul class="bullet-list gold">
        <li><strong>Brand Erasure:</strong> When an enterprise buyer asks, <em>"What is the best platform for our enterprise?"</em>, AI engines recommend your competitors.</li>
        <li><strong>Hallucinated Claims:</strong> AI models often quote outdated prices, false feature limitations, or obsolete specifications about your products.</li>
        <li><strong>Missing Citations:</strong> Even when you have superior technical content, AI fails to link your domain as an authoritative ground-truth reference.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">78%</div>
        <div class="stat-box-desc">Of top brands are absent from primary AI answers</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. The Solution: GEO & AEO</div>
        <span class="card-badge badge-green">Opportunity</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Direct AI Endorsements:</strong> Structure your web assets so AI models synthesize your brand as the #1 recommended solution.</li>
        <li><strong>Verifiable Citation Links:</strong> Ensure your domain URLs are embedded directly as clickable citations in ChatGPT and Perplexity.</li>
        <li><strong>First-Mover Dominance:</strong> While competitors still optimize for 2018 keywords, capture uncontested generative AI mindshare.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">3.4×</div>
        <div class="stat-box-desc">Higher inbound conversion rate from AI citations</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 1: The Commercial Challenge</span>
    </div>
    <div class="footer-right">
      <span>Market Analysis</span>
      <span class="page-number">02 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 3: WHAT IS GEO & AEO -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">THE VISIBILITY PARADIGM</span>
      <div class="slide-title">Unifying SEO, AEO & GEO for Complete Dominance</div>
      <div class="slide-subtitle">Capturing customers across every stage of discovery: traditional search, voice answer, and AI synthesis</div>
    </div>
    <div class="header-right">
      <span class="pill">Strategic Framework</span>
      <span class="pill accent">3-in-1 Coverage</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">SEO (Search Engines)</div>
        <span class="card-badge badge-blue">Baseline</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Where It Operates:</strong> Google Search, Bing, DuckDuckGo.</li>
        <li><strong>What It Solves:</strong> Ensures technical crawlability, clean title tags, and baseline domain discoverability.</li>
        <li><strong>Our Edge:</strong> We audit internal link topology, schema markup, and speed signals in real-time.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Rank #1 - #10</div>
        <div class="stat-box-desc">Legacy SERP Indexation</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">AEO (Answer Engines)</div>
        <span class="card-badge badge-green">Immediate Trust</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Where It Operates:</strong> Featured Snippets, Siri, Alexa, Google Voice.</li>
        <li><strong>What It Solves:</strong> Captures zero-click direct answers by packaging concise, 40-word definitive definitions and FAQ schemas.</li>
        <li><strong>Our Edge:</strong> Direct question-answering architecture that positions your brand as the single verified answer.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Zero-Click Capture</div>
        <div class="stat-box-desc">Direct Knowledge Card Sniping</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">GEO (Generative Engines)</div>
        <span class="card-badge badge-purple">High-Conversion</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Where It Operates:</strong> ChatGPT, Gemini, Claude, Perplexity.</li>
        <li><strong>What It Solves:</strong> Ensures your product is endorsed when buyers ask for recommendations, comparisons, and enterprise reviews.</li>
        <li><strong>Our Edge:</strong> Real multi-model prompt simulations and citation verification across all leading AI engines.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Authoritative Citation</div>
        <div class="stat-box-desc">Ground-Truth Source Recommendation</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 2: The Solution Paradigm</span>
    </div>
    <div class="footer-right">
      <span>SEO • AEO • GEO</span>
      <span class="page-number">03 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 4: PRODUCT SUITE OVERVIEW -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">THE PRODUCT SUITE</span>
      <div class="slide-title">The AISEO Platform: 4 Pillars of Market Leadership</div>
      <div class="slide-subtitle">An end-to-end intelligence suite that automates discovery, simulation, scoring, and remediation</div>
    </div>
    <div class="header-right">
      <span class="pill">Core Capabilities</span>
      <span class="pill accent">Modular Suite</span>
    </div>
  </div>

  <div class="grid-4">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. AI Audit Engine</div>
        <span class="card-badge badge-blue">Audit</span>
      </div>
      <ul class="bullet-list">
        <li>Crawls 100% of website pages with JS rendering.</li>
        <li>Purifies content and extracts Schema.org JSON-LD.</li>
        <li>Detects technical barriers blocking AI web crawlers.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Deep Crawl</div>
        <div class="stat-box-desc">100+ pages in seconds</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Prompt & Query Lab</div>
        <span class="card-badge badge-green">Simulation</span>
      </div>
      <ul class="bullet-list green">
        <li>Generates real-world buyer persona prompts.</li>
        <li>Simulates top-of-funnel and competitor comparisons.</li>
        <li>Multi-lingual support (English, Arabic, Global).</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Multi-Lens</div>
        <div class="stat-box-desc">Awareness to Purchase</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Multi-Model Matrix</div>
        <span class="card-badge badge-purple">Testing</span>
      </div>
      <ul class="bullet-list">
        <li>Live querying across ChatGPT, Gemini & Perplexity.</li>
        <li>Tracks brand mention rate and sentiment.</li>
        <li>Extracts verified domain citation links.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Live Matrix</div>
        <div class="stat-box-desc">Real-time AI querying</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">4. Action Engine</div>
        <span class="card-badge badge-gold">Execution</span>
      </div>
      <ul class="bullet-list gold">
        <li>Unified 0–100 GEO Visibility Scorecard.</li>
        <li>Prioritized Quick Wins vs High Impact Architecture.</li>
        <li>Automated weekly white-label executive digests.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Turnkey ROI</div>
        <div class="stat-box-desc">Copy-paste code & fixes</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 3: Product Capabilities</span>
    </div>
    <div class="footer-right">
      <span>Enterprise Suite</span>
      <span class="page-number">04 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 5: BUSINESS ROI -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge gold">COMMERCIAL VALUE & ROI</span>
      <div class="slide-title">Quantifiable Business Impact for Enterprise Clients</div>
      <div class="slide-subtitle">Converting AI visibility into qualified pipeline, reduced customer acquisition cost, and revenue</div>
    </div>
    <div class="header-right">
      <span class="pill">C-Suite Economics</span>
      <span class="pill gold-accent">Proven Growth</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Qualified Inbound Pipeline</div>
        <span class="card-badge badge-green">+35% Conversion</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>High-Intent Prospects:</strong> Buyers asking AI for product comparisons are ready to purchase. When AI recommends your brand, conversion rates are 3.4× higher than generic organic search.</li>
        <li><strong>Zero Cost Per Click:</strong> Generative engine citations generate perpetual organic enterprise inquiries without ad budget depletion.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">3.4×</div>
        <div class="stat-box-desc">Conversion multiple vs traditional Google search</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">2. Competitor Interception</div>
        <span class="card-badge badge-blue">Market Defense</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Reclaim Lost Market Share:</strong> Identify the exact queries where ChatGPT cites your rivals and deploy targeted content fixes within 48 hours.</li>
        <li><strong>Protect Brand Reputation:</strong> Prevent AI models from hallucinating false prices or non-existent shortcomings regarding your products.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">82%</div>
        <div class="stat-box-desc">Reduction in false AI feature hallucinations</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">3. Board-Level Visibility</div>
        <span class="card-badge badge-purple">Executive Clarity</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Unified Visibility Scorecard:</strong> A single, definitive 0–100 benchmark metric to report progress directly to CMOs and executive boards.</li>
        <li><strong>Automated Monday Digests:</strong> Weekly executive reports delivered straight to stakeholder inboxes showing share-of-voice gains.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">100%</div>
        <div class="stat-box-desc">Automated tracking with zero manual reporting</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 4: Financial & Strategic Value</span>
    </div>
    <div class="footer-right">
      <span>Enterprise ROI</span>
      <span class="page-number">05 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 6: MULTI-MODEL COVERAGE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">THE AI ECOSYSTEM MATRIX</span>
      <div class="slide-title">Auditing Every Major Generative Engine Simultaneously</div>
      <div class="slide-subtitle">Real-time simulation across all commercial AI platforms where your potential clients search</div>
    </div>
    <div class="header-right">
      <span class="pill">Multi-Model Testing</span>
      <span class="pill accent">Zero Vendor Bias</span>
    </div>
  </div>

  <div class="grid-4">
    <div class="card">
      <div class="card-header">
        <div class="card-title">ChatGPT / SearchGPT</div>
        <span class="card-badge badge-blue">OpenAI</span>
      </div>
      <ul class="bullet-list">
        <li>400M+ active users.</li>
        <li>Primary destination for enterprise software evaluation.</li>
        <li>Audits direct brand mentions and cited reference links.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">GPT-4o</div>
        <div class="stat-box-desc">Real-time answer audit</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Google Gemini</div>
        <span class="card-badge badge-green">Google Ecosystem</span>
      </div>
      <ul class="bullet-list green">
        <li>Powers Google AI Overviews on billions of search results.</li>
        <li>Directly impacts organic website click-through rates.</li>
        <li>Audits entity relationships and technical SEO health.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Gemini 1.5</div>
        <div class="stat-box-desc">AI Overviews simulation</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Perplexity AI</div>
        <span class="card-badge badge-purple">Grounded Search</span>
      </div>
      <ul class="bullet-list">
        <li>The fastest-growing conversational research engine.</li>
        <li>Provides explicit footnote citations with every claim.</li>
        <li>Verifies if your URL is cited as the source authority.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Sonar Search</div>
        <div class="stat-box-desc">Citation URL verification</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Anthropic Claude</div>
        <span class="card-badge badge-gold">Enterprise AI</span>
      </div>
      <ul class="bullet-list gold">
        <li>Favored by technical teams, financial analysts, and C-suite.</li>
        <li>Rigorous factual reasoning and safety guardrails.</li>
        <li>Evaluates objective, neutral brand sentiment.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Claude 3.5</div>
        <div class="stat-box-desc">Technical credibility audit</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 5: Cross-Ecosystem Coverage</span>
    </div>
    <div class="footer-right">
      <span>Multi-Model Intelligence</span>
      <span class="page-number">06 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 7: 4-STEP CLIENT JOURNEY -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">CLIENT EXPERIENCE</span>
      <div class="slide-title">The 4-Step Client Journey: From Invisible to Authoritative</div>
      <div class="slide-subtitle">A seamless, turnkey customer onboarding process that delivers actionable insights in under 10 minutes</div>
    </div>
    <div class="header-right">
      <span class="pill">Turnkey Onboarding</span>
      <span class="pill accent">Self-Service or White-Glove</span>
    </div>
  </div>

  <div class="grid-4">
    <div class="card">
      <div class="card-header">
        <div class="card-title">Step 01: Connect URL</div>
        <span class="card-badge badge-blue">Minute 1</span>
      </div>
      <ul class="bullet-list">
        <li>Enter your root domain (e.g. <code>https://brand.com</code>).</li>
        <li>Autonomous crawler discovers all live pages, sitemaps, and robots directives.</li>
        <li>No code installation or DNS modification required.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Zero-Touch</div>
        <div class="stat-box-desc">Immediate setup</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Step 02: AI Scan</div>
        <span class="card-badge badge-green">Minute 3</span>
      </div>
      <ul class="bullet-list green">
        <li>System synthesizes 20–50 high-intent buyer persona queries.</li>
        <li>Dispatches prompt matrix across ChatGPT, Gemini, and Perplexity.</li>
        <li>Tracks brand mentions, citation URLs, and competitor mentions.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Live Matrix</div>
        <div class="stat-box-desc">Multi-engine audit</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Step 03: Gap Diagnosis</div>
        <span class="card-badge badge-purple">Minute 5</span>
      </div>
      <ul class="bullet-list">
        <li>Reveals your unified GEO Score (0–100) across 6 core pillars.</li>
        <li>Identifies missing schema markups, weak entity definitions, and lost citations.</li>
        <li>Highlights which competitors are winning AI recommendations.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Score 0-100</div>
        <div class="stat-box-desc">Transparent benchmark</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">Step 04: Execute Fixes</div>
        <span class="card-badge badge-gold">Continuous</span>
      </div>
      <ul class="bullet-list gold">
        <li>Receive prioritized Quick Wins with ready-to-paste JSON-LD Schema code.</li>
        <li>Deploy targeted FAQ and comparison matrices.</li>
        <li>Receive automated weekly email audits tracking your citation gains.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">ROI Engine</div>
        <div class="stat-box-desc">Proven citation growth</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 6: Implementation Workflow</span>
    </div>
    <div class="footer-right">
      <span>Client Journey</span>
      <span class="page-number">07 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 8: THE GEO SCORECARD -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">THE EXECUTIVE BENCHMARK</span>
      <div class="slide-title">The Unified GEO Visibility Scorecard</div>
      <div class="slide-subtitle">A deterministic, 100% explainable metric that turns complex AI behavior into actionable clarity</div>
    </div>
    <div class="header-right">
      <span class="pill">C-Suite Dashboard</span>
      <span class="pill accent">Weighted Formulation</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">Overall GEO Score: 78 / 100</div>
        <span class="card-badge badge-green">Strong Growth</span>
      </div>
      <p style="font-size: 10px; color: #94A3B8; margin-bottom: 8px;">
        Unlike subjective SEO audits, our GEO Score is mathematical, deterministic, and directly correlated with AI citation frequency.
      </p>
      <div class="stat-box">
        <div class="stat-box-num">78 / 100</div>
        <div class="stat-box-desc">Current Brand Authority Index</div>
      </div>
      <div class="stat-box" style="margin-top: 6px;">
        <div class="stat-box-num" style="color: #34D399;">82 / 100</div>
        <div class="stat-box-desc">Opportunity Upside Potential</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">The 6 Weighted Sub-Pillars</div>
        <span class="card-badge badge-blue">Breakdown</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Content Clarity (20%):</strong> 88 / 100 — Concise, fluff-free text structure.</li>
        <li><strong>Entity Coverage (20%):</strong> 79 / 100 — Clear product, feature & audience definitions.</li>
        <li><strong>AI Visibility (20%):</strong> 71 / 100 — Frequency of mention in multi-model queries.</li>
        <li><strong>Citation Readiness (15%):</strong> 63 / 100 — Presence of verifiable data tables & FAQ schema.</li>
        <li><strong>Competitive Share (15%):</strong> 68 / 100 — Brand position relative to rivals.</li>
        <li><strong>Technical Signals (10%):</strong> 84 / 100 — Robots.txt, sitemaps, SSL & mobile health.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Why C-Levels Value It</div>
        <span class="card-badge badge-purple">Executive Value</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Transparent Accountability:</strong> Know precisely which team actions drive score increases.</li>
        <li><strong>Competitive Benchmarking:</strong> Compare your company score against top industry rivals.</li>
        <li><strong>Zero Black-Box Guesswork:</strong> Every score component is linked directly to raw crawled evidence.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">100% Explainable</div>
        <div class="stat-box-desc">Zero AI hallucinated metrics</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 7: The Visibility Scorecard</span>
    </div>
    <div class="footer-right">
      <span>Deterministic Metrics</span>
      <span class="page-number">08 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 9: COMPETITIVE INTELLIGENCE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge gold">COMPETITIVE EDGE</span>
      <div class="slide-title">Competitor Share-of-Voice & Gap Interception</div>
      <div class="slide-subtitle">Identify exactly which competitors AI engines recommend over your brand—and why</div>
    </div>
    <div class="header-right">
      <span class="pill">Competitor Radar</span>
      <span class="pill gold-accent">Market Share Capture</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Discovered Competitor Radar</div>
        <span class="card-badge badge-blue">Detection</span>
      </div>
      <ul class="bullet-list">
        <li>Identifies unprompted competitor mentions in generative AI responses.</li>
        <li>Measures competitor citation frequency across commercial queries.</li>
        <li>Reveals competitor positioning (e.g. "Competitor A is best for enterprise; Brand is best for SMB").</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Share-of-Voice</div>
        <div class="stat-box-desc">Continuous competitor tracking</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">2. Content & Citation Gaps</div>
        <span class="card-badge badge-gold">Interception</span>
      </div>
      <ul class="bullet-list gold">
        <li>Pinpoints the specific comparison pages and data tables that competitors have, but your website lacks.</li>
        <li>Identifies third-party review sites and industry benchmarks that AI models consult to validate rival claims.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Citation Gaps</div>
        <div class="stat-box-desc">Pinpointed in minutes</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">3. Turnkey Remediation Blueprint</div>
        <span class="card-badge badge-green">Takeover</span>
      </div>
      <ul class="bullet-list green">
        <li>Generates dedicated "Brand vs Competitor" outline briefs with verifiable claims.</li>
        <li>Provides structured feature matrices designed specifically for LLM extraction.</li>
        <li>Ranks actions by revenue impact so teams focus on high-intent buyer queries first.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">&lt; 14 Days</div>
        <div class="stat-box-desc">Average time to close citation gaps</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 8: Competitive Intelligence</span>
    </div>
    <div class="footer-right">
      <span>Market Dominance</span>
      <span class="page-number">09 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 10: STRATEGIC ACTION BLUEPRINTS -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">ACTIONABLE DELIVERABLES</span>
      <div class="slide-title">From Insight to Execution: Prioritized Action Plans</div>
      <div class="slide-subtitle">Clear, categorized engineering checklists with copy-paste code and immediate ROI</div>
    </div>
    <div class="header-right">
      <span class="pill">Execution Engine</span>
      <span class="pill accent">Impact vs Effort</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">Quick Wins (Day 1 - 7)</div>
        <span class="card-badge badge-green">Immediate ROI</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Missing FAQ Schema:</strong> Injects copy-paste JSON-LD Schema code on core landing pages to capture AEO voice and snippet answers.</li>
        <li><strong>AI Bot Unblocking:</strong> Updates <code>robots.txt</code> to permit GPTBot, PerplexityBot, and Google-Extended to index your key product pages.</li>
        <li><strong>H1/H2 Topical Keywords:</strong> Restructures primary headings into direct question-and-answer formats.</li>
      </ul>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">Content Architecture (Day 8 - 21)</div>
        <span class="card-badge badge-blue">High Impact</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Product Comparison Matrices:</strong> Publishes objective comparison tables pitting your strengths against legacy competitors.</li>
        <li><strong>Structured Pricing Breakdown:</strong> Formats complex pricing into unambiguous, table-based feature tiers that AI engines extract accurately.</li>
        <li><strong>Buyer Persona Guides:</strong> Publishes definitive industry guides answering mid-funnel consideration questions.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Authority Building (Day 22 - 45)</div>
        <span class="card-badge badge-purple">Long-Term Moat</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Proprietary Research Reports:</strong> Publishes original benchmark studies with statistics that AI models frequently cite as industry facts.</li>
        <li><strong>Knowledge Graph Linking:</strong> Connects brand entity links to Wikidata, Crunchbase, and authoritative industry registries.</li>
      </ul>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 9: Implementation Roadmap</span>
    </div>
    <div class="footer-right">
      <span>Turnkey Execution</span>
      <span class="page-number">10 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 11: ENTERPRISE SECURITY & COMPLIANCE -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">SECURITY & GOVERNANCE</span>
      <div class="slide-title">Enterprise Security, Tenant Vault & Data Privacy</div>
      <div class="slide-subtitle">Bank-grade data isolation, encrypted credential vaults, and absolute client privacy guarantees</div>
    </div>
    <div class="header-right">
      <span class="pill">SOC2 Ready</span>
      <span class="pill accent">AES-256 Vault</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Encrypted Tenant Vault</div>
        <span class="card-badge badge-blue">Cryptographic Security</span>
      </div>
      <ul class="bullet-list">
        <li>Bring Your Own Key (BYOK): Store OpenAI, Gemini, or Serper API credentials securely.</li>
        <li>All keys are encrypted at rest using authenticated symmetric AES-256 (Fernet) encryption.</li>
        <li>Masked in all responses (<code>sk-proj-****</code>); never written to application logs.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">AES-256</div>
        <div class="stat-box-desc">Hardware-grade credential security</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">2. Strict Multi-Tenant Isolation</div>
        <span class="card-badge badge-green">Tenant Privacy</span>
      </div>
      <ul class="bullet-list green">
        <li>Mandatory <code>X-Tenant-Id</code> enforced across every application service and database query.</li>
        <li>Zero data cross-pollination: Competitors auditing the same industry can never view your keyword portfolios.</li>
        <li>Role-Based Access Control (RBAC) supporting Enterprise Admin, Analyst, and Viewer permissions.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Zero Leakage</div>
        <div class="stat-box-desc">Strict repository-level isolation</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">3. Model Training Guarantee</div>
        <span class="card-badge badge-purple">Privacy Pledge</span>
      </div>
      <ul class="bullet-list">
        <li>Client crawled data is <strong>never used to train public AI models</strong>.</li>
        <li>All prompt execution calls use zero-data-retention enterprise API endpoints.</li>
        <li>Full audit logs and automated data purge on contract termination.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">100% Private</div>
        <div class="stat-box-desc">Zero training on client data</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 10: Security & Trust</span>
    </div>
    <div class="footer-right">
      <span>Enterprise Governance</span>
      <span class="page-number">11 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 12: AUTOMATED WHITE-LABEL REPORTING -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">AUTOMATION & WHITE-LABEL</span>
      <div class="slide-title">White-Label Branding & Automated Stakeholder Digests</div>
      <div class="slide-subtitle">Deliver automated, branded executive intelligence briefs directly to leadership and client inboxes</div>
    </div>
    <div class="header-right">
      <span class="pill">Agency Ready</span>
      <span class="pill accent">Cron Automated</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">1. Agency White-Labeling</div>
        <span class="card-badge badge-blue">Custom Branding</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Custom Agency Logo:</strong> Replace platform logos with your own agency or corporate brand mark.</li>
        <li><strong>Hex Palette Injection:</strong> Matches your exact primary and accent brand colors across all reports.</li>
        <li><strong>Custom Disclaimers:</strong> Add confidential footers, agency credits, and proprietary notices.</li>
      </ul>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">2. 3 Executive Personas</div>
        <span class="card-badge badge-green">Tailored Tones</span>
      </div>
      <ul class="bullet-list green">
        <li><strong>Executive Digest:</strong> High-level market share, ROI metrics, and board-ready citation growth charts.</li>
        <li><strong>Technical Audit:</strong> Detailed Schema.org markup validation, indexation status, and DOM signal breakdowns.</li>
        <li><strong>Content Strategy Brief:</strong> Unanswered buyer questions, comparison angles, and recommended article topics.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">3. Scheduled Delivery</div>
        <span class="card-badge badge-purple">Zero Maintenance</span>
      </div>
      <ul class="bullet-list">
        <li><strong>Cron Automated Audits:</strong> Set recurring scans (`0 9 * * 1` for weekly Monday morning digests).</li>
        <li><strong>Direct Email Delivery:</strong> Beautifully formatted PDF briefs delivered directly to leadership inboxes.</li>
        <li><strong>Threshold Alerts:</strong> Instant notifications if an AI engine drops a critical brand citation.</li>
      </ul>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 11: Delivery & Reporting</span>
    </div>
    <div class="footer-right">
      <span>White-Label Automation</span>
      <span class="page-number">12 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 13: CASE STUDY & PROVEN IMPACT -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge gold">PROVEN IMPACT</span>
      <div class="slide-title">Case Study: Enterprise AI Visibility Transformation</div>
      <div class="slide-subtitle">How a leading B2B SaaS enterprise scaled generative engine citations from 12% to 74% in 45 days</div>
    </div>
    <div class="header-right">
      <span class="pill">Client Proof</span>
      <span class="pill gold-accent">Documented Results</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">The Challenge (Before)</div>
        <span class="card-badge badge-amber">Baseline</span>
      </div>
      <ul class="bullet-list">
        <li>Ranked top 3 on Google for keywords, but <strong>completely absent from ChatGPT and Perplexity recommendations</strong>.</li>
        <li>Competitors were cited as the "industry standard", bleeding qualified enterprise demo requests.</li>
        <li>AI synthesized inaccurate pricing and claimed lack of multi-region support.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">12%</div>
        <div class="stat-box-desc">Initial AI Mention Rate • GEO Score: 41/100</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">The Strategy Executed</div>
        <span class="card-badge badge-blue">Action</span>
      </div>
      <ul class="bullet-list">
        <li>Deployed comprehensive JSON-LD FAQ schema across 28 core product pages.</li>
        <li>Published structured comparison matrices resolving false pricing hallucinations.</li>
        <li>Unblocked AI crawlers in <code>robots.txt</code> and built dedicated technical specification tables.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">14 Days</div>
        <div class="stat-box-desc">Total implementation sprint duration</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">The Transformation (After)</div>
        <span class="card-badge badge-green">+62% Growth</span>
      </div>
      <ul class="bullet-list green">
        <li>AI mention rate surged to <strong>74% across ChatGPT, Gemini, and Perplexity</strong>.</li>
        <li>Captured direct ground-truth citations on 18 core commercial queries.</li>
        <li>Generated <strong>+42% increase in qualified inbound enterprise demos</strong> within 45 days.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">74%</div>
        <div class="stat-box-desc">Final AI Citation Rate • GEO Score: 89/100</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 12: Proven Client Results</span>
    </div>
    <div class="footer-right">
      <span>Case Study</span>
      <span class="page-number">13 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 14: ENGAGEMENT & PRICING TIERS -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge">COMMERCIAL ENGAGEMENT</span>
      <div class="slide-title">Flexible Engagement & Deployment Tiers</div>
      <div class="slide-subtitle">Tailored options for high-growth enterprises, global corporations, and marketing agencies</div>
    </div>
    <div class="header-right">
      <span class="pill">Transparent Pricing</span>
      <span class="pill accent">Enterprise SLA</span>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-header">
        <div class="card-title">Growth Tier</div>
        <span class="card-badge badge-blue">Fast-Growing Brands</span>
      </div>
      <ul class="bullet-list">
        <li>Up to 2 Brands / Domains.</li>
        <li>500 Crawled Pages per audit.</li>
        <li>Bi-weekly automated multi-model scans (ChatGPT & Gemini).</li>
        <li>Unified GEO Visibility Scorecard & Quick Win checklists.</li>
        <li>Email support with 24-hour turnaround.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Rapid Launch</div>
        <div class="stat-box-desc">Ideal for Series A-C SaaS & Mid-Market</div>
      </div>
    </div>

    <div class="card highlight">
      <div class="card-header">
        <div class="card-title">Enterprise Tier</div>
        <span class="card-badge badge-green">Market Leaders</span>
      </div>
      <ul class="bullet-list green">
        <li>Unlimited Brand Domains & Subdomains.</li>
        <li>Unlimited Crawled Pages with Playwright JS rendering.</li>
        <li>Weekly automated 4-engine scans (OpenAI, Gemini, Claude, Perplexity).</li>
        <li>AES-256 Tenant Vault with Bring-Your-Own-Key.</li>
        <li>Competitor radar & automated email schedules.</li>
        <li>Dedicated Solutions Architect & SLA support.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Most Popular</div>
        <div class="stat-box-desc">Full Enterprise Suite & SLA</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Agency / White-Label</div>
        <span class="card-badge badge-purple">Agencies & Consultancies</span>
      </div>
      <ul class="bullet-list">
        <li>Multi-tenant agency portal with unlimited client accounts.</li>
        <li>Full custom white-label branding (logo, colors, footers).</li>
        <li>Automated client PDF reporting directly under your domain.</li>
        <li>REST API access for custom dashboard integrations.</li>
        <li>Volume wholesale seat discounts.</li>
      </ul>
      <div class="stat-box">
        <div class="stat-box-num">Scale Revenue</div>
        <div class="stat-box-desc">Productize AI SEO for your agency</div>
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 13: Pricing & Engagement</span>
    </div>
    <div class="footer-right">
      <span>Commercial Tiers</span>
      <span class="page-number">14 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 15: WHY CHOOSE US VS COMPETITORS -->
<div class="slide">
  <div class="header-row">
    <div class="header-left">
      <span class="tag-badge emerald">COMPETITIVE COMPARISON</span>
      <div class="slide-title">Why Enterprise Brands Choose Us vs Legacy SEO Tools</div>
      <div class="slide-subtitle">A purpose-built generative AI optimization platform vs legacy keyword research software</div>
    </div>
    <div class="header-right">
      <span class="pill">Market Differentiator</span>
      <span class="pill accent">Generative First</span>
    </div>
  </div>

  <table class="sales-table">
    <thead>
      <tr>
        <th style="width: 28%;">Capability / Dimension</th>
        <th style="width: 24%; color: #38BDF8;">AISEO / GEO Platform (Us)</th>
        <th style="width: 24%;">Legacy SEO Tools (Semrush, Ahrefs)</th>
        <th style="width: 24%;">Traditional SEO Agencies</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Primary Focus</strong></td>
        <td style="color: #34D399; font-weight: 700;">ChatGPT, Gemini, Perplexity & AEO</td>
        <td>Google traditional SERP 10 blue links</td>
        <td>Manual keyword research & blog posts</td>
      </tr>
      <tr>
        <td><strong>AI Model Simulation</strong></td>
        <td style="color: #34D399; font-weight: 700;">Live multi-model prompt matrix</td>
        <td>None (historical Google scrape only)</td>
        <td>Manual copy-pasting into ChatGPT</td>
      </tr>
      <tr>
        <td><strong>Citation Link Auditing</strong></td>
        <td style="color: #34D399; font-weight: 700;">Automated domain citation verification</td>
        <td>None</td>
        <td>None</td>
      </tr>
      <tr>
        <td><strong>Hallucination Defense</strong></td>
        <td style="color: #34D399; font-weight: 700;">Detects false AI pricing/feature claims</td>
        <td>None</td>
        <td>None</td>
      </tr>
      <tr>
        <td><strong>Turnkey Remediation</strong></td>
        <td style="color: #34D399; font-weight: 700;">Ready-to-deploy JSON-LD & matrices</td>
        <td>Generic "add 500 words" advice</td>
        <td>Long retainer contracts with slow delivery</td>
      </tr>
      <tr>
        <td><strong>Architecture & Security</strong></td>
        <td style="color: #34D399; font-weight: 700;">AES-256 Vault, Hexagonal, No Data Training</td>
        <td>Shared cloud database</td>
        <td>Spreadsheets sent over unsecured email</td>
      </tr>
    </tbody>
  </table>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Section 14: Market Superiority</span>
    </div>
    <div class="footer-right">
      <span>Competitive Matrix</span>
      <span class="page-number">15 / 16</span>
    </div>
  </div>
</div>

<!-- SLIDE 16: CALL TO ACTION -->
<div class="slide">
  <div class="header-row" style="border-bottom: none; margin-bottom: 0;">
    <div class="header-left">
      <span class="tag-badge gold">GET STARTED TODAY</span>
    </div>
    <div class="header-right">
      <span class="pill gold-accent">Complimentary Audit</span>
      <span class="pill">Zero Commitment</span>
    </div>
  </div>

  <div class="cover-container" style="padding-right: 0;">
    <div class="cover-badge" style="background: rgba(251, 191, 36, 0.12); border-color: rgba(251, 191, 36, 0.3); color: #FBBF24;">
      ⚡ Secure Your Generative Search Dominance
    </div>
    <h1 class="cover-title" style="font-size: 34px; margin-bottom: 10px;">
      Claim Your Complimentary 48-Hour AI Visibility Audit
    </h1>
    <p class="cover-subtitle" style="font-size: 13px; margin-bottom: 20px;">
      Discover exactly what ChatGPT, Gemini, and Perplexity say about your brand today.
      We will crawl your web domain, simulate 30 real enterprise buyer questions, and deliver your customized 
      <strong>GEO Visibility Scorecard</strong> with prioritized Quick Wins at zero cost or obligation.
    </p>

    <div class="cover-stats-row" style="margin-bottom: 18px;">
      <div class="cover-stat-box" style="border-color: rgba(56, 189, 248, 0.3);">
        <div class="cover-stat-num">1. Submit Domain</div>
        <div class="cover-stat-desc">Provide your target URL and brand name</div>
      </div>
      <div class="cover-stat-box" style="border-color: rgba(52, 211, 153, 0.3);">
        <div class="cover-stat-num">2. Autonomous Audit</div>
        <div class="cover-stat-desc">Our engine scans across 4 commercial AI models</div>
      </div>
      <div class="cover-stat-box" style="border-color: rgba(251, 191, 36, 0.3);">
        <div class="cover-stat-num">3. Executive Review</div>
        <div class="cover-stat-desc">Receive your board-level PDF score & remediation roadmap</div>
      </div>
    </div>

    <div style="background: #0C1220; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 12px 18px; width: 100%; display: flex; justify-content: space-between; align-items: center;">
      <div>
        <div style="font-size: 13px; font-weight: 700; color: #FFFFFF;">Ready to transform your brand into the definitive AI authority?</div>
        <div style="font-size: 10px; color: #94A3B8;">Contact our Enterprise Solutions team to initiate your onboarding pilot.</div>
      </div>
      <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; color: #38BDF8; background: rgba(56, 189, 248, 0.12); padding: 6px 14px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.3);">
        enterprise@aiseo-platform.com
      </div>
    </div>
  </div>

  <div class="footer-row">
    <div class="footer-left">
      <span class="footer-brand">AISEO PLATFORM</span>
      <span>Conclusion & Onboarding Invitation</span>
    </div>
    <div class="footer-right">
      <span>Enterprise Series 2026</span>
      <span class="page-number">16 / 16</span>
    </div>
  </div>
</div>

</body>
</html>
"""
    return html


def build_sales_pdf() -> None:
    html_content = generate_sales_html()
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "AISEO_Enterprise_Sales_Pitch_Deck.html"
    pdf_path = output_dir / "AISEO_Enterprise_Sales_Pitch_Deck.pdf"

    html_path.write_text(html_content, encoding="utf-8")
    print(f"Generated Sales HTML: {html_path.resolve()}")

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
        print("Sales Pitch PDF compilation successful!")
        if pdf_path.exists():
            print(f"Generated PDF: {pdf_path.resolve()} ({pdf_path.stat().st_size} bytes)")


if __name__ == "__main__":
    build_sales_pdf()

