
INSERT INTO "T_CATALOGUE_ROLE" VALUES (1, 'USER');
INSERT INTO "T_CATALOGUE_ROLE" VALUES (2, 'ADMIN');
INSERT INTO "T_CATALOGUE_ROLE" VALUES (3, 'MASTER');

/* queries to poblate the interests table*/
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (1, 'Tecnología');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (2, 'Inteligencia artificial');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (3, 'Literatura');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (4, 'Lingüística');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (5, 'Juegos');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (6, 'Animales');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (7, 'Astronomía');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (8, 'Moda');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (9, 'Economía');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (10, 'Entretenimiento');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (11, 'Cultura');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (12, 'Hogar');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (13, 'Vida cotidiana');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (14, 'Ciencia y educación');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (15, 'Comedia');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (16, 'Comida y bebidas');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (17, 'Vehículos');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (18, 'Anime');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (19, 'Música');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (20, 'Animales');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (21, 'Deportes');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (22, 'Salud');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (23, 'Belleza');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (24, 'Familia');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (25, 'Arte');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (26, 'Motivación');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (27, 'Viajes');
INSERT INTO "T_CATALOGUE_INTEREST" VALUES (28, 'DIY');

/* insert credentials values */
-- user
insert into "T_PROFILE" values (
	'0c7ceb44a155db2fd60058e64eb255mk',
	'user@brita.ai',
	'Brita1234,',
	'1',
	'Alejandro Vázquez',
	'H',
	false,
	'2023-07-31 19:20:06.548',
	'https://cdn-icons-png.flaticon.com/512/3577/3577429.png',
	''
);

insert into "T_USER_DATA" values (
	1,
	'0c7ceb44a155db2fd60058e64eb255mk',
	'TAMAULIPAS',
	'NUEVO LAREDO',
	'C6 DE NOVIEMBRE 1920 COL CAMPESTRE 88278 NUEVO LAREDO, TAMPS.',
	'1998-07-08',
	'DISM980708MTSPRR08',
	'https://cdn-icons-png.flaticon.com/512/3577/3577429.png',
	false,
	'',
	''
);

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

insert into "T_USER_DATA" values (
	2,
	'0c7ceb44a155db2fd60058e64eb255ch',
	'TAMAULIPAS',
	'NUEVO LAREDO',
	'C6 DE NOVIEMBRE 1920 COL CAMPESTRE 88278 NUEVO LAREDO, TAMPS.',
	'1999-05-08',
	'DIMS990701MTSPRR05',
	'https://aishlatino.com/wp-content/uploads/2021/11/que-tipo-de-persona-te-gustaria-ser-730x411-SP.jpg',
	false,
	'',
	''
);