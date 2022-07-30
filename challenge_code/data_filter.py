import pandas as pd
from datetime import datetime as dt
from utils import get_logger

#initializing the logger
logger = get_logger('data_filter')

def clean_data(nombres_de_archivos: list[str]) -> pd.DataFrame:
    '''
    Cleaning each dataframe before merging.
    we will keep the attribute 'fuente' to created the computed
    tables with it but well make sure to erase it after merging
    and computation'''
    logger.info('Starting to clean data')
    def rename_columns(df):
        """
        renaming the columns of the data frames
        """
        new_columns = ['cod_localidad',
                'id_provincia',
                'id_departamento',
                'categoria',
                'provincia',
                'localidad',
                'nombre',
                'domicilio',
                'codigo_postal',
                'numero_telefono',
                'mail',
                'web',
                'fuente']
        df.columns = [new_columns]

    ### loading the files
    file_name = 'museos/2022-07/26-07-2022.csv' 
    df_museos = pd.read_csv(file_name)
    df_cines = pd.read_csv('cines/2022-07/26-07-2022.csv')
    df_bib = pd.read_csv('bibliotecas/2022-07/26-07-2022.csv')
    logger.info('Finished loading files into DataFrames')

    ## Deleting the columns we dont need from the dataframes
    df_museos.drop(df_museos.columns[
        [3,4,10,12,16,17,18,19,21,22,23]
        ], axis=1, inplace=True)
    df_cines.drop(df_cines.columns[
        [3,6,10,12,16,17,18,19,21,22,23,24,25]
        ], axis=1, inplace=True)
    df_bib.drop(df_bib.columns[
        [3,5,7,11,13,17,18,19,20,22,23,24]
        ], axis=1, inplace=True)

    ## renaming the columns of the dataframse 
    rename_columns(df_museos)
    rename_columns(df_cines)
    rename_columns(df_bib)
    logger.info('Finished deleting homogenizing the dataframes')

    ###### First type of Table ########
    ### Concatenating the cleaned dataframes into an uniform single one
    df_combi = pd.concat([df_museos, df_cines, df_bib])


    #### Second type of table ########
    '''
    Creating 3 new tables with computated information by using group by. 
    The challenge info said it was one table but it makes more 
    sense like this in my humble opinion :).
    '''
    df_cat_total = df_combi.groupby('categoria', as_index=False)['cod_localidad'].count()
    df_cat_total.columns = ['categoria', 'total']
    df_fuente_total = df_combi.groupby('fuente', as_index=False )['cod_localidad'].count()
    df_fuente_total.columns = ['fuente', 'total']
    df_prov_cat_total = df_combi.groupby(['provincia', 'categoria'], as_index=False)['cod_localidad'].count()
    df_prov_cat_total.columns = ['provincia', 'categoria', 'total']


    # Erasing the attirubute 'fuente' because it is not needed 
    # a category that should be in the final merged dataframe
    df_combi.drop(['fuente'], axis=1, inplace=True)


    #### Thirth type of table ########
    # We use the raw cines dataframe to compute some values by
    # using the group by to answear some questions about cinemas 
    # in Argentina

    df_cines2 = pd.read_csv('cines/2022-07/26-07-2022.csv')
    df_comp = df_cines2.groupby('Provincia', as_index=False)['Pantallas','Butacas', 'espacio_INCAA'].sum()
    df_comp['espacio_INCAA'] = df_cines2.groupby('Provincia', as_index=False)['espacio_INCAA'].count()['espacio_INCAA']
    ### rename columns to fit the sql table
    df_comp.columns = ['provincia', 'num_pantallas', 'num_butacas', 'num_incaa']

    # Creating a dict object to pass the info to the database pusher function
    df_pairings = {
        #table name: dataframe
        'registros_combi': df_combi,
        'cines': df_comp,
        'categoria_total': df_cat_total,
        'fuentes_total': df_fuente_total,
        'categoria_provincia_total': df_prov_cat_total
    }
    logger.info('Finished cleaning data :)')
    return df_pairings