import os
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def connect_to_supabase():
    # Récupérer les informations de connexion
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    print(f"Tentative de connexion à {host}...")

    try:
        # Créer la connexion
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        # Créer un curseur pour exécuter des requêtes
        cursor = connection.cursor()
        
        # Exécuter une requête simple pour tester
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("CON-OK : Connexion réussie !")
        print(f"Version de la base de données : {db_version[0]}")

        # Fermer le curseur et la connexion
        cursor.close()
        connection.close()
        print("Connexion fermée proprement.")

    except Exception as e:
        print("ERR : Erreur lors de la connexion :")
        print(e)
        print("\nNOTE : Si vous voyez une erreur de 'timeout' ou 'Host unreachable',")
        print("il est possible que votre réseau ne supporte pas l'IPv6.")
        print("Dans ce cas, utilisez le Connection Pooler de Supabase (port 6543).")

if __name__ == "__main__":
    connect_to_supabase()
