from re import findall
from core.utils import pageLimit
from core.requester import requester, ether_requester

def getTransactions(address, processed, database, limit, etherscan_api_key=None):
    addresses = []
    increment = 0
    database[address] = {}
    pages = pageLimit(limit)
    for i in range(pages):
        if pages > 1 and increment != 0:
            trail = '?offset=%i' % increment
       
        if address.startswith('0x'):
            # If the address starts with '0x', it's an Ethereum address, and we're using the Etherscan API
            # The Etherscan API returns a JSON object with a list of transactions
            response = ether_requester(address, etherscan_api_key)
            transactions = response.json()['result']
            for tx in transactions:
                # Extract the addresses from 'to' and 'from' fields in the transaction
                from_addr = tx['from']
                to_addr = tx['to']
                if from_addr not in database[address]:
                    database[address][from_addr] = 0
                if to_addr not in database[address]:
                    database[address][to_addr] = 0
                database[address][from_addr] += 1
                database[address][to_addr] += 1
                addresses.extend([from_addr, to_addr])
        else:
            response = requester(address)
            # Otherwise, it's a Bitcoin address, and we're using the blockchain.info API
            # The blockchain.info API returns data in plain text which we parse using regular expressions
            matches = findall(r'"addr":".*?"', response)
            for match in matches:
                found = match.split('"')[3]
                if found not in database[address]:
                    database[address][found] = 0
                database[address][found] += 1
                addresses.append(found)
        increment += 50
        processed.add(address)
    return addresses
