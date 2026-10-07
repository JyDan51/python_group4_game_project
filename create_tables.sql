USE flight_game;

CREATE TABLE IF NOT EXISTS player (
    name VARCHAR(100) PRIMARY KEY,
    money INT NOT NULL DEFAULT 0,
    energy INT NOT NULL DEFAULT 100,
    airport VARCHAR(10) NOT NULL DEFAULT 'EFHK'
);

CREATE TABLE IF NOT EXISTS contracts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin_airport VARCHAR(10) NOT NULL,
    destination_airport VARCHAR(10) NOT NULL,
    reward INT NOT NULL
);