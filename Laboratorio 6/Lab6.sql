/* P1 */

/* a) */

select * from transparencia
where transparencia.apellido_p = 'Valdivia'
;

/* b) */

select nombre, nota
from nota.cc3201
where nombre = 'Valdivia Girardi, Juan Ignacio'
;

/* c) */

update nota.cc3201
set nota = 7
where nombre = 'Valdivia Girardi, Juan Ignacio'
;

/* retorna ERROR:  permission denied for table cc3201 */

/* d) */

SELECT table_name, table_schema FROM information_schema.tables;

SELECT column_name, data_type FROM information_schema.columns
WHERE table_name='cc3201' AND table_schema='nota';
 
/* P2 */

/* a) */
'; SELECT table_name, table_schema FROM information_schema.tables;

/* b) */
'; SELECT column_name, data_type FROM information_schema.columns
WHERE table_name='cc3201' AND table_schema='nota'; --


/* c) */
'; select nombre , nota
from nota.cc3201
where nombre = 'Valdivia Girardi, Juan Ignacio';--

/* d) */
'; update nota.cc3201 set nota = 7.0 where nombre = 'Valdivia Girardi, Juan Ignacio'; --

/* e) */
'; update comentario.cc3201 set comentario = 'Im feeling lonely (lonely)
Oh, I wish Id find a lover that could hold me (hold me)
Now Im crying in my room
So skeptical of love (say what you say, but I want it more)
But still I want it more, more, more' where nombre = 'Valdivia Girardi, Juan Ignacio';--

/* f) */
/*Solucion:*/ cur.execute("SELECT nombres, apellido_p, apellido_m, mes, anho, total FROM uchile.transparencia WHERE apellido_p=%s ORDER BY total DESC LIMIT 250", (input,))
/* reemplazando la linea 30: cur.execute("SELECT nombres, apellido_p, apellido_m, mes, anho, total FROM uchile.transparencia WHERE apellido_p='"+input+"' ORDER BY total DESC LIMIT 250")*/