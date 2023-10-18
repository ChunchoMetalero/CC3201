import psycopg2
import psycopg2.extras
import csv
import re

conn = psycopg2.connect (host = "cc3201.dcc.uchile.cl ",
database = "cc3201",
user = "cc3201",
password = "j'<3_cc3201" , port = "5440" )

cur = conn.cursor()

def findOrInsert(table, name):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]

with open('heroes.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        name = row['name']
        if not name:
            name = 'Superhero'
        superhero_id = findOrInsert('characters', name)
        cur.execute("insert into superheroes (character_id, alias, powers) values (%s, %s, %s)", [superhero_id, row['alias'], row['powers']])
        conn.commit()


