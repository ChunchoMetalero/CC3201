


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

conn = psycopg2.connect(host ="cc3201.dcc.uchile.cl",
database ="cc3201",
user ="cc3201",
password ="completo", port ="5521")

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
    PRIMARY KEY (Es_id, Pi_id),
    FOREIGN KEY (Es_id) REFERENCES Escuderia(id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id)
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
    Gp_id bigint not null,
    posicion_carrera INT,
    vuelta_rapida_c TIME,
    posicion_qualy INT,
    tiempo_qualy TIME,
    edad_piloto INT,
    PRIMARY KEY (EqEs_id,EqPi_id,Gp_id),
    FOREIGN KEY (EqEs_id,EqPi_id) REFERENCES Equipo(Es_id, Pi_id),
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
        if k>90:
            break
        
        ####    ENTIDADES    ####
        #Temporada
        year = row[1]
        cur.execute("select id from temporada where agno=%s limit 1", [year])
        r = cur.fetchone()
        if(r):
            T_id = r[0]
        else:
            cur.execute("insert into temporada (agno) values (%s) returning id", [year])
            T_id = cur.fetchone()[0]

        #Piloto
        piloto = row[3]
        piloto = unidecode(piloto)
        Pi_id = findOrInsert('piloto', piloto)

        #Escuderia
        escuderia = row[6]
        escuderia = unidecode(escuderia)
        Es_id = findOrInsert('escuderia', escuderia)

        #####   RELACIONES   ####
        #Equipo
        cur.execute("select * from equipo where (es_id,pi_id) = (%s, %s) limit 1", [Es_id,Pi_id])
        if (not cur.fetchone()):
            cur.execute("insert into equipo (es_id,pi_id) values (%s, %s)", [Es_id,Pi_id])


        #Temporada_Escuderia
        cur.execute("select * from temporada_escuderia where (t_id,es_id) = (%s, %s) limit 1", [T_id,Es_id])
        if not cur.fetchone():
            cur.execute("insert into temporada_escuderia (t_id,es_id,ptje_acumulado,es_campeon) values (%s, %s, %s, %s)", [T_id,Es_id,row[7],False])
        else:
            cur.execute("update temporada_escuderia set ptje_acumulado = ptje_acumulado + %s where (t_id,es_id) = (%s, %s)", [row[7],T_id,Es_id])
            #cur.execute("update temporada_escuderia set es_campeon = true where (t_id,es_id) = (%s, %s) and ptje_acumulado = (select max(ptje_acumulado) from temporada_escuderia where t_id = %s)", [T_id,Es_id,T_id])
        
        #Temporada_Piloto
        cur.execute("select * from temporada_piloto where (t_id,pi_id) = (%s, %s) limit 1", [T_id,Pi_id])
        if not cur.fetchone():
            cur.execute("insert into temporada_piloto (t_id,pi_id,ptje_acumulado,es_campeon,posicion_campeonato) values (%s, %s, %s, %s, %s)", [T_id,Pi_id,row[7],False,row[2]])
            
query_es_campeon_pilotos = """
UPDATE temporada_piloto AS t
SET es_campeon = (ptje_acumulado = (
        SELECT MAX(t2.ptje_acumulado)
        FROM temporada_piloto AS t2
        WHERE t2.t_id = t.t_id
    )
);
"""



query_es_campeon_constructor = """
UPDATE temporada_escuderia AS t
SET es_campeon = (ptje_acumulado = (
        SELECT MAX(t2.ptje_acumulado)
        FROM temporada_escuderia AS t2
        WHERE t2.t_id = t.t_id
    )
);
"""
cur.execute(query_es_campeon_constructor)
cur.execute(query_es_campeon_pilotos)
            


with open ('F1Drivers_Dataset.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ';', quotechar = '"')
    k = 0
    for row in reader: 
        k+=1
        if k==1:
            continue
        if k>30:
            break
    
        pais = row[1]
        pais = unidecode(pais)
        Pa_id = findOrInsert('pais', pais)

        #Piloto
        piloto = row[0]
        piloto = unidecode(piloto)
        Pi_id = Pi_id = findOrInsert('piloto', piloto)

        #Piloto_Pais
        cur.execute("select * from Piloto_Pais where (pa_id,pi_id) = (%s, %s) limit 1", [Pa_id,Pi_id])
        if (not cur.fetchone()):
            cur.execute("insert into Piloto_Pais (pa_id,pi_id) values (%s, %s)", [Pa_id,Pi_id])


with open ('circuits.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    k = 0
    for row in reader: 
        k+=1
        if k==1:
            continue
        if k>30:
            break

        #Circuito
        circuito = row[2]
        circuito_name = unidecode(circuito)
        ci_id = findOrInsert('circuito', circuito_name)

        #Pais circuito  
        pais = row[4]
        pais_name = unidecode(pais)
        Pa_id = findOrInsert('pais', pais_name)

        #Circuito_Pais
        cur.execute("select * from Circuito_Pais where (pa_id,cir_id) = (%s, %s) limit 1", [Pa_id,ci_id])
        if (not cur.fetchone()):
            cur.execute("insert into Circuito_Pais (pa_id,cir_id) values (%s, %s)", [Pa_id,ci_id])
        
       

with open ('races.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
        k = 0
        for row in reader:
            k+=1
            if k==1:
                continue
            if k>30:
               break

            #Nombre Gran Premio
            gp_name = row[4]
            gp_name = unidecode(gp_name)
            #Fecha Gran Premio
            gp_date = row[5]

            #gran premio
            cur.execute("select id from granpremio where nombre=%s and fecha= %s limit 1", [gp_name,gp_date])
            r = cur.fetchone()
            if(r):
                gp_id = r[0]
            else:
                cur.execute("insert into granpremio (nombre,fecha) values (%s,%s) returning id", [gp_name,gp_date])
                gp_id = cur.fetchone()[0]


            circuito_id = row[3]

            with open ('circuits.csv') as csvfile1:
                reader1 = csv.reader(csvfile1, delimiter = ',', quotechar = '"')
                i = 0
                for row1 in reader1:
                    i+=1
                    if i==1:
                        continue

                    if i>30:
                        break

                    if row1[0] == circuito_id:
                        circuito = row1[2]
                        cur.execute("select id from circuito where nombre=%s limit 1", [unidecode(circuito)])
                        cir_id = cur.fetchone()[0]
                        break
                    
            #gran premio_circuito
            cur.execute("select * from granpremio_circuito where (gp_id,cir_id) = (%s, %s) limit 1", [gp_id,cir_id])
            if (not cur.fetchone()):
                cur.execute("insert into granpremio_circuito (gp_id,cir_id) values (%s, %s)", [gp_id,cir_id])

            #equipo_granpremio
            cur.execute("select * from equipo_granpremio where (gp_id,eqes_id,eqpi_id) = (%s, %s, %s) limit 1", [gp_id,Es_id,Pi_id])
            if (not cur.fetchone()):
                cur.execute("insert into equipo_granpremio (gp_id,eqes_id,eqpi_id,posicion_carrera,vuelta_rapida_c,posicion_qualy,tiempo_qualy,edad_piloto) values (%s, %s, %s, %s, %s, %s, %s, %s)", [gp_id,Es_id,Pi_id,row[8],row[9],row[10],row[11],row[12]])





            
        
            



            


            

            """ 
            with open ('results.csv') as csvfile:
                reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
                i = 0
                for row in reader:
                    i+=1
                    if i==1:
                        continue
                    if id_race == row[1]:
                        pilot_id = row[2]
                        constructor_id = row[3]
                        with open ('constructor.csv') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
                            i = 0
                            for row in reader:
                                i+=1
                                if i==1:
                                    continue

        
                                
                              
            # Id de Temporada
            year= row[1]
            t_id = findOrInsert('temporada',year)

            
            id_race = row[0]
            id_circuit = row[3]    


            clima = "Sunny C:"
            #GranPremio
            cur.execute("select * from granpremio where (T_id,EqE_id,EqP_id,Cir_id,nombre,fecha,clima,posicion_carrera, vuelta_rapida_c,posicion_qualy,tiempo_qualy,edad_piloto) = (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) limit 1", [])
            if (not cur.fetchone()):
                cur.execute("insert into granpremio (T_id,EqE_id,EqP_id,Cir_id,nombre,fecha,clima,posicion_carrera, vuelta_rapida_c,posicion_qualy,tiempo_qualy,edad_piloto) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [])


    
            cur.execute("select id from granpremio where fecha=%s limit 1", [gp_date])
            r = cur.fetchone()
            gp_date_id = None
            if(r):
                gp_date_id = r[0]
            else:
                cur.execute("insert into granpremio (fecha) values (%s) returning id", [gp_date])
                gp_date_id = cur.fetchone()[0]
            """
    
conn.commit()

conn.close()



