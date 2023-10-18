import psycopg2
import psycopg2.extras
import csv
import re

conn = psycopg2.connect(host="localhost",
    database="anime",
    user="mtoro",
    password="", port="5432")


cur = conn.cursor()



def findOrInsert(table, name):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]


with open('Anime.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue
        #if i>3:
        #    break
        name = row[1]

        episodes = int(row[4].split('.')[0]) if row[4] else None
        studio = row[5]
        
        tags = [m.strip() for m in row[7].split(',')] 
        valid_tags = list(filter(lambda x: len(x)>0, tags))

        voice_actors = [m.strip() for m in row[15].split(',')] 
        voice_actors_ok = list(filter(lambda x: re.match('([^\:]+)\:([^\,]+)', x), voice_actors))
        valid_voice_actors = [[m.split(':')[0].strip(), m.split(':')[1].strip()] for m in voice_actors_ok]


        studio_id = findOrInsert('studio', studio.strip())

        tags_id = []
        for tag in valid_tags:
            tags_id.append(findOrInsert('tag', tag))

        vacs_id = []
        for vac in valid_voice_actors:
            vacs_id.append([findOrInsert('character', vac[0]), findOrInsert('voice_actor', vac[1])])


        cur.execute("select id from anime where name=%s limit 1", [name])
        r = cur.fetchone()
        anime_id = None
        if(r):
            anime_id = r[0]
        else:
            cur.execute("insert into anime (name, episodes) values (%s, %s) returning id", [name, episodes])
            anime_id = cur.fetchone()[0]

        if(anime_id):
            for tag_id in tags_id:
                cur.execute("select * from anime_tag where (anime_id, tag_id) = (%s, %s) limit 1", [anime_id, tag_id])
                if(not cur.fetchone()):
                    cur.execute("insert into anime_tag (anime_id, tag_id) values (%s, %s)", [anime_id, tag_id])
                
            for vac_id in vacs_id:
                cur.execute("select * from anime_voice_actor_character where (anime_id, voice_actor_id, character_id) = (%s, %s, %s)", [anime_id, vac_id[1], vac_id[0]])
                if(not cur.fetchone()):
                    cur.execute("insert into anime_voice_actor_character (anime_id, voice_actor_id, character_id) values (%s, %s, %s)", [anime_id, vac_id[1], vac_id[0]])
                

        
        
        print(anime_id)


        #print(name, episodes, studio, valid_tags, valid_voice_actors)
    conn.commit()
        

conn.close()
