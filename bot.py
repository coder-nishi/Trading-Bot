#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot
Supports Market, Limit, and Stop-Limit orders
"""

import sys
import argparse
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from config import API_KEY, API_SECRET, TESTNET_BASE_URL, DEFAULT_LEVERAGE
from utils import Logger, InputValidator, Formatter

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """
        Initialize the trading bot
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Use testnet environment
        """
        self.logger = Logger('BasicBot')
        self.validator = InputValidator()
        self.formatter = Formatter()
        
        try:
            # Initialize Binance client
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet
            )
            
            # Override base URL for futures testnet
            self.client.FUTURES_URL = TESTNET_BASE_URL
            
            self.logger.logger.info(f"{Fore.GREEN}Trading Bot initialized successfully")
            
        except Exception as e:
            self.logger.log_error(e, "Bot initialization")
            raise
    
    def setup_symbol(self, symbol, leverage=DEFAULT_LEVERAGE, margin_type='ISOLATED'):
        """
        Setup trading symbol with leverage and margin type
        
        Args:
            symbol (str): Trading symbol (e.g., BTCUSDT)
            leverage (int): Leverage amount
            margin_type (str): Margin type (ISOLATED or CROSSED)
        """
        try:
            # Change leverage
            self.client.futures_change_leverage(
                symbol=symbol,
                leverage=leverage
            )
            
            # Change margin type
            self.client.futures_change_margin_type(
                symbol=symbol,
                marginType=margin_type
            )
            
            self.logger.logger.info(
                f"Symbol setup: {symbol} | Leverage: {leverage}x | Margin: {margin_type}"
            )
            
        except BinanceAPIException as e:
            # Ignore error if margin type is already set
            if "No need to change margin type" not in e.message:
                self.logger.log_error(e, f"Symbol setup for {symbol}")
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order
        
        Args:
            symbol (str): Trading symbol
            side (str): BUY or SELL
            quantity (float): Order quantity
            
        Returns:
            dict: Order response
        """
        try:
            # Validate inputs
            valid, msg = self.validator.validate_symbol(symbol)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_side(side)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_quantity(quantity)
            if not valid:
                return {"error": msg}
            
            # Setup symbol
            self.setup_symbol(symbol)
            
            # Log the order
            self.logger.log_order("MARKET", symbol, side, quantity)
            
            # Place market order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            
            self.logger.log_response(order)
            return order
            
        except BinanceAPIException as e:
            error_msg = f"API Error in market order: {e.message}"
            self.logger.log_error(error_msg, "market_order")
            return {"error": error_msg}
        except BinanceOrderException as e:
            error_msg = f"Order Error in market order: {e.message}"
            self.logger.log_error(error_msg, "market_order")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error in market order: {str(e)}"
            self.logger.log_error(error_msg, "market_order")
            return {"error": error_msg}
    
    def place_limit_order(self, symbol, side, quantity, price, time_in_force='GTC'):
        """
        Place a limit order
        
        Args:
            symbol (str): Trading symbol
            side (str): BUY or SELL
            quantity (float): Order quantity
            price (float): Order price
            time_in_force (str): Time in force (GTC, IOC, FOK)
            
        Returns:
            dict: Order response
        """
        try:
            # Validate inputs
            valid, msg = self.validator.validate_symbol(symbol)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_side(side)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_quantity(quantity)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_price(price)
            if not valid:
                return {"error": msg}
            
            # Setup symbol
            self.setup_symbol(symbol)
            
            # Log the order
            self.logger.log_order("LIMIT", symbol, side, quantity, price)
            
            # Place limit order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type=Client.ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price,
                timeInForce=time_in_force
            )
            
            self.logger.log_response(order)
            return order
            
        except BinanceAPIException as e:
            error_msg = f"API Error in limit order: {e.message}"
            self.logger.log_error(error_msg, "limit_order")
            return {"error": error_msg}
        except BinanceOrderException as e:
            error_msg = f"Order Error in limit order: {e.message}"
            self.logger.log_error(error_msg, "limit_order")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error in limit order: {str(e)}"
            self.logger.log_error(error_msg, "limit_order")
            return {"error": error_msg}
    
    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price, time_in_force='GTC'):
        """
        Place a stop-limit order
        
        Args:
            symbol (str): Trading symbol
            side (str): BUY or SELL
            quantity (float): Order quantity
            price (float): Order price
            stop_price (float): Stop price
            time_in_force (str): Time in force (GTC, IOC, FOK)
            
        Returns:
            dict: Order response
        """
        try:
            # Validate inputs
            valid, msg = self.validator.validate_symbol(symbol)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_side(side)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_quantity(quantity)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_price(price)
            if not valid:
                return {"error": msg}
            
            valid, msg = self.validator.validate_price(stop_price)
            if not valid:
                return {"error": msg}
            
            # Setup symbol
            self.setup_symbol(symbol)
            
            # Log the order
            self.logger.log_order("STOP-LIMIT", symbol, side, quantity, price)
            self.logger.logger.info(f"Stop Price: {stop_price}")
            
            # Determine stop limit side
            stop_side = 'BUY' if side.upper() == 'BUY' else 'SELL'
            
            # Place stop-limit order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=stop_side,
                type=Client.FUTURE_ORDER_TYPE_STOP,
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce=time_in_force
            )
            
            self.logger.log_response(order)
            return order
            
        except BinanceAPIException as e:
            error_msg = f"API Error in stop-limit order: {e.message}"
            self.logger.log_error(error_msg, "stop_limit_order")
            return {"error": error_msg}
        except BinanceOrderException as e:
            error_msg = f"Order Error in stop-limit order: {e.message}"
            self.logger.log_error(error_msg, "stop_limit_order")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error in stop-limit order: {str(e)}"
            self.logger.log_error(error_msg, "stop_limit_order")
            return {"error": error_msg}
    
    def get_account_info(self):
        """Get futures account information"""
        try:
            account_info = self.client.futures_account()
            return account_info
        except Exception as e:
            self.logger.log_error(e, "get_account_info")
            return {"error": str(e)}
    
    def get_open_orders(self, symbol=None):
        """Get open orders"""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol)
            else:
                orders = self.client.futures_get_open_orders()
            return orders
        except Exception as e:
            self.logger.log_error(e, "get_open_orders")
            return {"error": str(e)}
    
    def cancel_order(self, symbol, order_id):
        """Cancel an open order"""
        try:
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            self.logger.logger.info(f"Order {order_id} cancelled successfully")
            return result
        except Exception as e:
            self.logger.log_error(e, "cancel_order")
            return {"error": str(e)}

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Binance Futures Testnet Trading Bot')
    
    # Required arguments
    parser.add_argument('--api-key', required=True, help='Binance API Key')
    parser.add_argument('--api-secret', required=True, help='Binance API Secret')
    
    # Order arguments
    parser.add_argument('--symbol', required=True, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--quantity', required=True, type=float, help='Order quantity')
    
    # Order type arguments
    parser.add_argument('--order-type', required=True, 
                       choices=['MARKET', 'LIMIT', 'STOP_LIMIT'], 
                       help='Order type')
    
    # Optional arguments
    parser.add_argument('--price', type=float, help='Order price (for LIMIT and STOP_LIMIT)')
    parser.add_argument('--stop-price', type=float, help='Stop price (for STOP_LIMIT)')
    parser.add_argument('--leverage', type=int, default=10, help='Leverage (default: 10)')
    
    args = parser.parse_args()
    
    # Initialize bot
    try:
        bot = BasicBot(args.api_key, args.api_secret, testnet=True)
    except Exception as e:
        print(f"Failed to initialize bot: {e}")
        sys.exit(1)
    
    # Execute order based on type
    if args.order_type == 'MARKET':
        result = bot.place_market_order(args.symbol, args.side, args.quantity)
    
    elif args.order_type == 'LIMIT':
        if not args.price:
            print("Error: --price is required for LIMIT orders")
            sys.exit(1)
        result = bot.place_limit_order(args.symbol, args.side, args.quantity, args.price)
    
    elif args.order_type == 'STOP_LIMIT':
        if not args.price or not args.stop_price:
            print("Error: --price and --stop-price are required for STOP_LIMIT orders")
            sys.exit(1)
        result = bot.place_stop_limit_order(
            args.symbol, args.side, args.quantity, args.price, args.stop_price
        )
    
    # Display result
    if 'error' in result:
        print(Formatter.format_error(result['error']))
        sys.exit(1)
    else:
        print(Formatter.format_order_response(result))

if __name__ == "__main__":
    main()
