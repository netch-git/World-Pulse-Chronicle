#!/usr/bin/env python3
"""
World Pulse Chronicle - Autonomous Overnight Harvester & Discovery Daemon
==========================================================================
このスクリプトは、国際オープンデータ（World Bank, CCKP, FAOSTAT, OECD, yfinance）
を自律的・貪欲に収集し、Gemini 3.8 Flash (google-genai SDK / Structured Outputs)
と最先端データサイエンス分析（ピアソン相関係数、時系列先行ラグ、レジーム転換点）
を統合して、新規因果関係テーマを連続自動生成・蓄積する自律型デーモンである。

ユーザー指示仕様:
「午前4時の時点で稼働しているテーマの生成完了をもって一度停止して私が確認する。
 それまでは自律的にオープンデータをどん欲に探すこと。
 可視化の方法についても、常に最新のデータサイエンス、データビジュアライズの技法を学んで実装する事。」

使用方法:
  python autonomous_harvester.py --until-hour 4 --interval-minutes 15
"""

import argparse
import asyncio
import datetime
import json
import logging
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Add base and backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))

from backend.main import (
    collect_all_10_themes_payload,
    compute_data_science_metrics,
    discover_new_theme_with_gemini,
    load_latest_report,
    save_report_to_storage,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [AUTONOMOUS-HARVESTER] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "harvester.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("autonomous_harvester")

REPORT_MD_PATH = BASE_DIR / "MORNING_INSPECTION_REPORT.md"
PROGRESS_JSON_PATH = BASE_DIR / "harvest_progress.json"


def generate_inspection_report(report: Dict[str, Any], cycle_num: int, is_final: bool = False) -> None:
    """Generates a high-precision Markdown report for user morning review."""
    themes = report.get("themes", [])
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S JST")
    status_header = "【最終確認用】午前4時 到着・自律停止レポート" if is_final else f"【進行中】自律データ探索レポート (Cycle {cycle_num})"

    lines: List[str] = [
        f"# World Pulse Chronicle - {status_header}",
        f"",
        f"- **記録日時:** `{now_str}`",
        f"- **累積テーマ数:** `{len(themes)} テーマ`（初期シード10 + 自律発見{max(0, len(themes) - 10)}）",
        f"- **データ同期状態:** `{report.get('sync_status', 'UNKNOWN')}`",
        f"- **世界総括ヘッドライン:** **{report.get('global_headline', 'N/A')}**",
        f"",
        f"> {report.get('global_summary', '')}",
        f"",
        f"---",
        f"",
        f"## 1. データサイエンス分析 & 相関マトリクス総括",
        f"",
        f"| ID | カテゴリ | テーマ名 | 相関係数 (Pearson r) | 因果先行ラグ | 転換点 (Tipping Point) | 主系列 CAGR | 副系列 CAGR |",
        f"| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    for t in themes:
        tid = t.get("id", "?")
        cat = t.get("category_tag", "")
        title = t.get("title", "")
        dsm = t.get("data_science_metrics") or {}
        r_val = dsm.get("pearson_r", 0.0)
        r_str = f"{r_val:+.3f}" if isinstance(r_val, (int, float)) else str(r_val)
        lag = dsm.get("lead_lag_years", 0.0)
        lag_str = f"{lag:+.1f}年" if lag != 0 else "同調 (0年)"
        tp = dsm.get("tipping_point_year", "N/A")
        cp = dsm.get("cagr_primary", 0.0)
        cs = dsm.get("cagr_secondary", 0.0)
        cagr_str = f"{cp:+.1f}% / {cs:+.1f}%"
        lines.append(f"| #{tid} | `{cat}` | **{title}** | `{r_str}` | `{lag_str}` | `{tp}` | `{cagr_str}` |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 2. 自律発見テーマ詳細ログ (ID 11〜{len(themes)})",
        f"",
    ])

    autonomous_themes = [t for t in themes if t.get("id", 0) > 10 or t.get("is_autonomous")]
    if not autonomous_themes:
        lines.append("*(自律発見テーマはまだ登録されていません)*\n")
    else:
        for t in autonomous_themes:
            tid = t.get("id")
            cat = t.get("category_tag")
            title = t.get("title")
            hl = t.get("headline")
            chain = t.get("causal_chain", [])
            story = t.get("deep_story", "")
            future = t.get("future_watch", "")
            sources = ", ".join(t.get("sources", [])) if t.get("sources") else "World Bank / CCKP / FAOSTAT / OECD / yfinance"
            dsm = t.get("data_science_metrics") or {}

            lines.extend([
                f"### Theme #{tid}: [{cat}] {title}",
                f"- **ヘッドライン:** {hl}",
                f"- **データソース:** {sources}",
                f"- **データサイエンス指標:** Pearson $r = {dsm.get('pearson_r', 'N/A')}$ (`{dsm.get('correlation_strength', '')}`) | 決定係数 $R^2 = {dsm.get('r_squared', 'N/A')}$ | 先行ラグ `{dsm.get('lead_lag_years', 0):+.1f}年` | 構造転換点 `{dsm.get('tipping_point_year', 'N/A')}`",
                f"- **4段階 因果連鎖:**",
            ])
            for idx, step in enumerate(chain, start=1):
                lines.append(f"  {idx}. {step}")
            lines.extend([
                f"- **構造的行間解説:** {story}",
                f"- **今後の注視点:** {future}",
                f"",
            ])

    lines.extend([
        f"---",
        f"",
        f"## 3. Webサイト閲覧方法",
        f"",
        f"ブラウザで `http://localhost:8000/` を開くと、上記全{len(themes)}テーマを「デジタル方眼ノート × ネオブルータリズム」UIにてインタラクティブに操作・閲覧できます。",
        f"- **3つの可視化モード切替:** `[ 2-AXIS COMBO ]` / `[ BASE 100 NORMALIZED ]` / `[ SCATTER & REGRESSION ]`",
        f"- **改善されたインデックスタブ:** 左右ナビゲーション (`◀` / `▶`)、ホイールスクロール、WRAP展開 (`▤ WRAP`) にて見切れなく快適に全テーマを巡回可能。",
    ])

    report_text = "\n".join(lines)
    REPORT_MD_PATH.write_text(report_text, encoding="utf-8")
    PROGRESS_JSON_PATH.write_text(
        json.dumps(
            {
                "updated_at": now_str,
                "cycle": cycle_num,
                "is_final": is_final,
                "total_themes": len(themes),
                "latest_theme": themes[-1] if themes else None,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    logger.info("Saved morning inspection review to %s and %s", REPORT_MD_PATH.name, PROGRESS_JSON_PATH.name)


async def run_discovery_cycle(cycle_num: int) -> int:
    logger.info("=== [Cycle %d] Starting Open Data collection & Theme Discovery ===", cycle_num)
    try:
        report = load_latest_report()
        existing_themes = report.get("themes", [])
        current_count = len(existing_themes)
        logger.info("Current active themes: %d", current_count)

        logger.info("Harvesting indicators across World Bank, CCKP, FAOSTAT, OECD, yfinance...")
        raw_payload = await collect_all_10_themes_payload()

        logger.info("Invoking Gemini 3.8 Flash Autonomous Discovery Engine...")
        new_theme = await discover_new_theme_with_gemini(existing_themes, raw_payload)

        # Ensure Data Science Metrics are attached
        if "chart_data" in new_theme and not new_theme.get("data_science_metrics"):
            cd = new_theme["chart_data"]
            new_theme["data_science_metrics"] = compute_data_science_metrics(
                cd.get("labels", []),
                cd.get("primary_series", {}).get("data", []),
                cd.get("secondary_series", {}).get("data", []),
            )

        # Check title duplication
        existing_titles = [t.get("title") for t in existing_themes]
        if new_theme.get("title") in existing_titles:
            logger.info("Theme '%s' already discovered. Refining ID...", new_theme.get("title"))
            new_theme["id"] = current_count + 1

        report["themes"].append(new_theme)
        report["sync_status"] = f"AUTONOMOUS DISCOVERY ({len(report['themes'])} THEMES)"
        report["updated_date"] = datetime.date.today().isoformat()

        persisted = save_report_to_storage(report)
        dsm = new_theme.get("data_science_metrics") or {}
        logger.info(
            "★ New Theme Discovered! #%d: [%s] %s (Pearson r=%.3f, Lag=%.1f yr, Tipping Point=%s)",
            new_theme.get("id"),
            new_theme.get("category_tag"),
            new_theme.get("title"),
            dsm.get("pearson_r", 0.0),
            dsm.get("lead_lag_years", 0.0),
            dsm.get("tipping_point_year", "N/A"),
        )
        logger.info("Headline: %s", new_theme.get("headline"))
        logger.info("Causal Chain: %s", " -> ".join(new_theme.get("causal_chain", [])))
        logger.info("Persisted to: %s", persisted)

        # Update live morning inspection report
        generate_inspection_report(report, cycle_num, is_final=False)

        return len(report["themes"])
    except Exception as exc:
        logger.error("Error during discovery cycle %d: %s", cycle_num, exc, exc_info=True)
        return -1


def compute_target_stop_datetime(until_hour: int = 4) -> datetime.datetime:
    """
    Computes the upcoming target stop time at `until_hour:00:00 JST`.
    If current local time is 21:00, stop time is tomorrow morning 04:00:00.
    If current local time is 02:00, stop time is today 04:00:00.
    """
    now = datetime.datetime.now()
    candidate = now.replace(hour=until_hour, minute=0, second=0, microsecond=0)
    if candidate <= now:
        candidate += datetime.timedelta(days=1)
    return candidate


async def main():
    parser = argparse.ArgumentParser(description="World Pulse Chronicle Autonomous Harvester")
    parser.add_argument("--interval-minutes", type=int, default=15, help="Minutes between discovery cycles")
    parser.add_argument("--max-themes", type=int, default=50, help="Maximum number of themes to grow until stopping")
    parser.add_argument("--until-hour", type=int, default=4, help="Stop at this morning hour JST (default: 4 for 04:00 AM)")
    args = parser.parse_args()

    stop_target = compute_target_stop_datetime(args.until_hour)
    interval_sec = args.interval_minutes * 60

    logger.info("=================================================================")
    logger.info("WORLD PULSE CHRONICLE: AUTONOMOUS OVERNIGHT HARVESTER STARTED")
    logger.info("Interval: %d minutes | Target Max: %d themes", args.interval_minutes, args.max_themes)
    logger.info("Target Graceful Stop Time: %s", stop_target.strftime("%Y-%m-%d %H:%M:%S JST"))
    logger.info("Rule: '午前4時の時点で稼働しているテーマの生成完了をもって一度停止'")
    logger.info("=================================================================")

    # Initial generation of report for current state
    initial_report = load_latest_report()
    generate_inspection_report(initial_report, 0, is_final=False)

    cycle = 1
    while True:
        now = datetime.datetime.now()

        # Check if 04:00 AM JST has already been reached before starting a new cycle
        if now >= stop_target:
            logger.info("=================================================================")
            logger.info("★ TARGET TIME %s (04:00 AM JST) REACHED ★", stop_target.strftime("%H:%M:%S"))
            logger.info("Stopping harvester daemon as requested for user morning inspection.")
            logger.info("=================================================================")
            final_report = load_latest_report()
            generate_inspection_report(final_report, cycle - 1, is_final=True)
            break

        logger.info("[Cycle %d] In-flight discovery started at %s", cycle, now.strftime("%H:%M:%S"))
        total = await run_discovery_cycle(cycle)

        # After finishing the in-flight cycle, check if 04:00 AM was reached during its execution
        finish_time = datetime.datetime.now()
        if finish_time >= stop_target:
            logger.info("=================================================================")
            logger.info("★ IN-FLIGHT CYCLE %d COMPLETED AT OR AFTER 04:00 AM JST (%s) ★", cycle, finish_time.strftime("%H:%M:%S"))
            logger.info("Graceful stop executed. All discovered themes persisted safely.")
            logger.info("=================================================================")
            final_report = load_latest_report()
            generate_inspection_report(final_report, cycle, is_final=True)
            break

        if total >= args.max_themes:
            logger.info("Reached maximum requested theme capacity (%d >= %d). Stopping.", total, args.max_themes)
            final_report = load_latest_report()
            generate_inspection_report(final_report, cycle, is_final=True)
            break

        remaining_sec = max(0, int((stop_target - finish_time).total_seconds()))
        hours, remainder = divmod(remaining_sec, 3600)
        minutes, _ = divmod(remainder, 60)
        logger.info(
            "Discovery cycle %d done. Total themes: %d. Time until 04:00 AM: %d hrs %d mins.",
            cycle,
            total,
            hours,
            minutes,
        )
        logger.info("Next discovery cycle in %d minutes... (Sleeping)", args.interval_minutes)
        await asyncio.sleep(interval_sec)
        cycle += 1


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Harvester stopped by user.")
