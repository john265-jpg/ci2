import csv
import sqlite3
import sys
import os


class WorldDatabase:
    """Builds db.sqlite from CSV files on disk and answers Q7."""

    def __init__(self, argv):
        self.db_path = "db.sqlite"
        self.csv_filenames = argv[1:]
        self.conn = None

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)

    def _table_exists(self, table_name):
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,),
        )
        return cursor.fetchone() is not None

    def _import_csv(self, csv_path):
        table_name = os.path.splitext(os.path.basename(csv_path))[0]

        if self._table_exists(table_name):
            print(f"Tabuľka '{table_name}' existuje")
            return

        with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";", quotechar='"')
            header = next(reader)
            rows = [row for row in reader if row]

        columns = ", ".join(f'"{col}" TEXT' for col in header)
        placeholders = ", ".join(["?"] * len(header))

        self.conn.execute(f'CREATE TABLE "{table_name}" ({columns});')
        self.conn.executemany(
            f'INSERT INTO "{table_name}" VALUES ({placeholders});', rows
        )
        self.conn.commit()
        print(f"Vložená '{csv_path}' -> Tabuľka '{table_name}' ({len(rows)} rows).")

    def import_csvs(self):
        for filename in self.csv_filenames:
            csv_path = filename if filename.lower().endswith(".csv") else filename + ".csv"
            self._import_csv(csv_path)

    def answer_query(self):
        question = "Populacia v meste ?"
        sql = (
            'SELECT SUM(CAST("Population" AS INTEGER)) '
            'FROM "city" WHERE "CountryCode" = ?;'
        )
        result = self.conn.execute(sql, ("USA",)).fetchone()
        total = result[0] if result and result[0] is not None else 0
        print(question)
        print(f"Počet duší: {total:,}")

    def run(self):
        self._connect()
        try:
            self.import_csvs()
            self.answer_query()
        finally:
            self.conn.close()


if __name__ == "__main__":
    app = WorldDatabase(sys.argv)
    app.run()
