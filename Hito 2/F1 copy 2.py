


import psycopg2
import psycopg2.extras
import csv
import re
import openpyxl
from unidecode import unidecode

################################################################################################################
################################################################################################################
'''                                             Conexión a la DBS                                            '''
################################################################################################################
################################################################################################################

conn = psycopg2.connect(host ="********",
database ="********",
user ="********",
password ="********", port ="********")

cur = conn.cursor()
cur.execute("SET search_path TO F1;")


################################################################################################################
################################################################################################################
'''                                         Creación del las tablas                                          '''
################################################################################################################
################################################################################################################
query_eliminar_tablas = """
DROP TABLE IF EXISTS Circuito_Pais;
DROP TABLE IF EXISTS GranPremio_Circuito;
DROP TABLE IF EXISTS Equipo_GranPremio;
DROP TABLE IF EXISTS Temporada_Piloto;
DROP TABLE IF EXISTS Temporada_Escuderia;
DROP TABLE IF EXISTS Piloto_Pais;
DROP TABLE IF EXISTS Equipo;
DROP TABLE IF EXISTS GranPremio;
DROP TABLE IF EXISTS Pais;
DROP TABLE IF EXISTS Piloto;
DROP TABLE IF EXISTS Escuderia;
DROP TABLE IF EXISTS Circuito;
DROP TABLE IF EXISTS Temporada;
"""

# Drop SUPremo
""" 
Drop Table if Exists Circuito_Pais, GranPremio_Circuito, Equipo_GranPremio, Temporada_Piloto, 
Temporada_Escuderia, Piloto_Pais, Equipo, GranPremio, Pais, Piloto, Escuderia, Circuito, Temporada CASCADE;
"""
cur.execute(query_eliminar_tablas)

query_creacion_tablas = """
CREATE TABLE Temporada (
    id serial PRIMARY KEY,
    agno INT
);
CREATE TABLE Circuito (
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);
CREATE TABLE Escuderia (
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);
CREATE TABLE Piloto (
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);
CREATE TABLE Pais (
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);
CREATE TABLE GranPremio (
    id serial PRIMARY KEY,
    nombre VARCHAR(255),
    fecha DATE,
    clima VARCHAR(255)
);
CREATE TABLE Equipo (
    Es_id bigint not null,
    Pi_id bigint not null,
    T_id bigint not null,
    PRIMARY KEY (Es_id, Pi_id, T_id),
    FOREIGN KEY (Es_id) REFERENCES Escuderia(id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id),
    Foreign Key (T_id) REFERENCES Temporada(id)
);
CREATE TABLE Piloto_Pais (
    Pi_id bigint not null,
    Pa_id bigint not null,
    PRIMARY KEY (Pi_id, Pa_id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id),
    FOREIGN KEY (Pa_id) REFERENCES Pais(id)
);
CREATE TABLE Temporada_Escuderia (
    Es_id bigint not null,
    T_id bigint not null,
    ptje_acumulado FLOAT,
    es_campeon BOOLEAN,
    PRIMARY KEY (Es_id, T_id),
    FOREIGN KEY (Es_id) REFERENCES Escuderia(id),
    FOREIGN KEY (T_id) REFERENCES Temporada(id)
);
CREATE TABLE Temporada_Piloto (
    T_id bigint not null,
    Pi_id bigint not null,
    ptje_acumulado FLOAT,
    es_campeon BOOLEAN,
    posicion_campeonato INT,
    PRIMARY KEY (T_id, Pi_id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id),
    FOREIGN KEY (T_id) REFERENCES Temporada(id)
);
CREATE TABLE Equipo_GranPremio (
    EqEs_id bigint not null,
    EqPi_id bigint not null,
    EqT_id bigint not null,
    Gp_id bigint not null,
    posicion_carrera INT,
    vuelta_rapida_c VARCHAR(255),
    posicion_qualy INT,
    tiempo_qualy VARCHAR(255),
    edad_piloto INT,
    PRIMARY KEY (EqEs_id,EqPi_id,Gp_id,EqT_id),
    FOREIGN KEY (EqEs_id,EqPi_id,EqT_id) REFERENCES Equipo(Es_id, Pi_id,T_id),
    FOREIGN KEY (Gp_id) REFERENCES GranPremio(id)
);
CREATE TABLE GranPremio_Circuito (
    Gp_id bigint not null,
    Cir_id bigint not null,
    PRIMARY KEY (Gp_id,Cir_id),
    FOREIGN KEY (Cir_id) REFERENCES Circuito(id),
    FOREIGN KEY (Gp_id) REFERENCES GranPremio(id)
);
CREATE TABLE Circuito_Pais (
    Cir_id bigint not null,
    Pa_id bigint not null,
    PRIMARY KEY (Cir_id, Pa_id),
    FOREIGN KEY (Cir_id) REFERENCES Circuito(id),
    FOREIGN KEY (Pa_id) REFERENCES Pais(id)
);"""

cur.execute(query_creacion_tablas)
    
################################################################################################################
################################################################################################################
'''                                        Rellenado de las tablas                                           '''
################################################################################################################
################################################################################################################

def findOrInsert(table, name):
    cur.execute("select id from "+table+" where nombre=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (nombre) values (%s) returning id", [name])
        return cur.fetchone()[0]

with open('drivers_championship_1950-2020.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    k = 0
    for row in reader: 
        k+=1
        if k==1:
            continue
        #if k>90:
        #    break
        
        #Piloto
        piloto = row[3]
        piloto = unidecode(piloto)
        Pi_id = findOrInsert('piloto', piloto)


with open('results.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    k = 0
    for row in reader:
        k+=1
        if k==1:
            continue
        #if k>30:
        #    break
        
        raceid = row[1]
        dirverid = row[2]

        print(raceid)

        if raceid >= '1051':
            continue

        i = 0
        with open('drivers.csv') as csvfile1:
            reader1 = csv.reader(csvfile1, delimiter = ',', quotechar = '"')
            i = 0
            for row1 in reader1:
                i+=1
                if i==1:
                    continue
                #if i>30:
                #    break
                if row1[0] == dirverid:
                    forename = row1[4]
                    surname = row1[5]
                    driver = unidecode(forename + ' ' + surname)
                    cur.execute("select id from piloto where nombre=%s limit 1", [driver])
                    Pi_id = cur.fetchone()[0]
                    break
        
        with open('races.csv') as csvfile2:
            reader2 = csv.reader(csvfile2, delimiter = ',', quotechar = '"')
            j = 0
            for row2 in reader2:
                j+=1
                if j==1:
                    continue
                #if j>30:
                #    break
                if row2[0] == raceid:
                    gp_name = row2[4]
                    gp_name = unidecode(gp_name)
                    gp_date = row2[5]
                    gp_year = row2[1]
                    cur.execute("select id from granpremio where nombre=%s and fecha=%s limit 1", [gp_name,gp_date])
                    gp_id = cur.fetchone()[0]
                    cur.execute("select id from temporada where agno=%s limit 1", [gp_year])
                    T_id = cur.fetchone()[0]
                    break
        
        equipo = cur.execute("select es_id from equipo where pi_id=%s and t_id=%s limit 1", [Pi_id,T_id])
        Es_id = cur.fetchone()[0]

        

        #equipo_granpremio
        cur.execute("select * from equipo_granpremio where (gp_id,eqpi_id) = (%s, %s) limit 1", [gp_id,Pi_id])
        if (not cur.fetchone()):
            cur.execute("insert into equipo_granpremio (eqes_id,eqpi_id,eqt_id,gp_id,posicion_carrera,vuelta_rapida_c,posicion_qualy,tiempo_qualy,edad_piloto) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", [Es_id,Pi_id,T_id,gp_id,1,"1:15.791",1,"1:15.791",30])
        
    
conn.commit()

conn.close()



