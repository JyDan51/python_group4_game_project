"""Database functions for Sky-Scavenger 2488."""

from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parent
SCHEMA_FILE = PROJECT_ROOT / "create_tables.sql"
REQUIRED_AIRPORT_COLUMNS = {"ident", "name", "latitude_deg", "longitude_deg"}


def load_dotenv():
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def get_config():
    load_dotenv()
    if not os.getenv("DB_USER"):
        raise RuntimeError("DB_USER is not set. Copy .env.example to .env.")

    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "database": os.getenv("DB_NAME", "fligth_game"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD", ""),
    }


def connect():
    config = get_config()
    try:
        import mysql.connector
    except ImportError as error:
        raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from error

    return mysql.connector.connect(**config)


def initialize_database():
    sql_text = SCHEMA_FILE.read_text(encoding="utf-8")
    statements = [part.strip() for part in sql_text.split(";") if part.strip()]

    connection = connect()
    cursor = connection.cursor()
    for statement in statements:
        cursor.execute(statement)
    connection.commit()
    cursor.close()
    connection.close()


def validate_airport_table():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SHOW COLUMNS FROM airport")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    columns = {row[0] for row in rows}
    missing = REQUIRED_AIRPORT_COLUMNS - columns
    if missing:
        raise RuntimeError("Airport table is missing: " + ", ".join(sorted(missing)))


def get_airports(airport_codes):
    placeholders = ", ".join(["%s"] * len(airport_codes))
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT ident, name, latitude_deg, longitude_deg "
        f"FROM airport WHERE ident IN ({placeholders})",
        airport_codes,
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    airports = {}
    for row in rows:
        airports[row["ident"]] = {
            "ident": row["ident"],
            "name": row["name"],
            "latitude": float(row["latitude_deg"]),
            "longitude": float(row["longitude_deg"]),
        }
    return airports


def get_player_by_name(name):
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, name, current_airport_ident, energy, money,
               deliveries_completed, status
        FROM ss_player
        WHERE name = %s
        """,
        (name,),
    )
    player = cursor.fetchone()
    cursor.close()
    connection.close()
    return dict(player) if player else None


def get_player(player_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, name, current_airport_ident, energy, money,
               deliveries_completed, status
        FROM ss_player
        WHERE id = %s
        """,
        (player_id,),
    )
    player = cursor.fetchone()
    cursor.close()
    connection.close()

    if player is None:
        raise RuntimeError("Saved player could not be found.")
    return dict(player)


def create_player(name, start_airport):
    import game_logic

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO ss_player
            (name, current_airport_ident, energy, money, deliveries_completed, status)
        VALUES (%s, %s, %s, %s, 0, 'active')
        """,
        (name, start_airport, game_logic.STARTING_ENERGY, game_logic.STARTING_MONEY),
    )
    connection.commit()
    player_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return get_player(player_id)


def reset_player(player_id, start_airport):
    import game_logic

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE ss_delivery SET status = 'cancelled' "
        "WHERE player_id = %s AND status = 'active'",
        (player_id,),
    )
    cursor.execute(
        """
        UPDATE ss_player
        SET current_airport_ident = %s,
            energy = %s,
            money = %s,
            deliveries_completed = 0,
            status = 'active'
        WHERE id = %s
        """,
        (start_airport, game_logic.STARTING_ENERGY, game_logic.STARTING_MONEY, player_id),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return get_player(player_id)


def save_player(player):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE ss_player
        SET current_airport_ident = %s,
            energy = %s,
            money = %s,
            deliveries_completed = %s,
            status = %s
        WHERE id = %s
        """,
        (
            player["current_airport_ident"],
            player["energy"],
            player["money"],
            player["deliveries_completed"],
            player["status"],
            player["id"],
        ),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_accepted_deliveries(player_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, player_id, origin_ident, destination_ident, reward, status, created_at
        FROM ss_delivery
        WHERE player_id = %s AND status = 'active'
        ORDER BY created_at, id
        """,
        (player_id,),
    )
    deliveries = cursor.fetchall()
    cursor.close()
    connection.close()
    return [dict(delivery) for delivery in deliveries]


def create_delivery(player_id, origin_ident, destination_ident, reward):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO ss_delivery
            (player_id, origin_ident, destination_ident, reward, status)
        VALUES (%s, %s, %s, %s, 'active')
        """,
        (player_id, origin_ident, destination_ident, reward),
    )
    connection.commit()
    cursor.close()
    connection.close()


def complete_deliveries_at_airport(player_id, airport_ident):
    deliveries = get_accepted_deliveries(player_id)
    completed = []
    for delivery in deliveries:
        if delivery["destination_ident"] == airport_ident:
            completed.append(delivery)

    if not completed:
        return []

    connection = connect()
    cursor = connection.cursor()
    for delivery in completed:
        cursor.execute(
            """
            UPDATE ss_delivery
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (delivery["id"],),
        )
    connection.commit()
    cursor.close()
    connection.close()
    return completed
