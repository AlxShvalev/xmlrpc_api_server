from server import server


def main():
    with server:
        server.serve_forever()


if __name__ == "__main__":
    main()
