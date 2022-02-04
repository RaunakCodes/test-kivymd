import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('data.db')
        self.cursor = self.con.cursor()
        self.create_db_table()

    def create_db_table(self):
        """Create tasks table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS password(id integer PRIMARY KEY AUTOINCREMENT, platform_name varchar(300) NOT NULL, email varchar(300) NOT NULL, epassword varchar(500) NOT NULL)")
        self.con.commit()
        

    def save_password(self, plat_nme, email, password):
        """Create a task"""
        self.cursor.execute("INSERT INTO password(platform_name, email, epassword) VALUES(?, ?, ?)", (plat_nme, email, password))
        self.con.commit()
        # GETTING THE LAST ENTERED ITEM SO WE CAN ADD IT TO THE TASK LIST
        saved_pass = self.cursor.execute("SELECT id, platform_name, email, epassword FROM password WHERE platform_name = ?", (plat_nme,)).fetchall()
        return saved_pass[-1]

    def get_one_pass(self, passid):
        one_pass = self.cursor.execute("SELECT id, platform_name, email, epassword FROM password WHERE id =?",(passid,)).fetchone()
        return one_pass
    
    def get_password(self):
        """Get tasks"""
        #uncomplete_tasks = self.cursor.execute("SELECT id, platform_name, email, password FROM password WHERE platform_name = ?", (plat_nme,)).fetchall()
        all_passwords = self.cursor.execute("SELECT id, platform_name, email, epassword FROM password").fetchall()

        return all_passwords
    
    def delete_password(self, id):
        """Delete a task"""
        self.cursor.execute("DELETE FROM password WHERE id=?", (id,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()