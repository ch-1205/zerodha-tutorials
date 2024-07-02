from kiteconnect import KiteConnect
import credentials as cred
import time
import datetime


def calculate_pnl():
    while True:
        try:
            positions = kite.positions()
            break
        except Exception as e:
            print(f"error fetching positions: {e}")
            time.sleep(1)
            continue
    if not positions:
        print('No positions yet, checking in 1 second')
        time.sleep(1)
        return 0

    pnl = 0

    for position in positions['net']:
        if position['product'] == 'NRML':
            qty = position['quantity']
            sell_value = position['sell_value']
            buy_value = position['buy_value']
            multiplier = position['multiplier']

            ltp_data = kite.ltp(f'NFO:{position["tradingsymbol"]}')
            ltp = ltp_data['NFO:' + position["tradingsymbol"]]['last_price']

            pnl += (sell_value - buy_value) + (qty * ltp * multiplier)

    return pnl


def main():
    while True:
        current_time = datetime.datetime.now()
        current_pnl = calculate_pnl()
        print(
            f"TimeL {current_time.strftime('%Y-%m-%d %H:%M:%S')} | P&L: {current_pnl}")
        time.sleep(0.5)


if __name__ == "__main__":
    global kite
    access_token = open('access_token.txt', 'r').read()
    kite = KiteConnect(api_key=cred.API_KEY)
    kite.set_access_token(access_token)
    main()
