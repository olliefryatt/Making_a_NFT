from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account

# URL's for us to use, note easier to do this. Could actually pull from individaul metadata files
dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

def main():
    print(f"Working on {network.show_active()}")
    # Engage with lattest version of the smart contract
    advanced_collectible = AdvancedCollectible[-1]
    # Take number of collectibles
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    # Loop through each token
    for token_id in range(number_of_collectibles):
        # get breed from token
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        # Check token uri hasn't been set
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])
            # note could replace "dog_metadata_dic" with queries pulling form each nft's metadata file

# This set
def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    # Set token URI is funtion in our smart contract, advanced collectible
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")