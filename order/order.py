from time import sleep
from web3 import Web3

web3 = Web3(
    # Web3.HTTPProvider("https://mainnet.infura.io/v3/ebb5d64c93c34767845272fdaf4b21ab")
    Web3.HTTPProvider("https://bsc-dataseed.binance.org/")
)
hash_code = "0xdf99af2cf4e4f2c5e185755bab36d68ad4afd78821de1e8ac6e7a73034966782"
while True:
    print("Waiting for transaction...")
    result = web3.eth.get_transaction_receipt(hash_code) # type: ignore
    print(result)
    confirm_number = web3.eth.block_number - result.blockNumber # type: ignore
    print("Confirm number: ", confirm_number)
    transaction = web3.eth.get_transaction(hash_code) # type: ignore
    print(transaction)
    sleep(5)


