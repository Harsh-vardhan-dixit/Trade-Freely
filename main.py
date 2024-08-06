import streamlit as st
from dhanhq import dhanhq
from dotenv import load_dotenv
import os
import schedule
import time
import threading

# Load environment variables
load_dotenv()

access_token = os.getenv('access-token')
client_id = os.getenv('client-id')

dhan = dhanhq(client_id, access_token)

# Define the buy and sell functions
def buy(securityId, quantity):
    dhan.place_order(
        transaction_type=dhan.BUY,
        exchange_segment=dhan.NSE,
        product_type=dhan.INTRA,
        order_type=dhan.MARKET,
        validity='DAY',
        security_id=securityId,
        quantity=quantity,
        disclosed_quantity=0,
        price=0,
        trigger_price=0,
        after_market_order=False,
        amo_time='OPEN',
        bo_profit_value=0,
        bo_stop_loss_Value=0,
        drv_expiry_date=None,
        drv_options_type=None,
        drv_strike_price=None    
    )

def sell(securityId, quantity):
    dhan.place_order(
        transaction_type=dhan.SELL,
        exchange_segment=dhan.NSE,
        product_type=dhan.INTRA,
        order_type=dhan.MARKET,
        validity='DAY',
        security_id=securityId,
        quantity=quantity,
        disclosed_quantity=0,
        price=0,
        trigger_price=0,
        after_market_order=False,
        amo_time='OPEN',
        bo_profit_value=0,
        bo_stop_loss_Value=0,
        drv_expiry_date=None,
        drv_options_type=None,
        drv_strike_price=None    
    )

# Function to schedule the buy and sell actions
def schedule_actions(buy_time, sell_time, securityId, quantity):
    schedule.clear()
    schedule.every().day.at(buy_time).do(buy, securityId, quantity)
    schedule.every().day.at(sell_time).do(sell, securityId, quantity)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Function to clear the schedule
def clear_schedule():
    schedule.clear()

# Streamlit app
st.title("Automatic Stock Buy and Sell")

# Input fields
stocks = {'AAPL': '12345', 'GOOGL': '23456', 'MSFT': '34567'}  # Example stock list
selected_stock = st.selectbox('Select Stock', options=list(stocks.keys()))
quantity = st.number_input('Select Quantity', min_value=1, step=1)
buy_time = st.text_input('Enter Buy Time (HH:MM format)')
sell_time = st.text_input('Enter Sell Time (HH:MM format)')

# Schedule button
if st.button('Schedule Buy and Sell'):
    securityId = stocks[selected_stock]
    try:
        # Validate time format
        time.strptime(buy_time, '%H:%M')
        time.strptime(sell_time, '%H:%M')

        # Start the scheduling in a separate thread
        threading.Thread(target=schedule_actions, args=(buy_time, sell_time, securityId, quantity)).start()
        
        st.success('Buy and Sell actions have been scheduled!')
    except ValueError:
        st.error('Invalid time format. Please enter time in HH:MM format.')

# Cancel button
if st.button('Cancel Schedule'):
    clear_schedule()
    st.success('All scheduled actions have been cancelled.')

# Running the Streamlit app
# No need to include st.run() since Streamlit is run from the command line
