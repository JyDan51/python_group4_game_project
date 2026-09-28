CREATE TABLE IF NOT EXISTS ss_player (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    current_airport_ident VARCHAR(40) NOT NULL,
    energy INT NOT NULL,
    money INT NOT NULL,
    deliveries_completed INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_ss_player_status (status),
    INDEX idx_ss_player_airport (current_airport_ident)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ss_delivery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    origin_ident VARCHAR(40) NOT NULL,
    destination_ident VARCHAR(40) NOT NULL,
    reward INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    INDEX idx_ss_delivery_player_status (player_id, status),
    CONSTRAINT fk_ss_delivery_player
        FOREIGN KEY (player_id) REFERENCES ss_player(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
