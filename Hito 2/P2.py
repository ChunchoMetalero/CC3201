
# Integrantes:
# Patricio Espinoza A.
# Monserrat Montero T.


import psycopg2
import psycopg2.extras
import csv
import re

conn = psycopg2.connect(host ="cc3201.dcc.uchile.cl",
database ="cc3201",
user ="cc3201",
password ="j'<3_cc3201", port ="5440")


cur = conn.cursor()

def findOrInsert(table, name):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]

with open('Laboratorio_05_data.csv') as csvfile:
    reader = csv.reader (csvfile,delimiter=',', quotechar='"')

    # (a) Creación de Superhero
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue
    

    
        ### CHARACTER ####
        id = row[0]
        full_name = row[8]
        superhero_name = row[1]

        if full_name == None or full_name == "Null": 
            full_name = superhero_name

        # Seleccione el id del personaje por nombre en caso de ya exista
        # De lo contrario insertelo y recupere su id
        character_id = findOrInsert('superheroes.KirbyCharacter',full_name.strip())
        
        
        ### SUPERHERO ####

        intelligence = row[2]
        if intelligence =="null":
            intelligence = None
        strength = row[3]
        if strength =="null":
            strength = None
        speed = row[4]
        if speed == "null":
            speed = None

        # Seleccione el id del superh´eroe dado el id del personaje del punto anterior. En caso de no existir, crealo.
        cur.execute("select Character_id from superheroes.KirbySuperhero where Character_id=%s limit 1", [character_id])
        r = cur.fetchone()
        superhero_id = None
        if(r):
            superhero_id = r[0]
        else:
            cur.execute("insert into superheroes.KirbySuperhero (Character_id,name, intelligence, strength, speed) values (%s, %s,%s, %s, %s) returning Character_id", [character_id,superhero_name, intelligence,strength,speed])
            superhero_id = cur.fetchone()[0]

        #### ALTEREGO ####
        
        ## Para cada alter ego (asuma que estan separados por “,” o “;”)
            # Elimine espacios blancos al comienzo y al final y comillas dobles => m.strip(' " ")

        
        
        alteregos = [m.strip() for m in re.split('[,;]', row[9])]
        

        valid_alteregos = list(filter(lambda x: len(x)>0, alteregos))
        # Busque si ya existe el alter ego para ese superheroe. Si no existe, insertelo.
        alteregos_id = []
        for alterego in valid_alteregos:
            alteregos_id.append(findOrInsert('superheroes.KirbyAlterego',alterego))
        

        #### WORKOCUPATION #####
        # Para cada ocupacion/oficio (asuma que estan separadas por “,” o “;”)
            #  Elimine espacios blancos al comienzo y al final, y comillas dobles.
        ocupaciones = [m.strip(' " ') for m in row[23].split(',;')]

        # B. Seleccione el id de la ocupacion dado el nombre de esta.

        ocupaciones_id = []
        for ocupacion in ocupaciones:
            ocupaciones_id.append(findOrInsert('superheroes.KirbyWorkOcupation',ocupacion))
        
        #Relacion de tablas
        if (superhero_id):
            for ocupacion_id in ocupaciones_id:
                cur.execute("select * from superheroes.KirbySuperheroe_WorkOcupation where (Character_id, WorkOcupation_id) = (%s, %s) limit 1", [superhero_id, ocupacion_id])
                if (not cur.fetchone()):
                    cur.execute("insert into superheroes.KirbySuperheroe_WorkOcupation (Character_id, WorkOcupation_id) values (%s, %s)", [superhero_id, ocupacion_id])
            for alterego_id in alteregos_id:    
                cur.execute("select * from superheroes.KirbySuperheroe_Alterego where (Character_id, Alterego_id) = (%s, %s) limit 1", [superhero_id, alterego_id])
                if (not cur.fetchone()):
                    cur.execute("insert into superheroes.KirbySuperheroe_Alterego (Character_id, Alterego_id) values (%s, %s)", [superhero_id, alterego_id])

    
    
    # II) Creacion de parientes    
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue
        # Seleccione el id del personaje (ya deber´ıa existir seg´un lo de arriba)
        chr_name =  row[1]
        cur.execute("select superheroes.KirbyCharacter from character where name = %s",[chr_name])
        chr_id = cur.fetchone()[0]
        
        parientes = [m.strip(' " ') for m in row[26].split(',;')] # Nombres
        # Para validar un pariente y separar el nombre de su parentesco
        m = re.search("([ˆ(]+)[ ]*\(([ˆ)]+)\)", parientes)
        if (m!=None):
            relative_names = m.group(1)
            relative_relations = m.group(2)

        relaciones_id = []
        for relative_relation in relative_relations:
            relaciones_id.append(findOrInsert('superheroes.KirbyRelation',relative_relation))
        
        i = 0
        for relative_name in relative_names:
            cur.execute("select superheroes.KirbyCharacter from character where name = %s",[relative_name])
            r = cur.fetchone()
            cur.execute("select superheroes.KirbySuperhero from superhero where name = %s",[relative_name])
            s = cur.fetchone()
            if (r or s):
                if (r):
                    pariente_id = r[0]
                else:
                    pariente_id = s[0]
            else: 
                cur.execute("insert into superheroes.KirbyCharacter (name) values (%s) returning id", [relative_name])
                pariente_id = cur.fetchone()[0]
            relacion_id = relaciones_id[i]
            cur.execute("select * from superheroes.KirbyCharacter_Relation_Superheroe where (character_id, pariente_id, relation_id) = (%s, %s,%s) limit 1", [chr_id, pariente_id,relacion_id])
            if (not cur.fetchone()):
                cur.execute("insert into superheroes.KirbyCharacter_Relation_Superheroe (character_id, pariente_id, relation_id) values (%s, %s,%s)", [chr_id,pariente_id,relacion_id])

        #select * from character_superhero_relation where 
        
        # Obtenga el id del personaje correspondiente al pariente, ya sea por el nombre de superheroe o de personaje. Si no encuentra al personaje, cree uno nuevo
        # Busque si existe la relaci´on de parentesco. Si no existe, cree una nueva


        # select personaje_id from character_relation where relation.name = '-' 

    #print(character, superheroe, relation, WorkOcupattion, Alterego)
    conn.commit()
        

conn.close()
