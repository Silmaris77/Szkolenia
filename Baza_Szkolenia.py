import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)
   return conn

def execute_sql(conn, sql):
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

def add_training(conn, training):
   sql = '''INSERT INTO trainings(training_name, start_date, end_date, trainer_id)
             VALUES(?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, training)
   conn.commit()
   return cur.lastrowid

def add_trainer(conn, trainer):
   sql = '''INSERT INTO trainers(first_name, last_name, email)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, trainer)
   conn.commit()
   return cur.lastrowid

def select_all(conn, table):
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()
   return rows

def select_where(conn, table, **query):
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def update(conn, table, id, **kwargs):
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE trainer_id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete_where(conn, table, **kwargs):
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

def delete_all(conn, table):
   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
   print("Deleted")

if __name__ == "__main__":
    db_file = "BazaSzkolen.db"
    conn = create_connection(db_file)
    if conn is not None:

        create_trainers_sql = """
        CREATE TABLE IF NOT EXISTS Trainers (
            trainer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        """
        
        create_trainings_sql = """
        CREATE TABLE IF NOT EXISTS Trainings (
            training_id INTEGER PRIMARY KEY,
            training_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            trainer_id INTEGER,
            FOREIGN KEY (trainer_id) REFERENCES Trainers (trainer_id)
        );
        """
        
        execute_sql(conn, create_trainers_sql)
        execute_sql(conn, create_trainings_sql)
        
        delete_all(conn, "trainings")
        delete_all(conn, "trainers")
        
        trainer_id =  add_trainer(conn, ("Jan", "Nowak", "jn@blueaccelerator.com"))
        add_training (conn,("Negocjacje", "2024-08-13 09:00:00", "2024-08-13 17:00:00", trainer_id))
        add_training (conn,("Techniki Sprzedaży", "2024-09-23 09:00:00", "2024-9-23 17:00:00", trainer_id))
        
        trainer_id =  add_trainer(conn, ("Ewa", "Kowalska", "ek@blueaccelerator.com"))
        add_training (conn,("Prezentacja", "2024-06-13 09:00:00", "2024-06-13 17:00:00", trainer_id))
        add_training (conn,("Komunikacja interpersonalna", "2024-09-10 09:00:00", "2024-09-10 17:00:00", trainer_id))

        trainer_id =  add_trainer(conn, ("Piotr", "Dąbrowski", "pd@blueaccelerator.com"))
        add_training (conn,("Merchandising", "2024-05-13 09:00:00", "2024-05-13 17:00:00", trainer_id))
        add_training (conn,("Category Management", "2024-09-11 09:00:00", "2024-09-11 17:00:00", trainer_id))

        trainer_id =  add_trainer(conn, ("Katarzyna", "Dobrowolska", "kd@blueaccelerator.com"))
        add_training (conn,("Merchandising", "2024-04-13 09:00:00", "2024-04-13 17:00:00", trainer_id))
        add_training (conn,("Category Management", "2024-09-12 09:00:00", "2024-09-12 17:00:00", trainer_id))

        add_trainer(conn, ("Tomasz", "Kot", "tk@blueaccelerator.com"))
        add_trainer(conn, ("Anna", "Wojton", "aw@blueaccelerator.com"))
      

    print(select_where(conn, "trainers", first_name="Tomasz"))

    update(conn, "trainers", 2, email="ewakowalska@onet.pl")
    print(select_all(conn, "trainers"))
    
    delete_where(conn, "trainers", trainer_id=1)
    print(select_all(conn, "trainers"))

    # delete_all(conn, "trainings")
    # delete_all(conn, "trainers")

    conn.close()