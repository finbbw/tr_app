import streamlit as st
import streamlit.components.v1 as components
import json
import math

st.set_page_config(layout="wide")

WIDGET_HEIGHT = 350
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

@st.cache
def get_widget_body(ticker: str, interval: str, studies: list):
    widget = {
      "width": WIDGET_WIDTH,
      "height": WIDGET_HEIGHT,
      "symbol": ticker,
      "interval": interval,
      "timezone": "exchange",
      "theme": WIDGET_THEME,
      "style": "1",
      "range": "YTD" if interval == "D" else "40M",
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

default_symbols = "MSFT,PANW,PLTR,NVDA,SMCI,RMBS,TAST,OPRA,ACLS,AVGO,HUBS,IAS,ELF,XM,ENTG,VRT,MNDY,GRBK,SHOP,LI,COCO,AMAT,GOOG"

# Add a text input field at the top of the app
input_symbols = st.text_input("Enter symbols (comma-separated):", default_symbols)

# Split the input string by comma and remove any leading/trailing spaces
symbols = [symbol.strip() for symbol in input_symbols.split(',')]


weekly_studies = [{"id": "MASimple@tv-basicstudies", "inputs": {"length": length}} for length in [10, 30]]
daily_studies = [{"id": "MASimple@tv-basicstudies", "inputs": {"length": length}} for length in [10, 20, 50, 200]]

# Calculate how many pages we have
pages = math.ceil(len(symbols) / 2.0)  # changed from 4.0 to 2.0

# Create a state variable for the current page
if 'page' not in st.session_state:
    st.session_state.page = 0

# Create a "Next" button in the sidebar
if st.sidebar.button('Next'):
    st.session_state.page = (st.session_state.page + 1) % pages

# Calculate start and end symbols for the current page
start_symbol = st.session_state.page * 2  # changed from * 4 to * Sorry, the previous response was cut-off. Here's the continuation:


# Calculate start and end symbols for the current page
start_symbol = st.session_state.page * 2  # changed from * 4 to * 2
end_symbol = start_symbol + 2  # changed from + 4 to + 2

# Define columns outside the loop
cols_weekly = st.columns(2)  # changed from 4 to 2
cols_daily = st.columns(2)  # changed from 4 to 2

# Create a row of daily and weekly charts for each symbol on the current page
for i in range(start_symbol, min(end_symbol, len(symbols))):
    symbol = symbols[i]

    with cols_weekly[i-start_symbol]:
        components.html(
            get_widget_header() + get_widget_body(symbol, "W", weekly_studies) + get_widget_footer(), 
            height=WIDGET_HEIGHT, 
            width=WIDGET_WIDTH,
        )

    with cols_daily[i-start_symbol]:
        components.html(
            get_widget_header() + get_widget_body(symbol, "D", daily_studies) + get_widget_footer(), 
            height=WIDGET_HEIGHT, 
            width=WIDGET_WIDTH,
        )
            
    # Insert a button after every 2 symbols
    if i == end_symbol - 1 and i != len(symbols) - 1:  # Add button if it is the last of the set and not the final symbol
        if st.button('Next', key=f'NextMain{i}'):
            st.session_state.page = (st.session_state.page + 1) % pages
            st.experimental_rerun()
