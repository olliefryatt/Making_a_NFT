from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

# Note these images have been used before, thus using this mapping to save time below & running ipfs node. 
# You could delete this, see "image_uri" below for more detail
breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    """"
    
    Ensure that IPFS node is running, or set up to work with Pinita. e.g. $ ipfs daemon
    see set up & more details if necessary here
    https://docs.ipfs.io/how-to/command-line-quick-start/

    """
    # Take the lattest deployed smart contract to work with
    advanced_collectible = AdvancedCollectible[-1]
    # Find number of NFT collectables we've made
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    # Start making the meta data for each breed
    for token_id in range(number_of_advanced_collectibles):
        # see get_breed() in helpful scripts, takes number & return string of actual breed
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        # Creat mapping to store metadata in, base it on pre-set template
        collectible_metadata = metadata_template
        # Check that metadata doesn't alreayd exsist
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        # If it doesn't exsist create metadata file & image uri
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            print(f"Metadata to look as: {collectible_metadata}")
            # Need to uploade image to IPFS, see funtion below
            # 1st create file name, note have to modify breed naming as in smart contract is writted in capitals
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            print(f"Image taken from this file: {image_path}")

            # Place image on ipfs or pinata, see funtion below for more detais
            # not as images already online we can point uri to pulic ones
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true": # Change this option in the .eng file
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            # Now save specific into
            collectible_metadata["image"] = image_uri
            # Save/dump dictionary into json file
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            # Can now upload whole file to ipfs, make sure ipfs daemon is running (see readme)
            # don't do this if we set upload to false
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)
            print(f"Saved locally: {metadata_file_name}")
            print(" ")

# Not make sure to upload images you have them saved in "img" file
# Note to see more detail on this see readme & notes on IPFS, as you need to run a IPFS node
# Note that if your local node goes down then NFT won't be visibe
# To counter this we could use "upload_to_pinata" script, and refrence it in this function
def upload_to_ipfs(filepath):
    # taking the filepath, opneing it in binary (rb, as will save in binary to ipfs)
    with Path(filepath).open("rb") as fp: 
        image_binary = fp.read() # image is now stored as binary
        # Now upload to IPFS
        ipfs_url = "http://127.0.0.1:5001" # this is our local node
        # now make an API call, check these parameters haven't changed on docs
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        # ipfs saves files as hash, can use this to point url to specific file
        ipfs_hash = response.json()["Hash"]
        # following codes spilts the following "./img/0-PUG.png" -- to -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        # now can set the uri (e.g. see example below with a hash in it)
        # example https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri