from typing import Union

import configs.config as config
from src.core.user import User
from src.utils.sqlite_orm import SQLiteConnectionHandler, SqliteORM

USER_TABLE = """CREATE TABLE IF NOT EXISTS [User] (
        id INTEGER PRIMARY KEY UNIQUE,
        id_str TEXT NOT NULL UNIQUE,
        name TEXT,
        screen_name TEXT NOT NULL,
        location TEXT,
        url TEXT,
        description TEXT,
        protected INTEGER,
        verified INTEGER,
        followers_count INTEGER,
        friends_count INTEGER,
        listed_count INTEGER,
        favourites_count INTEGER,
        statuses_count INTEGER,
        created_at TEXT,
        profile_banner_url TEXT,
        profile_image_url_https TEXT,
        default_profile INTEGER,
        default_profile_image INTEGER,
        first_scrape TEXT,
        last_update TEXT, 
        suspended INTEGER
    )
"""


class UserSqlite:
    def __init__(self, db_name: str):
        self.db_name = config.DB_FOLDER + db_name
        self.sqlite = SqliteORM(self.db_name)
        self._create_user_table(USER_TABLE)

    def _create_user_table(self, table) -> None:
        self.sqlite.create_table(table)

    def save(self, user: User) -> bool:
        self._insert_user(user)
        return True

    def does_this_user_exist(self, user: User) -> bool:
        conditions = bool(self.query_user_by_id(user.url))
        return conditions

    def query_user_by_id(self, id: str) -> tuple:
        with SQLiteConnectionHandler(self.db_name) as cursor:
            cursor.execute(f"SELECT * FROM [User] WHERE [id] = '{id}'")
            return cursor.fetchone()

    # TODO Criar método para dar update.
    def _insert_user(self, user) -> Union[int, None]:

        id = int(user.id)
        id_str = str(user.id_str)
        name = str(user.name)
        screen_name = str(user.screen_name)
        location = str(user.location)
        url = str(user.url)
        description = str(user.description)
        protected = int(bool(user.protected))
        verified = int(bool(user.verified))
        followers_count = int(user.followers_count)
        friends_count = int(user.friends_count)
        listed_count = int(user.listed_count)
        favourites_count = int(user.favourites_count)
        statuses_count = int(user.statuses_count)
        created_at = str(user.created_at)
        profile_banner_url = str(user.profile_banner_url)
        profile_image_url_https = str(user.profile_image_url_https)
        default_profile = int(bool(user.default_profile))
        default_profile_image = int(bool(user.default_profile_image))
        first_scrape = str(user.first_scrape)
        last_update = str(user.last_update)
        suspended = int(bool(user.suspended))

        with SQLiteConnectionHandler(self.db_name) as cursor:

            cursor.execute(
                """INSERT INTO [User] (
                    id,
                    id_str,
                    name,
                    screen_name,
                    location,
                    url,
                    description,
                    protected,
                    verified,
                    followers_count,
                    friends_count,
                    listed_count,
                    favourites_count,
                    statuses_count,
                    created_at,
                    profile_banner_url,
                    profile_image_url_https,
                    default_profile,
                    default_profile_image,
                    first_scrape,
                    last_update,
                    suspended
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    id,
                    id_str,
                    name,
                    screen_name,
                    location,
                    url,
                    description,
                    protected,
                    verified,
                    followers_count,
                    friends_count,
                    listed_count,
                    favourites_count,
                    statuses_count,
                    created_at,
                    profile_banner_url,
                    profile_image_url_https,
                    default_profile,
                    default_profile_image,
                    first_scrape,
                    last_update,
                    suspended,
                ),
            )
            return cursor.lastrowid
