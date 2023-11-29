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

/* Tabla que guarda la lista de intereses  */
CREATE TABLE "T_CATALOGUE_FEELING" (
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
    "AREA_CODE" VARCHAR(3) NOT NULL
    "PHONE_NUMBER" TEXT UNIQUE NOT NULL,
    "PASSWORD" TEXT NOT NULL,
    "ROLE_ID" INT NOT NULL DEFAULT (1),
    "NAME" TEXT NOT NULL,
    "GENDER" VARCHAR(1) NOT NULL,
    "BLOCKED" BOOLEAN NOT NULL DEFAULT FALSE,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    "PROFILE_PHOTO" TEXT,
    "DESCRIPTION" TEXT,
    "EMAIL" TEXT UNIQUE,
    CONSTRAINT "ROLE" 
        FOREIGN KEY ("ROLE_ID")
        REFERENCES "T_CATALOGUE_ROLE"("ID")
);

ALTER TABLE "T_PROFILE" ADD COLUMN "AREA_CODE" VARCHAR(3) NULL;

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
    "VERIFIED_PHONE" BOOLEAN NOT NULL DEFAULT FALSE,
    "COORDINATES" TEXT,
    "SECTION" VARCHAR(255) NOT NULL,
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID")
);

-- ALTER TABLE "T_USER_DATA" ADD COLUMN "SECTION" VARCHAR(255) NOT NULL;

 CREATE TABLE "T_USER_INTEREST" (
    "PROFILE_ID" VARCHAR(255) NOT NULL,
    "INTEREST_ID" INT NOT NULL,
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID"),
    CONSTRAINT "INTEREST" 
    FOREIGN KEY ("INTEREST_ID")
    REFERENCES "T_CATALOGUE_INTEREST"("ID")
 );

/* 
-------------------------------------------------------------------------------
    ADMIN: 
    Tablas que guardan los datos de los administradores
-------------------------------------------------------------------------------
 */

CREATE TABLE "T_ADMIN" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" INT NOT NULL
);

/* 
-------------------------------------------------------------------------------
    MASTER: 
    Tablas que guardan los datos de los masters
-------------------------------------------------------------------------------
 */

CREATE TABLE "T_MASTER" (
    "ID" BIGSERIAL PRIMARY KEY,
    "MASTER_ID" VARCHAR(255) NOT NULL,
    "ADMIN_ID" VARCHAR(255) NOT NULL
);

/* 
-------------------------------------------------------------------------------
    SHARE: 
    Tablas que guardan los datos de las insteracciones
-------------------------------------------------------------------------------
 */


CREATE TABLE "T_SHARE" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" VARCHAR(255) NOT NULL,
    "DESCRIPTION" VARCHAR(255) NOT NULL,
    "SHARE_TYPE" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID")
 );

  CREATE TABLE "T_SHARE_INTEREST" (
    "SHARE_ID" INT NOT NULL,
    "INTEREST_ID" INT NOT NULL,
    CONSTRAINT "SHARE" 
        FOREIGN KEY ("SHARE_ID")
        REFERENCES "T_SHARE"("ID"),
    CONSTRAINT "INTEREST" 
    FOREIGN KEY ("INTEREST_ID")
    REFERENCES "T_CATALOGUE_INTEREST"("ID")
 );


/* 
-------------------------------------------------------------------------------
    MULTIMEDIA: 
    Tablas que guardan los datos de las insteracciones
-------------------------------------------------------------------------------
 */


CREATE TABLE "T_MULTIMEDIA" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" VARCHAR(255) NOT NULL,
    "SHARE_ID" VARCHAR(255) NOT NULL,
    "SHARE_TYPE" VARCHAR(255) NOT NULL,
    "ARCHIVE_URL" VARCHAR(255) NOT NULL,
    "ARCHIVE_TYPE" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
 );


/* 
-------------------------------------------------------------------------------
    INTERACTION: 
    Tablas que guardan los datos de las insteracciones
-------------------------------------------------------------------------------
 */


 CREATE TABLE "T_INTERACTION_COMMENT" (
    "ID" BIGSERIAL PRIMARY KEY,
    "PROFILE_ID" VARCHAR(255) NOT NULL,
    "SHARE_ID" INT NOT NULL,
    "SHARE_TYPE" VARCHAR(255) NOT NULL,
    "TEXT" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID")
 );

 ALTER TABLE "T_INTERACTION_COMMENT" ADD COLUMN "FEELING_ID" INT ;
 ALTER TABLE "T_INTERACTION_COMMENT" 
 ADD CONSTRAINT "FEELING"
 FOREIGN KEY ("FEELING_ID") 
 REFERENCES "T_CATALOGUE_FEELING"("ID");
 
 ALTER TABLE "T_INTERACTION_COMMENT" ADD COLUMN "FEELING_PERCENTAGE" INT;

 CREATE TABLE "T_INTERACTION_LIKE" (
    "PROFILE_ID" VARCHAR(255) NOT NULL,
    "SHARE_ID" INT NOT NULL,
    "SHARE_TYPE" VARCHAR(255) NOT NULL,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    PRIMARY KEY ("PROFILE_ID","SHARE_ID","SHARE_TYPE"),
    CONSTRAINT "PROFILE" 
        FOREIGN KEY ("PROFILE_ID")
        REFERENCES "T_PROFILE"("ID")
 );



 CREATE TABLE "T_CHAT" (
    "ID" BIGSERIAL PRIMARY KEY,
    "SENDER_ID" VARCHAR(255) NOT NULL,
    "RECEIVER_ID" VARCHAR(255) NOT NULL,
    "TEXT" VARCHAR(255) NOT NULL
 )