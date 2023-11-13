
INSERT INTO "T_CATALOGUE_ROLE" VALUES (1, 'USER');
INSERT INTO "T_CATALOGUE_ROLE" VALUES (2, 'ADMIN');
INSERT INTO "T_CATALOGUE_ROLE" VALUES (3, 'MASTER');

/* queries to poblate the interests table*/
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (1, 'Ciencia y tecnología');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (2, 'Programas sociales');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (3, 'Deportes');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (4, 'Cultura');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (5, 'Medio ambiente');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (6, 'Economía');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (7, 'Seguridad');

INSERT INTO "T_CATALOGUE_FEELING" VALUES (1, 'Positivo');
INSERT INTO "T_CATALOGUE_FEELING" VALUES (2, 'Negativo');
INSERT INTO "T_CATALOGUE_FEELING" VALUES (3, 'Agresivo');

/* insert credentials values */
-- admin
insert into "T_PROFILE" values (
	'0c7ceb44a155db2fd60058e64eb255ch',
	'5555555555',
	'Brita1234,',
	2,
	'Victoria Hernández',
	'M',
	false,
	'2023-07-31 19:20:06.548',
	'https://aishlatino.com/wp-content/uploads/2021/11/que-tipo-de-persona-te-gustaria-ser-730x411-SP.jpg',
	'',
	'admin@brita.ai'
);

-- master
insert into "T_PROFILE" values (
	'0c7ceb44a155db2fd60058e64eb255as',
	'4444444444',
	'Brita1234,',
	3,
	'Cuenta master',
	'M',
	false,
	'2023-10-10 19:20:06.548',
	'https://img.freepik.com/foto-gratis/retrato-hermoso-mujer-joven-posicion-pared-gris_231208-10760.jpg',
	'',
	'master@brita.ai'
);