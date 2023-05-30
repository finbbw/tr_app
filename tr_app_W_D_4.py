import streamlit as st
import streamlit.components.v1 as components
#import pyperclip
import json

st.set_page_config(layout="wide")

WIDGET_HEIGHT = 500
WIDGET_WIDTH = 600
WIDGET_THEME = "dark"

def get_widget_header():
    return '''
      <div class="tradingview-widget-container">
      <div id="technical-analysis-chart-demo"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
    '''

def get_widget_footer():
    return '''
      );
      </script>
      </div>
    '''

@st.cache_data
def get_widget_body(ticker: str, interval: str, studies: list):
    widget = {
      "width": WIDGET_WIDTH,
      "height": WIDGET_HEIGHT,
      "symbol": ticker,
      "interval": interval,
      "timezone": "exchange",
      "theme": WIDGET_THEME,
      "style": "1",
      "range": "YTD" if interval == "D" else "60M",
      "withdateranges": True,
      "hide_side_toolbar": False,
      "allow_symbol_change": True,
      "studies": studies,
      "show_popup_button": True,
      "popup_width": "1900",
      "popup_height": "950",
      "locale": "en"
    }
    
    widget_str = json.dumps(widget)
    return widget_str

# Read the content of the clipboard
#clipboard_content = pyperclip.paste()
clipboard_content = "MSFT,PANW,PLTR,NVDA,SMCI,RMBS,TAST,OPRA,ACLS,AVGO,HUBS,IAS,ELF,XM,ENTG,VRT,MNDY,GRBK,SHOP,LI,COCO,AMAT,SNPS,MDB,MPWR,WDAY,ALTR,PEN,LNTH,INTT,BUR,INTA,CTIC,MRVL,WEAV,VYGR,RXST,AMD,ONTO,EXAS,BLDR,OKTA,CPA,META,DT,NOW,SMAR,DV,MSFT,MHO,CDNS,CRM,TOL,FICO,DUOL,ANET,MANH,CMG,PHM,ARCT,AMAM,PLAB,DDOG,KLAC,LRCX,ENS,NSSC,ASML,LPG,CXT,PANW,CPRT,TMHC,ORCL,INZY,CXM,LTH,NET,DSEY,NATI,NVO,NNOX,YMAB,ACVA,AEHR,DAKT,LQDA,TDC,TGTX,BASE,GOOG,NEO,EXP,DKNG,ETNB,ADBE,TTD,TPH,OTEX,SIBN,TDW,KBH,FTNT,RACE,FMX,VIST,MELI,FTAI,MRSN,NVTS,TNYA,ABST,CELH,NU,VECO,RCL,FLEX,ASRT,TSM,HLIT,ADMA,CRWD,GOOGL,JBL,NFLX,RYAAY,BSY,OLED,CSIQ,ARCO,VNT,SCPL,HUBB,CNM,SPNT,GE,ALGM,ANSS,WING,VERX,IOT,THC,TGLS,ONON,AI,IONQ,QTRX,CVGI,VICR,MOD,CFLT,SHAK,FTDR,CRSR,BDC,XPO,SPLK,RDN,INSP,SOVO,PGTI,BRBR,FOUR,TNK,KBAL,BKNG,PLYA,LW,WFRD,IMGN,RUTH,VSH,MORF,TBBK,ON,ESTC,LZ,FERG,DOLE,CLBT,HSBC,VIPS,YEXT,CVT,LFST,RPD,DECK,VRNA,WST,APLD,MDXG,SGH,KRYS,CRSP,EPM,GLBE,NSIT,NMIH,FLT,MMP,OC,MOMO,PRGS,QSR,NTES,ISRG,TK,DHI,YPF,NEWR,ACGL,LSCC,TERN,VECT,VSAT,ZUO,UBER,ADEA,ACAD,CVLT,DELL,VRSK,DOCN,TEAM,NABL,PRG,DRI,CHDN,CX,PAX,VMW,RRGB,TDG,AAPL,MNST,PWR,FLYW,SKX,LAUR,SWAV,MTH,ACLX,CRDO,KODK,APP,XP,AVDL,IMVT,UCTT,KNSA,PRTA,FROG"


# Split the input string by comma and remove any leading/trailing spaces
symbols = [symbol.strip() for symbol in clipboard_content.split(',')]

weekly_studies = [{"id": "MASimple@tv-basicstudies", "inputs": {"length": length}} for length in [10, 30]]
daily_studies = [{"id": "MASimple@tv-basicstudies", "inputs": {"length": length}} for length in [10, 20, 50, 200]]

# Iterate over symbols and create a new line every 4 symbols, then do it again for weekly chart
for i in range(0, len(symbols), 4):
    cols = st.columns(4)
    for j in range(i, min(i+4, len(symbols))):
        symbol = symbols[j]
        with cols[j-i]:
            components.html(
                get_widget_header() + get_widget_body(symbol, "W", weekly_studies) + get_widget_footer(), 
                height=WIDGET_HEIGHT, 
                width=WIDGET_WIDTH,
            )

    cols = st.columns(4)
    for j in range(i, min(i+4, len(symbols))):
        symbol = symbols[j]
        with cols[j-i]:
            components.html(
                get_widget_header() + get_widget_body(symbol, "D", daily_studies) + get_widget_footer(), 
                height=WIDGET_HEIGHT, 
                width=WIDGET_WIDTH,
            )
