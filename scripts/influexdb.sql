CREATE TABLE "T_USER" (
    "ID" BIGSERIAL PRIMARY KEY,
    "EMAIL" TEXT UNIQUE NOT NULL,
    "PASSWORD" TEXT NOT NULL,
    "NAME" TEXT NOT NULL,
    "GENDER" VARCHAR(1) NOT NULL,
    "STATE" TEXT NOT NULL,
    "MUNICIPALITY" TEXT NOT NULL,
    "COLONY" TEXT NOT NULL,
    "STREET" TEXT NOT NULL,
    "INT_NUMBER" TEXT,
    "EXT_NUMBER" TEXT NOT NULL,
    "BIRTHDATE" DATE NOT NULL,
    "CURP" VARCHAR(18) UNIQUE NOT NULL,
    "IDENTIFICATION_PHOTO" TEXT UNIQUE NOT NULL,
    "VERIFIED_EMAIL" BOOLEAN NOT NULL DEFAULT FALSE,
    "USER_TYPE" TEXT NOT NULL DEFAULT ('USER'),
    "BLOCKED" BOOLEAN NOT NULL DEFAULT FALSE,
    "CREATION_DATE" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    "PROFILE_PHOTO" TEXT,
    "DESCRIPTION" TEXT,
    "PHONE_NUMBER" TEXT UNIQUE,
    "COORDINATES" TEXT,

    "CITY" TEXT NOT NULL,  
);