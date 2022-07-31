from bs4 import BeautifulSoup as bs
import requests, coloredlogs, logging


def get_logger(name):
    ''' logger function with colors from coloredlogs'''
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    coloredlogs.install(fmt='%(asctime)s,%(msecs)03d %(levelname)s %(message)s', level='DEBUG', logger=logger)
    return logger

logger =  get_logger('utils')

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
        logger.exception(f'{url} not downloaded because {err}')
        exit()


def find_urls_from_html(url_dict):
    '''
    This function extracts the initial urls from the html files 
    with beautiful soup
    '''
    logger = get_logger('bs4')
    logger.info('Getting urls from html')
    url_files = []
    for link in url_dict.values():
        res = try_response(link)
        soup = bs(res.text, 'html.parser')
        ### bs4 finds the green big button with the download link
        url = soup.find('a', class_="btn btn-green btn-block").get('href')
        logger.info(f'{url} found')
        url_files.append(url)
    logger.info('finished getting urls from html')
    return url_files