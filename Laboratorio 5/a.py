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


""""
create table Mythra_Character(
    id serial primary key,
    name varchar(255) not null
);

create table Mythra_Superheroe(
    Character_id bigint not null,
    primary key (Character_id),
    foreign key (Character_id) references Mythra_Character(id),
    name varchar(255) not null,
    intelligence integer not null,
    strenght integer not null,
    speed integer not null
);

create table Mythra_Alterego(
    id serial primary key,
    name varchar(255) not null
);

create table Mythra_WorkOcupation(
    id serial primary key,
    name varchar(255) not null
);

create table Mythra_Relation(
    id serial primary key,
    name varchar(255) not null
);

create table Mythra_Superheroe_Alterego(
    Character_id bigint not null,
    Alterego_id bigint not null,
    primary key (Character_id, Alterego_id),
    foreign key (Character_id) references Mythra_Character(id),
    foreign key (Alterego_id) references Mythra_Alterego(id)
);

create table Mythra_Superheroe_WorkOcupation(
    Character_id bigint not null,
    WorkOcupation_id bigint not null,
    primary key (Character_id, WorkOcupation_id),
    foreign key (Character_id) references Mythra_Character(id),
    foreign key (WorkOcupation_id) references Mythra_WorkOcupation(id)
);

create table Mythra_Superheroe_Relation(
    Character_id bigint not null,
    Superheroe_id bigint not null,
    Relation_id bigint not null,
    primary key (Character_id, Relation_id, Superheroe_id),
    foreign key (Character_id) references Mythra_Character(id),
    foreign key (Relation_id) references Mythra_Relation(id),
    foreign key (Superheroe_id) references Mythra_Superheroe(Character_id)
);
"""



import csv
import psycopg2

# Conectarse a la base de datos
conn = psycopg2.connect(host="cc3201.dcc.uchile.cl", database="cc3201", user="cc3201", password="j'<3_cc3201", port="5440")
cur = conn.cursor()

# Leer el archivo CSV
with open('Laboratorio_05_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Obtener el nombre del personaje
        character_name = row['name'].strip()
        if not character_name:
            character_name = row['hero_names'].strip()
        if not character_name:
            continue

        # Buscar el id del personaje en la tabla Mythra_Character
        cur.execute("SELECT id FROM Mythra_Character WHERE name = %s", (character_name,))
        character_id = cur.fetchone()
        if character_id:
            character_id = character_id[0]
        else:
            # Insertar el personaje en la tabla Mythra_Character
            cur.execute("INSERT INTO Mythra_Character (name) VALUES (%s) RETURNING id", (character_name,))
            character_id = cur.fetchone()[0]

        # Buscar el id del superhéroe en la tabla Mythra_Superheroe
        cur.execute("SELECT Character_id FROM Mythra_Superheroe WHERE Character_id = %s", (character_id,))
        superhero_id = cur.fetchone()
        if superhero_id:
            superhero_id = superhero_id[0]
        else:
            # Insertar el superhéroe en la tabla Mythra_Superheroe
            cur.execute("INSERT INTO Mythra_Superheroe (Character_id, name, intelligence, strenght, speed) VALUES (%s, %s, %s, %s, %s) RETURNING Character_id", (character_id, row['hero_names'], row['intelligence'], row['strength'], row['speed']))
            superhero_id = cur.fetchone()[0]

        # Procesar los alter egos
        alter_egos = re.split(',|;', row['alter_egos'])
        for alter_ego in alter_egos:
            alter_ego = alter_ego.strip().strip('"')
            if not alter_ego:
                continue

            # Buscar el alter ego en la tabla Mythra_Alterego
            cur.execute("SELECT id FROM Mythra_Alterego WHERE name = %s AND id IN (SELECT Alterego_id FROM Mythra_Superheroe_Alterego WHERE Character_id = %s)", (alter_ego, superhero_id))
            alter_ego_id = cur.fetchone()
            if alter_ego_id:
                alter_ego_id = alter_ego_id[0]
            else:
                # Insertar el alter ego en la tabla Mythra_Alterego
                cur.execute("INSERT INTO Mythra_Alterego (name) VALUES (%s) RETURNING id", (alter_ego,))
                alter_ego_id = cur.fetchone()[0]

                # Insertar el registro en la tabla intermedia Mythra_Superheroe_Alterego
                cur.execute("INSERT INTO Mythra_Superheroe_Alterego (Character_id, Alterego_id) VALUES (%s, %s)", (character_id, alter_ego_id))

        # Procesar las ocupaciones/oficios
        occupations = re.split(',|;', row['occupation'])
        for occupation in occupations:
            occupation = occupation.strip().strip('"')
            if not occupation:
                continue

            # Buscar el id de la ocupación en la tabla Mythra_WorkOcupation
            cur.execute("SELECT id FROM Mythra_WorkOcupation WHERE name = %s", (occupation,))
            occupation_id = cur.fetchone()
            if occupation_id:
                occupation_id = occupation_id[0]
            else:
                # Insertar la ocupación en la tabla Mythra_WorkOcupation
                cur.execute("INSERT INTO Mythra_WorkOcupation (name) VALUES (%s) RETURNING id", (occupation,))
                occupation_id = cur.fetchone()[0]

            # Buscar si ya existe un registro en la tabla intermedia Mythra_Superheroe_WorkOcupation
            cur.execute("SELECT * FROM Mythra_Superheroe_WorkOcupation WHERE Character_id = %s AND WorkOcupation_id = %s", (character_id, occupation_id))
            if not cur.fetchone():
                # Insertar el registro en la tabla intermedia Mythra_Superheroe_WorkOcupation
                cur.execute("INSERT INTO Mythra_Superheroe_WorkOcupation (Character_id, WorkOcupation_id) VALUES (%s, %s)", (character_id, occupation_id))

# Guardar los cambios y cerrar la conexión
conn.commit()
cur.close()
conn.close()
