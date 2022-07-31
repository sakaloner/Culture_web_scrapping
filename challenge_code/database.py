from datetime import datetime as dt

from sqlalchemy import create_engine
from utils import get_logger
from decouple import config


logger = get_logger('database')

logger.info('Creating the connection to the server')
### Generating url to connect to the db from the env variables
user = config('DB_USER')
password = config('DB_PASSWORD')
port = config('PORT_DB')
db_url = f'postgresql://{user}:{password}@localhost:{port}/challenge_db'

### Creating the engine to connect to the db
engine = create_engine(db_url)
logger.info('Created the lazy connection to the server')

def upload_to_database(df_pairings):
    '''
    Now we will export the dataframe info to the sql server in docker.
    '''
    ### Make sure the tables are empty before populating them
    with engine.connect() as con:
        con.execute('DELETE FROM categoria_provincial_total')
        con.execute('DELETE FROM categoria_total')
        con.execute('DELETE FROM cines')
        con.execute('DELETE FROM fuentes_total')
        con.execute('DELETE FROM registros_combi')


    ### add a time stamp to all the dataframes
    ### Table - Datafram pairing
    for value in df_pairings.values():
        value['fecha_subida'] = dt.now().strftime('%Y-%m-%d')

    ## populating the tablereplaces
    for table, dataf in df_pairings.items():
        dataf.to_sql(table, engine, if_exists='append', index=False)
        logger.info(f'{table} populated')

    logger.info('Uploaded to database')

