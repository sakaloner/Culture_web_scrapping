from datetime import datetime
import os

from bs4 import BeautifulSoup as bs
import requests

from ..environment import *
from utils import get_logger

logger = get_logger('web_data')

def try_response(url):
    '''
    try to get the response from the url
    '''
    logger.info(f'Trying to get response from {url}')
    try:    
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status
        logger.info(f'{url} downloaded')
        return response
    except Exception as err:
        logger.exception(f'{url} not downloaded becausec {err}')
        exit()


def save_file(url, local_filename):
    res = try_response(url)
    with requests.get(url) as r:
        r.raise_for_status()
        with open("instagram.ico", "wb") as f:
            f.write(r.content)
            return f


def download_csv_files():
    ## Uncomment the last  if you want to use beautiful soup to extract the
    ## urls from the html files. You will also need to use
    ## url_files = find_urls_from_html()
    logger.info('Downloading csv files')
    urlfiles_and_names = url_files_dict

    for url, name in urlfiles_and_names:
        time = datetime.now()
        subfolder = datetime.strftime(time, "%Y-%m")
        file_name = datetime.strftime(time, "%d-%m-%Y")
        os.makedirs(f'../data_csv/{name}/{subfolder}', exist_ok=True)
        logger.info(f"created folder for {subfolder}")

        save_file(url, f'../data_csv/{name}/{subfolder}/{file_name}.csv')
        logger.info(f'{name} downloaded in {subfolder}')

def get_web_data():
    download_csv_files()
    logger.info('#####################\nDownloaded files')    
