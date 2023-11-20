
/* ENTIDADES */

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


/* RELACIONES */

CREATE TABLE Equipo (
    Es_id bigint not null,
    Pi_id bigint not null,
    PRIMARY KEY (Es_id, Pi_id),
    FOREIGN KEY (Es_id) REFERENCES Escuderia(id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id)
);

CREATE TABLE GranPremio (
    T_id bigint not null,
    EqE_id bigint not null,
    EqP_id bigint not null,
    Cir_id bigint not null,
    nombre VARCHAR(255),
    fecha DATE,
    clima VARCHAR(255),
    posicion_carrera INT,
    vuelta_rapida_c TIME,
    posicion_qualy INT,
    tiempo_qualy TIME,
    edad_piloto INT,
    PRIMARY KEY (T_id, EqE_id, EqP_id),
    FOREIGN KEY (T_id) REFERENCES Temporada(id),
    FOREIGN KEY (EqE_id,EqP_id) REFERENCES Equipo(Es_id,Pi_id),
    FOREIGN KEY (Cir_id) REFERENCES Circuito(id)
);

CREATE TABLE Nacionalidad (
    Pi_id bigint not null,
    Pa_id bigint not null,
    PRIMARY KEY (Pi_id, Pa_id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id),
    FOREIGN KEY (Pa_id) REFERENCES Pais(id)
);

CREATE TABLE EstaEn (
    Cir_id bigint not null,
    Pa_id bigint not null,
    PRIMARY KEY (Cir_id, Pa_id),
    FOREIGN KEY (Cir_id) REFERENCES Circuito(id),
    FOREIGN KEY (Pa_id) REFERENCES Pais(id)
);

CREATE TABLE Ch_Constructores (
    Es_id bigint not null,
    T_id bigint not null,
    ptje_acumulado INT,
    es_campeon BOOLEAN,
    PRIMARY KEY (Es_id, T_id),
    FOREIGN KEY (Es_id) REFERENCES Escuderia(id),
    FOREIGN KEY (T_id) REFERENCES Temporada(id)
);

CREATE TABLE Ch_Pilotos (
    T_id bigint not null,
    Pi_id bigint not null,
    ptje_acumulado INT,
    es_campeon BOOLEAN,
    numero_piloto INT,
    PRIMARY KEY (T_id, Pi_id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id),
    FOREIGN KEY (T_id) REFERENCES Temporada(id)
);