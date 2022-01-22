CREATE TABLE IF NOT EXISTS sv_hotel_in (
  id char(36) NOT NULL,
  hora_creacion time NOT NULL,
  vuelo varchar(128) NOT NULL,
  hora_de_vuelo varchar(9) NOT NULL,
  fecha date NOT NULL,
  nro_habitacion int NOT NULL,
  nro_personas int NOT NULL,
  origen varchar(128) NOT NULL,
  destino varchar(128) NOT NULL,
  PRIMARY KEY (id)
);