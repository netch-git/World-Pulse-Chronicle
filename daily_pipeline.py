"""
Daily Open Data Pipeline: Macro & Micro Synchronizer
Runs once per day (e.g. 06:00 JST) to collect:
1. Micro: Hiroshima Prefecture & Takehara City Real-time Pulse (Weather, Solar NOAA, Tide, Calendar, e-Stat)
2. Macro: Global Chronicle Themes Sync
3. Dashboard Integration & Static Export
"""

import sys
import subprocess
import datetime
import os
import json

def run_step(step_name, command):
    print(f"\n=======================================================")
    print(f"==> [DAILY PIPELINE] {step_name}")
    print(f"    Command: {command}")
    print(f"=======================================================")
    res = subprocess.run(command, shell=True)
    if res.returncode != 0:
        print(f"Error in {step_name} (exit code: {res.returncode})", file=sys.stderr)
        return False
    return True

def main():
    now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    print(f"=== WORLD PULSE CHRONICLE - DAILY SYNC INITIATED ===")
    print(f"Current Execution Timestamp: {now_jst.strftime('%Y-%m-%d %H:%M:%S JST')}")

    # Step 1: Harvest Hiroshima & Takehara Micro Open Data (e-Stat, JMA, Open-Meteo, Tide, Solar)
    ok = run_step(
        "Harvesting Micro Open Data (Hiroshima & Takehara)",
        "python3 backend/collect_hiroshima_takehara.py"
    )
    if not ok:
        print("Warning: Micro harvesting completed with warnings, proceeding with available cache.")

    # Step 2: Integrate into latest_cache.json & frontend/latest.json
    ok = run_step(
        "Integrating Micro Data into Central Cache",
        "python3 -c \""
        "import json, shutil; "
        "cache = json.load(open('latest_cache.json')); "
        "micro = json.load(open('backend/hiroshima_takehara_opendata.json')); "
        "cache['micro_pulse'] = micro; "
        "cache['updated_date'] = '" + now_jst.strftime('%Y-%m-%d') + "'; "
        "json.dump(cache, open('latest_cache.json', 'w'), ensure_ascii=False, indent=2); "
        "json.dump(cache, open('frontend/latest.json', 'w'), ensure_ascii=False, indent=2); "
        "shutil.copy('backend/hiroshima_takehara_opendata.json', 'frontend/hiroshima_takehara_opendata.json'); "
        "print('Synchronized central cache successfully.')\""
    )

    # Step 3: Integrate into frontend/index.html (Single-page App Self-containment)
    ok = run_step(
        "Rebuilding Frontend Self-Contained Index",
        "python3 backend/integrate_micro_dashboard.py"
    )

    # Step 4: Optional Git Commit & Push if in Git environment
    if os.path.exists(".git"):
        auto_commit = os.getenv("AUTO_GIT_PUSH", "true").lower() in ("true", "1")
        if auto_commit:
            commit_msg = f"chore(daily-sync): automated open data update [{now_jst.strftime('%Y-%m-%d')}] [skip ci]"
            cmd = f'git add latest_cache.json frontend/latest.json frontend/index.html backend/hiroshima_takehara_opendata.json frontend/hiroshima_takehara_opendata.json && ' \
                  f'git diff-index --quiet HEAD || (git commit -m "{commit_msg}" && git push origin main)'
            run_step("Committing & Pushing Daily Update to GitHub", cmd)

    print(f"\n[DAILY PIPELINE] Finished successfully at {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S JST')}")

if __name__ == "__main__":
    main()
