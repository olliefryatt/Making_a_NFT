**About this project**

This repo makes two types of NFTs. a "Simple Collectible" and a "Advanced collectible". 

**Dependencies**

• Brownie & Ganahce CLI
• Working with Rinkyeby, need test eth
• IPFS command line, see promots on https://docs.ipfs.io/how-to/command-line-quick-start/
    - Once downloaded will want to run our own ipfs node --> $ ipfs daemon
    - Importnat we have a 2nd shell runningt our ipfs node
• Pinata, we will use their service to pin NFT image (in case we turn of local node) set up https://www.pinata.cloud/

**Simple collectible**

This is the easyiest means to have an a NFT. It does not contain any metadata.
• 1st Set up SimpleCollectible.sol this is based upon the Openzepplin ERC721 contract. 
• 2nd set out "deploy_and_create.py" script. 

**Advanced collectible**

1st Set up IPFS node to host image on. 
> $ ipfs daemon

Set up the AdvancedCollectible.sol smart contract, includes linking to smart contracts of openzepllin ER721 and Chainline random number.

Now set out script to "deploy_and_create.py" a NFT. This script deploys our smart contract & mints our first NFT from it. Check on testnet for "tokenCounter".
> "deploy_and_create.py"

Check we can now interact with the smart contract & mint additionaly NFTs.
> "create_collectible.py"

Currently the NFTs have no data behind them. Thus we need to set all their specific traints and we do that in the metadata script. Result is that we should have copies of the metadata saved in "metadata/rinkeby". Note we havn't set token URI, so images will still be blank. Ensure IPFS is set up and you have a local nodel. Note you may need to delete previous metadata files if this was run in the past. 
> create_metadata.py

5th, Set the token uri to assign a specific image.
>> "set_tokenuri.py"

Finished. We now have several NFTs with their metadata.

**.env should contain**

PRIVATE_KEY=______
WEB3_INFURA_PROJECT_ID=______
ETHERSCAN_TOKEN=______
PINATA_API_KEY=______
PINATA_API_SECRET=______
UPLOAD_IPFS=true


