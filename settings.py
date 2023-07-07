class Settings:
    DB_NAME: str = "xmlrpc_encrypt"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"

    @property
    def database_url(self) -> str:
        """Get DB connection url."""
        # return "sqlite:///sqlite3.db"
        return (
            "postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
