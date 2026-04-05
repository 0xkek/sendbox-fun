"""
Generate a local dashboard HTML for tracking directory submissions.
Opens in browser, provides copy-paste text for each field, and tracks status.
"""
import json
import html
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
SUBMISSIONS_JSON = ROOT / "submissions.json"
DASHBOARD_HTML = ROOT / "dashboard.html"


def esc(s):
    return html.escape(str(s) if s else "", quote=True)


def render_dashboard(data):
    site = data["site"]
    dirs = data["directories"]

    submitted = sum(1 for d in dirs if d["status"] != "not_submitted")
    approved = sum(1 for d in dirs if d["status"] == "approved")

    rows = []
    for d in dirs:
        status_color = {
            "not_submitted": "#6B7280",
            "submitted": "#F59E0B",
            "approved": "#10B981",
            "rejected": "#DC2626",
        }.get(d["status"], "#6B7280")
        status_label = d["status"].replace("_", " ").title()
        date_str = d["submitted_date"] or "—"
        rows.append(f"""
        <tr data-id="{esc(d['id'])}">
          <td><strong>{esc(d['name'])}</strong><br><span style="font-size:12px;color:#6B7280;">{esc(d['notes'])}</span></td>
          <td><span class="status" style="background:{status_color}20;color:{status_color};">{esc(status_label)}</span></td>
          <td>{esc(date_str)}</td>
          <td>
            <a href="{esc(d['submit_url'])}" target="_blank" class="btn-primary">Open form</a>
            <button onclick="copyAll('{esc(d['id'])}')" class="btn-secondary">Copy fields</button>
            <button onclick="markSubmitted('{esc(d['id'])}')" class="btn-status">Mark submitted</button>
            <button onclick="markApproved('{esc(d['id'])}')" class="btn-status">Approved</button>
          </td>
        </tr>""")

    # Copy-to-clipboard fields for each directory
    js_data = json.dumps({
        "site": site,
        "dirs": {d["id"]: d for d in dirs}
    })

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>sendbox.fun — Directory Submission Tracker</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #FAFAF9; color: #1A1A2E; padding: 40px 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; }}
.subtitle {{ color: #6B7280; margin-bottom: 32px; }}
.stats {{ display: flex; gap: 24px; margin-bottom: 32px; }}
.stat {{ background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px 28px; }}
.stat-num {{ font-size: 28px; font-weight: 800; color: #7C3AED; }}
.stat-label {{ font-size: 13px; color: #6B7280; text-transform: uppercase; font-weight: 600; }}
.card {{ background: white; border: 1px solid #E5E7EB; border-radius: 16px; padding: 24px; margin-bottom: 24px; }}
.card h2 {{ font-size: 18px; font-weight: 700; margin-bottom: 16px; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ text-align: left; padding: 12px; font-size: 12px; text-transform: uppercase; color: #6B7280; font-weight: 700; letter-spacing: 0.5px; border-bottom: 2px solid #E5E7EB; }}
td {{ padding: 16px 12px; border-bottom: 1px solid #E5E7EB; vertical-align: top; font-size: 14px; }}
tr:last-child td {{ border-bottom: none; }}
.status {{ display: inline-block; padding: 4px 10px; border-radius: 99px; font-size: 12px; font-weight: 600; }}
.btn-primary, .btn-secondary, .btn-status {{ display: inline-block; padding: 8px 14px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; border: none; margin-right: 6px; margin-bottom: 4px; text-decoration: none; font-family: inherit; }}
.btn-primary {{ background: #7C3AED; color: white; }}
.btn-primary:hover {{ background: #6D28D9; }}
.btn-secondary {{ background: #EDE9FE; color: #7C3AED; }}
.btn-status {{ background: #F3F4F6; color: #374151; }}
.btn-status:hover {{ background: #E5E7EB; }}
.field-list {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.field {{ background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px 16px; }}
.field-label {{ font-size: 12px; color: #6B7280; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; }}
.field-value {{ font-size: 14px; color: #1A1A2E; word-break: break-word; }}
.field-actions {{ margin-top: 6px; }}
.copy-btn {{ background: white; border: 1px solid #E5E7EB; border-radius: 6px; padding: 4px 10px; font-size: 12px; cursor: pointer; font-family: inherit; }}
.copy-btn:hover {{ border-color: #7C3AED; color: #7C3AED; }}
.toast {{ position: fixed; bottom: 24px; right: 24px; background: #10B981; color: white; padding: 12px 20px; border-radius: 8px; font-weight: 600; transform: translateY(100px); opacity: 0; transition: all 0.3s; }}
.toast.show {{ transform: translateY(0); opacity: 1; }}
.instructions {{ background: #EDE9FE; border-left: 4px solid #7C3AED; padding: 16px 20px; border-radius: 8px; margin-bottom: 24px; font-size: 14px; line-height: 1.6; }}
</style>
</head>
<body>
<div class="container">
  <h1>🚀 Directory Submission Tracker</h1>
  <p class="subtitle">sendbox.fun — submit to {len(dirs)} directories to grow traffic and backlinks</p>

  <div class="stats">
    <div class="stat"><div class="stat-num">{submitted}/{len(dirs)}</div><div class="stat-label">Submitted</div></div>
    <div class="stat"><div class="stat-num">{approved}</div><div class="stat-label">Approved</div></div>
    <div class="stat"><div class="stat-num">{len(dirs) - submitted}</div><div class="stat-label">Remaining</div></div>
  </div>

  <div class="instructions">
    <strong>Workflow:</strong> Click <strong>Open form</strong> for a directory → it opens in a new tab.
    Come back here, click <strong>Copy fields</strong>. Now paste fields into the form (Tab to move between fields, Cmd+V to paste).
    Solve the CAPTCHA, click Submit, then click <strong>Mark submitted</strong> here.
  </div>

  <div class="card">
    <h2>📝 Your site info (auto-filled into every form)</h2>
    <div class="field-list">
      <div class="field">
        <div class="field-label">Name</div>
        <div class="field-value" id="field-name">{esc(site['name'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText('{esc(site['name'])}')">Copy</button></div>
      </div>
      <div class="field">
        <div class="field-label">URL</div>
        <div class="field-value">{esc(site['url'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText('{esc(site['url'])}')">Copy</button></div>
      </div>
      <div class="field">
        <div class="field-label">Tagline</div>
        <div class="field-value">{esc(site['tagline'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText({json.dumps(site['tagline'])})">Copy</button></div>
      </div>
      <div class="field">
        <div class="field-label">Category</div>
        <div class="field-value">{esc(site['category'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText({json.dumps(site['category'])})">Copy</button></div>
      </div>
      <div class="field" style="grid-column:1/-1;">
        <div class="field-label">Short Description</div>
        <div class="field-value">{esc(site['short_desc'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText({json.dumps(site['short_desc'])})">Copy</button></div>
      </div>
      <div class="field" style="grid-column:1/-1;">
        <div class="field-label">Long Description</div>
        <div class="field-value">{esc(site['long_desc'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText({json.dumps(site['long_desc'])})">Copy</button></div>
      </div>
      <div class="field">
        <div class="field-label">Logo URL</div>
        <div class="field-value">{esc(site['logo_url'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText('{esc(site['logo_url'])}')">Copy</button></div>
      </div>
      <div class="field">
        <div class="field-label">Pricing</div>
        <div class="field-value">{esc(site['pricing'])}</div>
        <div class="field-actions"><button class="copy-btn" onclick="copyText('{esc(site['pricing'])}')">Copy</button></div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>🎯 Directories</h2>
    <table>
      <thead>
        <tr><th>Directory</th><th>Status</th><th>Submitted</th><th>Actions</th></tr>
      </thead>
      <tbody>{"".join(rows)}</tbody>
    </table>
  </div>
</div>

<div class="toast" id="toast">Copied!</div>

<script>
const data = {js_data};
const STORAGE_KEY = 'sendbox-submissions';

function loadStatus() {{
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) return;
  const s = JSON.parse(saved);
  Object.entries(s).forEach(([id, status]) => {{
    const row = document.querySelector(`tr[data-id="${{id}}"]`);
    if (row && status.status) {{
      const cell = row.querySelector('.status');
      const colors = {{ not_submitted: '#6B7280', submitted: '#F59E0B', approved: '#10B981', rejected: '#DC2626' }};
      cell.style.background = colors[status.status] + '20';
      cell.style.color = colors[status.status];
      cell.textContent = status.status.replace('_', ' ').replace(/\\b\\w/g, c => c.toUpperCase());
      if (status.date) row.children[2].textContent = status.date;
    }}
  }});
  updateStats();
}}

function saveStatus(id, status) {{
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
  saved[id] = {{ status, date: status !== 'not_submitted' ? new Date().toISOString().split('T')[0] : null }};
  localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
  loadStatus();
}}

function updateStats() {{
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
  const total = document.querySelectorAll('tr[data-id]').length;
  let submitted = 0, approved = 0;
  Object.values(saved).forEach(s => {{
    if (s.status && s.status !== 'not_submitted') submitted++;
    if (s.status === 'approved') approved++;
  }});
  document.querySelectorAll('.stat-num')[0].textContent = submitted + '/' + total;
  document.querySelectorAll('.stat-num')[1].textContent = approved;
  document.querySelectorAll('.stat-num')[2].textContent = total - submitted;
}}

function markSubmitted(id) {{ saveStatus(id, 'submitted'); showToast('Marked as submitted'); }}
function markApproved(id) {{ saveStatus(id, 'approved'); showToast('🎉 Marked as approved'); }}

function copyText(text) {{
  navigator.clipboard.writeText(text).then(() => showToast('Copied!'));
}}

function copyAll(dirId) {{
  const text = `Name: ${{data.site.name}}
URL: ${{data.site.url}}
Tagline: ${{data.site.tagline}}
Category: ${{data.site.category}}
Pricing: ${{data.site.pricing}}

Short description:
${{data.site.short_desc}}

Long description:
${{data.site.long_desc}}

Logo: ${{data.site.logo_url}}`;
  navigator.clipboard.writeText(text).then(() => showToast('All fields copied to clipboard'));
}}

function showToast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}}

loadStatus();
</script>
</body>
</html>"""


def main():
    with open(SUBMISSIONS_JSON) as f:
        data = json.load(f)

    html_out = render_dashboard(data)
    DASHBOARD_HTML.write_text(html_out, encoding="utf-8")
    print(f"Dashboard: file://{DASHBOARD_HTML}")
    print(f"Tracking {len(data['directories'])} directories")


if __name__ == "__main__":
    main()
