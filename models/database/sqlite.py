import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            facultet varchar(255),
            wand varchar(255),
            
            PRIMARY KEY (id)
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, Name: str):
        sql = """
        INSERT INTO Users (id, Name) 
        VALUES (?, ?)
      
        """
        self.execute(sql, parameters=(id, Name), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def count_users_by_facultet(self):
        sql = """
        SELECT facultet, COUNT(*) 
        FROM Users 
        WHERE facultet IS NOT NULL
        GROUP BY facultet;
        """
        return self.execute(sql, fetchall=True)   
    def update_user_facultet(self, id: int, facultet: str):
        sql = """
        UPDATE Users 
        SET facultet = ? 
        WHERE id = ?;
        """
        self.execute(sql, parameters=(facultet, id), commit=True)
    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def count_facultet_members(self, facultet: str):
        sql = """
        SELECT COUNT(*) 
        FROM Users 
        WHERE facultet = ?;
        """
        return self.execute(sql, parameters=(facultet,), fetchone=True)[0]

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")