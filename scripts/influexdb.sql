/* 
-------------------------------------------------------------------------------
    CATALOGUE: 
    Tablas encargadas de guardar parametrias, listas o configuraciones
-------------------------------------------------------------------------------
 */

/* Tabla que guarda los roles que se pueden asignar  */
CREATE TABLE "T_CATALOGUE_ROLE" (
    "ID" INT PRIMARY KEY NOT NULL,
    "DESCRIPTION" VARCHAR(255) NOT NULL
);

/* Tabla que guarda la lista de intereses  */
CREATE TABLE "T_CATALOGUE_INTEREST" (
    "ID" INT PRIMARY KEY NOT NULL,
    "DESCRIPTION" VARCHAR(255) NOT NULL
);


/* 
-------------------------------------------------------------------------------
    PROFILE: 
    Tabla principal que guarda los datos basicos de todos los perfiles
-------------------------------------------------------------------------------
 */

CREATE TABLE "T_PROFILE" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "EMAIL" TEXT UNIQUE NOT NULL,
    "PASSWORD" TEXT NOT NULL,
    "ROLE_ID" INT NOT NULL DEFAULT (1),
    "NAME" TEXT NOT NULL,
    "GENDER" VARCHAR(1) NOT NULL,
    "BLOCKED" BOOLEAN NOT NULL DEFAULT FALSE,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    "PROFILE_PHOTO" TEXT,
    "DESCRIPTION" TEXT,
    CONSTRAINT "ROLE" 
        FOREIGN KEY ("ROLE_ID")
        REFERENCES "T_CATALOGUE_ROLE"("ID")
);


/* 
-------------------------------------------------------------------------------
    USER: 
    Tablas que guardan los datos de los usuarios
-------------------------------------------------------------------------------
 */

 /* Falta foto de perfil */

/* INE */
CREATE TABLE "T_USER_DATA" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" VARCHAR(255) NOT NULL,
    "STATE" TEXT NOT NULL,
    "MUNICIPALITY" TEXT NOT NULL,
    "ADDRESS" TEXT NOT NULL,
    "BIRTHDATE" DATE NOT NULL,
    "CURP" VARCHAR(18) UNIQUE NOT NULL,
    "IDENTIFICATION_PHOTO" TEXT UNIQUE NOT NULL,
    "VERIFIED_EMAIL" BOOLEAN NOT NULL DEFAULT FALSE,
    "PHONE_NUMBER" TEXT UNIQUE,
    "COORDINATES" TEXT ,
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID")
);

CREATE TABLE "T_USER_INTEREST" (
    "ID" BIGSERIAL PRIMARY KEY,
    CONSTRAINT "ROLE" 
        FOREIGN KEY ("ROLE_ID")
        REFERENCES "T_CATALOGUE_ROLE"("ID")
)

/* 
-------------------------------------------------------------------------------
    ADMIN: 
    Tablas que guardan los datos de los administradores
-------------------------------------------------------------------------------
 */

CREATE TABLE "T_ADMIN" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" INT NOT NULL,
);

/* 
-------------------------------------------------------------------------------
    MASTER: 
    Tablas que guardan los datos de los masters
-------------------------------------------------------------------------------
 */

CREATE TABLE "T_MASTER" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" INT NOT NULL,

);

/* 
-------------------------------------------------------------------------------
    SHARE: 
    Tablas que guardan los datos de las insteracciones
-------------------------------------------------------------------------------
 */


 CREATE TABLE "T_SHARE" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" INT NOT NULL,
    "DESCRIPTION" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID")
 )


/* 
-------------------------------------------------------------------------------
    MULTIMEDIA: 
    Tablas que guardan los datos de las insteracciones
-------------------------------------------------------------------------------
 */


 CREATE TABLE "T_MULTIMEDIA" (
    "ID" BIGSERIAL PRIMARY KEY,
    "INTERACTION_ID" INT NOT NULL,
    "INTERACTION_TYPE" VARCHAR(255) NOT NULL,
    "ARCHIVE_URL" VARCHAR(255) NOT NULL,
    "ARCHIVE_TYPE" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
 )


/* 
-------------------------------------------------------------------------------
    INTERACTION: 
    Tablas que guardan los datos de las insteracciones
-------------------------------------------------------------------------------
 */

/* Las historias, reals y post tienen comentarios, por eso se pone */
/* Pero eso quita la posibilidad de usar como llave foranea el ID de la historia, post, etc */
/* El front se debe de encargar de mandar el valor correctamente */



 CREATE TABLE "T_INTERACTION_COMMENT" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" INT NOT NULL,
    "INTERACTION_ID" INT NOT NULL,
    "INTERACTION_TYPE" VARCHAR(255) NOT NULL,
    "DESCRIPTION" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID"),
 )

/* Llave primaria */
 CREATE TABLE "T_INTERACTION_LIKE" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" INT NOT NULL,
    "INTERACTION_ID" INT NOT NULL,
    "INTERACTION_TYPE" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID")
 )