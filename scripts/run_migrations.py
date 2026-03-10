import os
from alembic import command
from alembic.config import Config

def main():
    # Alembic needs the config file path
    alembic_cfg = Config("alembic.ini")

    # Ensure DATABASE_URL is present when deploying (Render)
    # If not set, Alembic falls back to alembic.ini which can be wrong in deploy.
    if not os.getenv("DATABASE_URL"):
        print("WARNING: DATABASE_URL not set. Using alembic.ini sqlalchemy.url")

    print("Running alembic upgrade head...")
    command.upgrade(alembic_cfg, "head")
    print("Migrations complete.")

if __name__ == "__main__":
    main()