


import psycopg2
import psycopg2.extras
import csv
import re
import openpyxl
from unidecode import unidecode

conn = psycopg2.connect(host ="cc3201.dcc.uchile.cl",
database ="cc3201",
user ="cc3201",
password ="completo", port ="5521")

cur = conn.cursor()
cur.execute("SET search_path TO F1;")

def findOrInsert(table, name):
    cur.execute("select id from "+table+" where nombre=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (nombre) values (%s) returning id", [name])
        return cur.fetchone()[0]
    
####   LEER CSV'S   #####
with open('drivers_championship_1950-2020.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    k = 0
    for row in reader: 
        k+=1
        if k==1:
            continue
        #if k>3:
        #    break
        
        ####    ENTIDADES    ####
        #Temporada
        year = row[1]
        cur.execute("select id from temporada where agno=%s limit 1", [year])
        r = cur.fetchone()
        T_id = None
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


        #puntaje_acumulado_chpi = row[7]


with open ('F1Drivers_Dataset.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ';', quotechar = '"')
    k = 0
    for row in reader: 
        k+=1
        if k==1:
            continue
        #if k>277:
        #    break
    
        pais = row[1]
        pais = unidecode(pais)
        Pa_id = findOrInsert('pais', pais)

        #Piloto
        piloto = row[0]
        piloto = unidecode(piloto)
        Pi_id = Pi_id = findOrInsert('piloto', piloto)

        #Nacionalidad
        cur.execute("select * from nacionalidad where (pa_id,pi_id) = (%s, %s) limit 1", [Pa_id,Pi_id])
        if (not cur.fetchone()):
            cur.execute("insert into nacionalidad (pa_id,pi_id) values (%s, %s)", [Pa_id,Pi_id])
        





with open ('circuits.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    k = 0
    for row in reader: 
        k+=1
        if k==1:
            continue
        #if k>3:
        #    break

        #Circuito
        circuito = row[2]
        circuito = unidecode(circuito)
        ci_id = findOrInsert('circuito', circuito)
        #Pais circuito  
        pais = row[4]
        pais = unidecode(pais)
        Pa_id = findOrInsert('pais', pais)

        #EstaEn
        cur.execute("select * from estaen where (pa_id,cir_id) = (%s, %s) limit 1", [Pa_id,ci_id])
        if (not cur.fetchone()):
            cur.execute("insert into estaen (pa_id,cir_id) values (%s, %s)", [Pa_id,ci_id])
        

        
"""
 
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

            # Id de Temporada
            year= row[1]
            t_id = findOrInsert('temporada',year)

            
            id_race = row[0]
            id_circuit = row[3]
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



