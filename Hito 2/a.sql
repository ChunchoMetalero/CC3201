/*Temporada(agno: Int) 
Gran Premio (T_agno:Int, nombre: Str, fecha: Date, pais: String , circuito: String, clima: String) 
T_agno REF Temporada(agno) 
Posicion(T_agno:Int, G_nombre: Str, E_nombre: String, P_nombre: String, P_nacionalidad: String, posicion: Int, posicion-carrera: Int, vuelta_rapida_c: Time, posicion_qualy: Int, tiempo_qualy: Time)
T_agno REF Temporada(agno) 
G_nombre REF Gran Premio(nombre)
E_nombre REF Piloto(nombre) 
P_nombre REF Piloto(nombre)
P_nacionalidad REF Piloto(nacionalidad)
Piloto(E_nombre::String, nombre::String, nacionalidad::String, numero: Int, edad: Int)
E_nombre REF Escuderia(nombre) 
Escuderia(nombre:String) 
Participa-P(P_nombre:String, P_nacionalidad:String, E_nombre:String, T_agno: Date, ptje_acumulado: Int, es_campeon:Bool) 
P_nombre REF Piloto(nombre)
P_nacionalidad REF Piloto(nacionalidad)
E_nombre REF Piloto(nombre)
T_agno REF Temporada(agno)        
Participa-E(E_nombre:String, T_agno: Date, ptje_acumulado:Int, es_campeon:Bool) 
E_nombre REF Escuderia(nombre)
T_agno REF Temporada(agno)
*/




CREATE TABLE Temporada (
    agno INT NOT NULL,
    PRIMARY KEY (agno)
);

CREATE TABLE GranPremio (
    id SERIAL PRIMARY KEY,
    T_agno INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    pais VARCHAR(50) NOT NULL,
    circuito VARCHAR(50) NOT NULL,
    clima VARCHAR(50) NOT NULL,
    UNIQUE (nombre, T_agno),  -- Add a unique constraint on name and T_agno
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno)
);

CREATE TABLE Piloto (
    E_nombre VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    nacionalidad VARCHAR(50) NOT NULL,
    numero INT NOT NULL,
    edad INT NOT NULL,
    PRIMARY KEY (E_nombre, nombre, nacionalidad),
    UNIQUE (nombre, nacionalidad),
    FOREIGN KEY (E_nombre) REFERENCES Escuderia(nombre)
);


CREATE TABLE Escuderia (
    nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (nombre)
);


/* 
CREATE TABLE GranPremio (
    id SERIAL PRIMARY KEY,
    T_agno INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    pais VARCHAR(50) NOT NULL,
    circuito VARCHAR(50) NOT NULL,
    clima VARCHAR(50) NOT NULL,
    UNIQUE (id), -- Agrega esta línea para crear una clave única en id
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno)
);
*/


/*
ALTER TABLE GranPremio ADD UNIQUE (nombre);

-- Cambia el tipo de datos de la columna "id" en la tabla "GranPremio" a VARCHAR(50)
ALTER TABLE GranPremio ALTER COLUMN id TYPE VARCHAR(50);

-- Luego, crea la clave foránea en la tabla "Temporada_GranPremio"
CREATE TABLE Temporada_GranPremio (
    T_agno INT NOT NULL,
    G_nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (T_agno, G_nombre),
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno),
    FOREIGN KEY (G_nombre) REFERENCES GranPremio(id)
);*/



/*there is no unique constraint matching given keys for referenced table "granpremio"*/
CREATE TABLE Temporada_GranPremio (
    T_agno INT NOT NULL,
    G_nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (T_agno, G_nombre),
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno),
    FOREIGN KEY (G_nombre) REFERENCES GranPremio(id)   
);



CREATE TABLE GranPremio_Piloto (
    T_agno INT NOT NULL,
    G_nombre VARCHAR(50) NOT NULL,
    E_nombre VARCHAR(50) NOT NULL,
    P_nombre VARCHAR(50) NOT NULL,
    P_nacionalidad VARCHAR(50) NOT NULL,
    posicion INT NOT NULL,
    posicion_carrera INT NOT NULL,
    vuelta_rapida_c TIME NOT NULL,
    posicion_qualy INT NOT NULL,
    tiempo_qualy TIME NOT NULL,
    PRIMARY KEY (T_agno, G_nombre, E_nombre, P_nombre, P_nacionalidad),
    FOREIGN KEY (T_agno, G_nombre) REFERENCES GranPremio(T_agno, nombre),
    FOREIGN KEY (E_nombre, P_nombre, P_nacionalidad) REFERENCES Piloto(E_nombre, nombre, nacionalidad)
);

CREATE TABLE Temporada_Piloto (
    T_agno INT NOT NULL,
    P_nombre VARCHAR(50) NOT NULL,
    P_nacionalidad VARCHAR(50) NOT NULL,
    E_nombre VARCHAR(50) NOT NULL,
    ptje_acumulado INT NOT NULL,
    es_campeon BOOLEAN NOT NULL,
    PRIMARY KEY (T_agno, P_nombre, P_nacionalidad),
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno),
    FOREIGN KEY (P_nombre, P_nacionalidad) REFERENCES Piloto(nombre, nacionalidad),
    FOREIGN KEY (E_nombre) REFERENCES Escuderia(nombre)
);

CREATE TABLE Temporada_Escuderia (
    T_agno INT NOT NULL,
    E_nombre VARCHAR(50) NOT NULL,
    ptje_acumulado INT NOT NULL,
    es_campeon BOOLEAN NOT NULL,
    PRIMARY KEY (T_agno, E_nombre),
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno),
    FOREIGN KEY (E_nombre) REFERENCES Escuderia(nombre)
);


CREATE TABLE Escuderia_Piloto (
    E_nombre VARCHAR(50) NOT NULL,
    P_nombre VARCHAR(50) NOT NULL,
    P_nacionalidad VARCHAR(50) NOT NULL,
    PRIMARY KEY (E_nombre, P_nombre, P_nacionalidad),
    FOREIGN KEY (E_nombre) REFERENCES Escuderia(nombre),
    FOREIGN KEY (P_nombre, P_nacionalidad) REFERENCES Piloto(nombre, nacionalidad)
);

CREATE TABLE Participa_P (
    P_nombre VARCHAR(50) NOT NULL,
    P_nacionalidad VARCHAR(50) NOT NULL,
    E_nombre VARCHAR(50) NOT NULL,
    T_agno INT NOT NULL,
    ptje_acumulado INT NOT NULL,
    es_campeon BOOLEAN NOT NULL,
    PRIMARY KEY (P_nombre, P_nacionalidad, E_nombre, T_agno),
    FOREIGN KEY (P_nombre, P_nacionalidad) REFERENCES Piloto(nombre, nacionalidad),
    FOREIGN KEY (E_nombre) REFERENCES Escuderia(nombre),
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno)
);

CREATE TABLE Participa_E (
    E_nombre VARCHAR(50) NOT NULL,
    T_agno INT NOT NULL,
    ptje_acumulado INT NOT NULL,
    es_campeon BOOLEAN NOT NULL,
    PRIMARY KEY (E_nombre, T_agno),
    FOREIGN KEY (E_nombre) REFERENCES Escuderia(nombre),
    FOREIGN KEY (T_agno) REFERENCES Temporada(agno)
);

