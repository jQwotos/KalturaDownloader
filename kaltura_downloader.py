# Based on anime_scrapers by jQwotos

import os
import re
import requests
import subprocess
import json
import logging
import argparse
from progress.bar import Bar

LINK_PAT = re.compile('(https://)(.*)\n')

logger = logging.getLogger()
logger.setLevel("INFO")
logger.addHandler(logging.StreamHandler())

def parseLinks(raw_links):
    return list(map(lambda tuple_link: "".join(tuple_link),
              re.findall(LINK_PAT, raw_links)))

def download_video(raw_links, file_name):
    logger.info(f'Downloading file "{file_name}"')

    parsed_links = parseLinks(raw_links)
    
    tmp_name = f"{file_name}.ts"
    
    bar = Bar('Downloading', max=len(parsed_links), suffix='%(percent)d%%')

    with open(tmp_name, 'wb') as f:
        for link in parsed_links:
            bar.next()
            attempts = 0
            while attempts < 3:
                attempts += 1
                try:
                    download = requests.get(link, stream=True, timeout=10)
                    break
                except requests.exceptions.ConnectionError:
                    logging.error(f'Connection error for {link}, retrying {attempts} / 3')
                except:
                    logger.error(f"An error was caught, retrying {attempts} / 3")
                    
                    
            if download.status_code == 200:
                f.write(download.content)
    bar.finish()

parser = argparse.ArgumentParser()

parser.add_argument('dump', type=str, help="Data dump from Kaltura", nargs="?")

parser.add_argument('name', type=str, help="Name of output file", nargs="?")

args = parser.parse_args()

def main(args):
    with open(args.dump, 'r') as f:
        data = f.read()
        download_video(data, args.name)


if __name__ == "__main__":
    main(args)