-- SKY-SCAVENGER 2488
-- N:n tiedosto — Database & SQL Developer
--
-- SINUN VASTUUSI:
-- 1. Luo pelin tarvitsemat omat taulut.
-- 2. Pelaajan tallennuksessa tarvitaan esimerkiksi:
--      nimi
--      raha
--      energia
--      nykyinen lentokenttä
-- 3. Tee tarvittaessa rahtisopimusten taulu.
-- 4. Älä poista flight_game-tietokannan valmista airport-taulua.
-- 5. Varmista, että database.py käyttää samoja taulujen ja sarakkeiden nimiä.
--
-- TODO N: lisää CREATE TABLE -lauseet tähän.

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
);a