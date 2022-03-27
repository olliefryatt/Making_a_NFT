"""
This script should only be used once the deploy_and_create script as been run. 
As it will engage with the NFT contract previously deployed there.
In fact this code is all in the script deploy_and_create. 
As it engages with the contract to produce a single additional NFT.
"""

from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = advanced_collectible.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Collectible created!")