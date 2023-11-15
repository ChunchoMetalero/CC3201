/*Character: id, name primary key id
Superheroe: subclase de character name, intelligence, strenght, speed
Alterego: id, name primary key id
WorkOcupation: id, name, id primary key
Relation: id, name, id primary key */

/* P1 */

create table Mythra_Character(
    id serial primary key,
    name varchar(255) not null
);

create table Mythra_Superheroe(
    Character_id bigint not null,
    primary key (Character_id),
    foreign key (Character_id) references Mythra_Character(id),
    name varchar(255) not null,
    intelligence integer not null default 0,
    strenght integer not null default 0,
    speed integer not null default 0
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

/* P3 */

/* a) */
select s.name as Superheroe, count(r.character_id) as Parientes
from Mythra_Superheroe as s
inner join Mythra_Superheroe_Relation as r on s.Character_id = r.Superheroe_id
group by s.name
order by Parientes desc
fetch first 3 rows only;

/* b) */

select c.name as character_name, count(sr.Character_id) as Parientes
from Mythra_Character as c
inner join Mythra_Superheroe_Relation as sr on c.id = sr.Character_id
group by c.name
order by num_relatives desc
fetch first 3 rows only;

/* c) */

select s.name as superhero_name, count(sr.Character_id) as Parientes_superheroes
from Mythra_Superheroe as s
join Mythra_Superheroe_Relation as sr on s.Character_id = sr.Superheroe_id
group by s.name
order by Parientes_superheroes desc
fetch first 5 rows only;

/* d) */

select r.name as relacion, count(sr.Relation_id) as cantidad
from Mythra_Relation as r
join Mythra_Superheroe_Relation as sr on r.id = sr.Relation_id
group by r.name
order by cantidad desc
fetch first 1 row only;

/* e) */
select w.name as trabajo, count(*) as cantidad 
from Mythra_WorkOcupation as w
join Mythra_Superheroe_WorkOcupation sw on w.id = sw.WorkOcupation_id
group by w.name
order by cantidad desc
fetch first 3 row only;