import sqlite3
from sqlite3 import Connection


class DataConverter:
    @staticmethod
    def list_to_string(values: list) -> str:
        return "[" + ", ".join("'" + str(e) + "'" for e in values) + "]"


class SQLiteConnectionHandler:
    def __init__(self, db_name: str):
        self.file = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        try:
            self.conn.commit()
        except:
            self.conn.rollback()
            self.conn.close()
            raise Exception("Something went wrong while commiting the changes ")
        finally:
            self.conn.close()


class SqliteORM:
    def __init__(self, db_name):
        self.db_name: str = db_name
        self.connection: Connection

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.db_name)

    def close(self) -> None:
        self.connection.close()

    def rollback(self) -> None:
        self.connection.rollback()

    def try_to_commit_and_close(self):
        try:
            self.connection.commit()
        except:
            self.connection.rollback()
            self.connection.close()
            raise Exception(
                "Something went wrong while running 'try_to_commit_and_close()'"
            )
        finally:
            self.connection.close()

    def create_table(self, table: str) -> None:
        with SQLiteConnectionHandler(self.db_name) as cursor:
            cursor.execute(table)

    def query_all_from_table(self, table: str, *columns: str) -> list:
        with SQLiteConnectionHandler(self.db_name) as cursor:
            cols = ", ".join(columns) or "*"
            cursor.execute(f"SELECT {cols.lower()} FROM {table.lower()}")
            return cursor.fetchall()

    def insert_into(self, table: str, **values):
        pass

    # NOTUSED
    def query_definitions_by_word_id(self, word_id: int) -> list:
        with SQLiteConnectionHandler(self.db_name) as cursor:
            cursor.execute(
                f"""
                SELECT 
                    *                
                FROM definitions
                WHERE definitions.word_id = '{word_id}'
                """
            )
            return cursor.fetchall()

    def query_all_from_table_and_filter(
        self, table: str, *columns: str, **filters: str
    ) -> list:
        filter_str = "WHERE "
        if len(filters) == 1:
            for key, value in filters.items():
                filter_str += f"{key} = '{value}'"
        elif len(filters) > 1:
            for key, value in filters.items():
                filter_str += f"{key} = '{value}'"
                filter_str += " AND "
            filter_str = filter_str[:-5]
        with SQLiteConnectionHandler(self.db_name) as cursor:
            cols = ", ".join(columns) or "*"
            cursor.execute(f"SELECT {cols.lower()} FROM {table.lower()} {filter_str}")
            return cursor.fetchall()

    def insert_many_definitions(self, values: list) -> None:
        cursor = self.connection.cursor()
        cursor.executemany(
            "INSERT INTO definitions VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            values,
        )

    # # NOTUSED
    # def query_examples_by_word_id(self, word_id: int) -> list:
    #     with SQLiteConnectionHandler(self.db_name) as cursor:
    #         cursor.execute(
    #             f"""
    #             SELECT
    #                 words.id AS word_id,
    #                 definitions.id AS def_id,
    #                 examples.id AS ex_id,

    #                 words.word,
    #                 words.cefr,
    #                 words.speaking,
    #                 words.writing,
    #                 words.word_type,
    #                 words.ipa_nam,
    #                 words.ipa_br,

    #                 definitions.definition,
    #                 definitions.cefr AS def_cefr,
    #                 definitions.grammar,
    #                 definitions.def_type,
    #                 definitions.context AS def_context,
    #                 definitions.labels AS def_labels,
    #                 definitions.variants,
    #                 definitions.use,
    #                 definitions.synonyms,

    #                 examples.example,
    #                 examples.context AS ex_context,
    #                 examples.labels AS ex_labels

    #             FROM examples
    #             INNER JOIN words ON examples.word_id = words.id
    #             INNER JOIN definitions ON examples.definition_id = definitions.id
    #             WHERE examples.word_id = '{word_id}'
    #             """
    #         )
    #         return cursor.fetchall()
