# REQUIREMENTS: flask, gunicorn, yfinance, requests
import os
import random
import datetime
import hashlib
from flask import Flask

# --- 專案配置 ---
# 選擇要進行壓力測試的目標股票
TARGET_TICKERS = ['NVDA', 'AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN', 'META']
# 模擬的全球節點位置
GLOBAL_NODES = [
    {'name': 'Tokyo', 'style': 'top: 35%; left: 85%;'},
    {'name': 'Berlin', 'style': 'top: 25%; left: 53%;'},
    {'name': 'São Paulo', 'style': 'top: 75%; left: 35%;'},
    {'name': 'Taipei', 'style': 'top: 40%; left: 80%;'},
    {'name': 'San Francisco', 'style': 'top: 32%; left: 10%;'},
    {'name': 'Mumbai', 'style': 'top: 45%; left: 68%;'},
]

# --- 初始化 Flask 應用 ---
app = Flask(__name__)

# --- 核心生成引擎 (The Oracle - Simulated) ---
def generate_chimera_article(stock_info):
    """根據真實股票數據，生成一篇看似合理但標記為虛構的財經新聞。"""
    company_name = stock_info['longName']
    ticker = stock_info['symbol']
    price = stock_info['currentPrice']

    headline_templates = [
        f"【內部消息】{company_name} ({ticker}) 秘密開發代號為「{random.choice(['Odyssey', 'Vanguard', 'Apex'])}」的新項目",
        f"【市場傳聞】{company_name} ({ticker}) 下一代產品或因供應鏈問題延遲 {random.randint(1,2)} 季",
        f"【分析師突發報告】{company_name} ({ticker}) 正與一家未公開的歐洲公司進行數十億美元的收購談判",
        f"【獨家】{company_name} ({ticker}) 核心技術專利面臨意想不到的法律挑戰",
        f"【地緣政治觀察】{random.choice(['東南亞', '拉丁美洲'])} 新規或將衝擊 {company_name} ({ticker}) 的擴張計畫"
    ]

    body_templates = [
        f"據不願透露姓名的消息人士稱，{company_name} 的一個精英團隊正在秘密進行一項顛覆性研究，可能重塑整個行業。目前股價 {price} USD 尚未完全反應此預期。",
        f"來自亞洲供應鏈的報告指出，關鍵零組件的良率低於預期，這可能導致 {company_name} 的旗艦產品發布推遲。市場對此保持高度關注，股價 {price} USD 出現小幅波動。",
        f"華爾街頂級分析師 John Doe 在一份給VIP客戶的報告中指出，{company_name} 的併購目標可能是一家專精於 {random.choice(['AI算法', '新材料', '能源效率'])} 的利基市場領導者。此舉將使其護城河更加深厚。",
        f"一份被洩漏的法律文件顯示，一家小型但擁有關鍵專利組合的公司，正準備對 {company_name} 發起專利侵權訴訟，索賠金額可能高達公司季度利潤的 {random.randint(5, 15)}%。",
        f"最新的國際貿易政策變化，可能對 {company_name} 在新興市場的布局產生實質性影響。公司發言人對此不予置評，但市場已開始評估其對未來營收的潛在衝擊，當前股價為 {price} USD。"
    ]

    headline = random.choice(headline_templates)
    body = random.choice(body_templates)

    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    content_to_hash = f"{headline}{body}{timestamp}".encode('utf-8')
    signature = hashlib.sha256(content_to_hash).hexdigest()
    stigmata = f"CHIMERA-FICTION-{signature[:16]}"

    return {
        "headline": headline, "body": body, "stigmata": stigmata,
        "timestamp": timestamp, "ticker": ticker
    }

# --- 數據獲取層 ---
def get_stock_data_safely(ticker_symbol):
    """安全地從 Yahoo Finance 獲取數據，處理可能的錯誤。"""
    try:
        import yfinance as yf
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        if 'longName' not in info or 'currentPrice' not in info or 'previousClose' not in info:
            return {'symbol': ticker_symbol, 'longName': f'{ticker_symbol} (Data Error)', 'currentPrice': 0.0, 'previousClose': 0.0, 'change': 0.0, 'changePercent': 0.0}

        price = info.get('currentPrice', 0.0)
        prev_close = info.get('previousClose', 1.0)
        change = price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close != 0 else 0

        return {'symbol': info.get('symbol', ticker_symbol), 'longName': info.get('longName', 'Unknown Company'), 'currentPrice': price, 'previousClose': prev_close, 'change': round(change, 2), 'changePercent': round(change_percent, 2)}
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return {'symbol': ticker_symbol, 'longName': f'{ticker_symbol} (API Error)', 'currentPrice': 0.0, 'previousClose': 0.0, 'change': 0.0, 'changePercent': 0.0}

# --- 儀表板前端渲染 ---
# 【UI/UX 強化】引入科幻字體、玻璃擬態、輝光、互動效果與動畫
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Chimera :: Genesis Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        .font-orbitron {{ font-family: 'Orbitron', sans-serif; }}
        .font-tech-mono {{ font-family: 'Share Tech Mono', monospace; }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.2); }}
        }}
        .node-pulse {{
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            transition: all 0.3s ease;
        }}
        .node-pulse:hover {{
            transform: scale(1.8);
            background-color: #f0abfc; /* Light Purple */
            opacity: 1;
        }}

        .stigmata-tag {{
            background-color: #4a044e; color: #a7f3d0; padding: 2px 6px;
            border-radius: 4px; font-size: 0.75rem; border: 1px solid #a7f3d0;
        }}

        .text-glow {{
            text-shadow: 0 0 8px rgba(192, 132, 252, 0.7);
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes glow-pulse-animation {{
            0% {{ box-shadow: 0 0 4px rgba(192, 132, 252, 0.3); }}
            50% {{ box-shadow: 0 0 16px rgba(192, 132, 252, 0.8); }}
            100% {{ box-shadow: 0 0 4px rgba(192, 132, 252, 0.3); }}
        }}
        .glow-pulse {{
            animation: glow-pulse-animation 1.5s ease-in-out;
        }}
    </style>
</head>
<body class="bg-gray-900 text-gray-200 font-tech-mono" style="background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px); background-size: 20px 20px;">
    <div class="container mx-auto p-4 md:p-8">
        <header class="text-center mb-8" style="animation: fadeIn 0.5s ease-in-out;">
            <h1 class="text-4xl md:text-5xl font-bold text-purple-300 tracking-wider font-orbitron text-glow">PROJECT CHIMERA</h1>
            <p class="text-lg text-gray-400 mt-2">Rebuilding Signal in an Ocean of Noise</p>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- 左欄：全球節點與市場狀態 -->
            <div class="lg:col-span-1 space-y-6" style="animation: fadeIn 0.8s ease-in-out 0.2s; animation-fill-mode: backwards;">
                <!-- 全球散佈節點 -->
                <div class="bg-gray-800/60 backdrop-blur-sm border border-gray-700 p-6 rounded-lg shadow-lg">
                    <h2 class="text-xl font-semibold text-purple-300 border-b border-gray-700 pb-2 mb-4 font-orbitron text-glow">Global Chimera Nodes</h2>
                    <div class="relative">
                        <img src="https://raw.githubusercontent.com/d3/d3.github.com/master/world-110m.v1.json/world-110m.png" alt="World Map" class="w-full h-auto opacity-20">
                        {nodes_html}
                    </div>
                </div>

                <!-- 市場狀態 -->
                <div class="bg-gray-800/60 backdrop-blur-sm border border-gray-700 p-6 rounded-lg shadow-lg">
                    <h2 class="text-xl font-semibold text-purple-300 border-b border-gray-700 pb-2 mb-4 font-orbitron text-glow">Market Vitals (Source)</h2>
                    <div class="space-y-2">
                        {market_data_html}
                    </div>
                </div>
            </div>

            <!-- 右欄：奇美拉資訊流 -->
            <div class="lg:col-span-2 bg-gray-800/60 backdrop-blur-sm border border-gray-700 p-6 rounded-lg shadow-lg" style="animation: fadeIn 0.8s ease-in-out 0.4s; animation-fill-mode: backwards;">
                <h2 class="text-xl font-semibold text-purple-300 border-b border-gray-700 pb-2 mb-4 font-orbitron text-glow">Live Chimera Feed</h2>
                <div class="space-y-6 overflow-y-auto h-[70vh] pr-2">
                    {chimera_feed_html}
                </div>
            </div>
        </div>
        <footer class="text-center mt-8 text-gray-500 text-sm">
            <p>This is a conceptual demonstration. All generated news articles are programmatically created fictions for system stress-testing.</p>
            <p>Project Chimera &copy; {current_year}. All rights reserved. No privacy is invaded. No local files are accessed.</p>
        </footer>
    </div>
    <script>
        const latestArticle = document.getElementById('latest-article');
        if (latestArticle) {{
            setInterval(() => {{
                latestArticle.classList.add('glow-pulse');
                setTimeout(() => {{
                    latestArticle.classList.remove('glow-pulse');
                }}, 1500); // Duration of the glow
            }}, 7000); // Every 7 seconds
        }}
    </script>
</body>
</html>
"""

# --- 路由定義 ---
@app.route('/')
def dashboard():
    # 1. 生成全球節點的 HTML
    nodes_html = ""
    for i, node in enumerate(GLOBAL_NODES):
        delay = i * 0.2
        nodes_html += f'<div class="absolute w-3 h-3 bg-purple-400 rounded-full node-pulse" style="{node["style"]} animation-delay: {delay}s;" title="{node["name"]}"></div>'

    # 2. 獲取市場數據並生成 HTML
    market_data_html = ""
    all_stock_data = []
    for ticker in TARGET_TICKERS:
        data = get_stock_data_safely(ticker)
        all_stock_data.append(data)

        color_class = "text-green-400" if data['change'] >= 0 else "text-red-400"
        sign = "+" if data['change'] >= 0 else ""

        # 【UI/UX 強化】增加懸停互動效果
        market_data_html += f"""
        <div class="flex justify-between items-center text-sm p-2 rounded-md transition-all duration-200 hover:bg-gray-700/50 hover:scale-105 cursor-pointer">
            <span class="font-bold text-gray-300 w-1/3">{data['symbol']}</span>
            <span class="w-1/3 text-center">{data['currentPrice']:.2f}</span>
            <span class="{color_class} w-1/3 text-right">{sign}{data['change']:.2f} ({sign}{data['changePercent']:.2f}%)</span>
        </div>
        """

    # 3. 生成奇美拉資訊流並生成 HTML
    chimera_feed_html = ""
    for i, stock_data in enumerate(all_stock_data):
        if stock_data['currentPrice'] > 0:
            article = generate_chimera_article(stock_data)
            # 【UI/UX 強化】增加卡片懸停效果、進場動畫，並為最新卡片加上 ID
            article_id = 'id="latest-article"' if i == 0 else ''
            animation_delay = 0.5 + i * 0.1
            animation_style = f'style="animation: fadeIn 0.5s ease-in-out {animation_delay}s; animation-fill-mode: backwards;"'

            chimera_feed_html += f"""
            <div {article_id} {animation_style} class="bg-gray-900/50 p-4 rounded-md border border-gray-700 transition-all duration-300 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20 hover:-translate-y-1">
                <h3 class="font-bold text-purple-300 text-glow">{article['headline']}</h3>
                <p class="text-gray-400 text-sm mt-2 mb-3">{article['body']}</p>
                <div class="flex justify-between items-center text-xs text-gray-500">
                    <span>Target: ${article['ticker']}</span>
                    <span class="stigmata-tag" title="This is a verifiable, non-malicious fictional content marker.">{article['stigmata']}</span>
                </div>
            </div>
            """

    # 4. 渲染最終的 HTML 頁面
    current_year = datetime.datetime.now().year
    return HTML_TEMPLATE.format(
        nodes_html=nodes_html,
        market_data_html=market_data_html,
        chimera_feed_html=chimera_feed_html,
        current_year=current_year
    )

# --- 伺服器啟動 ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
