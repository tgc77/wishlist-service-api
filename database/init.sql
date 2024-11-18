CREATE DATABASE IF NOT EXISTS luizalabs_db;

CREATE USER IF NOT EXISTS 'api.admin'@'%' IDENTIFIED BY 'Api.admin#2024';

GRANT ALL PRIVILEGES ON *.* TO 'api.admin'@'%';

FLUSH PRIVILEGES;

USE luizalabs_db;

CREATE TABLE IF NOT EXISTS tb_api_client (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(50) NOT NULL,
   	name VARCHAR(50) NOT NULL,
   	PRIMARY KEY (id),
   	CONSTRAINT UNIQUE (email),
   	INDEX (email)
);

CREATE TABLE IF NOT EXISTS tb_api_product (
	id CHAR(32) NOT NULL,
	title VARCHAR(50) NOT NULL,
	brand VARCHAR(50) NOT NULL,
	price DECIMAL(6, 2) NOT NULL,
	image VARCHAR(150),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tb_api_client_favorite_products_list (
	id INT NOT NULL AUTO_INCREMENT,
	client_id INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (client_id) REFERENCES tb_api_client(id)
		ON DELETE CASCADE,
	CONSTRAINT UNIQUE (client_id) 
);

CREATE TABLE IF NOT EXISTS tb_api_client_favorite_products (
	id INT NOT NULL AUTO_INCREMENT,
	favorite_products_list_id INT NOT NULL,
	product_id CHAR(32) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (favorite_products_list_id) REFERENCES tb_api_client_favorite_products_list(id)
		ON DELETE CASCADE,
	FOREIGN KEY (product_id) REFERENCES tb_api_product(id)
		ON DELETE CASCADE,
	CONSTRAINT UNIQUE (favorite_products_list_id, product_id)
);

CREATE TABLE IF NOT EXISTS `tb_api_access_credentials` (
	`id` int NOT NULL AUTO_INCREMENT,
  	`client_id` int NOT NULL,
  	`email` varchar(50) NOT NULL,
  	`username` varchar(30) NOT NULL,
  	`active` tinyint(1) NOT NULL,
  	`scope` varchar(10) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	PRIMARY KEY (`id`),
  	UNIQUE KEY `ix_tb_api_access_credentials_username` (`username`),
  	UNIQUE KEY `ix_tb_api_access_credentials_email` (`email`),
  	KEY `ix_tb_api_access_credentials_id` (`id`),
  	KEY `ix_tb_api_access_credentials_client_id` (`client_id`),
  	CONSTRAINT `tb_api_access_credentials_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `tb_api_client` (`id`),
  	CONSTRAINT `tb_api_access_credentials_ibfk_2` FOREIGN KEY (`email`) REFERENCES `tb_api_client` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Clients
INSERT INTO tb_api_client (email, name) VALUES ('api.admin@gmail.com', 'API Admin');
INSERT INTO tb_api_client (email, name) VALUES ('api.client@gmail.com', 'API Client');

INSERT INTO tb_api_access_credentials (client_id, email, username, active, scope, password)
VALUES 
	(1, 'api.admin@gmail.com', 'api.admin', 1, 'admin', '$2b$12$i/xV7x3xop942U7Wulya1OQ11wFWYThIPekthQ67e6HO0aXzGuGOO'),
	(2, 'api.client@gmail.com', 'api.client', 1, 'client', '$2b$12$KSYM4/w4dQscZXbMv9Av.OThVte8DySKF7JwI79BJvLuSl9B2HqbG')