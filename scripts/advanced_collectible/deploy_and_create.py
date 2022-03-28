from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)
from brownie import AdvancedCollectible, network, config

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy_and_create():
    """
    Deploys & Creates first NFT. 
    arg: none
    retruns: NFT contract & first collectible
    """
    print("Starting...")
    print(f"The active network is {network.show_active()}")
    account = get_account()
    print(f"Account being used: {account}")
    print("Deploying AdvancedCollectible Smart contract")
    advanced_collectible = AdvancedCollectible.deploy(
        # The Smart contract construction requires 4 parameters
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False), #if no verify then false = don't do it
    )
    print(f"AdvancedCollectible contract now deployed: {advanced_collectible.address}")
    print("")
    # Fund with link, as this is necessary to get random number from vrf_coordinator
    print("Funding with link")
    fund_with_link(advanced_collectible.address)
    print("Start interaction with our Smart contract to create a NFT")
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")
    return advanced_collectible, creating_tx

    
def main():
    deploy_and_create()