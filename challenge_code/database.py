from sqlalchemy import create_engine
from datetime import datetime as dt
from utils import get_logger


logger = get_logger('database')

logger.info('Creating the connection to the server')
engine = create_engine('postgresql://docker:docker@localhost:5432/challenge_db')
logger.info('Created the connection to the server')

def upload_to_database(df_pairings):
    '''
    Now we will export the dataframe info to the sql server in docker.
    '''
    ### add a time stamp to all the dataframes
    ### Table - Datafram pairing
    for value in df_pairings.values():
        value['fecha_subida'] = dt.now().strftime('%Y-%m-%d')

    ## populating the tablereplaces
    for table, dataf in df_pairings.items():
        dataf.to_sql(table, engine, if_exists='append', index=False)
        logger.info(f'{table} populated')

    logger.info('#####################\nUploaded to database')