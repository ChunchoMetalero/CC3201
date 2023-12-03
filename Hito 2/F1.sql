
/* ENTIDADES */

CREATE TABLE Temporada ( /* tuki */
    id serial PRIMARY KEY,
    agno INT
);

CREATE TABLE Circuito (/* tuki */
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);

CREATE TABLE Escuderia (/* tuki */
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);

CREATE TABLE Piloto (/* tuki */
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);

CREATE TABLE Pais (/* tuki */
    id serial PRIMARY KEY,
    nombre VARCHAR(255)
);

CREATE TABLE GranPremio (/* tuki */
    id serial PRIMARY KEY,
    nombre VARCHAR(255),
    fecha DATE,
    clima VARCHAR(255)
);


/* RELACIONES */

CREATE TABLE Equipo (/* tuki */
    Es_id bigint not null,
    Pi_id bigint not null,
    PRIMARY KEY (Es_id, Pi_id),
    FOREIGN KEY (Es_id) REFERENCES Escuderia(id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id)
);

CREATE TABLE Piloto_Pais (/* tuki */
    Pi_id bigint not null,
    Pa_id bigint not null,
    PRIMARY KEY (Pi_id, Pa_id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id),
    FOREIGN KEY (Pa_id) REFERENCES Pais(id)
);

CREATE TABLE Temporada_Escuderia (/* tuki */
    Es_id bigint not null,
    T_id bigint not null,
    ptje_acumulado INT,
    es_campeon BOOLEAN,
    PRIMARY KEY (Es_id, T_id),
    FOREIGN KEY (Es_id) REFERENCES Escuderia(id),
    FOREIGN KEY (T_id) REFERENCES Temporada(id)
);

CREATE TABLE Temporada_Piloto (/* tuki */
    T_id bigint not null,
    Pi_id bigint not null,
    ptje_acumulado INT,
    es_campeon BOOLEAN,
    numero_piloto INT,
    PRIMARY KEY (T_id, Pi_id),
    FOREIGN KEY (Pi_id) REFERENCES Piloto(id),
    FOREIGN KEY (T_id) REFERENCES Temporada(id)
);

CREATE TABLE Equipo_GranPremio (
    EqEs_id bigint not null,
    EqPi_id bigint not null,
    Gp_id bigint not null,
    posicion_carrera INT,
    vuelta_rapida_c TIME,
    posicion_qualy INT,
    tiempo_qualy TIME,
    edad_piloto INT,
    PRIMARY KEY (EqEs_id,EqPi_id,Gp_id),
    FOREIGN KEY (EqEs_id,EqPi) REFERENCES Equipo(Es_id, Pi_id),
    FOREIGN KEY (Gp_id) REFERENCES GranPremio(id)


);

CREATE TABLE GranPremio_Circuito ( /* tuki */
    Gp_id bigint not null,
    Cir_id bigint not null,
    PRIMARY KEY (Gp_id,Cir_id),
    FOREIGN KEY (Cir_id) REFERENCES Circuito(id),
    FOREIGN KEY (Gp_id) REFERENCES GranPremio(id)
);

CREATE TABLE Circuito_Pais ( /* tuki */
    Cir_id bigint not null,
    Pa_id bigint not null,
    PRIMARY KEY (Cir_id, Pa_id),
    FOREIGN KEY (Cir_id) REFERENCES Circuito(id),
    FOREIGN KEY (Pa_id) REFERENCES Pais(id)
);