from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json
import requests

app = Flask(__name__)

# Connect to your Ethereum network (e.g., local Ganache)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.defaultAccount = w3.eth.accounts[0]

# Load contract ABI and address
with open('../build/contracts/MusicNFT.json') as f:
    contract_data = json.load(f)

contract_address = contract_data['networks']['5777']['address']
contract_abi = contract_data['abi']
music_nft = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/mint', methods=['POST'])
def mint_nft():
    token_uri = request.form.get('tokenURI')
    if not token_uri:
        return jsonify({'error': 'tokenURI is required'}), 400

    try:
        tx_hash = music_nft.functions.mint(token_uri).transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        return jsonify({'status': 'success', 'transactionHash': tx_hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/token/<int:token_id>', methods=['GET'])
def get_token_details(token_id):
    try:
        token_uri = music_nft.functions.tokenURI(token_id).call()
        return jsonify({'tokenId': token_id})
    except Exception as e:
        return jsonify({'error': 'Token does not exist or an error occurred'}), 404

@app.route('/withdraw', methods=['POST'])
def withdraw():
    try:
        tx_hash = music_nft.functions.withdraw().transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        return jsonify({'status': 'success', 'transactionHash': tx_hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoints for rendering HTML files
@app.route('/', methods=['GET'])
def add_token_uri_page():
    return render_template('tokenuri.html', response=None)

@app.route('/tokenidpage', methods=['GET'])
def add_token_id_page():
    return render_template('tokenid.html', response=None)

@app.route('/withdrawpage', methods=['GET'])
def add_withdraw_page():
    return render_template('withdraw.html', response=None)

# API endpoints for form actions
@app.route('/addtokenuriform', methods=['GET','POST'])
def add_token_uri_form():
    token_uri = request.form.get('tokenURI')
    if not token_uri:
        return render_template('tokenuri.html', response='tokenURI is required')

    try:
        response = requests.post('http://127.0.0.1:4000/mint', data={'tokenURI': token_uri})
        response_data = response.json()
        if response.status_code == 200:
            return render_template('tokenuri.html', response=f"Minted successfully! Transaction Hash: {response_data['transactionHash']}")
        else:
            return render_template('tokenuri.html', response=response_data['error'])
    except Exception as e:
        return render_template('tokenuri.html', response=str(e))
@app.route('/addtokenidform', methods=['GET','POST'])
def add_token_id_form():
    token_id = request.form.get('tokenId')
    if not token_id:
        return render_template('tokenid.html', response='Token ID is required')

    try:
        response = requests.get(f'http://127.0.0.1:4000/token/{token_id}')
        print(response.json())  # Log the response for debugging
        return render_template('tokenid.html', response=response.json())
    except Exception as e:
        print(f"Error retrieving token details: {str(e)}")
        return render_template('tokenid.html', response='An error occurred while retrieving token details.')

@app.route('/addwithdrawform', methods=['GET','POST'])
def add_withdraw_form():
    try:
        response = requests.post('http://127.0.0.1:4000/withdraw')
        response_data = response.json()
        if response.status_code == 200:
            return render_template('withdraw.html', response=f"Withdraw successful! Transaction Hash: {response_data['transactionHash']}")
        else:
            return render_template('withdraw.html', response=response_data['error'])
    except Exception as e:
        return render_template('withdraw.html', response=str(e))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=4000,
        debug=True
    )
