import requests
import re

def requester(url):
    transcation_hash_pattern = re.compile('^[a-fA-F0-9]{64}$')

    if transcation_hash_pattern.match(url):
	    return requests.get('https://blockchain.info/rawtx/' + url).text
    else:
        return requests.get("https://blockchain.info/rawaddr/" + url).text
         

def ether_requester(address, etherscan_api_key = 'HWEFSWY2MIXCIDX3XSJPDGBI22Q9RIQXNA'):
    # Using regex pattern to distinguish address pattern 
    wallet_address_pattern = re.compile('^0x[a-fA-F0-9]{40}$')
    transaction_hash_pattern = re.compile('^0x[a-fA-F0-9]{64}$')
    
    if wallet_address_pattern.match(address):
        params = {
             'module': 'account',
             'action': 'txlist',
             'address': address,
             'start_block': 0,
             'end_block': 99999999,
             'page': 1,
             'offset': 50,
             'sort': 'desc',
             'apikey': etherscan_api_key
        }
    elif transaction_hash_pattern.match(address):
        params = {
            'module': 'proxy',
            'action': 'eth_getTransactionByHash',
            'txhash': address,
            'apikey': etherscan_api_key
        }
    return requests.get("https://api.etherscan.io/api", params=params)