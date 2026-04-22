import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def seed_database():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    print(f"Connexion à {host}...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        
        print("Lecture du fichier init_db.sql...")
        with open("init_db.sql", "r") as f:
            sql = f.read()
        
        print("Exécution du script d'initialisation...")
        cur.execute(sql)
        conn.commit()
        
        print("SQL-OK : Base de données initialisée avec succès !")
        
        # Vérification
        cur.execute("SELECT COUNT(*) FROM patients;")
        count = cur.fetchone()[0]
        print(f"Nombre de patients insérés : {count}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print("ERR : Erreur :", e)

if __name__ == "__main__":
    seed_database()
