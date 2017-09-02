# coding=utf-8
"""Economist Covers database"""

import os
import sqlite3


class Database(object):
    """Database for storing Economist Covers data"""

    def execute_sql(self, statement, params=None):
        """
        Executes SQL on the database.
        @param str statement: the main body of the SQL statement to execute
        @param (str,) params: optional SQL parameters
        """
        """Execute SQL statement, with optional parameters."""
        action = statement.split(' ', 1)[0]
        database_connection = sqlite3.connect(self.name)
        with database_connection:
            database_cursor = database_connection.cursor()
            if params:
                database_cursor.execute(statement, params)
            else:
                database_cursor.execute(statement)
            database_connection.commit()
            if action == "SELECT":
                return database_cursor.fetchall()
            else:
                return True

    def __init__(self, name):
        self.name = os.path.expanduser(name)
        if not os.path.exists(self.name):
            self.execute_sql("CREATE TABLE covers ("
                             "url TEXT UNIQUE, "
                             "cover BLOB, "
                             "issue_date TEXT)")

    def add_cover(self, cover_url, cover_image, issue_date):
        """
        Add a cover image (and its associated URL / date) to the database.
        :param str cover_url: the URL to the cover image
        :param str cover_image: cover image
        :param str issue_date: date of magazine on which the cover was featured
        """
        self.execute_sql("INSERT INTO covers (url, cover, issue_date) VALUES (?, ?, ?)",
                         (cover_url, cover_image, issue_date))

    def get_covers(self):
        """Returns all covers the database knows about."""
        return self.execute_sql("SELECT cover, issue_date FROM covers ORDER BY issue_date")
