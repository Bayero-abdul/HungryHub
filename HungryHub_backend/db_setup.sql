--prepraring mysql server for HungryHub users on our platform
--The name of the database is Hungryhub_db
--It uses this to connect to sqlalchemy  
--DATABASE_URI="mysql://username:password@host:port/database_used"
CREATE DATABASE IF NOT EXISTS Hungryhub_db;
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '$Hungryhub67';
GRANT ALL PRIVILEGES ON Hungryhub_db.* TO 'root'@'localhost';
GRANT SELECT ON performance_schema.* TO 'root'@'localhost';
FLUSH PRIVILEGES;