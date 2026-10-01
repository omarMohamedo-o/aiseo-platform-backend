import React, { useEffect, useState } from "react";
import {
  Bell,
  Calendar,
  CheckCircle2,
  Clock,
  Mail,
  Palette,
  Plus,
  Send,
  Trash2,
} from "lucide-react";
import {
  apiClient,
  ReportBranding,
  ReportSchedule,
} from "@/api/client";

export const EmailReportsTab: React.FC = () => {
  const [schedules, setSchedules] = useState<ReportSchedule[]>([]);
  const [branding, setBranding] = useState<ReportBranding>({
    company_name: "",
    logo_url: "",
    primary_color: "#b6f36a",
    accent_color: "#38bdf8",
    support_email: "",
    footer_text: "",
  });

  const [testEmail, setTestEmail] = useState("");
  const [sendingTest, setSendingTest] = useState(false);
  const [testSuccess, setTestSuccess] = useState(false);

  const [isCreatingSchedule, setIsCreatingSchedule] = useState(false);
  const [newSchedule, setNewSchedule] = useState({
    name: "",
    cron_expression: "0 8 * * 1",
    recipients: "",
    report_type: "weekly-digest",
    tone: "executive",
  });

  const [savingBranding, setSavingBranding] = useState(false);

  const loadData = async () => {
    try {
      const [schedulesRes, brandingRes] = await Promise.all([
        apiClient.getSchedules(),
        apiClient.getBranding(),
      ]);
      setSchedules(schedulesRes || []);
      if (brandingRes) setBranding(brandingRes);
    } catch (err) {
      console.error("Failed to load email reports data", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSendTestEmail = async () => {
    if (!testEmail) return;
    setSendingTest(true);
    setTestSuccess(false);
    try {
      await apiClient.sendTestEmail(testEmail, "weekly-digest");
      setTestSuccess(true);
      setTimeout(() => setTestSuccess(false), 5000);
    } catch (err) {
      console.error("Failed to dispatch test email", err);
    } finally {
      setSendingTest(false);
    }
  };

  const handleCreateSchedule = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const recipientList = newSchedule.recipients
        .split(",")
        .map((r) => r.trim())
        .filter(Boolean);

      const created = await apiClient.createSchedule({
        name: newSchedule.name,
        cron_expression: newSchedule.cron_expression,
        recipients: recipientList,
        report_type: newSchedule.report_type,
        tone: newSchedule.tone,
      });

      setSchedules((prev) => [created, ...prev]);
      setIsCreatingSchedule(false);
    } catch (err) {
      console.error("Failed to create schedule", err);
    }
  };

  const handleDeleteSchedule = async (id: string) => {
    try {
      await apiClient.deleteSchedule(id);
      setSchedules((prev) => prev.filter((s) => s.id !== id));
    } catch (err) {
      console.error("Failed to delete schedule", err);
    }
  };

  const handleSaveBranding = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingBranding(true);
    try {
      const updated = await apiClient.saveBranding(branding);
      setBranding(updated);
    } catch (err) {
      console.error("Failed to save branding", err);
    } finally {
      setSavingBranding(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header and Fast Test Email Dispatch */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
            <Mail className="w-5 h-5 text-primary" />
            Automated Email Reports & Scheduled Delivery
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Deliver white-labeled AI visibility digests directly to stakeholders via Resend API
          </p>
        </div>

        <div className="flex items-center gap-2">
          <input
            type="email"
            value={testEmail}
            onChange={(e) => setTestEmail(e.target.value)}
            placeholder="stakeholder@company.com"
            className="bg-slate-900 dark:bg-slate-50 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-slate-50 placeholder-slate-400 focus:outline-none focus:border-primary w-64"
          />
          <button
            onClick={handleSendTestEmail}
            disabled={sendingTest || !testEmail}
            className="px-4 py-2 rounded-xl bg-primary hover:bg-lime-400 text-slate-950 text-xs font-bold flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            {sendingTest ? "Sending..." : "Send Test Report"}
          </button>
        </div>
      </div>

      {testSuccess && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>Branded test report dispatched successfully via Resend adapter!</span>
        </div>
      )}

      {/* Schedules & White-Label Branding 2-Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Scheduled Reports Table */}
        <div className="lg:col-span-2 space-y-4">
          <div className="glass-panel p-6 rounded-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <Clock className="w-4 h-4 text-blue-400" />
                Active Distribution Schedules ({schedules.length})
              </h3>
              <button
                onClick={() => setIsCreatingSchedule(!isCreatingSchedule)}
                className="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 transition-all"
              >
                <Plus className="w-3.5 h-3.5" />
                New Schedule
              </button>
            </div>

            {/* Create Schedule Modal / Drawer Inline */}
            {isCreatingSchedule && (
              <form onSubmit={handleCreateSchedule} className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 space-y-3 mb-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                      Schedule Name
                    </label>
                    <input
                      type="text"
                      value={newSchedule.name}
                      onChange={(e) => setNewSchedule({ ...newSchedule, name: e.target.value })}
                      className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                      required
                    />
                  </div>
                  <div>
                    <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                      Cron Schedule Expression
                    </label>
                    <input
                      type="text"
                      value={newSchedule.cron_expression}
                      onChange={(e) => setNewSchedule({ ...newSchedule, cron_expression: e.target.value })}
                      placeholder="0 8 * * 1 (Every Monday at 8 AM)"
                      className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                    Recipients (comma separated emails)
                  </label>
                  <input
                    type="text"
                    value={newSchedule.recipients}
                    onChange={(e) => setNewSchedule({ ...newSchedule, recipients: e.target.value })}
                    className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                    required
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setIsCreatingSchedule(false)}
                    className="px-3 py-1.5 rounded-lg text-xs text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-1.5 rounded-lg bg-primary text-slate-950 text-xs font-bold"
                  >
                    Create Distribution Schedule
                  </button>
                </div>
              </form>
            )}

            {/* Schedules List */}
            <div className="space-y-2.5">
              {schedules.map((s) => (
                <div
                  key={s.id}
                  className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-slate-900 dark:text-slate-50">{s.name}</span>
                      <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono">
                        Active
                      </span>
                    </div>
                    <div className="flex items-center gap-3 text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                      <span>Cron: {s.cron_expression}</span>
                      <span>•</span>
                      <span>{s.recipients.length} Recipients: {s.recipients.join(", ")}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleDeleteSchedule(s.id)}
                    className="p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                    title="Delete Schedule"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Custom Branding Configuration */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50 mb-4 flex items-center gap-2">
              <Palette className="w-4 h-4 text-purple-400" />
              White-Label Report Branding
            </h3>

            <form onSubmit={handleSaveBranding} className="space-y-3.5">
              <div>
                <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                  Company / Organization Name
                </label>
                <input
                  type="text"
                  value={branding.company_name}
                  onChange={(e) => setBranding({ ...branding, company_name: e.target.value })}
                  className="w-full bg-slate-900 dark:bg-slate-50 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                />
              </div>

              <div>
                <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                  Logo Image URL
                </label>
                <input
                  type="text"
                  value={branding.logo_url}
                  onChange={(e) => setBranding({ ...branding, logo_url: e.target.value })}
                  className="w-full bg-slate-900 dark:bg-slate-50 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                    Primary Brand Color
                  </label>
                  <div className="flex items-center gap-2">
                    <input
                      type="color"
                      value={branding.primary_color}
                      onChange={(e) => setBranding({ ...branding, primary_color: e.target.value })}
                      className="w-7 h-7 rounded border-0 bg-transparent cursor-pointer"
                    />
                    <span className="text-xs font-mono text-slate-600 dark:text-slate-400">{branding.primary_color}</span>
                  </div>
                </div>
                <div>
                  <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                    Accent Color
                  </label>
                  <div className="flex items-center gap-2">
                    <input
                      type="color"
                      value={branding.accent_color}
                      onChange={(e) => setBranding({ ...branding, accent_color: e.target.value })}
                      className="w-7 h-7 rounded border-0 bg-transparent cursor-pointer"
                    />
                    <span className="text-xs font-mono text-slate-600 dark:text-slate-400">{branding.accent_color}</span>
                  </div>
                </div>
              </div>

              <div>
                <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                  Support Reply-To Email
                </label>
                <input
                  type="email"
                  value={branding.support_email}
                  onChange={(e) => setBranding({ ...branding, support_email: e.target.value })}
                  className="w-full bg-slate-900 dark:bg-slate-50 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                />
              </div>

              <button
                type="submit"
                disabled={savingBranding}
                className="w-full py-2.5 mt-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all disabled:opacity-50"
              >
                {savingBranding ? "Saving..." : "Save Branding Configuration"}
              </button>
            </form>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-700 text-[10px] text-slate-500 dark:text-slate-400 font-mono text-center">
            Rendered server-side with Resend templates
          </div>
        </div>
      </div>
    </div>
  );
};
