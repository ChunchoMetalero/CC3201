create table anime(
	id serial primary key,
	name varchar(255) not null,
	episodes integer
);

create table studio(
	id serial primary key,
	name varchar(255) not null
);

create table anime_studio(
	anime_id bigint not null,
	studio_id bigint not null,
	primary key (anime_id, studio_id),
	foreign key (anime_id) references anime(id),
	foreign key (studio_id) references studio(id)
);

create table character(
	id serial primary key,
	name varchar(255) not null
);

create table voice_actor(
	id serial primary key,
	name varchar(255) not null
);

create table tag(
	id serial primary key,
	name varchar(255) not null
);

create table anime_voice_actor_character(
	anime_id bigint not null,
	character_id bigint not null,
	voice_actor_id bigint not null,
	primary key (anime_id, character_id, voice_actor_id),
	foreign key (anime_id) references anime(id),
	foreign key (character_id) references character(id),
	foreign key (voice_actor_id) references voice_actor(id)
);

create table anime_tag(
	anime_id bigint not null,
	tag_id bigint not null,
	primary key (anime_id, tag_id),
	foreign key (anime_id) references anime(id),
	foreign key (tag_id) references tag(id)
);










