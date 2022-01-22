CREATE TABLE IF NOT EXISTS transport_comments_out (
  id char(36) PRIMARY KEY,
  comment varchar(1024) DEFAULT NULL,
  FOREIGN KEY (id) REFERENCES sv_hotel_out (id)
);