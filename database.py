import psycopg2
import config

class db:
    def __init__(self):
        self.base = psycopg2.connect(
            host=config.HOST,
            database=config.DATABASE_NAME,
            password=config.PASSWORD,
            user=config.USER,
            port=config.PORT
        )
        print("Connected!")
        self.c = self.base.cursor()

    def commit(self):
        self.base.commit()
        self.base.close()

    def create_table(self, table_name, values):
        self.c.execute(
            f"create table if not exists {str(table_name)} ({values})"
        )
        print(f"Created {table_name} table")
        self.commit()

    def drop_table(self, table_name):
        self.c.execute(
            f"drop table {table_name}"
        )
        print(f"Delete {table_name} table")
        self.commit()

    def update(self, table_name, value1, word1, value2, word2):
        try:
            self.c.execute(
                f"update {table_name} set {value1} = '{word1}' where {value2} = '{word2}'"
            )
            print(f"Updated {table_name} table {value2} = {word2}")
            self.commit()
        except:

            print("Not updated ")

    def delete(self, table_name, value, word):
        try:
            self.c.execute(
                f"delete from {table_name} where {value}='{word}'"
            )
            print(f"Delete {table_name} table {value} = {word}")
            self.commit()
        except:
            print("Not deleted ")

    def add(self, table_name, *values):
        try:
            self.c.execute(
                f"insert into {str(table_name)} values {values}"
            )
            print(f"Add informations")
            self.commit()
        except:
            print("Not add")

    def filter(self, table_name, value, word, all=False):
        try:
            if all:
                self.c.execute(
                    f"select * from {table_name}")
                return self.c.fetchall()
            else:
                self.c.execute(
                    f"select * from {table_name} where {value} = '{word}'")
                return self.c.fetchall()
        except:
            return False


if __name__ == "__main__":
    db().create_table("users", """
        id text,
        first_name text,
        username text,
        step text
    
    """)
    db().create_table("contents", """
        button_name text,
        message_id text,
        from_chat_id text
    """)
    db().create_table("keyboards","""
        markup_name text,
        button_name text
    """ )
    db().create_table("channels", """
        name text,
        url text
    """)
    db().add("channels","MoonLight | Company","moonlightdesign")

