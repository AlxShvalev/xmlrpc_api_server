from db.models import create_db_tables
from server import server


def main():
    create_db_tables()
    with server:
        server.serve_forever()


if __name__ == "__main__":
    main()
