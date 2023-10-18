/*Character: id, name primary key id
Superheroe: subclase de character name, intelligence, strenght, speed
Alterego: id, name primary key id
WorkOcupation: id, name, id primary key
Relation: id, name, id primary key */

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
    Superheroe_id bigint not null,
    Alterego_id bigint not null,
    primary key (Superheroe_id, Alterego_id),
    foreign key (Superheroe_id) references Mythra_Superheroe(Character_id),
    foreign key (Alterego_id) references Mythra_Alterego(id)
);

create table Mythra_Superheroe_WorkOcupation(
    Superheroe_id bigint not null,
    WorkOcupation_id bigint not null,
    primary key (Superheroe_id, WorkOcupation_id),
    foreign key (Superheroe_id) references Mythra_Superheroe(Character_id),
    foreign key (WorkOcupation_id) references Mythra_WorkOcupation(id)
);

create table Mythra_Superheroe_Relation(
    Superheroe_id bigint not null,
    Relation_id bigint not null,
    primary key (Superheroe_id, Relation_id),
    foreign key (Superheroe_id) references Mythra_Superheroe(Character_id),
    foreign key (Relation_id) references Mythra_Relation(id)
);