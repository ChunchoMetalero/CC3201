import psycopg2
import psycopg2.extras
import csv
import re

# ssh -p 240 cc3201@cc3201.dcc.uchile.cl


conn = psycopg2.connect (host = "cc3201.dcc.uchile.cl",
database = "cc3201",
user = "cc3201",
password = "j'<3_cc3201" , port = "5440" )

cur = conn.cursor()
cur.execute("SET search_path TO superheroes;")

def findOrInsert(table, name):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]
    

with open('Laboratorio_05_data.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader: 
        i+=1
        if i==1:
            continue

        #if i>10:
        #    break

        name = row[1]

        intelligence = int(row[2]) if row[2] != 'null' else 'null' 
        strenght = int(row[3]) if row[3] != 'null' else 'null'
        speed = int(row[4]) if row[4] != 'null' else 'null'

        if intelligence == 'null':
            intelligence = 0

        if strenght == 'null':
            strenght = 0

        if speed == 'null':
            speed = 0
        


        alter_ego = [m.strip() for m in row[9].split(',')]
        valid_alter_egos = list(filter(lambda x: len(x)>0, alter_ego))


        work_occupation = [m.strip() for m in row[23].split(',')]
        valid_work_occupations = list(filter(lambda x: len(x)>0, work_occupation))


        alter_egos_id = []
        for alter_ego in valid_alter_egos:
            alter_egos_id.append(findOrInsert('mythra_Alterego', alter_ego))

        work_occupations_id = []
        for work_occupation in valid_work_occupations:
            work_occupations_id.append(findOrInsert('mythra_WorkOcupation', work_occupation))


        cur.execute("select id from mythra_character where name=%s limit 1", [name])
        r = cur.fetchone()
        character_id = None
        if(r):
            character_id = r[0]
        else:
            cur.execute("insert into mythra_character (name) values (%s) returning id", [name])
            character_id = cur.fetchone()[0]

        if(character_id):
            if(r):
                character_id = r[0]
            else:            
                cur.execute("insert into mythra_superheroe (character_id, name, intelligence, strenght, speed) values (%s, %s, %s, %s, %s) returning character_id", [character_id, name, intelligence, strenght, speed])
                cur.fetchone()[0]

                for alter_ego_id in alter_egos_id:
                    cur.execute("select * from mythra_superheroe_alterego where (character_id, alterego_id) = (%s, %s) limit 1", [character_id, alter_ego_id])
                    if(not cur.fetchone()):
                        cur.execute("insert into mythra_superheroe_alterego (character_id, alterego_id) values (%s, %s)", [character_id, alter_ego_id])


                for work_occupation_id in work_occupations_id:
                    cur.execute("select * from mythra_superheroe_workocupation where (character_id, workocupation_id) = (%s, %s) limit 1", [character_id, work_occupation_id])
                    if(not cur.fetchone()):
                        cur.execute("insert into mythra_superheroe_workocupation (character_id, workocupation_id) values (%s, %s)", [character_id, work_occupation_id])
    

### Parientes ###

with open('Laboratorio_05_data.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    k = 0
    for row in reader: 
        k+=1
        if k==1:
            continue

        #if k>10:
        #    break

        name = row[1]

        pariente = [m.strip() for m in row[26].split(';')]
        relations_id = []
        for parientes in pariente:
            pariente_ok = re.search("([^(]+)[ ]*\(([^)]+)\)", parientes)
            if pariente_ok:
                
                findOrInsert('mythra_character', pariente_ok.group(1))
                relations_id.append([findOrInsert('mythra_character', pariente_ok.group(1)), findOrInsert('mythra_relation', pariente_ok.group(2))])
            else:
                continue

        cur.execute("select id from mythra_character where name=%s limit 1", [name])
        r = cur.fetchone()
        character_id = None
        if(r):
            character_id = r[0]
        else:
            cur.execute("insert into mythra_character (name) values (%s) returning id", [name])
            character_id = cur.fetchone()[0]



        for relations_id in relations_id:
            cur.execute("select character_id from mythra_superheroe_relation where character_id=%s limit 1", [relations_id[0]])
            g = cur.fetchone()
            rel_id = None
            if(g):
                rel_id = g[0]
            else:
                cur.execute("insert into mythra_superheroe_relation (character_id, relation_id, Superheroe_id) values (%s, %s, %s) returning character_id", [relations_id[0], relations_id[1], character_id])
                rel_id = cur.fetchone()[0]




        

conn.commit()

conn.close()


