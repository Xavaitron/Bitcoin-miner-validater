### Solution

1. Inputting via json/os lib.

Change the path if required
It throws error if file is not found or can't be opened.

![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/9ba9a71c-9a8a-4f1d-a038-cf1b3762aeb0)

2. Creating a double sha256 function that takes a hex(string format) as input and hashes it twice.

![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/675fc633-1acb-4e8d-9be2-6ab6df505bb0)

3. Create Merkle root function that pairs up transactions, and in the case, there are odd transactions the last transaction is hashed with itself. It's a recursive function that hashes a layer of transactions and pass it again till we have one final hash.

![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/6cd6781f-b807-4684-9c57-c883329d064a)

4. Validating transactions and calculating transaction fees.
It returns valid only when the sum of inputs is greater/ than the sum of outputs. In the case of greater inputs, the difference is taken as transaction fees that goes to the miner adding to the block reward.
![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/1197cec8-316e-4a17-a451-a8b04bde9680)

5. Making the coinbase transaction as a dictionary which is later converted to json object.

![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/6613fb48-b97c-46e1-b1bd-e42672cf4a79)

6. Similarly made the block header
 used the time library to get the current time in unix format.
![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/d92bca24-d99f-4c9f-ab4c-4a3d39d3fe9d)

7. Mining the block 
concatenate the block content in standard bitcoin format and double hash it. Ran a while loop on the nonce till the hash reached below the target.

![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/b5da9206-1a45-4d02-a1b7-a1ee1ffb339e)

8. Outputting the json file with indentation.

![image](https://github.com/Xavaitron/Bitcoin-miner-validater/assets/143639958/c8a18ecd-72cd-4063-ae6e-76b478d8230a)

#Performance
1. The file is created within 0.2s on my PC(pretty fast)
2. The nonce is created using the current time.







