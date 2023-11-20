
/*  P1)  */
CREATE TABLE trx_p.Itsuki_estado (
    nombre varchar (255) PRIMARY KEY,
	voto_electoral smallint,
	cierre time,
	num_candidatos smallint
);

INSERT INTO Itsuki_estado SELECT * FROM estado;

CREATE TABLE trx_p.Itsuki_condado (
    nombre varchar (255),
	estado varchar (255),
    PRIMARY KEY (nombre, estado),
    foreign key (estado) references Itsuki_estado (nombre),
	reportado float check (reportado >= 0 and reportado <= 1)
);

INSERT INTO Itsuki_condado SELECT * FROM condado;

CREATE TABLE trx_p.Itsuki_candidato (
    nombre varchar (255) PRIMARY KEY,
	partido varchar (255)
);

INSERT INTO Itsuki_candidato SELECT * FROM candidato;

CREATE TABLE trx_p.Itsuki_votosPorCondado (
    candidato varchar (255),
	condado varchar (255),
	estado varchar (255),
    PRIMARY KEY (candidato, condado, estado),
    votos int DEFAULT 0
);

INSERT INTO Itsuki_votosPorCondado SELECT * FROM votosPorCondado;

/*  P2)  */
Update Itsuki_votosPorCondado
set votos = votosPorCondado1.votos
from votosPorCondado1
where Itsuki_votosPorCondado.candidato = votosPorCondado1.candidato 
and Itsuki_votosPorCondado.condado = votosPorCondado1.condado 
and Itsuki_votosPorCondado.estado = votosPorCondado1.estado;

/*  P3)  */
Update Itsuki_condado
set reportado = condado1.reportado
from condado1
where Itsuki_condado.nombre = condado1.nombre
and Itsuki_condado.estado = condado1.estado;

/*  P4)  */
Begin Transaction;
    Update Itsuki_votosPorCondado
        set votos = votosPorCondado2.votos
        from votosPorCondado2
        where Itsuki_votosPorCondado.candidato = votosPorCondado2.candidato
            and Itsuki_votosPorCondado.condado = votosPorCondado2.condado
            and Itsuki_votosPorCondado.estado = votosPorCondado2.estado;
    Update Itsuki_condado
        set reportado = condado2.reportado
        from condado2
        where Itsuki_condado.nombre = condado2.nombre
            and Itsuki_condado.estado = condado2.estado;
commit;

/*  P5)  */
/* Esto se puede repetir cambiando la hora */
Begin Transaction;
    Update Itsuki_votosPorCondado
        set votos = votosPorCondado9.votos
        from votosPorCondado9
        where Itsuki_votosPorCondado.candidato = votosPorCondado9.candidato
            and Itsuki_votosPorCondado.condado = votosPorCondado9.condado
            and Itsuki_votosPorCondado.estado = votosPorCondado9.estado;
    Update Itsuki_condado
        set reportado = condado9.reportado
        from condado9
        where Itsuki_condado.nombre = condado9.nombre
            and Itsuki_condado.estado = condado9.estado;
commit;

/*  P6)  */
/* Carga de votosPorCondadoX y condadoX */
Begin Transaction;
    Update Itsuki_votosPorCondado
        set votos = votosPorCondadoX.votos
        from votosPorCondadoX
        where Itsuki_votosPorCondado.candidato = votosPorCondadoX.candidato
            and Itsuki_votosPorCondado.condado = votosPorCondadoX.condado
            and Itsuki_votosPorCondado.estado = votosPorCondadoX.estado;
    Update Itsuki_condado
        set reportado = condadoX.reportado
        from condadoX
        where Itsuki_condado.nombre = condadoX.nombre
            and Itsuki_condado.estado = condadoX.estado;
commit;
/*  
    Output: ERROR:  new row for relation "itsuki_condado" violates check constraint "itsuki_condado_reportado_check"
    DETAIL:  Failing row contains (Real County, Texas, 100).
    ROLLBACK 
*/
select nombre,estado, reportado from Itsuki_condado where nombre = 'Real County' and estado = 'Texas';
select candidato, condado, estado, votos from Itsuki_votosPorCondado where condado = 'Real County' and estado = 'Texas' and candidato = 'H. Clinton';

/* Putin no lo logro :D */

