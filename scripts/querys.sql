
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

/* insert credentials values */
-- admin
insert into "T_PROFILE" values (
	'0c7ceb44a155db2fd60058e64eb255ch',
	'admin@brita.ai',
	'Brita1234,',
	'2',
	'Victoria Hernández',
	'M',
	false,
	'2023-07-31 19:20:06.548',
	'https://aishlatino.com/wp-content/uploads/2021/11/que-tipo-de-persona-te-gustaria-ser-730x411-SP.jpg',
	''
);