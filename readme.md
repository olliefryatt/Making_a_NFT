**Dependencies**

• Brownie & Ganahce CLI
• Working with Rinkyeby, need test eth
• IPFS command line, see promots on https://docs.ipfs.io/how-to/command-line-quick-start/
    - Once downloaded will want to run our own ipfs node --> $ ipfs daemon
    - Importnat we have a 2nd shell runningt our ipfs node --> click "+" see that we have two shells
• Pinata, we will use their service to pin NFT image (in case we turn of local node) set up https://www.pinata.cloud/

**Advanced collectible**

1st Set up Advanced Collectible contract, includes linking to smart contracts of openzepllin ER721 and Chainline random number

2nd build/deploy "deploy_and_create.py". This script deploys our smart contract & mint our first NFT from it. Check on testnet for "tokenCounter".
>> "deploy_and_create.py"

3rd check we can now interact with the smart contract & mint additionaly NFTs.
>> "create_collectible.py"

4th, Currently the NFTs have no data behind them. Thus we need to set all their specific traints and we do that in the metadata script. Result is that we should have copies of the metadata saved in "metadata/rinkeby". Note we havn't set token URI, so images will still be blank. Ensure IPFS is set up and you have a local nodel. Note you may need to delete previous metadata files if this was run in the past. 
>> create_metadata.py

5th, Set the token uri to assign a specific image.
>> "set_tokenuri.py"

**.env should contain**

PRIVATE_KEY=______
WEB3_INFURA_PROJECT_ID=______
ETHERSCAN_TOKEN=______
PINATA_API_KEY=______
PINATA_API_SECRET=______
UPLOAD_IPFS=true


