import time
from datetime import datetime
from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_HOST = "db"
DB_PORT = "5432"
DB_NAME = "counter_db"
DB_USER = "user"
DB_PASSWORD = "password"


@app.before_request
def setup():
    init_db()


def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError as exc:
            retries -= 1
            time.sleep(0.5)
    raise ConnectionError("Could not connect to the database.")


def init_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS table_counter (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP NOT NULL,
            client_info TEXT
        );
        """)
        conn.commit()
    conn.close()


@app.route('/')
def hello():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        client_info = request.headers.get('User-Agent', 'Unknown')
        current_time = datetime.now()

        cursor.execute(
            "INSERT INTO table_counter (datetime, client_info) VALUES (%s, %s) RETURNING id;",
            (current_time, client_info)
        )
        conn.commit()

        cursor.execute("SELECT COUNT(*) as count FROM table_counter;")
        count = cursor.fetchone()['count']

    conn.close()
    return f"Hello World! I have been seen {count} times.\n"


@app.route('/view')
def view_records():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM table_counter ORDER BY datetime DESC;")
        records = cursor.fetchall()
    conn.close()
    return render_template('view.html', records=records)


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)
