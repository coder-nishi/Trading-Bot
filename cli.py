#!/usr/bin/env python3
"""
Enhanced CLI interface for the trading bot
"""

import cmd
import sys
from getpass import getpass
from bot import BasicBot
from utils import Formatter, Logger

class TradingBotCLI(cmd.Cmd):
    intro = """
╔══════════════════════════════════════════════╗
║          BINANCE FUTURES TRADING BOT         ║
║                 (TESTNET)                    ║
╚══════════════════════════════════════════════╝

Type 'help' or '?' for available commands.
Type 'exit' to quit.
"""
    prompt = '\n(bot) '
    
    def __init__(self):
        super().__init__()
        self.bot = None
        self.logger = Logger('CLI')
        self.authenticated = False
    
    def preloop(self):
        """Setup before command loop starts"""
        self.do_login(None)
    
    def do_login(self, arg):
        """Login to Binance Testnet: login"""
        if self.authenticated and self.bot:
            print("Already authenticated. Use 'logout' first to change credentials.")
            return
        
        try:
            print("\n=== Binance Testnet Authentication ===")
            api_key = input("API Key: ").strip()
            api_secret = getpass("API Secret: ").strip()
            
            if not api_key or not api_secret:
                print("Error: API Key and Secret are required")
                return
            
            self.bot = BasicBot(api_key, api_secret, testnet=True)
            self.authenticated = True
            print(f"\n{Formatter.format_order_response({'status': 'AUTHENTICATED'})}")
            
        except Exception as e:
            print(f"Authentication failed: {e}")
            self.authenticated = False
    
    def do_logout(self, arg):
        """Logout and clear credentials: logout"""
        self.bot = None
        self.authenticated = False
        print("Logged out successfully")
    
    def do_market(self, arg):
        """Place market order: market SYMBOL SIDE QUANTITY
        Example: market BTCUSDT BUY 0.001"""
        if not self._check_auth():
            return
        
        try:
            args = arg.split()
            if len(args) != 3:
                print("Usage: market SYMBOL SIDE QUANTITY")
                return
            
            symbol, side, quantity = args
            result = self.bot.place_market_order(symbol, side, float(quantity))
            self._handle_order_result(result)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_limit(self, arg):
        """Place limit order: limit SYMBOL SIDE QUANTITY PRICE
        Example: limit BTCUSDT BUY 0.001 50000"""
        if not self._check_auth():
            return
        
        try:
            args = arg.split()
            if len(args) != 4:
                print("Usage: limit SYMBOL SIDE QUANTITY PRICE")
                return
            
            symbol, side, quantity, price = args
            result = self.bot.place_limit_order(symbol, side, float(quantity), float(price))
            self._handle_order_result(result)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_stop_limit(self, arg):
        """Place stop-limit order: stop_limit SYMBOL SIDE QUANTITY PRICE STOP_PRICE
        Example: stop_limit BTCUSDT SELL 0.001 49000 49500"""
        if not self._check_auth():
            return
        
        try:
            args = arg.split()
            if len(args) != 5:
                print("Usage: stop_limit SYMBOL SIDE QUANTITY PRICE STOP_PRICE")
                return
            
            symbol, side, quantity, price, stop_price = args
            result = self.bot.place_stop_limit_order(
                symbol, side, float(quantity), float(price), float(stop_price)
            )
            self._handle_order_result(result)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_orders(self, arg):
        """View open orders: orders [SYMBOL]"""
        if not self._check_auth():
            return
        
        try:
            symbol = arg.strip() if arg else None
            orders = self.bot.get_open_orders(symbol)
            
            if 'error' in orders:
                print(Formatter.format_error(orders['error']))
            elif not orders:
                print("No open orders")
            else:
                print(f"\n=== Open Orders ({len(orders)}) ===")
                for order in orders:
                    print(f"ID: {order['orderId']} | {order['symbol']} | "
                          f"{order['side']} {order['type']} | "
                          f"Qty: {order['origQty']} | Price: {order['price']} | "
                          f"Status: {order['status']}")
                        
        except Exception as e:
            print(f"Error: {e}")
    
    def do_account(self, arg):
        """View account information: account"""
        if not self._check_auth():
            return
        
        try:
            account = self.bot.get_account_info()
            
            if 'error' in account:
                print(Formatter.format_error(account['error']))
            else:
                print(f"\n=== Account Information ===")
                print(f"Total Wallet Balance: {account['totalWalletBalance']}")
                print(f"Available Balance: {account['availableBalance']}")
                print(f"Total Unrealized P&L: {account['totalUnrealizedProfit']}")
                print(f"Total Margin Balance: {account['totalMarginBalance']}")
                
                # Display positions
                positions = [p for p in account['positions'] if float(p['positionAmt']) != 0]
                if positions:
                    print(f"\n=== Open Positions ({len(positions)}) ===")
                    for pos in positions:
                        if float(pos['positionAmt']) != 0:
                            print(f"{pos['symbol']} | Size: {pos['positionAmt']} | "
                                  f"Entry: {pos['entryPrice']} | P&L: {pos['unRealizedProfit']}")
                        
        except Exception as e:
            print(f"Error: {e}")
    
    def do_cancel(self, arg):
        """Cancel an order: cancel SYMBOL ORDER_ID"""
        if not self._check_auth():
            return
        
        try:
            args = arg.split()
            if len(args) != 2:
                print("Usage: cancel SYMBOL ORDER_ID")
                return
            
            symbol, order_id = args
            result = self.bot.cancel_order(symbol, int(order_id))
            
            if 'error' in result:
                print(Formatter.format_error(result['error']))
            else:
                print("Order cancelled successfully")
                        
        except Exception as e:
            print(f"Error: {e}")
    
    def do_exit(self, arg):
        """Exit the trading bot: exit"""
        print("Thank you for using the Trading Bot. Goodbye!")
        return True
    
    def _check_auth(self):
        """Check if user is authenticated"""
        if not self.authenticated or not self.bot:
            print("Please login first using 'login' command")
            return False
        return True
    
    def _handle_order_result(self, result):
        """Handle order result display"""
        if 'error' in result:
            print(Formatter.format_error(result['error']))
        else:
            print(Formatter.format_order_response(result))

if __name__ == "__main__":
    TradingBotCLI().cmdloop()
