from brownie import accounts, network, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3


# List enrionments so our scripts can adapt depending on local vs. live testing
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]
# Putting a url so we can look at NFT's on opensea
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
# Map the breeds of our NFT's to numeric values, note this matches the mapping set out in the smart contact
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    """
    Takes a numeric inputs & returns a string saying what the nft is 
    """
    return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    """
    Returns the account (wallet/address) to use. 
    Looks at if we are wroking with local or test net & returns correct account
    arg = none necessary
    """
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    #if network.show_active() in config["networks"]:
    return accounts.add(config["wallets"]["from_key"])
    return None


contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    """
    This function will either:
        - Get an address from the config
        - Or deploy a Mock to use for a network that doesn't have the contract
    Args:
        contract_name (string): This is the name of the contract that we will get
        from the config or deploy
    Returns:
        brownie.network.contract.ProjectContract: This is the most recently deployed
        Contract of the type specified by a dictionary. This could either be a mock
        or a 'real' contract on a live network.
    """
    # link_token
    # LinkToken
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        print(f"Live so use address in config for: {contract_name}")
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print("Deploying mocks function starting...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("Mocks are all done!")
    print("")


# vrf_coordinator requirs link for payment
def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    """
    Funds an address with Link, necessary to get random number from chainlink.
    Arg: address to fund
    """
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded with link:{contract_address}")
    return funding_tx