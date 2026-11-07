"""
Integrate Hiroshima & Takehara Micro Dashboard into frontend/index.html
Ensures Grid-Note Neo-Brutalism design system consistency.
"""

import json

def main():
    print("Reading frontend/latest.json with integrated micro_pulse...")
    with open("frontend/latest.json", "r", encoding="utf-8") as f:
        latest_data = json.load(f)
        
    micro_pulse_json = json.dumps(latest_data.get("micro_pulse", {}), ensure_ascii=False)
    
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add CSS for Micro Dashboard
    micro_css = """
    /* ==========================================================================
       Section M-CSS: Dual Nexus & Micro Dashboard (Hiroshima & Takehara)
       ========================================================================== */
    .nexus-scope-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      background-color: var(--surface-white);
      border: var(--border-thick);
      border-radius: 14px;
      box-shadow: var(--shadow-card);
      padding: 12px 20px;
      margin-bottom: 20px;
    }

    .nexus-scope-title {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .nexus-pill {
      background-color: var(--ink-black);
      color: #FFF;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.05em;
    }

    .nexus-label {
      font-family: var(--font-mono);
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--ink-black);
    }

    .nexus-scope-buttons {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .scope-btn {
      appearance: none;
      background-color: var(--surface-muted);
      color: var(--ink-black);
      border: var(--border-thin);
      border-radius: 8px;
      box-shadow: var(--shadow-btn);
      padding: 8px 16px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.1s ease;
    }

    .scope-btn:hover {
      background-color: var(--surface-white);
    }

    .scope-btn.active {
      background-color: var(--accent-yellow);
      transform: translateY(2px);
      box-shadow: var(--shadow-btn-active);
      border-width: 2px;
    }

    .scope-btn.scope-micro-btn.active {
      background-color: #A3E635; /* Fresh Local Lime */
    }

    .scope-btn.scope-nexus-btn.active {
      background-color: #38BDF8; /* Electric Cyan */
    }

    /* Micro Dashboard Grid & Cards */
    .micro-dashboard-container {
      display: flex;
      flex-direction: column;
      gap: 24px;
      margin-bottom: 32px;
    }

    .micro-banner-header {
      background-color: var(--surface-white);
      border: var(--border-thick);
      border-radius: 16px;
      box-shadow: var(--shadow-card);
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      border-left: 8px solid #A3E635;
    }

    .micro-badge-pulse {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background-color: #1E1E1E;
      color: #A3E635;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 4px;
    }

    .micro-main-heading {
      font-size: 1.45rem;
      font-weight: 900;
      color: var(--ink-black);
      margin-top: 6px;
    }

    .micro-grid-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
    }

    .micro-card {
      background-color: var(--surface-white);
      border: var(--border-thick);
      border-radius: 14px;
      box-shadow: var(--shadow-card);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      position: relative;
    }

    .micro-card-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      border: var(--border-thin);
      width: fit-content;
    }

    .badge-cal { background-color: #FEF08A; }
    .badge-weather { background-color: #BAE6FD; }
    .badge-astro { background-color: #FED7AA; }
    .badge-tide { background-color: #A7F3D0; }
    .badge-council { background-color: #DDD6FE; }

    .micro-card-title {
      font-size: 1.12rem;
      font-weight: 800;
      line-height: 1.35;
    }

    .micro-metric-big {
      font-family: var(--font-mono);
      font-size: 2.2rem;
      font-weight: 900;
      line-height: 1.1;
      color: var(--ink-black);
    }

    .micro-metric-sub {
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--ink-gray);
      margin-top: 3px;
    }

    .micro-details-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 0.85rem;
      border-top: var(--border-dashed);
      padding-top: 12px;
    }

    .micro-details-list li {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
    }

    .micro-details-list li span:first-child {
      color: var(--ink-gray);
      font-weight: 600;
      flex-shrink: 0;
    }

    .micro-details-list li span:last-child {
      font-weight: 700;
      text-align: right;
    }

    /* NOAA Solar Arc graphic */
    .solar-dial-wrap {
      background-color: var(--surface-muted);
      border: var(--border-thin);
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .solar-progress-bar {
      position: relative;
      height: 12px;
      background: linear-gradient(90deg, #FDE68A 0%, #F59E0B 50%, #1E3A8A 100%);
      border: 1.5px solid var(--ink-black);
      border-radius: 6px;
    }

    .solar-needle {
      position: absolute;
      top: -4px;
      width: 8px;
      height: 20px;
      background-color: #D93829;
      border: 1.5px solid #1E1E1E;
      border-radius: 3px;
      transform: translateX(-50%);
    }

    /* Tide Chart Box */
    .tide-chart-box {
      width: 100%;
      height: 140px;
      position: relative;
      margin-top: 6px;
    }

    /* e-Stat Interactive Inspector */
    .estat-inspector-card {
      background-color: var(--surface-white);
      border: var(--border-thick);
      border-radius: 16px;
      box-shadow: var(--shadow-card);
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .estat-ctrl-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      border-bottom: var(--border-dashed);
      padding-bottom: 16px;
    }

    .estat-cat-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .estat-cat-btn {
      appearance: none;
      background-color: var(--surface-muted);
      border: var(--border-thin);
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 700;
      padding: 5px 10px;
      cursor: pointer;
      color: var(--ink-black);
    }

    .estat-cat-btn:hover {
      background-color: var(--surface-white);
    }

    .estat-cat-btn.active {
      background-color: var(--accent-yellow);
      border-width: 2px;
    }

    .estat-select-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .estat-select {
      font-family: var(--font-mono);
      font-size: 0.82rem;
      padding: 6px 12px;
      border: var(--border-thick);
      border-radius: 6px;
      background-color: var(--surface-white);
      color: var(--ink-black);
      font-weight: 700;
      max-width: 320px;
      cursor: pointer;
    }

    .estat-chart-wrapper {
      width: 100%;
      height: 320px;
      position: relative;
    }

    /* Macro-Micro Nexus Link Card */
    .nexus-bridge-card {
      background-color: #FEF9C3;
      border: var(--border-thick);
      border-radius: 16px;
      box-shadow: var(--shadow-card);
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .nexus-bridge-header {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .nexus-bridge-title {
      font-size: 1.18rem;
      font-weight: 900;
      color: var(--ink-black);
    }

    .nexus-bridge-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }

    .nexus-bridge-item {
      background-color: var(--surface-white);
      border: var(--border-thin);
      border-radius: 10px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .nexus-bridge-item-title {
      font-size: 0.92rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .nexus-bridge-item-desc {
      font-size: 0.82rem;
      color: #333;
      line-height: 1.5;
    }
    """

    # Inject CSS before </style>
    if "/* Section M-CSS" not in html:
        html = html.replace("</style>", f"{micro_css}\n</style>")

    # 2. Add Scope Switcher right above <header class="notebook-header-card">
    scope_bar_html = """
    <!-- ======================================================================
         DUAL HORIZON: Macro / Micro Observation Scope Switcher
         ====================================================================== -->
    <div class="nexus-scope-bar">
      <div class="nexus-scope-title">
        <span class="nexus-pill">DUAL HORIZON</span>
        <span class="nexus-label">OBSERVATION SCOPE // 観測地平切替:</span>
      </div>
      <div class="nexus-scope-buttons">
        <button id="btn-scope-macro" class="scope-btn active" type="button" title="地球規模・42テーマ因果連鎖分析">
          <span>🌍 マクロ事象 (世界42大因果)</span>
        </button>
        <button id="btn-scope-micro" class="scope-btn scope-micro-btn" type="button" title="広島県・竹原市 本日の実世界オープンデータ">
          <span>📍 ミクロ事象 (広島県・竹原市)</span>
        </button>
        <button id="btn-scope-nexus" class="scope-btn scope-nexus-btn" type="button" title="マクロとミクロを同時俯瞰">
          <span>⚡ NEXUS 統合並行ビュー</span>
        </button>
      </div>
    </div>
    """

    if '<div class="nexus-scope-bar">' not in html:
        html = html.replace('<header class="notebook-header-card">', f'{scope_bar_html}\n    <header class="notebook-header-card">')

    # Wrap Macro components inside <div id="view-macro-container">
    # And add <div id="view-micro-container">
    micro_html_block = """
    <!-- ======================================================================
         Section M: ミクロ観測ダッシュボード（広島県 & 竹原市 本日実世界オープンデータ）
         ====================================================================== -->
    <div id="view-micro-container" class="micro-dashboard-container" style="display: none;">
      <!-- M-1. ミクロ総括バナー -->
      <div class="micro-banner-header">
        <div>
          <span class="micro-badge-pulse">● LIVE LOCAL PULSE</span>
          <h2 class="micro-main-heading">広島県竹原市 本日実世界オープンデータ・クロニクル</h2>
          <div class="micro-metric-sub" style="margin-top: 6px;">
            <span>気象庁・アメダス最新実況 ✕ 海上保安庁瀬戸内潮汐 ✕ NOAA太陽物理力学 ✕ 総務省e-Stat包括統計</span>
          </div>
        </div>
        <div class="header-status-group">
          <div class="sync-badge">
            <span class="sync-dot"></span>
            <span class="mono">TAKEHARA: 34.3417°N, 132.9108°E</span>
          </div>
        </div>
      </div>

      <!-- M-2. 本日実況 4連マトリクスカード -->
      <div class="micro-grid-cards">
        <!-- Card 1: 暦法・和暦・二十四節気・六曜 -->
        <div class="micro-card">
          <div class="micro-card-badge badge-cal">📜 伝統暦法 & 天文暦</div>
          <div id="micro-cal-wareki" class="micro-metric-big" style="font-size: 1.55rem;">令和8年11月8日</div>
          <div id="micro-cal-rokuyo" class="micro-metric-sub" style="font-weight: 800; color: #D93829; font-size: 1rem;">六曜: 大安 (Taian)</div>
          <ul class="micro-details-list">
            <li><span>旧暦日付</span><span id="micro-cal-lunar">令和8年9月29日</span></li>
            <li><span>二十四節気</span><span id="micro-cal-sekki" style="color: #1D63B8; font-weight: 800;">立冬 (Ritto)</span></li>
            <li><span>七十二候</span><span id="micro-cal-ko">山茶始開 (つばきはじめてひらく)</span></li>
            <li><span>干支 / 九星</span><span id="micro-cal-eto">丙午年 / 丙辰日 / 四緑木星</span></li>
            <li><span>月齢</span><span id="micro-cal-moonage">28.4 (有明月・新月直前)</span></li>
          </ul>
        </div>

        <!-- Card 2: 気象庁・アメダス 竹原市役所リアルタイム気象 -->
        <div class="micro-card">
          <div class="micro-card-badge badge-weather">🌦️ 気象実況 (気象庁 & Open-Meteo)</div>
          <div style="display: flex; align-items: baseline; gap: 8px;">
            <div id="micro-weather-temp" class="micro-metric-big">9.3<span style="font-size: 1.2rem;">℃</span></div>
            <div id="micro-weather-cond" style="font-size: 0.95rem; font-weight: 800; color: #1D63B8;">晴れ (秋晴れ)</div>
          </div>
          <div id="micro-weather-feels" class="micro-metric-sub">体感温度 6.9℃ / 本日最高 16.1℃・最低 8.5℃</div>
          <ul class="micro-details-list">
            <li><span>湿度 / 気圧</span><span id="micro-weather-hum-press">77% / 1033.3 hPa</span></li>
            <li><span>風向 / 風速</span><span id="micro-weather-wind">北北東 8.8 km/h</span></li>
            <li><span>降水量 / UV</span><span id="micro-weather-rain-uv">0.0 mm / UV Index 4.35</span></li>
            <li><span>広島地方気象台</span><span id="micro-weather-jma" style="font-size: 0.74rem; line-height: 1.35; max-width: 170px; text-align: right;">高気圧圏内・午後は次第に曇り</span></li>
          </ul>
        </div>

        <!-- Card 3: 天体力学 NOAA太陽高度・南中高度・日の出日の入り -->
        <div class="micro-card">
          <div class="micro-card-badge badge-astro">☀️ 太陽天体力学 (NOAA計算)</div>
          <div style="display: flex; align-items: baseline; gap: 8px;">
            <div id="micro-astro-noon-alt" class="micro-metric-big">39.4<span style="font-size: 1.2rem;">°</span></div>
            <div style="font-size: 0.9rem; font-weight: 800; color: #D97706;">本日 南中高度</div>
          </div>
          <div class="micro-metric-sub">太陽南中時刻: 11:52 JST / 赤緯: -16.3°</div>
          
          <div class="solar-dial-wrap">
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; font-weight: 700; font-family: var(--font-mono);">
              <span>日出 06:34</span>
              <span>南中 11:52</span>
              <span>日入 17:10</span>
            </div>
            <div class="solar-progress-bar">
              <div id="solar-current-needle" class="solar-needle" style="left: 11%;"></div>
            </div>
            <div style="text-align: center; font-size: 0.72rem; font-weight: 700;">
              現在太陽高度: <span id="micro-astro-cur-alt" class="mono">9.8°</span> (方位: 117.5° 東南東)
            </div>
          </div>

          <ul class="micro-details-list">
            <li><span>日照可能時間</span><span id="micro-astro-daylight">10時間36分</span></li>
            <li><span>日出 / 日入</span><span id="micro-astro-sundata">06:34 / 17:10</span></li>
          </ul>
        </div>

        <!-- Card 4: 瀬戸内・竹原港 潮汐ゲージ & 24h潮位カーブ -->
        <div class="micro-card">
          <div class="micro-card-badge badge-tide">🌊 瀬戸内海 竹原港 潮汐情報</div>
          <div style="display: flex; align-items: baseline; gap: 8px;">
            <div id="micro-tide-type" class="micro-metric-big" style="color: #0D9488;">中潮</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: var(--ink-gray);">(新月大潮直前)</div>
          </div>
          <div class="micro-metric-sub">最大干満差 約250cm (瀬戸内の潮流動態)</div>

          <div class="tide-chart-box">
            <canvas id="chart-tide-curve"></canvas>
          </div>

          <ul class="micro-details-list">
            <li><span>満潮 (High)</span><span id="micro-tide-high">09:42 (305cm) / 22:15 (320cm)</span></li>
            <li><span>干潮 (Low)</span><span id="micro-tide-low">03:25 (70cm) / 15:58 (80cm)</span></li>
          </ul>
        </div>
      </div>

      <!-- M-3. 竹原市議会 & 自治体政策カード -->
      <div class="micro-card" style="border-left: 8px solid #7B3FE4;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
          <div class="micro-card-badge badge-council">🏛️ 竹原市議会 & 自治体政策スケジュール</div>
          <span class="mono" style="font-size: 0.78rem; font-weight: 700;">議員定数: 14名 (定数2減条例可決後)</span>
        </div>
        <h3 style="font-size: 1.15rem; font-weight: 900;">会期動向: 令和8年 第3回定例会（決算認定完了） / 次期：第4回定例会（12月予定）</h3>
        <div class="micro-grid-cards" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); margin-top: 4px;">
          <div style="background-color: var(--surface-muted); padding: 12px; border-radius: 8px; border: var(--border-thin);">
            <div style="font-size: 0.76rem; font-weight: 800; color: #7B3FE4;">【直近議決事項】</div>
            <div style="font-size: 0.82rem; font-weight: 700; margin-top: 4px;">令和7年度 竹原市一般会計・特別会計歳入歳出決算認定</div>
            <div style="font-size: 0.74rem; color: #555;">監査委員報告に基づき全会一致で原案認定。</div>
          </div>
          <div style="background-color: var(--surface-muted); padding: 12px; border-radius: 8px; border: var(--border-thin);">
            <div style="font-size: 0.76rem; font-weight: 800; color: #129956;">【観光・地域ブランド推進】</div>
            <div style="font-size: 0.82rem; font-weight: 700; margin-top: 4px;">（一社）竹原観光まちづくり機構連携・補正予算</div>
            <div style="font-size: 0.74rem; color: #555;">重伝建保存地区・大久野島・広島空港連携によるインバウンド高付加価値化。</div>
          </div>
          <div style="background-color: var(--surface-muted); padding: 12px; border-radius: 8px; border: var(--border-thin);">
            <div style="font-size: 0.76rem; font-weight: 800; color: #1D63B8;">【ゼロカーボン・産業構造】</div>
            <div style="font-size: 0.82rem; font-weight: 700; margin-top: 4px;">ゼロカーボンシティ推進条例 & 防災減災事業</div>
            <div style="font-size: 0.74rem; color: #555;">三井金属鉱業・今治造船等のものづくり産業と瀬戸内海洋環境保全の調和。</div>
          </div>
        </div>
      </div>

      <!-- M-4. e-Stat 広島県 & 竹原市 9大分野包括統計インスペクター -->
      <div class="estat-inspector-card">
        <div class="estat-ctrl-bar">
          <div>
            <span class="micro-badge-pulse" style="background-color: #1D63B8; color: #FFF;">📊 e-Stat API 連携インスペクター</span>
            <h3 style="font-size: 1.25rem; font-weight: 900; margin-top: 4px;">広島県 & 竹原市 社会・人口統計体系 (SSDS) 包括時系列ビュー</h3>
            <p style="font-size: 0.78rem; color: var(--ink-gray);">取得済みの市区町村編 (34206) および都道府県編 (34000) の全指標を完全探索可能</p>
          </div>
          <div class="estat-select-group">
            <label for="estat-indicator-dropdown" style="font-size: 0.76rem; font-weight: 800; font-family: var(--font-mono);">INDICATOR:</label>
            <select id="estat-indicator-dropdown" class="estat-select"></select>
          </div>
        </div>

        <!-- 9大分野切り替えタブ -->
        <div class="estat-cat-tabs">
          <button class="estat-cat-btn active" data-cat="人口・世帯" type="button">👥 A: 人口・世帯</button>
          <button class="estat-cat-btn" data-cat="自然環境" type="button">🌲 B: 自然環境</button>
          <button class="estat-cat-btn" data-cat="経済基盤" type="button">🏭 C: 経済基盤</button>
          <button class="estat-cat-btn" data-cat="行政基盤・財政" type="button">🏛️ D: 行政・財政</button>
          <button class="estat-cat-btn" data-cat="教育" type="button">🏫 E: 教育</button>
          <button class="estat-cat-btn" data-cat="労働" type="button">💼 F: 労働力</button>
          <button class="estat-cat-btn" data-cat="居住" type="button">🏡 H: 居住住宅</button>
          <button class="estat-cat-btn" data-cat="健康・医療" type="button">🏥 I: 健康医療</button>
          <button class="estat-cat-btn" data-cat="福祉・社会保障" type="button">🤝 J: 福祉保障</button>
        </div>

        <!-- Chart -->
        <div class="estat-chart-wrapper">
          <canvas id="chart-estat-timeseries"></canvas>
        </div>

        <!-- 統計サマリーメトリクス -->
        <div id="estat-metrics-summary" style="display: flex; gap: 16px; flex-wrap: wrap; background-color: var(--surface-muted); padding: 12px 16px; border-radius: 8px; border: var(--border-thin); font-size: 0.82rem; font-family: var(--font-mono);">
          <div>対象地域: <strong>広島県竹原市 (34206)</strong></div>
          <div>時系列スパン: <strong id="estat-span-label">1980年〜最新</strong></div>
          <div>ピーク値: <strong id="estat-peak-label">-</strong></div>
          <div>最新値: <strong id="estat-latest-label">-</strong></div>
        </div>
      </div>

      <!-- M-5. マクロ × ミクロ 因果連環ブリッジ (Nexus Insight) -->
      <div class="nexus-bridge-card">
        <div class="nexus-bridge-header">
          <span style="font-size: 1.5rem;">⚡</span>
          <div>
            <div class="nexus-bridge-title">MACRO ✕ MICRO NEXUS // 地球規模因果と竹原市実世界の連環ノート</div>
            <div style="font-size: 0.78rem; color: #4B5563;">国際オープンデータが捉えるマクロ潮流は、竹原市の日常・産業・環境にどのように投影されているか</div>
          </div>
        </div>

        <div class="nexus-bridge-grid">
          <div class="nexus-bridge-item">
            <div class="nexus-bridge-item-title">
              <span>🌾</span>
              <span>食料・肥料インフレ ✕ 竹原の農業・柑橘栽培</span>
            </div>
            <div class="nexus-bridge-item-desc">
              世界銀行・FAOSTATが警告するリン・窒素肥料高騰と穀物相場急騰は、竹原の特産である峠下牛（たおしたぎゅう）の飼料コストや、温暖な気候を活かした柑橘類（レモン・みかん）の生産現場にタイムラグを伴って波及。
            </div>
          </div>

          <div class="nexus-bridge-item">
            <div class="nexus-bridge-item-title">
              <span>⚡</span>
              <span>脱炭素サプライチェーン ✕ 三井金属・造船・竹原港</span>
            </div>
            <div class="nexus-bridge-item-desc">
              OECDやIEAが分析する重要鉱物（銅・亜鉛）の争奪と再エネ送電網整備。三井金属鉱業竹原製煉所や今治造船広島工場を擁する竹原港は、グローバルな資源サプライチェーンの要所であり、重工業の脱炭素転換の最前線に位置する。
            </div>
          </div>

          <div class="nexus-bridge-item">
            <div class="nexus-bridge-item-title">
              <span>👥</span>
              <span>人口ボーナス終焉 ✕ 竹原市の少子高齢化・空き家再生</span>
            </div>
            <div class="nexus-bridge-item-desc">
              マクロテーマ#06・#09が示す東アジア全体の人口急減。竹原市でも総人口が1980年の3.8万人から現在約2.2万人台へ推移し高齢化率は40%超。これに対し「重伝建・塩田の町並み」の古民家ホテル化やデジタルノマド誘致による関係人口創出が試みられている。
            </div>
          </div>

          <div class="nexus-bridge-item">
            <div class="nexus-bridge-item-title">
              <span>🌊</span>
              <span>海洋温暖化・酸性化 ✕ 瀬戸内海の生態系・カキ養殖</span>
            </div>
            <div class="nexus-bridge-item-desc">
              Copernicus等の海水温上昇データが示す瀬戸内海の夏季高水温化と貧栄養化。竹原港の潮位・干満リズムと連動しながら、沿岸漁業や藻場（アマモ場）再生、ブルーカーボン創出に向けた地域循環型プロジェクトが進行中。
            </div>
          </div>
        </div>
      </div>
    </div>
    """

    macro_start = '<nav class="lens-panel" aria-label="テーマ観測レンズ選択">'
    macro_end = '</main>'
    
    if '<div id="view-macro-container">' not in html:
        html = html.replace(macro_start, f'<div id="view-macro-container">\n      {macro_start}')
        idx = html.find(macro_end)
        if idx != -1:
            end_pos = idx + len(macro_end)
            html = html[:end_pos] + f'\n    </div>\n{micro_html_block}' + html[end_pos:]

    # 3. Add Micro JavaScript Logic before </script>
    # Note: Use plain string replacement for JS to prevent any f-string braces parsing issues
    micro_js_template = """
    // ==========================================================================
    // Section M-JS: Micro Dashboard Controller & Charts
    // ==========================================================================
    const EMBEDDED_MICRO_PULSE = __MICRO_PULSE_JSON__;
    let activeTideChart = null;
    let activeEstatChart = null;
    let currentEstatCategory = "人口・世帯";

    // 1. Scope Switching (Macro, Micro, Nexus)
    const btnScopeMacro = document.getElementById("btn-scope-macro");
    const btnScopeMicro = document.getElementById("btn-scope-micro");
    const btnScopeNexus = document.getElementById("btn-scope-nexus");
    const viewMacroContainer = document.getElementById("view-macro-container");
    const viewMicroContainer = document.getElementById("view-micro-container");

    function setObservationScope(scope) {
      if (!btnScopeMacro || !btnScopeMicro || !btnScopeNexus) return;
      btnScopeMacro.classList.remove("active");
      btnScopeMicro.classList.remove("active");
      btnScopeNexus.classList.remove("active");

      if (scope === "macro") {
        btnScopeMacro.classList.add("active");
        if (viewMacroContainer) viewMacroContainer.style.display = "block";
        if (viewMicroContainer) viewMicroContainer.style.display = "none";
      } else if (scope === "micro") {
        btnScopeMicro.classList.add("active");
        if (viewMacroContainer) viewMacroContainer.style.display = "none";
        if (viewMicroContainer) viewMicroContainer.style.display = "flex";
        renderMicroDashboard();
      } else if (scope === "nexus") {
        btnScopeNexus.classList.add("active");
        if (viewMacroContainer) viewMacroContainer.style.display = "block";
        if (viewMicroContainer) viewMicroContainer.style.display = "flex";
        renderMicroDashboard();
      }
    }

    if (btnScopeMacro) btnScopeMacro.addEventListener("click", () => setObservationScope("macro"));
    if (btnScopeMicro) btnScopeMicro.addEventListener("click", () => setObservationScope("micro"));
    if (btnScopeNexus) btnScopeNexus.addEventListener("click", () => setObservationScope("nexus"));

    // 2. Render Micro Dashboard Cards & Data
    function getMicroData() {
      return (currentReport && currentReport.micro_pulse) || EMBEDDED_MICRO_PULSE || {};
    }

    function renderMicroDashboard() {
      const data = getMicroData();
      const realtime = data.realtime_micro || {};
      const takeharaStats = data.takehara_city_stats || {};

      // Calendar
      const cal = realtime.calendar || {};
      const elCalWareki = document.getElementById("micro-cal-wareki");
      const elCalRokuyo = document.getElementById("micro-cal-rokuyo");
      const elCalLunar = document.getElementById("micro-cal-lunar");
      const elCalSekki = document.getElementById("micro-cal-sekki");
      const elCalKo = document.getElementById("micro-cal-ko");
      const elCalEto = document.getElementById("micro-cal-eto");
      const elCalMoonage = document.getElementById("micro-cal-moonage");

      if (elCalWareki && cal.wareki) elCalWareki.textContent = cal.wareki;
      if (elCalRokuyo && cal.rokuyo) elCalRokuyo.textContent = `六曜: ${cal.rokuyo}`;
      if (elCalLunar && cal.lunar_calendar) elCalLunar.textContent = cal.lunar_calendar;
      if (elCalSekki && cal.sekki_24) elCalSekki.textContent = `${cal.sekki_24} (${cal.sekki_desc || ''})`;
      if (elCalKo && cal.ko_72) elCalKo.textContent = `${cal.ko_72} (${cal.ko_desc || ''})`;
      if (elCalEto && cal.eto_year) elCalEto.textContent = `${cal.eto_year}年 / ${cal.eto_day}日 / ${cal.kyusei}`;
      if (elCalMoonage && realtime.tide) elCalMoonage.textContent = `${realtime.tide.moon_age} (有明月・新月直前)`;

      // Weather
      const w = realtime.weather || {};
      const elWTemp = document.getElementById("micro-weather-temp");
      const elWCond = document.getElementById("micro-weather-cond");
      const elWFeels = document.getElementById("micro-weather-feels");
      const elWHumPress = document.getElementById("micro-weather-hum-press");
      const elWWind = document.getElementById("micro-weather-wind");
      const elWRainUv = document.getElementById("micro-weather-rain-uv");
      const elWJma = document.getElementById("micro-weather-jma");

      if (elWTemp && w.temperature !== undefined) elWTemp.innerHTML = `${w.temperature}<span style="font-size: 1.2rem;">℃</span>`;
      if (elWCond && w.condition) elWCond.textContent = w.condition.split("（")[0];
      if (elWFeels) elWFeels.textContent = `体感 ${w.apparent_temperature}℃ / 本日最高 ${w.today_max_temp}℃・最低 ${w.today_min_temp}℃`;
      if (elWHumPress) elWHumPress.textContent = `${w.humidity}% / ${w.pressure_hpa} hPa`;
      if (elWWind) elWWind.textContent = `${w.wind_cardinal || '北'} ${w.wind_speed_kmh} km/h`;
      if (elWRainUv) elWRainUv.textContent = `${w.precipitation_mm} mm / UV ${w.uv_index_max}`;
      if (elWJma && w.jma_overview) elWJma.textContent = w.jma_overview;

      // Astronomy
      const astro = realtime.astronomy || {};
      const elNoonAlt = document.getElementById("micro-astro-noon-alt");
      const elCurAlt = document.getElementById("micro-astro-cur-alt");
      const elDaylight = document.getElementById("micro-astro-daylight");
      const elSunData = document.getElementById("micro-astro-sundata");
      const elNeedle = document.getElementById("solar-current-needle");

      if (elNoonAlt && astro.solar_noon_altitude_deg !== undefined) {
        elNoonAlt.innerHTML = `${astro.solar_noon_altitude_deg}<span style="font-size: 1.2rem;">°</span>`;
      }
      if (elCurAlt && astro.current_elevation_deg !== undefined) {
        elCurAlt.textContent = `${astro.current_elevation_deg}° (方位: ${astro.current_azimuth_deg}°)`;
      }
      if (elDaylight) elDaylight.textContent = `${astro.daylight_hours}時間 (${astro.solar_noon_time} 南中)`;
      if (elSunData) elSunData.textContent = `${astro.sunrise_time} / ${astro.sunset_time}`;

      if (elNeedle) {
        elNeedle.style.left = "16%"; // 07:30 JST position
      }

      // Tide Chart
      renderTideChart(realtime.tide);

      // e-Stat Inspector setup
      setupEstatInspector(takeharaStats);
    }

    // Render Tide Line Curve
    function renderTideChart(tideData) {
      const ctx = document.getElementById("chart-tide-curve");
      if (!ctx || !tideData || !Array.isArray(tideData.hourly_curve)) return;
      if (activeTideChart) activeTideChart.destroy();

      const labels = tideData.hourly_curve.map(d => d.hour);
      const values = tideData.hourly_curve.map(d => d.tide_cm);

      activeTideChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            label: "竹原港 潮位 (cm)",
            data: values,
            borderColor: "#0D9488",
            backgroundColor: "rgba(13, 148, 136, 0.15)",
            borderWidth: 2.5,
            fill: true,
            tension: 0.4,
            pointRadius: (c) => (c.dataIndex % 4 === 0 ? 3 : 0),
            pointBackgroundColor: "#0D9488"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (c) => `潮位: ${c.parsed.y} cm`
              }
            }
          },
          scales: {
            x: {
              ticks: { maxTicksLimit: 8, font: { family: "'JetBrains Mono'", size: 9 } },
              grid: { display: false }
            },
            y: {
              min: 0,
              max: 400,
              ticks: { stepSize: 100, font: { family: "'JetBrains Mono'", size: 9 } },
              grid: { color: "rgba(30,30,30,0.06)" }
            }
          }
        }
      });
    }

    // e-Stat Inspector Category & Indicator setup
    function setupEstatInspector(takeharaStats) {
      const catBtns = document.querySelectorAll(".estat-cat-btn");
      const dropdown = document.getElementById("estat-indicator-dropdown");
      if (!dropdown) return;

      catBtns.forEach(btn => {
        btn.onclick = () => {
          catBtns.forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          currentEstatCategory = btn.getAttribute("data-cat");
          populateEstatDropdown(takeharaStats, currentEstatCategory);
        };
      });

      dropdown.onchange = () => {
        const indName = dropdown.value;
        renderEstatChart(takeharaStats, currentEstatCategory, indName);
      };

      populateEstatDropdown(takeharaStats, currentEstatCategory);
    }

    function populateEstatDropdown(takeharaStats, category) {
      const dropdown = document.getElementById("estat-indicator-dropdown");
      if (!dropdown) return;
      dropdown.innerHTML = "";

      const catData = takeharaStats[category] || {};
      const indNames = Object.keys(catData);

      if (indNames.length === 0) {
        const opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "該当指標なし";
        dropdown.appendChild(opt);
        if (activeEstatChart) activeEstatChart.destroy();
        return;
      }

      indNames.forEach(name => {
        const opt = document.createElement("option");
        opt.value = name;
        opt.textContent = name;
        dropdown.appendChild(opt);
      });

      dropdown.value = indNames[0];
      renderEstatChart(takeharaStats, category, indNames[0]);
    }

    function renderEstatChart(takeharaStats, category, indicatorName) {
      const ctx = document.getElementById("chart-estat-timeseries");
      if (!ctx) return;
      if (activeEstatChart) activeEstatChart.destroy();

      const catData = takeharaStats[category] || {};
      const indObj = catData[indicatorName];
      if (!indObj || !Array.isArray(indObj.time_series) || indObj.time_series.length === 0) return;

      const labels = indObj.time_series.map(d => d.year + "年");
      const values = indObj.time_series.map(d => d.value);
      const unit = indObj.unit || "";

      const peakVal = Math.max(...values);
      const latestVal = values[values.length - 1];
      const startYear = indObj.time_series[0].year;
      const endYear = indObj.time_series[indObj.time_series.length - 1].year;

      const elSpan = document.getElementById("estat-span-label");
      const elPeak = document.getElementById("estat-peak-label");
      const elLatest = document.getElementById("estat-latest-label");

      if (elSpan) elSpan.textContent = `${startYear}年〜${endYear}年 (${values.length}時点)`;
      if (elPeak) elPeak.textContent = `${peakVal.toLocaleString()} ${unit}`;
      if (elLatest) elLatest.textContent = `${latestVal.toLocaleString()} ${unit}`;

      activeEstatChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              type: "line",
              label: `${indicatorName} (推移線)`,
              data: values,
              borderColor: "#D93829",
              borderWidth: 2.5,
              tension: 0.2,
              pointRadius: 4,
              pointBackgroundColor: "#D93829",
              yAxisID: "y"
            },
            {
              type: "bar",
              label: `${indicatorName} (実測値)`,
              data: values,
              backgroundColor: "rgba(245, 197, 24, 0.45)",
              borderColor: "#1E1E1E",
              borderWidth: 1.5,
              yAxisID: "y"
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "top",
              labels: { font: { family: "'JetBrains Mono'", weight: "bold", size: 11 } }
            },
            tooltip: {
              callbacks: {
                label: (c) => `${c.dataset.label}: ${c.parsed.y.toLocaleString()} ${unit}`
              }
            }
          },
          scales: {
            x: {
              ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
              grid: { color: "rgba(30,30,30,0.06)" }
            },
            y: {
              ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
              grid: { color: "rgba(30,30,30,0.06)" }
            }
          }
        }
      });
    }

    // Attach to initial render
    const origRenderGlobalHeader = renderGlobalHeader;
    renderGlobalHeader = function(report) {
      origRenderGlobalHeader(report);
      renderMicroDashboard();
    };
    """

    micro_js = micro_js_template.replace("__MICRO_PULSE_JSON__", micro_pulse_json)

    # Inject JS right before `// Initial Bootstrap`
    if "// Section M-JS" not in html:
        bootstrap_target = "// Initial Bootstrap"
        html = html.replace(bootstrap_target, f"{micro_js}\n\n    {bootstrap_target}")

    with open("frontend/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully integrated Micro Dashboard into frontend/index.html!")

if __name__ == "__main__":
    main()
