
import sys
import time
import os
%matplotlib inline
import matplotlib.pyplot as plt
from toy_exchange_client import ExchangeClient, BID_SIDE, ASK_SIDE, Order
from IPython.display import clear_output

BUY=BID_SIDE
SELL=ASK_SIDE

# Addresses for the test and real exchange
TEST_EXCHANGE="http://api.test-toy-exchange.svc.cluster.local:5000"
REAL_EXCHANGE="http://api.toy-exchange.svc.cluster.local:5000"

BADGE="unimelb_12" # TODO: this is the username we have given to you
SECRET="loving-pig-95" # TODO: Change this to the password we have given to you
# EXCHANGE = TEST_EXCHANGE # TODO: Change me to REAL_EXCHANGE when you're ready
EXCHANGE = REAL_EXCHANGE

client = ExchangeClient(
        badge=BADGE,
        secret=SECRET,
        exchange_url=EXCHANGE
        )

# Below code are used to plot a graph of current price for a product
# Modify it to suit your need
last_tops = []
def plot_market_state(top_result):
    global last_tops
    
    last_tops.append(top_result)
    last_tops = last_tops[-10:]
    
    reversed_indexes = range(len(last_tops), 0, -1)
    timescale = list(map(lambda x: f't-{x}', reversed_indexes))
    
    ask, = plt.plot(timescale,list(map(lambda top: top['ask'] , last_tops)), label='ASK')
    bid, = plt.plot(timescale,list(map(lambda top: top['bid'] , last_tops)), label='BID')
    last_trade, = plt.plot(timescale,list(map(lambda top: top['last_trade'] , last_tops)), label='Last Trade')
    
    plt.legend(handles=[ask, bid, last_trade])
    plt.show()
    
# These flags control what the output is during each iteration
print_feed = True
print_positions = True
plot_feed = False # Turn this on for graph plotting


def check_pos(client):
    sauce, dough = -client.positions()['PIZZA'], -client.positions()['PIZZA']
    sauce -= client.positions()['CALZONE']
    dough -= 2*client.positions()['CALZONE']
    
    print(f"Net sauce {sauce+client.positions()['SAUCE']}\nNet dough {dough+client.posisionts()['DOUGH']}")



def trade_loop():
    clear_output(wait=True) # This clears the output so we don't spam the log
    sauce_top = client.top("SAUCE")
    pizza_top = client.top("PIZZA")
    dough_top = client.top("DOUGH")
    calzo_top = client.top("CALZONE")
    
    if sauce_top["ask"] and dough_top["ask"] and pizza_top["bid"]:
        if sauce_top["ask"] + dough_top["ask"] < pizza_top["bid"]:
            quantity = min(sauce_top["ask_qty"], dough_top["ask_qty"], pizza_top["bid_qty"]) // 2
            if quantity:
                client.hit("SAUCE", BUY, sauce_top["ask"], quantity)
                client.hit("DOUGH", BUY, dough_top["ask"], quantity)
                client.hit("PIZZA", SELL, pizza_top["bid"], quantity)
    
    elif sauce_top["bid"] and dough_top["bid"] and pizza_top["ask"]:
        if sauce_top["bid"] + dough_top["bid"] > pizza_top["ask"]:
            quantity = min(sauce_top["bid_qty"], dough_top["bid_qty"], pizza_top["ask_qty"]) // 2
            if quantity:
                client.hit("SAUCE", SELL, sauce_top["bid"], quantity)
                client.hit("DOUGH", SELL, dough_top["bid"], quantity)
                client.hit("PIZZA", BUY, pizza_top["ask"], quantity) 
    
    if sauce_top["ask"] and dough_top["ask"] and calzo_top["bid"]:
        if sauce_top["ask"] + 2 * dough_top["ask"] < calzo_top["bid"]:
            quantity = min(sauce_top["ask_qty"], dough_top["ask_qty"], calzo_top["bid_qty"]) // 4
            if quantity:
                client.hit("SAUCE", BUY, sauce_top["ask"], quantity)
                client.hit("DOUGH", BUY, dough_top["ask"], 2 * quantity)
                client.hit("CALZONE", SELL, calzo_top["bid"], quantity)
    
    elif sauce_top["bid"] and dough_top["bid"] and calzo_top["ask"]:
        if sauce_top["bid"] + 2 * dough_top["bid"] > calzo_top["ask"]:
            quantity = min(sauce_top["bid_qty"], dough_top["bid_qty"], calzo_top["ask_qty"]) // 4
            if quantity:
                client.hit("SAUCE", SELL, sauce_top["bid"], quantity)
                client.hit("DOUGH", SELL, dough_top["bid"], 2 * quantity)
                client.hit("CALZONE", BUY, calzo_top["ask"], quantity)   
    
    if print_feed:
        print("Top Bid/Offer for SAUCE:")
        print(sauce_top)
        print(pizza_top)
        print(dough_top)
        print(calzo_top)

    
    if print_positions:
        print("Positions:")
        print(client.positions())
        # check_pos(client)
    
    if plot_feed:
        plot_market_state(sauce_top)
        
client.run(trade_loop)







