from web_data import get_web_data
from data_filter import clean_data
from database import upload_to_database
from utils import get_logger

logger = get_logger('main')

if __name__ == '__main__':
    logger.info('Starting the program')
    get_web_data()
    logger.info('Finished getting web data')
    df_cleaned = clean_data(['sadf', 'sadf'])
    logger.info('Finished cleaning data')
    upload_to_database(df_cleaned)
    logger.info('Finished uploading to database')
