import os
from dotenv import load_dotenv

load_dotenv()

# Binance Testnet Configuration
TESTNET_BASE_URL = "https://testnet.binancefuture.com"
TESTNET_WEBSOCKET_URL = "wss://stream.binancefuture.com/ws"

# API Credentials (should be set in .env file)
API_KEY = os.getenv('BINANCE_TESTNET_API_KEY')
API_SECRET = os.getenv('BINANCE_TESTNET_API_SECRET')

# Trading Configuration
DEFAULT_LEVERAGE = 10
DEFAULT_MARGIN_TYPE = 'ISOLATED'

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
