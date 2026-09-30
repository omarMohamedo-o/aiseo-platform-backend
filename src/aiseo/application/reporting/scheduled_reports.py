"""Application service for managing report schedules, rendering branded HTML emails, and delivery."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from aiseo.application.reporting.opportunity_scorer import OpportunityScorerService
from aiseo.application.reporting.report_generator import ReportGeneratorService
from aiseo.domain.reporting.report_models import (
    OpportunityScore,
    ReportBranding,
    ReportKeyword,
    ReportSchedule,
    ReportSummary,
    ReportToneType,
)
from aiseo.ports.notifications.email_port import EmailPort


def render_report_html(
    summary: ReportSummary,
    schedule_name: str,
    branding: ReportBranding,
    scores: list[OpportunityScore],
) -> str:
    """Render a responsive HTML email report with corporate white-label branding."""
    accent = branding.accent_color or "#1689e8"
    company = branding.company_name or "SignalOS"
    logo_tag = (
        f'<img src="{branding.logo_url}" alt="{company}" style="max-height:42px;max-width:180px;object-fit:contain;margin-bottom:12px" />'
        if branding.logo_url
        else ""
    )

    insights_html = "".join(f"<li style='margin-bottom:6px;'>{item}</li>" for item in summary.insights)
    actions_html = "".join(f"<li style='margin-bottom:6px;'>{item}</li>" for item in summary.actions)

    score_rows = "".join(
        f"<tr>"
        f"<td style='padding:8px;border-bottom:1px solid #e2e8f0;font-weight:500;'>{s.keyword}</td>"
        f"<td style='padding:8px;border-bottom:1px solid #e2e8f0;color:#2563eb;font-weight:700;'>{s.score}/100</td>"
        f"<td style='padding:8px;border-bottom:1px solid #e2e8f0;color:#64748b;'>{s.volume}</td>"
        f"<td style='padding:8px;border-bottom:1px solid #e2e8f0;color:#64748b;'>{s.difficulty:.0f}</td>"
        f"</tr>"
        for s in scores[:15]
    )

    now_formatted = datetime.now(UTC).strftime("%b %d, %Y")

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{company} · AI Visibility Report</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #1e293b; padding: 24px; margin: 0;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 680px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
    <!-- Header -->
    <tr>
      <td style="border-top: 6px solid {accent}; padding: 28px 32px 18px 32px;">
        {logo_tag}
        <h1 style="margin: 0 0 6px 0; font-size: 24px; font-weight: 700; color: #0f172a;">{company} · AI Visibility Brief</h1>
        <p style="margin: 0; color: #64748b; font-size: 14px;">{schedule_name} · Generated on {now_formatted}</p>
      </td>
    </tr>
    <!-- Executive Headline & Summary -->
    <tr>
      <td style="padding: 12px 32px 20px 32px;">
        <div style="background-color: #f1f5f9; padding: 18px 22px; border-radius: 8px; border-left: 4px solid {accent};">
          <h2 style="margin: 0 0 8px 0; font-size: 17px; font-weight: 600; color: #1e293b;">{summary.headline}</h2>
          <p style="margin: 0; font-size: 14px; line-height: 1.5; color: #475569;">{summary.summary}</p>
        </div>
      </td>
    </tr>
    <!-- Insights & Actions -->
    <tr>
      <td style="padding: 0 32px 20px 32px;">
        <h3 style="margin: 16px 0 10px 0; font-size: 15px; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Key Observations</h3>
        <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #334155; line-height: 1.5;">
          {insights_html}
        </ul>
        <h3 style="margin: 20px 0 10px 0; font-size: 15px; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Action Items</h3>
        <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #334155; line-height: 1.5;">
          {actions_html}
        </ul>
      </td>
    </tr>
    <!-- Opportunity Scores Table -->
    <tr>
      <td style="padding: 0 32px 28px 32px;">
        <h3 style="margin: 16px 0 12px 0; font-size: 15px; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Opportunity Scoreboard</h3>
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; font-size: 13px;">
          <thead>
            <tr style="background-color: #f8fafc; text-align: left; color: #64748b;">
              <th style="padding: 8px; border-bottom: 2px solid #e2e8f0;">Keyword</th>
              <th style="padding: 8px; border-bottom: 2px solid #e2e8f0;">Score</th>
              <th style="padding: 8px; border-bottom: 2px solid #e2e8f0;">Volume</th>
              <th style="padding: 8px; border-bottom: 2px solid #e2e8f0;">Difficulty</th>
            </tr>
          </thead>
          <tbody>
            {score_rows}
          </tbody>
        </table>
      </td>
    </tr>
    <!-- Footer -->
    <tr>
      <td style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 18px 32px; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #94a3b8;">{branding.footer_text}</p>
      </td>
    </tr>
  </table>
</body>
</html>"""


class ScheduledReportsService:
    """Orchestrates scheduled report configuration, rendering, and automated email dispatch."""

    def __init__(
        self,
        email_adapter: EmailPort,
        report_generator: ReportGeneratorService,
        opportunity_scorer: OpportunityScorerService,
    ) -> None:
        self._email = email_adapter
        self._generator = report_generator
        self._scorer = opportunity_scorer
        # In-memory stores for schedules and branding per tenant
        self._schedules: dict[tuple[str, str], ReportSchedule] = {}
        self._branding: dict[str, ReportBranding] = {}

    def get_branding(self, tenant_id: str) -> ReportBranding:
        return self._branding.get(tenant_id, ReportBranding())

    def save_branding(self, tenant_id: str, branding: ReportBranding) -> ReportBranding:
        self._branding[tenant_id] = branding
        return branding

    def list_schedules(self, tenant_id: str) -> list[ReportSchedule]:
        return [s for (t, _), s in self._schedules.items() if t == tenant_id]

    def create_schedule(
        self,
        tenant_id: str,
        name: str,
        cron: str,
        recipient_email: str,
        tone: ReportToneType = "executive",
        keywords: list[ReportKeyword] | None = None,
    ) -> ReportSchedule:
        schedule_id = str(uuid.uuid4())[:8]
        branding = self.get_branding(tenant_id)
        sched = ReportSchedule(
            id=schedule_id,
            tenant_id=tenant_id,
            name=name,
            cron=cron,
            recipient_email=recipient_email,
            tone=tone,
            enabled=True,
            branding=branding,
            keywords=keywords or [],
        )
        self._schedules[(tenant_id, schedule_id)] = sched
        return sched

    def delete_schedule(self, tenant_id: str, schedule_id: str) -> bool:
        return self._schedules.pop((tenant_id, schedule_id), None) is not None

    async def execute_report_run(
        self,
        tenant_id: str,
        schedule_id: str,
    ) -> bool:
        sched = self._schedules.get((tenant_id, schedule_id))
        if not sched or not sched.enabled:
            return False

        branding = self.get_branding(tenant_id)
        scores, _ = self._scorer.score_keywords(tenant_id, sched.keywords)
        summary = await self._generator.generate_summary(sched.keywords, tone=sched.tone)

        html = render_report_html(summary, sched.name, branding, scores)
        text = f"{summary.headline}\n\n{summary.summary}\n\n" + "\n".join(summary.actions)

        subject = f"{branding.company_name} · {sched.name}"
        return await self._email.send_email(
            to=[sched.recipient_email],
            subject=subject,
            html=html,
            text=text,
        )

    async def send_test_report(
        self,
        tenant_id: str,
        recipient_email: str,
        tone: ReportToneType = "executive",
        keywords: list[ReportKeyword] | None = None,
    ) -> bool:
        """Trigger an instant one-click test report email."""
        kw_list = keywords or [
            ReportKeyword(keyword="ai visibility", volume="12,000", difficulty=45, cpc="$4.50", serp_features=4),
            ReportKeyword(keyword="answer engine optimization", volume="8,500", difficulty=32, cpc="$3.20", serp_features=3),
            ReportKeyword(keyword="generative engine optimization", volume="15,400", difficulty=55, cpc="$6.80", serp_features=5),
        ]

        branding = self.get_branding(tenant_id)
        scores, _ = self._scorer.score_keywords(tenant_id, kw_list)
        summary = await self._generator.generate_summary(kw_list, tone=tone)

        html = render_report_html(summary, "Test Email Verification", branding, scores)
        text = f"{summary.headline}\n\n{summary.summary}\n\n" + "\n".join(summary.actions)

        subject = f"[TEST] {branding.company_name} · AI Visibility Report"
        return await self._email.send_email(
            to=[recipient_email],
            subject=subject,
            html=html,
            text=text,
        )
