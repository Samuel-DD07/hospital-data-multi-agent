import os
import json
import psycopg2
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
# Ces paramètres sont récupérés depuis le fichier .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "votre_mot_de_passe")
}

mcp = FastMCP("hopital-db")

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@mcp.tool()
def get_schema() -> str:
    """
    Retourne le schema complet de la base de donnees hopitaldb.
    Appeler cet outil en premier avant toute requete SQL.
    """
    schema = {
        "tables": {
            "services": {
                "colonnes": ["id", "nom", "nb_lits", "responsable"],
                "description": "Services hospitaliers"
            },
            "medecins": {
                "colonnes": ["id", "nom", "prenom", "specialite", "service_id"],
                "cles_etrangeres": {"service_id": "services.id"},
                "description": "Medecins rattaches a un service"
            },
            "patients": {
                "colonnes": ["id", "nom", "prenom", "date_naissance", "sexe", "adresse"],
                "description": "Patients de l hopital"
            },
            "sejours": {
                "colonnes": ["id", "patient_id", "service_id", "medecin_id", "date_entree", "date_sortie", "cout_sejour", "statut"],
                "cles_etrangeres": {
                    "patient_id": "patients.id",
                    "service_id": "services.id",
                    "medecin_id": "medecins.id"
                },
                "valeurs_statut": ["en_cours", "termine", "urgent"],
                "description": "Sejours hospitaliers. date_sortie NULL = patient encore hospitalise"
            },
            "diagnostics": {
                "colonnes": ["id", "sejour_id", "code_cim", "libelle", "gravite", "date_pose"],
                "cles_etrangeres": {"sejour_id": "sejours.id"},
                "gravite": "entier de 1 (benigné) a 5 (critique)",
                "description": "Diagnostics poses lors d un sejour"
            }
        }
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)

@mcp.tool()
def run_sql(query: str) -> str:
    """
    Execute une requete SQL SELECT sur la base hopitaldb et retourne les resultats.
    query : requete SQL SELECT a executer
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Récupérer les noms des colonnes
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        # Transformer les résultats en liste de dictionnaires
        result = [dict(zip(columns, row)) for row in rows]
        return json.dumps(result, ensure_ascii=False, default=str)
        
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import uvicorn
    app = mcp.streamable_http_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
