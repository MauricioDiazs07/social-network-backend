/* Guarda los tipos de roles */
CREATE TABLE T_ROLE_PRIVILAGES (
    role_id INT PRIMARY KEY NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);

INSERT INTO T_ROLE_PRIVILAGES VALUES (0, 'USER');
INSERT INTO T_ROLE_PRIVILAGES VALUES (1, 'ADMIN');
INSERT INTO T_ROLE_PRIVILAGES VALUES (2, 'INFLUEX');


/* Guarda toda la informacion de los usuarios (normales, administradores, especiales) */
CREATE TABLE T_USER_DATA (
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE, 
    usr_password VARCHAR(255) NOT NULL,
    gender VARCHAR(255) NOT NULL,
    current_state VARCHAR(255) NOT NULL,
    municipality VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    role_id INT NOT null,
    PRIMARY KEY (email, full_name, usr_password),
    CONSTRAINT roleId 
        FOREIGN KEY (role_id)
        REFERENCES T_ROLE_PRIVILAGES(role_id)
);

INSERT INTO T_USER_DATA VALUES 
('Yair Vazquez', 'yair.vazquez@brita.ai', 'a12345', 'M', 'XXXXX', 'XXXXX', '1998-12-14',0);

INSERT INTO T_USER_DATA VALUES 
('Mauricio', 'mauricio.diaz@brita.ai', 'b12345', 'M', 'XXXXX', 'XXXXX', '1997-05-22',0);

INSERT INTO T_USER_DATA VALUES 
('Brita', 'brita@brita.ai', 'brita', 'X', 'XXXXX', 'XXXXX', '1998-12-14',1);

INSERT INTO T_USER_DATA VALUES 
('Influex', 'influex@influex.com', 'influex', 'X', 'XXXXX', 'XXXXX', '1998-12-14',2);
