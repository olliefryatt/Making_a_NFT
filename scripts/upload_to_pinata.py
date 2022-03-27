
"""
This script is for our advanced collectible, and it's an alterntive to storing metadata on a local ipfs node
see "create_metadata.py" for context.

Note we can pick if we want to use our local ipfs node or upload to pinita. Make this modification
in the create_metadata.py script

"""
import os
from pathlib import Path
import requests

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
# Change this filepath
filepath = "./img/pug.png"
filename = filepath.split("/")[-1:][0]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())


if __name__ == "__main__":
    main()