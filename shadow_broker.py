import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import requests
import time
import schedule
from flask import Flask
from threading import Thread
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("🟢 INITIATING SHADOW BROKER: Live Paper-Trading Engine [TELEGRAM EDITION]")

# ==========================================
# 1. LIVE CONFIGURATION & CREDENTIALS
# ==========================================
TELEGRAM_TOKEN = "8926726527:AAF8-xAb7zRwSCwWim3bypMP2xRfWmbxrW0"  # Paste your BotFather token here
CHAT_ID = "" # Leave blank; the script will auto-detect this

TICKERS = [
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
# 2. TELEGRAM SECURE BRIDGE
# ==========================================
def get_chat_id():
    global CHAT_ID
    if CHAT_ID != "": return CHAT_ID
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        response = requests.get(url).json()
        if response.get("result"):
            CHAT_ID = str(response["result"][0]["message"]["chat"]["id"])
            send_telegram_msg("🟢 *Apex Engine Online*\nAI Brain successfully trained. Monitoring live markets.")
            return CHAT_ID
        else:
            print("[!] Cannot find Chat ID. Did you send a message to your bot on Telegram?")
            return None
    except Exception as e:
        print(f"[!] Telegram Connection Error: {e}")
        return None

def send_telegram_msg(msg):
    if not get_chat_id(): return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, data=payload)
    print(f"[TELEGRAM SENT]")

# ==========================================
# 3. CORE INDICATORS 
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
# RENDER.COM KEEP-ALIVE HACK
# ==========================================
app = Flask(__name__)

@app.route('/')
def heartbeat():
    return "Apex Engine is ALIVE."

def run_server():
    # Render automatically provides a PORT environment variable
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

# ==========================================
# 4. STARTUP: TRAIN THE AI BRAIN FOR TODAY
# ==========================================
def train_current_brain():
    global rf_model, scaler
    print("[*] Downloading historical data to train the AI for today's market...")
    
    nifty = yf.download(MACRO_TICKER, start="2019-01-01", end="2024-01-01", progress=False)
    nifty.index = pd.to_datetime(nifty.index).tz_localize(None)
    nifty['Macro_Bull'] = nifty['Close'] > nifty['Close'].ewm(span=200, adjust=False).mean()
    macro_dict = nifty['Macro_Bull'].to_dict()

    master_df = []
    for ticker in TICKERS:
        df = yf.download(ticker, start="2019-01-01", end="2024-01-01", progress=False)
        if df.empty: continue
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

    combined = pd.concat(master_df).dropna().sort_index()
    X = combined[['F_RSI', 'F_Vol_Ratio', 'F_Distance_EMA', 'F_ATR_Pct']]
    y = combined['Target_Hit']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, class_weight='balanced')
    rf_model.fit(X_scaled, y)
    print(f"✅ AI Brain trained on {len(combined)} historical setups.")

# ==========================================
# 5. LIVE MARKET SCANNER
# ==========================================
def scan_markets():
    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{now}] 📡 Scanning NSE for institutional setups...")
    
    try:
        nifty = yf.download(MACRO_TICKER, period="200d", progress=False)
        nifty_close = float(nifty['Close'].iloc[-1])
        nifty_200 = float(nifty['Close'].ewm(span=200, adjust=False).mean().iloc[-1])
        
        if nifty_close < nifty_200:
            print("[!] Macro Regime is BEARISH. AI is physically locked down.")
            return

        for ticker in TICKERS:
            df = yf.download(ticker, period="150d", progress=False)
            if df.empty or len(df) < 100: continue
            
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
                    
                    with open("paper_ledger.csv", "a") as f:
                        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')},{ticker},{close},{qty},{sl},{t1},{ai_prob}\n")
                        
    except Exception as e:
        print(f"[!] Error in scan loop: {e}")

# ==========================================
# 6. EXECUTION ENGINE
# ==========================================
if __name__ == "__main__":
    keep_alive()           # <-- THIS MUST BE FIRST!
    get_chat_id()
    train_current_brain()
    
    schedule.every(30).minutes.do(scan_markets)
    print("\n✅ System armed. Monitoring live markets in the background...")
    scan_markets() 
    
    while True:
        schedule.run_pending()
        time.sleep(60)
