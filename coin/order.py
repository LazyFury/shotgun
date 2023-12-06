from time import sleep
from web3 import Web3

web3 = Web3(
    # Web3.HTTPProvider("https://mainnet.infura.io/v3/ebb5d64c93c34767845272fdaf4b21ab")
    Web3.HTTPProvider("https://bsc-dataseed.binance.org/")
    # Web3.HTTPProvider("https://api.trongrid.io")
    # tron 
    # Web3.HTTPProvider("https://api.trongrid.io")
)
hash_code = "b257aedf5e38bf4da96290ac6fad346721a20133002d2ca66d41bf96c58fde08"
while True:
    print("Waiting for transaction...")
    try:
        result = web3.eth.get_transaction_receipt(hash_code)  # type: ignore
        print(result)
        confirm_number = web3.eth.block_number - result.blockNumber  # type: ignore
        print("Confirm number: ", confirm_number)
        transaction = web3.eth.get_transaction(hash_code)  # type: ignore
        print(transaction)
    except Exception as e:
        print(e)
    sleep(5)


