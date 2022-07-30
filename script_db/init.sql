\c challenge_db;
\echo 'Loading Database';
CREATE TABLE IF NOT EXISTS registros_combi  (
    item_id SERIAL PRIMARY KEY, /* ID do item */ 
    cod_localidad INT,
    id_provincia INT,
    id_departamento INT,
    categoria TEXT,
    provincia TEXT,
    localidad TEXT,
    nombre TEXT,
    domicilio TEXT,
    codigo_postal TEXT,
    numero_telefono TEXT,
    mail TEXT,
    web TEXT,
    fecha_subida TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cines (
    provincia TEXT PRIMARY KEY,
    num_pantallas INT,
    num_butacas INT,
    num_incaa INT,
    fecha_subida TIMESTAMP
);
/* Create computation tables from combines datase  */
CREATE TABLE IF NOT EXISTS categoria_total (
    categoria TEXT PRIMARY KEY,
    total INT,
    fecha_subida TIMESTAMP
);
CREATE TABLE IF NOT EXISTS fuentes_total (
    fuente TEXT PRIMARY KEY,
    total INT,
    fecha_subida TIMESTAMP
);
CREATE TABLE IF NOT EXISTS categoria_provincia_total (
    id SERIAL PRIMARY KEY,
    provincia TEXT,
    categoria TEXT,
    total INT,
    fecha_subida TIMESTAMP
);
