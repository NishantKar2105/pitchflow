import re
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from pitchflow.config import settings

engine = create_engine(settings.db_dsn)
RAW_DATA_DIR = Path("data/2022-23")


def load_fixture_data():
    print("Loading fixture.csv")
    file_path = RAW_DATA_DIR / "fixtures.csv"
    if not file_path.exists():
        print(f"Fixtures file not found in {file_path}")
        return

    df = pd.read_csv(file_path)
    df["season"] = "22-23"

    df.to_sql(
        "raw_fixtures", engine, if_exists="replace", index=False, method="multi", chunksize=1000
    )
    print(f"Successfully loaded {len(df)} rows into raw_fixtures.")


def load_gw_data():
    print("Loading gameweek data")

    gw_path = RAW_DATA_DIR / "gws"
    if not gw_path.exists():
        print(f"Gws file not found in {gw_path}")
        return

    with engine.connect() as connection:
        connection.execute(text("TRUNCATE TABLE raw_player_gw;"))
        connection.commit()
    print("Cleared existing data in raw_player_gw for a clean load.")

    total_rows = 0

    def extract_gw_number(file_path):
        match = re.search(r"gw(\d+)", file_path.name, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    for file_path in sorted(gw_path.glob("gw*.csv"), key=extract_gw_number):
        gw = extract_gw_number(file_path)
        df = pd.read_csv(file_path)
        df["season"] = "22-23"
        df.to_sql(
            "raw_player_gw",
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )
        total_rows += len(df)
        print(f"Loaded Gameweek {gw} ")
    print(f"Successfully loaded all gameweeks! Total rows inserted: {total_rows:,}")


if __name__ == "__main__":
    print("Starting Bronze Layer Ingestion for 2022-23...")
    load_fixture_data()
    load_gw_data()
    print("Ingestion complete!")
