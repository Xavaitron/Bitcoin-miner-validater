#importing the libs
import json
import os
import time
import hashlib

#double hash function
def HASH256(str_hex):
    binary = bytes.fromhex(str_hex)  # convert to binary from hex
    hash1 = hashlib.sha256(binary).digest()  # hash and convert to binary
    hash2 = hashlib.sha256(hash1).hexdigest()  # hash and convert to hex string
    return hash2

def merkleroot(txids_list):
    if len(txids_list) == 1:
        return txids_list[0]

    hashes = []
    for i in range(0, len(txids_list), 2):
        first = txids_list[i]
        if i == (len(txids_list) - 1):# this only happens when len is odd
            sum = first + first  # add with itself when odd length
        else:
            second = txids_list[i + 1]
            sum = first + second  # add with the next one
        # adding to the temp list
        hashes.append(HASH256(sum))
    # pass the temp list
    return merkleroot(hashes)

# global variable tx_fees
tx_fees = 0

def check_validity_calculate_tx_fees(transaction):
    global tx_fees
    valid = True

    input_sum = 0
    for input in transaction["vin"]:
        input_sum += input["prevout"]["value"]
        if input["txid"] == "":
            valid = False

    output_sum = 0
    for output in transaction["vout"]:
        output_sum += output["value"]

    if input_sum < output_sum:
        valid = False
    elif input_sum > output_sum:
        tx_fees += (input_sum - output_sum)

    return valid

Serialized_Coinbase_Transaction = {
    "txid": "5764f22fc3b00f4df8e46f9bcd6938d24a12f223ecbd10d1fe5d3c652d16184c",
    "vin": [
        {
            "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303233204368616e63656c6c6f72206f6e20626974636f696e2062756c6c",
            "sequence": 4294967295
        }
    ],
    "vout": [
        {
            "value": 625000000,
            "scriptPubKey": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"
        }
    ]
}

validated_transactions = [Serialized_Coinbase_Transaction["txid"]]

for filename in os.listdir(r"Assignment-1\mempool"):
    if filename.endswith(".json"):
        file_path = os.path.join(r"Assignment-1\mempool", filename)
        txid = filename.replace(".json", "")

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if check_validity_calculate_tx_fees(data):
                    validated_transactions.append(txid)
        except FileNotFoundError:
            print(f"Can't find the file {filename}")
        except json.JSONDecodeError:
            print(f"File format not correct for {filename}, try something else")

Serialized_Coinbase_Transaction["vout"][0]["value"] += tx_fees

# Our block
Block_Header = {
    "version": 1,
    "previous_block_hash": "0000111100000000000000000000000000000000000000000000000000000000",
    "merkle_root": merkleroot(validated_transactions),
    "timestamp": int(time.time()),
    "difficulty_target": "0000ffff00000000000000000000000000000000000000000000000000000000",
    "nonce": 0
}

def mine_block(header):
    while True:
        # according to bitcoin standards:
        # version : 4 bytes = 8 hex characters
        # previous_block_hash : 32 bytes = 64 hex characters
        # merkle_root : 32 bytes = 64 hex characters
        # timestamp :  4 bytes = 8 hex characters
        # difficulty_target : 32 bytes = 64 hex characters
        # nonce :  4 bytes = 8 hex characters
        content = (hex(header["version"])[2:].zfill(8) +
                   header["previous_block_hash"] +
                   header["merkle_root"] +
                   hex(header["timestamp"])[2:].zfill(8) +
                   header["difficulty_target"] +
                   hex(header["nonce"])[2:].zfill(8))
        # hex(xyz) returns 0xabcde
        # hex(xyz)[2:] returns abcde
        # hex(xyz)[2:].zfill(8) returns 000abcde (makes it 8 digits by adding zeroes)
        hash = HASH256(content)
        if int(hash, 16) < int(header["difficulty_target"], 16):
            break
        else:
            header["nonce"] += 1
    return header["nonce"]

Block_Header["nonce"] = mine_block(Block_Header)

# outputing a output.json file
with open(r"Assignment-1\output.json", "w") as output_file:
    output_file.write(json.dumps(Block_Header, indent=4) + "\n")
    output_file.write(json.dumps(Serialized_Coinbase_Transaction, indent=4) + "\n")
    for tx in validated_transactions:
        output_file.write(json.dumps(tx, indent=4) + "\n")
