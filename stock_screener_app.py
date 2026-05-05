"""
Stock Screener Desktop App
Parses Stock_Screener.xlsm and generates a self-contained stock_screener.html
that works as a full desktop-quality app in any browser.

Usage: python3 stock_screener_app.py [path/to/Stock_Screener.xlsm]
"""

import zipfile
import xml.etree.ElementTree as ET
import json
import sys
import os
import webbrowser

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

# ── Excel parser ────────────────────────────────────────────────────────────

def load_shared_strings(zf):
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    result = []
    for si in root.findall(f"{{{NS}}}si"):
        text = "".join(t.text or "" for t in si.iter(f"{{{NS}}}t"))
        result.append(text)
    return result


def cell_value(c, shared):
    t = c.get("t", "")
    v = c.find(f"{{{NS}}}v")
    if v is None:
        return None
    raw = v.text
    if t == "s":
        return shared[int(raw)]
    if t == "b":
        return bool(int(raw))
    try:
        return float(raw)
    except (TypeError, ValueError):
        return raw


def parse_sheet(zf, filename, shared):
    root = ET.fromstring(zf.read(f"xl/worksheets/{filename}"))
    rows = []
    for row in root.findall(f".//{{{NS}}}row"):
        cells = {}
        for c in row.findall(f"{{{NS}}}c"):
            ref = c.get("r", "")
            col = "".join(ch for ch in ref if ch.isalpha())
            cells[col] = cell_value(c, shared)
        rows.append(cells)
    return rows


def load_data(xlsm_path):
    zf = zipfile.ZipFile(xlsm_path)
    shared = load_shared_strings(zf)

    # Weights sheet (sheet1)
    w_rows = parse_sheet(zf, "sheet1.xml", shared)
    weights = {}
    for row in w_rows:
        cat = row.get("A")
        wt  = row.get("B")
        if isinstance(cat, str) and isinstance(wt, float):
            weights[cat] = round(wt * 100, 1)

    # Screener sheet (sheet2) — row index 2 = headers, 3+ = data
    s_rows = parse_sheet(zf, "sheet2.xml", shared)
    header_row = s_rows[2] if len(s_rows) > 2 else {}

    col_map = {v: k for k, v in header_row.items() if v}

    stocks = []
    for row in s_rows[3:]:
        ticker = row.get("A")
        if not isinstance(ticker, str) or not ticker.strip():
            continue
        stocks.append({
            "ticker":          ticker,
            "company":         row.get("B") or "",
            "roe":             row.get("C"),
            "roic":            row.get("D"),
            "op_income":       row.get("E"),
            "net_income":      row.get("F"),
            "revenue":         row.get("G"),
            "net_margin":      row.get("H"),
            "op_margin":       row.get("I"),
            "fcf_ni":          row.get("J"),
            "rev_growth":      row.get("K"),
            "eps_growth":      row.get("L"),
            "fwd_eps_growth":  row.get("M"),
            "eps_beat":        row.get("N"),
            "fwd_pe":          row.get("O"),
            "peg":             row.get("P"),
            "ev_ebitda":       row.get("Q"),
            "net_debt_ebitda": row.get("R"),
            "current_ratio":   row.get("S"),
            "earnings_date":   row.get("T") or "",
            "days_to_earn":    row.get("U"),
            "iv_rank":         row.get("V"),
            "open_interest":   row.get("W"),
            "bid_ask":         row.get("X"),
            "score_prof":      row.get("Y"),
            "score_growth":    row.get("Z"),
            "score_val":       row.get("AA"),
            "score_bs":        row.get("AB"),
            "score_cat":       row.get("AC"),
            "score_opts":      row.get("AD"),
            "composite":       row.get("AE"),
            "verdict":         row.get("AF") or "",
            "sizing":          row.get("AG") or "",
            "period":          row.get("AI") or "",
        })

    return weights, stocks


# ── HTML generation ─────────────────────────────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stock Screener</title>
<style>
  :root {
    --bg:       #0f1117;
    --surface:  #1a1d27;
    --surface2: #222636;
    --border:   #2e3350;
    --text:     #e2e8f0;
    --muted:    #8892aa;
    --accent:   #6366f1;
    --green:    #22c55e;
    --yellow:   #eab308;
    --red:      #ef4444;
    --orange:   #f97316;
    --blue:     #38bdf8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; font-size: 13px; }

  /* ── Header ── */
  header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 14px 20px; display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
  header h1 { font-size: 18px; font-weight: 700; color: var(--accent); letter-spacing: 0.5px; }
  header .subtitle { color: var(--muted); font-size: 12px; }

  /* ── Layout ── */
  .layout { display: flex; height: calc(100vh - 55px); overflow: hidden; }
  .sidebar { width: 240px; min-width: 200px; background: var(--surface); border-right: 1px solid var(--border); overflow-y: auto; padding: 16px 14px; flex-shrink: 0; }
  .main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

  /* ── Sidebar ── */
  .sidebar h2 { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); margin-bottom: 10px; }
  .weight-row { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid var(--border); }
  .weight-row:last-child { border-bottom: none; }
  .weight-label { color: var(--text); font-size: 12px; }
  .weight-val { font-size: 12px; font-weight: 600; color: var(--accent); }
  .weight-bar { width: 100%; height: 4px; background: var(--border); border-radius: 2px; margin-top: 3px; }
  .weight-bar-fill { height: 4px; background: var(--accent); border-radius: 2px; }

  .scale-section { margin-top: 18px; }
  .scale-row { display: flex; align-items: center; gap: 8px; padding: 4px 0; font-size: 11px; }
  .scale-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

  .threshold-section { margin-top: 18px; }
  .threshold-row { padding: 5px 0; border-bottom: 1px solid var(--border); font-size: 11px; display: flex; gap: 6px; align-items: center; }
  .threshold-row:last-child { border-bottom: none; }

  /* ── Controls bar ── */
  .controls { padding: 10px 14px; background: var(--surface2); border-bottom: 1px solid var(--border); display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
  .search-box { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 5px 10px; color: var(--text); font-size: 12px; width: 200px; outline: none; }
  .search-box:focus { border-color: var(--accent); }
  .filter-btn { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 5px 12px; color: var(--muted); font-size: 12px; cursor: pointer; transition: all 0.15s; }
  .filter-btn:hover { border-color: var(--accent); color: var(--text); }
  .filter-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 600; }
  .count-badge { margin-left: auto; font-size: 11px; color: var(--muted); }

  /* ── Table ── */
  .table-wrap { flex: 1; overflow: auto; }
  table { width: 100%; border-collapse: collapse; white-space: nowrap; }
  thead { position: sticky; top: 0; z-index: 10; }
  thead tr:first-child th { background: var(--surface); color: var(--muted); font-size: 10px; text-transform: uppercase; letter-spacing: 0.6px; padding: 8px 10px 4px; border-bottom: 1px solid var(--border); text-align: left; }
  thead tr:last-child th { background: var(--surface2); color: var(--text); font-size: 11px; font-weight: 600; padding: 6px 10px 8px; border-bottom: 2px solid var(--border); cursor: pointer; user-select: none; text-align: left; }
  thead tr:last-child th:hover { color: var(--accent); }
  thead th .sort-icon { display: inline-block; margin-left: 3px; color: var(--muted); font-size: 10px; }
  tbody tr { border-bottom: 1px solid var(--border); transition: background 0.1s; }
  tbody tr:hover { background: var(--surface2); }
  tbody td { padding: 7px 10px; vertical-align: middle; }
  .ticker { font-weight: 700; color: var(--blue); font-size: 13px; }
  .company { color: var(--muted); max-width: 200px; overflow: hidden; text-overflow: ellipsis; font-size: 11px; }
  .num { text-align: right; font-variant-numeric: tabular-nums; }
  .na { color: var(--muted); }

  /* ── Score bars ── */
  .score-bar-wrap { display: flex; align-items: center; gap: 5px; }
  .score-bar { width: 40px; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
  .score-bar-fill { height: 6px; border-radius: 3px; }
  .score-num { font-size: 12px; font-weight: 600; min-width: 24px; text-align: right; }

  /* ── Composite score ── */
  .composite-pill { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 700; }

  /* ── Verdict badge ── */
  .verdict-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; letter-spacing: 0.3px; }
  .v-strong-buy { background: rgba(34,197,94,0.15); color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
  .v-buy        { background: rgba(56,189,248,0.15); color: var(--blue); border: 1px solid rgba(56,189,248,0.3); }
  .v-hold       { background: rgba(234,179,8,0.15);  color: var(--yellow); border: 1px solid rgba(234,179,8,0.3); }
  .v-pass       { background: rgba(239,68,68,0.1);   color: var(--red); border: 1px solid rgba(239,68,68,0.2); }

  .eps-beat-y { color: var(--green); font-weight: 600; }
  .eps-beat-n { color: var(--red); }

  /* ── Detail panel ── */
  .detail-panel { display: none; position: fixed; right: 0; top: 0; width: 500px; height: 100vh; background: var(--surface); border-left: 1px solid var(--border); overflow: hidden; z-index: 100; box-shadow: -4px 0 24px rgba(0,0,0,0.5); flex-direction: column; }
  .detail-panel.open { display: flex; }
  .detail-header { padding: 14px 16px 10px; border-bottom: 1px solid var(--border); flex-shrink: 0; }
  .detail-close { float: right; cursor: pointer; color: var(--muted); font-size: 18px; line-height: 1; padding: 2px 6px; border-radius: 4px; }
  .detail-close:hover { background: var(--surface2); color: var(--text); }
  .detail-ticker { font-size: 22px; font-weight: 800; color: var(--blue); margin-top: 4px; }
  .detail-company { color: var(--muted); font-size: 12px; margin-bottom: 8px; }
  /* ── TradingView chart ── */
  .tv-chart-wrap { flex-shrink: 0; height: 300px; border-bottom: 1px solid var(--border); background: #131722; }
  .tv-chart-wrap .tradingview-widget-container { height: 100%; width: 100%; }
  .tv-chart-wrap .tradingview-widget-container__widget { height: calc(100% - 32px); width: 100%; }
  .tv-chart-wrap .tradingview-widget-copyright { font-size: 11px; padding: 4px 8px; }
  /* ── Scrollable detail body ── */
  .detail-body { flex: 1; overflow-y: auto; padding: 16px; }
  .detail-section { margin-bottom: 16px; }
  .detail-section h3 { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); margin-bottom: 8px; padding-bottom: 4px; border-bottom: 1px solid var(--border); }
  .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .detail-field { background: var(--surface2); border-radius: 6px; padding: 8px 10px; }
  .detail-field .label { font-size: 10px; color: var(--muted); margin-bottom: 2px; }
  .detail-field .value { font-size: 13px; font-weight: 600; }
  .detail-scores { display: flex; flex-direction: column; gap: 8px; }
  .detail-score-row { display: flex; align-items: center; gap: 8px; }
  .detail-score-label { width: 100px; font-size: 12px; color: var(--muted); }
  .detail-score-bar { flex: 1; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
  .detail-score-fill { height: 8px; border-radius: 4px; }
  .detail-score-num { font-size: 12px; font-weight: 700; width: 28px; text-align: right; }

  .fmt-million { font-size: 11px; }
</style>
</head>
<body>

<header>
  <div>
    <h1>&#9679; Stock Screener</h1>
    <div class="subtitle">Fundamental scoring · Weighted composite · Auto-ranked</div>
  </div>
</header>

<div class="layout">

  <!-- Sidebar -->
  <div class="sidebar">
    <h2>Category Weights</h2>
    <div id="weights-list"></div>

    <div class="scale-section">
      <h2 style="margin-top:0">Score Scale</h2>
      <div class="scale-row"><span class="scale-dot" style="background:var(--green)"></span><span>5 — Excellent</span></div>
      <div class="scale-row"><span class="scale-dot" style="background:#86efac"></span><span>4 — Above avg</span></div>
      <div class="scale-row"><span class="scale-dot" style="background:var(--yellow)"></span><span>3 — Average</span></div>
      <div class="scale-row"><span class="scale-dot" style="background:var(--orange)"></span><span>2 — Below avg</span></div>
      <div class="scale-row"><span class="scale-dot" style="background:var(--red)"></span><span>1 — Poor</span></div>
    </div>

    <div class="threshold-section">
      <h2 style="margin-top:0">Decision Thresholds</h2>
      <div class="threshold-row"><span class="verdict-badge v-strong-buy">Strong Buy</span><span>&ge; 4.0</span></div>
      <div class="threshold-row"><span class="verdict-badge v-buy">Buy</span><span>3.5 – 3.99</span></div>
      <div class="threshold-row"><span class="verdict-badge v-hold">Hold</span><span>3.0 – 3.49</span></div>
      <div class="threshold-row"><span class="verdict-badge v-pass">Pass</span><span>&lt; 3.0</span></div>
    </div>
  </div>

  <!-- Main area -->
  <div class="main">
    <div class="controls">
      <input class="search-box" id="search" placeholder="Search ticker or company…" />
      <button class="filter-btn active" data-filter="All">All</button>
      <button class="filter-btn" data-filter="Strong Buy">Strong Buy</button>
      <button class="filter-btn" data-filter="Buy">Buy</button>
      <button class="filter-btn" data-filter="Hold/Watch">Hold</button>
      <button class="filter-btn" data-filter="Pass">Pass</button>
      <span class="count-badge" id="count-badge"></span>
    </div>

    <div class="table-wrap">
      <table id="main-table">
        <thead>
          <tr>
            <th colspan="2">Identity</th>
            <th colspan="6">Profitability</th>
            <th colspan="4">Growth</th>
            <th colspan="3">Valuation</th>
            <th colspan="2">Balance Sheet</th>
            <th colspan="2">Catalysts</th>
            <th colspan="3">Options Setup</th>
            <th colspan="6">Category Scores</th>
            <th colspan="3">Output</th>
          </tr>
          <tr id="col-headers"></tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- Detail panel -->
<div class="detail-panel" id="detail-panel">
  <div class="detail-header">
    <span class="detail-close" onclick="closeDetail()">&#x2715;</span>
    <div id="detail-header-content"></div>
  </div>
  <div class="tv-chart-wrap" id="tv-chart-wrap"></div>
  <div class="detail-body" id="detail-content"></div>
</div>

<script>
const WEIGHTS = __WEIGHTS_JSON__;
const STOCKS  = __STOCKS_JSON__;

const COLS = [
  { key: "ticker",          label: "Ticker",        fmt: "ticker" },
  { key: "company",         label: "Company",       fmt: "company" },
  { key: "roe",             label: "ROE %",         fmt: "pct1" },
  { key: "roic",            label: "ROIC %",        fmt: "pct1" },
  { key: "net_margin",      label: "Net Mgn %",     fmt: "pct1" },
  { key: "op_margin",       label: "Op Mgn %",      fmt: "pct1" },
  { key: "fcf_ni",          label: "FCF/NI",        fmt: "x2" },
  { key: "revenue",         label: "Revenue",       fmt: "mil" },
  { key: "rev_growth",      label: "Rev Grw%",      fmt: "pct1" },
  { key: "eps_growth",      label: "EPS Grw%",      fmt: "pct1" },
  { key: "fwd_eps_growth",  label: "Fwd EPS Grw%",  fmt: "pct1" },
  { key: "eps_beat",        label: "EPS Beat?",     fmt: "beat" },
  { key: "fwd_pe",          label: "Fwd P/E",       fmt: "x1" },
  { key: "peg",             label: "PEG",           fmt: "x2" },
  { key: "ev_ebitda",       label: "EV/EBITDA",     fmt: "x1" },
  { key: "net_debt_ebitda", label: "ND/EBITDA",     fmt: "x1" },
  { key: "current_ratio",   label: "Cur Ratio",     fmt: "x2" },
  { key: "days_to_earn",    label: "Days→Earn",     fmt: "int" },
  { key: "iv_rank",         label: "IV Rank%",      fmt: "int" },
  { key: "open_interest",   label: "OI (K)",        fmt: "int" },
  { key: "bid_ask",         label: "Bid-Ask%",      fmt: "x2" },
  { key: "score_prof",      label: "Profit",        fmt: "score" },
  { key: "score_growth",    label: "Growth",        fmt: "score" },
  { key: "score_val",       label: "Val",           fmt: "score" },
  { key: "score_bs",        label: "B/S",           fmt: "score" },
  { key: "score_cat",       label: "Cat",           fmt: "score" },
  { key: "score_opts",      label: "Opts",          fmt: "score" },
  { key: "composite",       label: "Composite",     fmt: "composite" },
  { key: "verdict",         label: "Verdict",       fmt: "verdict" },
  { key: "sizing",          label: "Sizing",        fmt: "text" },
];

let sortKey = "composite", sortAsc = false, activeFilter = "All", searchQ = "";

// ── Formatters ───────────────────────────────────────────────────────────────

function scoreColor(s) {
  if (s == null) return "#666";
  if (s >= 4.5) return "#22c55e";
  if (s >= 3.5) return "#86efac";
  if (s >= 2.5) return "#eab308";
  if (s >= 1.5) return "#f97316";
  return "#ef4444";
}

function compositeColor(v) {
  if (v == null) return "#666";
  if (v >= 4.0) return "#22c55e";
  if (v >= 3.5) return "#86efac";
  if (v >= 3.0) return "#eab308";
  if (v >= 2.0) return "#f97316";
  return "#ef4444";
}

function fmtNum(v, decimals) {
  if (v == null || isNaN(v)) return '<span class="na">—</span>';
  return (v >= 0 ? "" : "") + v.toFixed(decimals);
}

function fmtPct(v) {
  if (v == null || isNaN(v)) return '<span class="na">—</span>';
  const pct = (v * 100).toFixed(1);
  const color = v >= 0 ? "#86efac" : "#f87171";
  return `<span style="color:${color}">${pct}%</span>`;
}

function fmtMil(v) {
  if (v == null || isNaN(v)) return '<span class="na">—</span>';
  const abs = Math.abs(v), sign = v < 0 ? "-" : "";
  if (abs >= 1e9) return `<span class="fmt-million">${sign}$${(abs/1e9).toFixed(1)}B</span>`;
  if (abs >= 1e6) return `<span class="fmt-million">${sign}$${(abs/1e6).toFixed(0)}M</span>`;
  return `<span class="fmt-million">${sign}$${abs.toFixed(0)}</span>`;
}

function fmtScore(s) {
  if (s == null) return '<span class="na">—</span>';
  const pct = ((s - 1) / 4) * 100;
  const col = scoreColor(s);
  return `<div class="score-bar-wrap">
    <div class="score-bar"><div class="score-bar-fill" style="width:${pct}%;background:${col}"></div></div>
    <span class="score-num" style="color:${col}">${s.toFixed(1)}</span>
  </div>`;
}

function fmtComposite(v) {
  if (v == null) return '<span class="na">—</span>';
  const col = compositeColor(v);
  return `<span class="composite-pill" style="background:${col}22;color:${col};border:1px solid ${col}44">${v.toFixed(2)}</span>`;
}

function fmtVerdict(v) {
  const cls = { "Strong Buy": "v-strong-buy", "Buy": "v-buy", "Hold/Watch": "v-hold", "Pass": "v-pass" }[v] || "v-pass";
  return `<span class="verdict-badge ${cls}">${v || "—"}</span>`;
}

function fmtBeat(v) {
  if (!v) return '<span class="na">—</span>';
  if (v === "Y") return '<span class="eps-beat-y">✓ Y</span>';
  if (v === "N") return '<span class="eps-beat-n">✗ N</span>';
  return v;
}

function formatCell(key, fmt, val) {
  switch (fmt) {
    case "ticker":    return `<span class="ticker">${val||"—"}</span>`;
    case "company":   return `<span class="company" title="${val||""}">${val||"—"}</span>`;
    case "pct1":      return fmtPct(val);
    case "x1":        return fmtNum(val, 1);
    case "x2":        return fmtNum(val, 2);
    case "int":       return val != null ? Math.round(val).toString() : '<span class="na">—</span>';
    case "mil":       return fmtMil(val);
    case "score":     return fmtScore(val);
    case "composite": return fmtComposite(val);
    case "verdict":   return fmtVerdict(val);
    case "beat":      return fmtBeat(val);
    case "text":      return `<span style="font-size:11px;color:#8892aa">${val||"—"}</span>`;
    default:          return val != null ? val : '<span class="na">—</span>';
  }
}

// ── Render ───────────────────────────────────────────────────────────────────

function buildHeaders() {
  const tr = document.getElementById("col-headers");
  COLS.forEach(col => {
    const th = document.createElement("th");
    const icon = col.key === sortKey ? (sortAsc ? " ▲" : " ▼") : ' <span style="opacity:0.3">⇅</span>';
    th.innerHTML = col.label + `<span class="sort-icon">${icon}</span>`;
    th.dataset.key = col.key;
    th.addEventListener("click", () => {
      if (sortKey === col.key) sortAsc = !sortAsc;
      else { sortKey = col.key; sortAsc = false; }
      render();
    });
    tr.appendChild(th);
  });
}

function filtered() {
  return STOCKS.filter(s => {
    if (activeFilter !== "All" && s.verdict !== activeFilter) return false;
    if (searchQ) {
      const q = searchQ.toLowerCase();
      if (!s.ticker.toLowerCase().includes(q) && !s.company.toLowerCase().includes(q)) return false;
    }
    return true;
  });
}

function sorted(arr) {
  return [...arr].sort((a, b) => {
    let va = a[sortKey], vb = b[sortKey];
    if (va == null && vb == null) return 0;
    if (va == null) return 1;
    if (vb == null) return -1;
    if (typeof va === "string") return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
    return sortAsc ? va - vb : vb - va;
  });
}

function render() {
  // Update header icons
  const tr = document.getElementById("col-headers");
  tr.innerHTML = "";
  buildHeaderCells();

  const rows = sorted(filtered());
  document.getElementById("count-badge").textContent = `${rows.length} of ${STOCKS.length} stocks`;

  const tbody = document.getElementById("table-body");
  tbody.innerHTML = rows.map(s => {
    const cells = COLS.map(col => `<td class="${col.fmt === 'num' ? 'num' : ''}">${formatCell(col.key, col.fmt, s[col.key])}</td>`).join("");
    return `<tr onclick="showDetail('${s.ticker}')" style="cursor:pointer">${cells}</tr>`;
  }).join("");
}

function buildHeaderCells() {
  const tr = document.getElementById("col-headers");
  COLS.forEach(col => {
    const th = document.createElement("th");
    const isCurrent = col.key === sortKey;
    const icon = isCurrent ? (sortAsc ? " ▲" : " ▼") : ' <span style="opacity:0.3">⇅</span>';
    th.innerHTML = col.label + `<span class="sort-icon">${icon}</span>`;
    th.dataset.key = col.key;
    th.style.color = isCurrent ? "var(--accent)" : "";
    th.addEventListener("click", () => {
      if (sortKey === col.key) sortAsc = !sortAsc;
      else { sortKey = col.key; sortAsc = false; }
      render();
    });
    tr.appendChild(th);
  });
}

// ── Weights sidebar ──────────────────────────────────────────────────────────

function buildWeights() {
  const container = document.getElementById("weights-list");
  const cats = ["Profitability", "Growth", "Valuation", "Balance Sheet", "Catalysts", "Options Setup"];
  cats.forEach(cat => {
    const wt = WEIGHTS[cat] || 0;
    container.innerHTML += `
      <div style="padding:6px 0; border-bottom:1px solid var(--border)">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:12px">${cat}</span>
          <span style="font-size:12px;font-weight:600;color:var(--accent)">${wt}%</span>
        </div>
        <div class="weight-bar"><div class="weight-bar-fill" style="width:${wt}%"></div></div>
      </div>`;
  });
}

// ── Detail panel ─────────────────────────────────────────────────────────────

function showDetail(ticker) {
  const s = STOCKS.find(x => x.ticker === ticker);
  if (!s) return;
  const col = compositeColor(s.composite);
  const scores = [
    { label: "Profitability", key: "score_prof", wt: WEIGHTS["Profitability"] },
    { label: "Growth",        key: "score_growth", wt: WEIGHTS["Growth"] },
    { label: "Valuation",     key: "score_val",  wt: WEIGHTS["Valuation"] },
    { label: "Balance Sheet", key: "score_bs",   wt: WEIGHTS["Balance Sheet"] },
    { label: "Catalysts",     key: "score_cat",  wt: WEIGHTS["Catalysts"] },
    { label: "Options",       key: "score_opts", wt: WEIGHTS["Options Setup"] },
  ];
  const scoreBars = scores.map(sc => {
    const v = s[sc.key];
    const pct = v != null ? ((v - 1) / 4) * 100 : 0;
    const c = scoreColor(v);
    return `<div class="detail-score-row">
      <span class="detail-score-label">${sc.label} <span style="color:var(--muted);font-size:10px">(${sc.wt}%)</span></span>
      <div class="detail-score-bar"><div class="detail-score-fill" style="width:${pct}%;background:${c}"></div></div>
      <span class="detail-score-num" style="color:${c}">${v != null ? v.toFixed(1) : "—"}</span>
    </div>`;
  }).join("");

  function field(label, val) {
    return `<div class="detail-field"><div class="label">${label}</div><div class="value">${val}</div></div>`;
  }
  function pct(v) { return v != null ? (v*100).toFixed(1)+"%" : "—"; }
  function x1(v)  { return v != null ? v.toFixed(1) : "—"; }
  function x2(v)  { return v != null ? v.toFixed(2) : "—"; }

  // Header
  document.getElementById("detail-header-content").innerHTML = `
    <div class="detail-ticker">${s.ticker}</div>
    <div class="detail-company">${s.company}</div>
    <div>${fmtVerdict(s.verdict)} &nbsp; ${fmtComposite(s.composite)}</div>
  `;

  // TradingView chart — recreate the container so the widget re-initialises
  const chartWrap = document.getElementById("tv-chart-wrap");
  chartWrap.innerHTML = "";
  const tvContainer = document.createElement("div");
  tvContainer.className = "tradingview-widget-container";
  const tvWidget = document.createElement("div");
  tvWidget.className = "tradingview-widget-container__widget";
  const tvCopyright = document.createElement("div");
  tvCopyright.className = "tradingview-widget-copyright";
  tvCopyright.innerHTML = `<a href="https://www.tradingview.com/symbols/${encodeURIComponent(s.ticker)}/" rel="noopener nofollow" target="_blank"><span class="blue-text">${s.ticker} chart</span></a><span> by TradingView</span>`;
  const tvScript = document.createElement("script");
  tvScript.type = "text/javascript";
  tvScript.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
  tvScript.async = true;
  tvScript.textContent = JSON.stringify({
    symbol: s.ticker,
    interval: "D",
    timezone: "Etc/UTC",
    theme: "dark",
    style: "1",
    locale: "en",
    backgroundColor: "#131722",
    gridColor: "rgba(99,102,241,0.08)",
    hide_top_toolbar: false,
    hide_side_toolbar: true,
    hide_legend: false,
    hide_volume: false,
    allow_symbol_change: false,
    save_image: true,
    calendar: false,
    withdateranges: false,
    autosize: true
  });
  tvContainer.appendChild(tvWidget);
  tvContainer.appendChild(tvCopyright);
  tvContainer.appendChild(tvScript);
  chartWrap.appendChild(tvContainer);

  // Scrollable body
  document.getElementById("detail-content").innerHTML = `
    <div class="detail-section">
      <h3>Scoring Breakdown</h3>
      <div class="detail-scores">${scoreBars}</div>
    </div>
    <div class="detail-section">
      <h3>Profitability</h3>
      <div class="detail-grid">
        ${field("ROE %", pct(s.roe))}
        ${field("ROIC %", pct(s.roic))}
        ${field("Net Margin %", pct(s.net_margin))}
        ${field("Op Margin %", pct(s.op_margin))}
        ${field("FCF / NI", x2(s.fcf_ni))}
        ${field("Revenue", s.revenue != null ? "$"+(s.revenue/1e9).toFixed(2)+"B" : "—")}
      </div>
    </div>
    <div class="detail-section">
      <h3>Growth</h3>
      <div class="detail-grid">
        ${field("Rev Growth YoY", pct(s.rev_growth))}
        ${field("EPS Growth YoY", pct(s.eps_growth))}
        ${field("Fwd EPS Growth", pct(s.fwd_eps_growth))}
        ${field("Last EPS Beat?", s.eps_beat || "—")}
      </div>
    </div>
    <div class="detail-section">
      <h3>Valuation</h3>
      <div class="detail-grid">
        ${field("Fwd P/E", x1(s.fwd_pe))}
        ${field("PEG", x2(s.peg))}
        ${field("EV/EBITDA", x1(s.ev_ebitda))}
      </div>
    </div>
    <div class="detail-section">
      <h3>Balance Sheet</h3>
      <div class="detail-grid">
        ${field("Net Debt/EBITDA", x1(s.net_debt_ebitda))}
        ${field("Current Ratio", x2(s.current_ratio))}
      </div>
    </div>
    <div class="detail-section">
      <h3>Catalysts &amp; Options</h3>
      <div class="detail-grid">
        ${field("Earnings Date", s.earnings_date || "—")}
        ${field("Days to Earn", s.days_to_earn != null ? Math.round(s.days_to_earn)+"d" : "—")}
        ${field("IV Rank %", s.iv_rank != null ? Math.round(s.iv_rank)+"%" : "—")}
        ${field("Open Interest", s.open_interest != null ? Math.round(s.open_interest)+"K" : "—")}
        ${field("Bid-Ask Spread", s.bid_ask != null ? s.bid_ask.toFixed(2)+"%" : "—")}
      </div>
    </div>
    <div class="detail-section">
      <h3>Trade Recommendation</h3>
      <div style="background:var(--surface2);border-radius:6px;padding:10px 12px;font-size:12px;color:var(--text)">${s.sizing || "—"}</div>
    </div>
  `;
  document.getElementById("detail-panel").classList.add("open");
}

function closeDetail() {
  document.getElementById("detail-panel").classList.remove("open");
}

// ── Filter buttons ───────────────────────────────────────────────────────────

document.querySelectorAll(".filter-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    activeFilter = btn.dataset.filter;
    render();
  });
});

document.getElementById("search").addEventListener("input", e => {
  searchQ = e.target.value.trim();
  render();
});

// ── Init ─────────────────────────────────────────────────────────────────────

buildWeights();
buildHeaderCells();
render();
document.getElementById("count-badge").textContent = `${STOCKS.length} of ${STOCKS.length} stocks`;
</script>
</body>
</html>
"""


def generate_html(weights, stocks, output_path):
    html = HTML_TEMPLATE
    html = html.replace("__WEIGHTS_JSON__", json.dumps(weights, indent=2))
    html = html.replace("__STOCKS_JSON__",  json.dumps(stocks,  indent=2))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    xlsm_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "Stock_Screener.xlsm")
    if not os.path.exists(xlsm_path):
        print(f"Error: file not found: {xlsm_path}")
        sys.exit(1)

    out_path = os.path.join(script_dir, "stock_screener.html")

    print(f"Parsing {xlsm_path} ...")
    weights, stocks = load_data(xlsm_path)
    print(f"  {len(stocks)} stocks loaded, {len(weights)} weight categories")

    print(f"Generating {out_path} ...")
    generate_html(weights, stocks, out_path)
    print(f"Done. Open stock_screener.html in your browser.")

    try:
        webbrowser.open(f"file://{out_path}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
