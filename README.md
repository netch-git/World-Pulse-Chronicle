# World Pulse Chronicle (国際オープンデータ自律因果分析フィールドノート)

> **「デジタル方眼ノート × ネオブルータリズム」デザインで編む、国際オープンデータ自律因果分析パイプライン**

![World Pulse Chronicle Architecture](https://img.shields.io/badge/Gemini_API-3.8_Flash-blue?style=flat-square)
![Design](https://img.shields.io/badge/Design-Grid--Note%20%C3%97%20Neo--Brutalism-F5C518?style=flat-square)
![Open Data](https://img.shields.io/badge/Open_Data-WB%20%7C%20CCKP%20%7C%20FAO%20%7C%20OECD%20%7C%20Markets-green?style=flat-square)
![Deploy](https://img.shields.io/badge/Cloudflare_Pages-Ready-F38020?style=flat-square)

---

## 📖 概要

『World Pulse Chronicle』は、世界銀行（World Bank）、気候変動ナレッジポータル（CCKP）、国際連合食糧農業機関（FAOSTAT）、経済協力開発機構（OECD）、および国際商品先物・為替市場のオープンデータを定期・自律収集し、Gemini APIを用いて異種データ間の4段階因果連鎖を構造化解説する自律型インテリジェンス・システムです。

### 🌟 特徴

1. **デジタル方眼ノート × ネオブルータリズム デザイン:**
   - 20px方眼紙テクスチャ（`#FAF8F0`）、ソリッド黒枠（`1.5px/2px solid #1E1E1E`）、ソリッドシャドウ（`0px 4px 0px #1E1E1E`）。ぼかし影を一切排除した知的でクリーンな手帳スタイル。
   - 見切れのないスムーズ・インデックスタブ（左右ナビゲーション `◀` / `▶`、ホイール横スクロール連動、`▤ WRAP` 表示切替）。
2. **最先端データサイエンス分析エンジン:**
   - **ピアソン相関係数 ($r$) & 決定係数 ($R^2$):** 変数間の線形相関度を自動算出。
   - **時系列ラグ相互相関 ($\tau$):** 主系列が副系列に対して何年先行（または遅行）しているかを判定。
   - **レジーム転換点 (Tipping Point):** 2系列の複合変化率が最大となった構造的急変年度を自動同定。
   - **年平均成長率 (CAGR):** 両系列の成長速度を対比。
3. **3つの可視化モード (`Chart.js 4.x`):**
   - `[ 2-AXIS COMBO ]`: 標準2軸（棒グラフ $\times$ 折れ線グラフ）
   - `[ BASE 100 NORMALIZED ]`: 基準年2017=100.0 相対比較（単位差を超えた真のデカップリング・ダイバージェンス追跡）
   - `[ SCATTER & REGRESSION ]`: 2変数散布図 ＋ 最小二乗回帰トレンドライン（$y = ax + b$）
4. **自律的テーマ発見・夜通し成長エンジン (`autonomous_harvester.py`):**
   - 15分間隔でオープンデータを探索し、Gemini 3.8 Flash (google-genai SDK / Structured Outputs) により新しい因果テーマを自律発見・蓄積。

---

## 📁 ディレクトリ構成

```text
World-Pulse-Chronicle/
├── frontend/
│   └── index.html               # 「方眼ノート×ネオブルータリズム」単体動作SPA
├── backend/
│   ├── main.py                  # FastAPI バックエンド (データ取得・Gemini推論・API提供)
│   ├── requirements.txt         # Python 依存ライブラリ
│   └── Dockerfile               # Cloud Run / Docker 用コンテナ定義
├── autonomous_harvester.py       # 夜通し自律オープンデータ収集・テーマ発見デーモン
├── MORNING_INSPECTION_REPORT.md # 毎朝の点検用自動生成サマリードキュメント
├── latest_cache.json            # 蓄積された最新全テーマデータセット
└── deploy.sh                    # GCP Cloud Run & Cloud Scheduler 自動デプロイスクリプト
```

---

## 🚀 クイックスタート

### 1. ローカル起動 (FastAPI + フロントエンド)

```bash
# 依存パッケージのインストール
pip install -r backend/requirements.txt

# サーバー起動 (ポート 8000)
python -m uvicorn backend.main:app --port 8000
```

ブラウザで `http://localhost:8000/` を開くと、全テーマの閲覧およびインタラクティブ分析が可能です。

### 2. 自律ハーベスターの実行

```bash
# 翌朝 04:00 JST まで15分間隔で新テーマを自律発掘・成長させる
python autonomous_harvester.py --until-hour 4 --interval-minutes 15
```

---

## ☁️ デプロイ

### Cloudflare Pages
フロントエンドは `frontend/index.html` 単体で完全動作（内蔵シードデータおよびクライアント側データサイエンス算出）するように設計されており、Cloudflare Pages に即時デプロイ可能です。

### GCP (Cloud Run + Cloud Scheduler)
常時無料枠（Always Free）構成に最適化されています。

```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 📜 ライセンス

MIT License
