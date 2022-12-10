# stdlib imports
import json
import os

#third party imports
from solcx import compile_standard, install_solc
from web3 import Web3
from web3.exceptions import ContractLogicError
from dotenv import load_dotenv

# loading environment variables
load_dotenv()



# getting the solidity file
with open("./personal_info.sol", "r") as file:
    solidity_file = file.read()

# compiling solidity file
compiled_solidity_file = compile_standard(
    {
        "language" : "Solidity",
        "sources": {"personal_info.sol": {"content": solidity_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        }
    },
    solc_version='0.8.7'
)

with open("compiled_sol.json", "w") as file:
    json.dump(compiled_solidity_file, file)


                                              ## DEPLOYMENT ####

# get bytecode
bytecode = compiled_solidity_file["contracts"]["personal_info.sol"]["PersonalInfo"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_solidity_file["contracts"]["personal_info.sol"]["PersonalInfo"]["metadata"]
)["output"]["abi"]


print("Conecting To TestNet")
# connecting to A Sepolia Testnet Using Infura
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/cc4561cfb15540ebb15da6802357e6f2'))
chain_id = 11155111
address = os.getenv('ADDRESS')
private_key = os.getenv('PRIVATE_KEY')
nonce = w3.eth.get_transaction_count(address)
print("Connected To TestNet")

# create the contract
personal_info_contract = w3.eth.contract(abi=abi, bytecode=bytecode)

#making a transaction
transaction = personal_info_contract.constructor().buildTransaction(
    {
        "chainId" : chain_id,
        "gasPrice" : w3.eth.gas_price,
        "from" : address,
        "nonce" : nonce
    }
)

# signing the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying Contract")
# sending the transaction an getting the trasaction hash
hashed_signed_transaction= w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# verifying that the transaction went through(waiting for it to be mined and added to the blockchain and then get the trnsaction receipt) <-- BEST PRACTICE
transaction_receipt = w3.eth.wait_for_transaction_receipt(hashed_signed_transaction)
print("Contract Deployed")


#                                     ### Contract Interaction ###
contract = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)





#                                     # Functions
def get_person(name, contract):
    try:
        #calling the contrcat function that returns a person's info
        get_person_info = contract.functions.get_person_info(name).call()
    except ContractLogicError as err:
        print(err)

def create_person(contract, name, phone_number, residence): 
    nonce = w3.eth.get_transaction_count(address)
    try:
        # making a transaction with the contract's create_person function.
        transaction= contract.functions.create_person(name, phone_number, residence).buildTransaction(
            {
                "chainId" : chain_id,
                "gasPrice" : w3.eth.gas_price,
                "from" : address,
                "nonce" : nonce
            }
        )
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        hashed_transaction = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(hashed_transaction)
        print("Created Person Successfully")
        print("Getting Person Now, Please Wait....")
        get_person(name, contract)
    except ContractLogicError as err:
        print(err)


def delete_person(contract, name):
    nonce = w3.eth.get_transaction_count(address)
    try:
        transaction = contract.functions.delete_person(name).buildTransaction(
            {
                "chainId" : chain_id,
                "gasPrice" : w3.eth.gas_price,
                "from" : address,
                "nonce" : nonce
            }
        )
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        hashed_transaction = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(hashed_transaction)
        print("Deleted Successfully!")
        print("Trying to Get User now.")
        get_person(name, contract)
    except ContractLogicError as err:
        print(err)





# create_person(contract, "Efosa", 2349020705214, "Lagos, Nigeria")
# get_person('Efosa', contract)
# delete_person(contract, "Efosa")