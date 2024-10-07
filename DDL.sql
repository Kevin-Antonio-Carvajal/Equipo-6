----------------------------------------------------------------------------------------------
-- OJO: Este archivo solo es una guía para el mapeo de los modelos en el proyecto de django.--
----------------------------------------------------------------------------------------------

--
-- TABLA USUARIO
--
CREATE TABLE `Usuario` (
    `id_usuario` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `nombre` VARCHAR(255) NOT NULL,
    `correo` VARCHAR(255) NOT NULL UNIQUE,
    `username` VARCHAR(64) NOT NULL UNIQUE,
    `password` VARCHAR(64) NOT NULL
);
-- Llave primaria --
ALTER TABLE `Usuario`
ADD CONSTRAINT `pk_Usuario`
PRIMARY KEY (`id_usuario`);

--
-- TABLA OBJETIVO
--
CREATE TABLE `Objetivo` (
    `id_objetivo` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `tipo` ENUM('diario', 'semanal', 'mensual') NOT NULL DEFAULT 'diario' -- diario, mensual, semanal
);
-- Llave primaria --
ALTER TABLE `Objetivo`
ADD CONSTRAINT `pk_Objetivo`
PRIMARY KEY (`id_objetivo`);

--
-- TABLA DIA
--
CREATE TABLE `Dia` (
    `id_objetivo` INT NOT NULL,
    `dia` INT NOT NULL CHECK (`dia` BETWEEN 1 AND 31) -- 1, 2, ... , 31
);
-- Llaves primarias y foraneas
ALTER TABLE `Dia`
ADD CONSTRAINT `pk_Dia`
PRIMARY KEY (`id_objetivo`, `dia`) -- Llave compuesta
FOREIGN KEY (`id_objetivo`) REFERENCES `Objetivo`(`id_objetivo`)
ON DELETE CASCADE
ON UPDATE CASCADE;

--
-- TABLA HABITO
--
CREATE TABLE `Habito` (
    `id_habito` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `id_usuario` INT NOT NULL,
    `id_objetivo` INT NOT NULL,
    `id_categoria` INT NOT NULL,
    `nombre` VARCHAR(64) NOT NULL,    
    `descripcion` VARCHAR(255) DEFAULT NULL,
    `frecuencia` INT NOT NULL DEFAULT 1, -- cuantas veces al dias se realiza
    `titulo_recordatorio` VARCHAR(64) DEFAULT 'No olvides que tienes un objetivo',
    `mensaje_recordatorio` VARCHAR(255) DEFAULT 'Recuerda que cada día se vuelve más fácil, lo dificil es hacerlo todos los días.',
    `notificar` BOOLEAN DEFAULT TRUE, -- si se notifica al usuario o no
    `estatus` BOOLEAN DEFAULT TRUE, -- habilitado o inhabilitado
    `fecha_creacion` TIMESTAMP NOT NULL DEFAULT current_timestamp()
);
-- Llave primaria --
ALTER TABLE `Habito`
ADD CONSTRAINT `pk_Habito`
PRIMARY KEY (`id_habito`);
-- Llave foranea Usuario --
ALTER TABLE `Habito`
ADD CONSTRAINT `fk_HabitoUsuario`
FOREIGN KEY (`id_usuario`)
REFERENCES `Usuario`(`id_usuario`)
ON DELETE CASCADE
ON UPDATE CASCADE;
-- Llave foranea Objetivo --
ALTER TABLE `Habito`
ADD CONSTRAINT `fk_HabitoObjetivo`
FOREIGN KEY (`id_objetivo`)
REFERENCES `Objetivo`(`id_objetivo`)
ON DELETE CASCADE
ON UPDATE CASCADE;
-- Llave foranea Categoria --
ALTER TABLE `Categoria`
ADD CONSTRAINT `fk_HabitoCategoria`
FOREIGN KEY (`id_categoria`)
REFERENCES `Categoria`(`id_categoria`)
ON DELETE CASCADE
ON UPDATE CASCADE;

--
-- TABLA CATEGORIA
--
CREATE TABLE `Categoria` (
    `id_categoria` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `nombre` VARCHAR(64) NOT NULL,
    `descripcion` TEXT DEFAULT NULL,
    `color` CHAR(7) -- Color en hexadecimal
);
-- Llave primaria --
ALTER TABLE `Categoria`
ADD CONSTRAINT `pk_Categoria`
PRIMARY KEY (`id_categoria`);

--
-- TABLA REGISTRO
--
CREATE TABLE `Registro` (
    `id_registro` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `id_habito` INT NOT NULL,
    `estatus` BOOLEAN DEFAULT TRUE, -- completado o incompleto
    `fecha_creacion` TIMESTAMP NOT NULL DEFAULT current_timestamp()
);
-- Llave primaria --
ALTER TABLE `Registro`
ADD CONSTRAINT `pk_Registro`
PRIMARY KEY (`id_registro`);
-- Llave foranea --
ALTER TABLE `Registro`
ADD CONSTRAINT `fk_Registro`
FOREIGN KEY (`id_habito`)
REFERENCES `Habito`(`id_habito`)
ON DELETE CASCADE
ON UPDATE CASCADE;

--
-- TABLA RECORDATORIO
--
CREATE TABLE `Recordatorio` (
    `id_habito` INT NOT NULL,
    `hora` TIME NOT NULL, -- e.g. 16:00 
);
-- Llaves primarias y foraneas
ALTER TABLE `Recordatorio`
ADD CONSTRAINT `pk_Recordatorio`
PRIMARY KEY (`id_habito`, `hora`) -- Llave compuesta
FOREIGN KEY (`id_habito`) REFERENCES `Habito`(`id_habito`)
ON DELETE CASCADE
ON UPDATE CASCADE;

