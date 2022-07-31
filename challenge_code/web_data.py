from datetime import datetime
from pathlib import Path
import os, time

import requests
from decouple import config

from utils import get_logger

## initializing logger
logger = get_logger('web_data')

def try_response(url):
    '''
    check the response from the url.
    Retry if it times out
    '''
    logger.info(f'Trying to get response from {url}')
    try:    
        response = requests.get(url, timeout=10)
        # If the response was successful, no Exception will be raised
        response.raise_for_status
        logger.info(f'{url} downloaded')
        return response
    except requests.exceptions.Timeout as err: 
        logger.exception(f'{url} not downloaded because it TIMED OUT')
        time.sleep(5)
        try_response(url)
    except Exception as err:
        logger.exception(f'{url} not downloaded because {err}')
        exit()

def save_file(url, local_filename):
    '''
    Save local_filename from url'''
    res = try_response(url)
    with open(f"{local_filename}.csv", "wb") as f:
        f.write(res.content)
        return f

def download_csv_files():
    '''
    Download the csv files from the web using urls from the
    .env file. It uses the datetime module to create the directories
    and file names.
    Alternatively the urls for downloading the files can be found
    using beautifulsoup to extract them from 
    the original url (not the url of the csv files). This can be done
    uncommenting the next line and deleting the other variable with the same name,
    and creating the correct mapping of variables to urls'''
    ## url_files_and_names = find_urls_from_html()

    logger.info('Downloading csv files')

    ### creating a dictionary that pairs name of the file
    ### subfolder with an url of the file
    url_files_dict = {
        'museos': config('URL_MUSEOS'),
        'salas de cine': config('URL_CINES'),
        'bibliotecas': config('URL_BIBLIOTECAS')
    }
    urlfiles_and_names = url_files_dict

    for name, url in urlfiles_and_names.items():
        logger.info(f'name: {name}, url: {url}')

        time_now = datetime.now()       
        subfolder = datetime.strftime(time_now, "%Y-%m")
        file_name_time = datetime.strftime(time_now, "%d-%m-%Y")

        path_subfolder = Path(f'data_csv/{name}/{subfolder}')
        os.makedirs(path_subfolder, exist_ok=True)
        logger.info(f"created folder for {subfolder}")

        path_file = Path(f'data_csv/{name}/{subfolder}/{file_name_time}')
        save_file(url, path_file)
        logger.info(f'{name} downloaded in {subfolder}')

def get_web_data():
    download_csv_files()
    logger.info('Downloaded all the files')    

if __name__ == '__main__':
    get_web_data()