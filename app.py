import streamlit as st
import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'previous_hash': previous_hash
        }
        block['hash'] = self.hash(block)
        self.transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, battery_id, location, status):
        self.transactions.append({
            'battery_id': battery_id,
            'location': location,
            'status': status
        })

    @property
    def last_block(self):
        return self.chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_valid(self):
        for i in range(1, len(self.chain)):
            if self.chain[i]['previous_hash'] != self.chain[i-1]['hash']:
                return False
        return True

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

bc = st.session_state.blockchain

st.title("EV Battery Blockchain - Textile Industry")

battery_id = st.text_input("Battery ID")
location = st.text_input("Location")
status = st.selectbox("Status", ["Manufactured", "In Use", "Recycled"])

if st.button("Add Transaction"):
    bc.add_transaction(battery_id, location, status)
    st.success("Transaction Added!")

if st.button("Mine Block"):
    block = bc.create_block(bc.last_block['hash'])
    st.success(f"Block {block['index']} Mined!")

if st.button("View Blockchain"):
    st.json(bc.chain)

if st.button("Check Validity"):
    if bc.is_valid():
        st.success("Blockchain is Valid")
    else:
        st.error("Blockchain is NOT Valid")
