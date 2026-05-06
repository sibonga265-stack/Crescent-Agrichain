# pip install streamlit web3 streamlit-js-eval

# ==========================================
# config.py
# ==========================================
"""
This file contains all the configuration settings for the Crescent AgriChain App.
"""

# --- APPLICATION DISPLAY SETTINGS ---
APP_NAME = "Crescent AgriChain"
APP_TAGLINE = "Empowering Direct Agricultural Trade"
APP_DESCRIPTION = "A blockchain-powered marketplace connecting farmers and retailers with secure escrow, transparent logistics, and automated payments."
LOGO_PATH = "logo.png"

# --- BLOCKCHAIN CONNECTION SETTINGS ---
SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CONTRACT_ADDRESS = "0x6BE7Fc5b030367396e6A9eb7a06C23eDC7654Ee7"

# --- HUMAN READABLE CONSTANTS ---
ORDER_STATUS_LABELS = {
    0: "Listed for Sale",
    1: "Order Placed (In Escrow)",
    2: "In Transit",
    3: "Delivered",
    4: "Completed (Payment Released)",
    5: "Disputed"
}

# --- SMART CONTRACT ABI ---
CONTRACT_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"}
        ],
        "name": "DeliveryConfirmed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"}
        ],
        "name": "DisputeRaised",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"}
        ],
        "name": "InTransit",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": False, "internalType": "address", "name": "retailer", "type": "address"}
        ],
        "name": "OrderPlaced",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "PaymentReleased",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": False, "internalType": "address", "name": "farmer", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "itemType", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "price", "type": "uint256"}
        ],
        "name": "ProduceListed",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "admin",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "confirmDelivery",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_itemType", "type": "string"},
            {"internalType": "uint256", "name": "_quantity", "type": "uint256"},
            {"internalType": "uint256", "name": "_price", "type": "uint256"},
            {"internalType": "uint256", "name": "_deliveryDate", "type": "uint256"}
        ],
        "name": "listProduce",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_id", "type": "uint256"},
            {"internalType": "string", "name": "_itemType", "type": "string"},
            {"internalType": "uint256", "name": "_quantity", "type": "uint256"},
            {"internalType": "uint256", "name": "_price", "type": "uint256"},
            {"internalType": "uint256", "name": "_deliveryDate", "type": "uint256"}
        ],
        "name": "updateProduce",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "listings",
        "outputs": [
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "address payable", "name": "farmer", "type": "address"},
            {"internalType": "address", "name": "retailer", "type": "address"},
            {"internalType": "string", "name": "itemType", "type": "string"},
            {"internalType": "uint256", "name": "quantity", "type": "uint256"},
            {"internalType": "uint256", "name": "price", "type": "uint256"},
            {"internalType": "uint256", "name": "deliveryDate", "type": "uint256"},
            {"internalType": "enum CrescentAgriChain.State", "name": "status", "type": "uint8"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "placeOrder",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "produceCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "raiseDispute",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_id", "type": "uint256"},
            {"internalType": "bool", "name": "refundRetailer", "type": "bool"}
        ],
        "name": "resolveDispute",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "startTransport",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]