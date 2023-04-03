# SimpleTradingCode

# Some Notes
## Exchange GUI
- The real exchange is at https://exchange.imctradingcompetition.com/
- The test exchange is at https://test-exchange.imctradingcompetition.com/

## Optional features
Sections marked as optional below are features supported by the exchange but not necessarily needed for writing a working arbitrager script. However, you are more than welcome to try it!



## Rules
- The aim of this challenge is to write an automated algorithm to trade
- Once the competition is completed, we will inspect the code to ensure that you've acted in good faith. We reserve the right to disqualify if we determine this is not the case.
- We do not impose a hard limit on position, but try to keep it flat.
- You are allowed to manually place orders via the web gui if you wish.



## Conversions
- 1 Pizza = 1 Sauce + 1 Dough
- 1 Calzone = 1 Sauce + 2 Dough



## Setting up
We first need an ExchangeClient to send orders and read market data. Please note that by default it is set to connect to the test exchange.

from toy_exchange_client import ExchangeClient, BID_SIDE, ASK_SIDE, Order
import os

TEST_EXCHANGE="http://api.test-toy-exchange.svc.cluster.local:5000"
REAL_EXCHANGE="http://api.toy-exchange.svc.cluster.local:5000"

badge="TODO" # TODO: Change this to be the username we have given to you
secret="TODO" # TODO: Change this to be the password we have given to you

exchange_url=TEST_EXCHANGE

client = ExchangeClient(badge=badge, secret=secret, exchange_url=exchange_url)



## Query the market
To see the current market state, we call `client.top` for "SAUCE".
%pdef client.top

client.top("SAUCE")

As you can see from the output above, `ask` is the current best price someone is willing to sell and `bid` is the current best price someone is willing to buy in the market. `ask_qty` and `bid_qty` indicate their respective quantity.



## Sending Orders
Now that we've set up our client, let's get into making some orders!
### Hit - Immediate or Cancel Orders (IOC)

IOC orders are orders that will either be filled (either partially or fully), and if not, cancelled. The remaining units that cannot be immediately filled will not remain on the market. This is commonly known as "hitting".

%pdef client.hit
# Send an IOC order to Sell 1 sauce at price 500
client.hit(symbol="SAUCE", side=ASK_SIDE, price=500, qty=1)



### Quote - Good For Day Orders (GFD) (Optional)
GFD orders are orders that will remain on the market until they are fully filled. This is commonly known as 'quoting', and we can make quotes with our `ExchangeClient` instance `client` that we defined above.

%pdef client.quote
# Send a GFD order to Buy 1 sauce at price 5
gfd_order = client.quote(symbol="SAUCE", side=BID_SIDE, price=100, qty=1)
gfd_order

Note here in the return value of both `client.quote` and `client.hit`, there is a `trades` list that tells you whether you've made a trade when you send the order.



## Cancel an Order (Optional)

When we make an order, we get an `order_id`. We can use this `order_id` to cancel any orders we may think are no longer attractive to keep on the market. Note that we can only cancel GFD orders, as IOC orders will be automatically cancelled if they aren't fully filled.

%pdef client.cancel
gfd_order_id = gfd_order['order']['id']
client.cancel("SAUCE", gfd_order_id)



### Mass Cancel (Optional)

If the market has shifted too quickly for us, we can cancel all the quotes (or GFD) we have on the market. We can cancel for just one symbol, or every symbol.

%pdef client.mass_cancel
client.mass_cancel()



## View your positions

To view our current outstanding positions, we call `client.positions()`. Note this will show all your positions for all tradeable instruments, `SAUCE`, `DOUGH`, `PIZZA` and `CALZONE`. 

client.positions()



## View the trades you have made

We can also view all the trades we've made historically on this particular run of the competition

client.trades()



### Mass Quote (Optional)

Similiar to a mass cancel, we can also mass quote. We define a list of all the GFD orders we want to send as a list and call `client.mass_quote()`

%pdef client.mass_quote
client.mass_quote( 
    [
        Order(symbol='SAUCE', price=500, side=BID_SIDE, qty=100), # GFD order to buy 100 Sauce at 500
        Order(symbol='DOUGH', price=500, side=BID_SIDE, qty=100), # GFD order to buy 100 Dough at 500
        Order(symbol='PIZZA', price=1100, side=ASK_SIDE, qty=100), # GFD order to sell 1100 Pizza at 1100
    ]
)


Result
https://exchange.imctradingcompetition.com/j?subpage=net_positions_total

<img width="646" alt="Screenshot 2023-04-03 at 14 21 00" src="https://user-images.githubusercontent.com/127374462/229410783-39d096a8-adbb-46fc-914d-0e72ddf04226.png">


