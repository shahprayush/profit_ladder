import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import requests
import time
import schedule
from datetime import datetime
import warnings
from flask import Flask
from threading import Thread
import os

warnings.filterwarnings('ignore')

print("🟢 INITIATING SHADOW BROKER: Live Paper-Trading Engine [TELEGRAM EDITION]")

# ==========================================
# 1. LIVE CONFIGURATION & CREDENTIALS
# ==========================================
TELEGRAM_TOKEN = "8926726527:AAF8-xAb7zRwSCwWim3bypMP2xRfWmbxrW0"  # <-- Paste your BotFather token here
CHAT_ID = "2056261877"                # <-- Paste your numeric Chat ID here (from @userinfobot)

TICKERS = [
    # Large Cap (Nifty 50)
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
    "HINDUNILVR.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS",
    "LT.NS","AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","ASIANPAINT.NS",
    "WIPRO.NS","HCLTECH.NS","TITAN.NS","ULTRACEMCO.NS","SUNPHARMA.NS",
    "NESTLEIND.NS","POWERGRID.NS","NTPC.NS","TATASTEEL.NS","JSWSTEEL.NS",
    "ADANIENT.NS","ADANIPORTS.NS","COALINDIA.NS","ONGC.NS","BAJAJFINSV.NS",
    "TECHM.NS","DRREDDY.NS","CIPLA.NS","EICHERMOT.NS","HEROMOTOCO.NS",
    "DIVISLAB.NS","BRITANNIA.NS","GRASIM.NS","HINDALCO.NS","INDUSINDBK.NS",
    "BPCL.NS","TATACONSUM.NS","APOLLOHOSP.NS","UPL.NS","SBILIFE.NS",
    "HDFCLIFE.NS","SHRIRAMFIN.NS","BAJAJ-AUTO.NS","M&M.NS",
    
    # Nifty Next 50
    "ADANIGREEN.NS","ADANIPOWER.NS","AMBUJACEM.NS","DMART.NS",
    "GODREJCP.NS","HAVELLS.NS","ICICIGI.NS","INDIGO.NS","IOC.NS",
    "IRCTC.NS","JINDALSTEL.NS","LODHA.NS","LUPIN.NS",
    "MOTHERSON.NS","MUTHOOTFIN.NS","NAUKRI.NS","OFSS.NS","PAGEIND.NS",
    "PFC.NS","PIDILITIND.NS","POLYCAB.NS","RECLTD.NS","SIEMENS.NS",
    "SRF.NS","TATAPOWER.NS","TORNTPHARM.NS","TRENT.NS","VBL.NS",
    "VEDL.NS","ZOMATO.NS","ZYDUSLIFE.NS","NYKAA.NS","PAYTM.NS",
    "CANBK.NS","BANKBARODA.NS","NHPC.NS","HUDCO.NS",
    
    # MidCap
    "ABCAPITAL.NS","ACC.NS","AIAENG.NS","ALKEM.NS","APLAPOLLO.NS",
    "APOLLOTYRE.NS","ASHOKLEY.NS","ASTRAL.NS","ATUL.NS","AUBANK.NS",
    "AUROPHARMA.NS","BALKRISIND.NS","BANDHANBNK.NS","BATAINDIA.NS",
    "BERGEPAINT.NS","BIOCON.NS","BOSCHLTD.NS","BSOFT.NS","CANFINHOME.NS",
    "CHOLAFIN.NS","COFORGE.NS","CONCOR.NS","CROMPTON.NS","CUMMINSIND.NS",
    "DABUR.NS","DALBHARAT.NS","DCBBANK.NS","DEEPAKNTR.NS","DELHIVERY.NS",
    "DIXON.NS","EMAMILTD.NS","ENDURANCE.NS","ESCORTS.NS","EXIDEIND.NS",
    "FEDERALBNK.NS","GLENMARK.NS","GODREJPROP.NS",
    "GRANULES.NS","GUJGASLTD.NS","HAL.NS","HFCL.NS","HINDPETRO.NS",
    "IDFCFIRSTB.NS","IEX.NS","IPCALAB.NS","IRB.NS",
    "JKCEMENT.NS","JUBLPHARMA.NS","JUBLFOOD.NS","KAJARIACER.NS",
    "KPITTECH.NS","LALPATHLAB.NS","LAURUSLABS.NS","LICHSGFIN.NS","LTTS.NS",
    "MANAPPURAM.NS","MARICO.NS","MAXHEALTH.NS","MCX.NS","METROPOLIS.NS",
    "MFSL.NS","MGL.NS","MPHASIS.NS","NAM-INDIA.NS","NATIONALUM.NS",
    "NBCC.NS","NCC.NS","NMDC.NS","OBEROIRLTY.NS","OIL.NS",
    "PATANJALI.NS","PERSISTENT.NS","PETRONET.NS","PIIND.NS","PNB.NS",
    "POLICYBZR.NS","PRESTIGE.NS","PVRINOX.NS","RAMCOCEM.NS",
    "SCHAEFFLER.NS","SKFINDIA.NS","SONACOMS.NS","STARHEALTH.NS","SYNGENE.NS",
    "TATACOMM.NS","TATAELXSI.NS","TVSMOTOR.NS","UNIONBANK.NS",
    "VOLTAS.NS","ZEEL.NS","MOTILALOFS.NS","CDSL.NS","ANGELONE.NS",
    "NUVAMA.NS","IRFC.NS","IREDA.NS","RVNL.NS","TITAGARH.NS",
    "RAILTEL.NS","TEJASNET.NS","JSWENERGY.NS","SJVN.NS","JPPOWER.NS",
    
    # SmallCap
    "AARTIIND.NS","ACE.NS","AJANTPHARM.NS","AKZOINDIA.NS",
    "ANANTRAJ.NS","APARINDS.NS","APTUS.NS","ASAHIINDIA.NS",
    "BEML.NS","BEL.NS","BLUESTARCO.NS","BRIGADE.NS",
    "CAMPUS.NS","CARBORUNIV.NS","CASTROLIND.NS","CEATLTD.NS",
    "CESC.NS","CLEAN.NS","CMSINFO.NS","COCHINSHIP.NS",
    "COROMANDEL.NS","CRAFTSMAN.NS","DELTACORP.NS","EIDPARRY.NS",
    "EPL.NS","EQUITASBNK.NS","FINEORG.NS","FORCEMOT.NS","FORTIS.NS",
    "GALAXYSURF.NS","GHCL.NS","GLAXO.NS","GNFC.NS","GRINDWELL.NS",
    "HAPPSTMNDS.NS","HEG.NS","HIKAL.NS","IGL.NS",
    "INDHOTEL.NS","INDIAMART.NS","INOXWIND.NS","JAMNAAUTO.NS",
    "JBCHEPHARM.NS","JINDALPOLY.NS","JKTYRE.NS",
    "JUSTDIAL.NS","KANSAINER.NS","KARURVYSYA.NS","KNRCON.NS",
    "KRBL.NS","KTKBANK.NS","LAOPALA.NS","MATRIMONY.NS",
    "MEDPLUS.NS","MIDHANI.NS","MOIL.NS","MRPL.NS",
    "NATCOPHARM.NS","NAVINFLUOR.NS","NILKAMAL.NS","NOCIL.NS","NUVOCO.NS",
    "ORIENTCEM.NS","PGHH.NS","PHOENIXLTD.NS","PNCINFRA.NS",
    "PRINCEPIPE.NS","RADICO.NS","RATNAMANI.NS","REDINGTON.NS",
    "RELAXO.NS","ROSSARI.NS","SAFARI.NS","SAREGAMA.NS",
    "SOBHA.NS","SPARC.NS","STLTECH.NS","SURYAROSNI.NS","SYMPHONY.NS",
    "TANLA.NS","TATACHEM.NS","TATAINVEST.NS","TCIEXP.NS",
    "TEAMLEASE.NS","THERMAX.NS","THYROCARE.NS","TIMKEN.NS",
    "TTKPRESTIG.NS","UCOBANK.NS","UJJIVANSFB.NS","UNOMINDA.NS",
    "VGUARD.NS","VINATIORGA.NS","VSTIND.NS","WABAG.NS",
    "WONDERLA.NS","ZENSARTECH.NS","SOLARINDS.NS","POLYMED.NS",
    "NEULANDLAB.NS","JYOTHYLAB.NS","GENUSPOWER.NS","ELGIEQUIP.NS",
    "ECLERX.NS","CYIENT.NS","CHEMPLASTS.NS","DATAPATTNS.NS",
    "CREDITACC.NS","AETHER.NS","ADFFOODS.NS","ACCELYA.NS",
    "GPIL.NS","GESHIP.NS"
]
MACRO_TICKER = "^NSEI"  

INITIAL_CAPITAL = 36000.0
RISK_PER_TRADE = 0.04
FAST_LEN, SLOW_LEN, TREND_LEN = 13, 34, 100

# [OPTIMIZED METRICS]
T1_PCT, T2_PCT, T3_PCT = 0.06, 0.12, 0.20  
ATR_LEN, ATR_SL_MULT = 14, 0.3
AI_CONFIDENCE_THRESHOLD = 0.62  

rf_model = None
scaler = None

# ==========================================
# 2. RENDER.COM KEEP-ALIVE WEB SERVER HACK
# ==========================================
web_app = Flask(__name__)

@web_app.route('/')
def heartbeat():
    return "Shadow Broker Apex Engine is ALIVE and running."

def run_server():
    port = int(os.environ.get('PORT', 8080))
    web_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    print("🚀 Flask Web Server opened successfully. Render port scan satisfied.")

# ==========================================
# 3. TELEGRAM BRIDGE
# ==========================================
def send_telegram_msg(msg):
    if not CHAT_ID or "YOUR_" in CHAT_ID:
        print("[!] Chat ID not hardcoded properly. Skipping alert.")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, data=payload)
        print("[TELEGRAM SENT]")
    except Exception as e:
        print(f"[!] Error sending Telegram message: {e}")

# ==========================================
# 4. CORE INDICATORS 
# ==========================================
def calculate_rsi(data, window=14):
    delta = data.diff()
    up, down = delta.clip(lower=0), -1 * delta.clip(upper=0)
    rs = up.ewm(com=window-1, adjust=False).mean() / down.ewm(com=window-1, adjust=False).mean()
    return 100 - (100 / (1 + rs))

def calculate_atr(df, window=14):
    ranges = pd.concat([
        df['High'] - df['Low'],
        np.abs(df['High'] - df['Close'].shift()),
        np.abs(df['Low'] - df['Close'].shift())
    ], axis=1)
    return np.max(ranges, axis=1).ewm(alpha=1/window, adjust=False).mean()

# ==========================================
# 5. STARTUP: TRAIN THE AI BRAIN
# ==========================================
def train_current_brain():
    global rf_model, scaler
    print("[*] Downloading historical data to train the AI for today's market...")
    
    nifty = yf.download(MACRO_TICKER, start="2019-01-01", end="2024-01-01", progress=False)
    if isinstance(nifty.columns, pd.MultiIndex):
        nifty.columns = nifty.columns.get_level_values(0)
    
    nifty.index = pd.to_datetime(nifty.index).tz_localize(None)
    nifty['Macro_Bull'] = nifty['Close'] > nifty['Close'].ewm(span=200, adjust=False).mean()
    macro_dict = nifty['Macro_Bull'].to_dict()

    master_df = []
    for ticker in TICKERS:
        try:
            df = yf.download(ticker, start="2019-01-01", end="2024-01-01", progress=False)
            if df.empty or len(df) < 100: continue
            
            # [CRITICAL MULTIINDEX FLATTENER]
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            df.index = pd.to_datetime(df.index).tz_localize(None)
            
            df['EMA_Fast'] = df['Close'].ewm(span=FAST_LEN, adjust=False).mean()
            df['EMA_Slow'] = df['Close'].ewm(span=SLOW_LEN, adjust=False).mean()
            df['EMA_Trend'] = df['Close'].ewm(span=TREND_LEN, adjust=False).mean()
            df['ATR'] = calculate_atr(df, ATR_LEN)
            df['Vol_SMA'] = df['Volume'].rolling(window=20).mean()
            df['F_RSI'] = calculate_rsi(df['Close'], 14)
            df['F_Vol_Ratio'] = df['Volume'] / df['Vol_SMA']
            df['F_Distance_EMA'] = (df['Close'] - df['EMA_Fast']) / df['Close']
            df['F_ATR_Pct'] = df['ATR'] / df['Close']
            
            df['Trend_Ok'] = (df['Close'] > df['EMA_Trend']) & (df['EMA_Slow'] > df['EMA_Trend'])
            df['Pullback_Ok'] = (df['Close'].shift(1) < df['EMA_Fast'].shift(1)) | (df['Close'].shift(2) < df['EMA_Fast'].shift(2))
            df['Cross_Ok'] = (df['Close'].shift(1) < df['EMA_Fast'].shift(1)) & (df['Close'] >= df['EMA_Fast'])
            
            df['Future_High'] = df['High'].rolling(window=15).max().shift(-15)
            df['Target_Hit'] = (df['Future_High'] >= df['Close'] * (1 + T1_PCT)).astype(int)
            df['Macro_Bull'] = df.index.map(macro_dict).fillna(False)
            
            valid = df[df['Trend_Ok'] & df['Pullback_Ok'] & df['Cross_Ok'] & df['Macro_Bull']].copy()
            if not valid.empty: master_df.append(valid)
        except Exception as e:
            continue

    if not master_df:
        print("[!] No training setups found. Falling back to default random initialization.")
        return

    combined = pd.concat(master_df).dropna().sort_index()
    X = combined[['F_RSI', 'F_Vol_Ratio', 'F_Distance_EMA', 'F_ATR_Pct']]
    y = combined['Target_Hit']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, class_weight='balanced')
    rf_model.fit(X_scaled, y)
    print(f"✅ AI Brain successfully trained on {len(combined)} historical setups.")
    send_telegram_msg("🟢 *Apex Engine Online*\nAI Engine deployed on Render. Actively monitoring Nifty 500.")

# ==========================================
# 6. LIVE MARKET SCANNER
# ==========================================
def scan_markets():
    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{now}] 📡 Scanning NSE for institutional setups...")
    if rf_model is None or scaler is None:
        print("[!] AI Model not loaded yet. Skipping scan.")
        return
        
    try:
        nifty = yf.download(MACRO_TICKER, period="200d", progress=False)
        if isinstance(nifty.columns, pd.MultiIndex):
            nifty.columns = nifty.columns.get_level_values(0)
            
        nifty_close = float(nifty['Close'].iloc[-1])
        nifty_200 = float(nifty['Close'].ewm(span=200, adjust=False).mean().iloc[-1])
        
        if nifty_close < nifty_200:
            print("[!] Macro Regime is BEARISH. AI scanner is safety-locked.")
            return

        for ticker in TICKERS:
            try:
                df = yf.download(ticker, period="150d", progress=False)
                if df.empty or len(df) < 100: continue
                
                # [CRITICAL MULTIINDEX FLATTENER]
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                close = float(df['Close'].iloc[-1])
                low = float(df['Low'].iloc[-1])
                volume = float(df['Volume'].iloc[-1])
                
                ema_fast = df['Close'].ewm(span=FAST_LEN, adjust=False).mean()
                ema_slow = df['Close'].ewm(span=SLOW_LEN, adjust=False).mean()
                ema_trend = df['Close'].ewm(span=TREND_LEN, adjust=False).mean()
                atr = calculate_atr(df, ATR_LEN)
                vol_sma = df['Volume'].rolling(window=20).mean()
                rsi = calculate_rsi(df['Close'], 14)
                
                cur_ema_fast = float(ema_fast.iloc[-1])
                cur_ema_slow = float(ema_slow.iloc[-1])
                cur_ema_trend = float(ema_trend.iloc[-1])
                cur_atr = float(atr.iloc[-1])
                cur_rsi = float(rsi.iloc[-1])
                cur_vol_ratio = volume / float(vol_sma.iloc[-1])
                
                trend_ok = (close > cur_ema_trend) and (cur_ema_slow > cur_ema_trend)
                pullback_ok = (float(df['Close'].iloc[-2]) < float(ema_fast.iloc[-2])) or (float(df['Close'].iloc[-3]) < float(ema_fast.iloc[-3]))
                cross_ok = (float(df['Close'].iloc[-2]) < float(ema_fast.iloc[-2])) and (close >= cur_ema_fast)
                
                if trend_ok and pullback_ok and cross_ok:
                    dist_ema = (close - cur_ema_fast) / close
                    atr_pct = cur_atr / close
                    features = scaler.transform([[cur_rsi, cur_vol_ratio, dist_ema, atr_pct]])
                    ai_prob = rf_model.predict_proba(features)[0][1]
                    
                    if ai_prob >= AI_CONFIDENCE_THRESHOLD:
                        risk_per_share = max(close - (low - ATR_SL_MULT * cur_atr), close * 0.005)
                        total_risk = INITIAL_CAPITAL * RISK_PER_TRADE
                        qty = int(min(total_risk / risk_per_share, (INITIAL_CAPITAL * 0.50) / close))
                        
                        t1 = round(close * (1 + T1_PCT), 2)
                        sl = round(close - risk_per_share, 2)
                        
                        msg = f"🔥 *PAPER ENTRY SIGNAL*\n" \
                              f"Ticker: {ticker}\n" \
                              f"Price: ₹{close:.2f}\n" \
                              f"AI Confidence: {ai_prob*100:.1f}%\n" \
                              f"Qty: {qty} shares\n" \
                              f"Target 1: ₹{t1} | SL: ₹{sl}"
                        
                        send_telegram_msg(msg)
            except Exception as ticker_err:
                continue
                        
    except Exception as e:
        print(f"[!] Error in scan loop: {e}")

# ==========================================
# 7. EXECUTION ENGINE
# ==========================================
if __name__ == "__main__":
    # 1. Open web server instantly so Render port scanner passes
    keep_alive()
    
    # 2. Train the internal brain matrix
    train_current_brain()
    
    # 3. Schedule operational scan loops every 30 minutes
    schedule.every(30).minutes.do(scan_markets)
    scan_markets() 
    
    while True:
        schedule.run_pending()
        time.sleep(60)
