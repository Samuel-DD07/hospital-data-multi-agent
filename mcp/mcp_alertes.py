import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hopital-alertes")

# Stockage en memoire des alertes de la session
alertes_session = []

@mcp.tool()
def creer_alerte(niveau: str, service: str, message: str) -> str:
    """
    Cree une alerte medicale et la stocke en memoire pour la session.
    niveau : "info" | "warning" | "critique"
    service : nom du service concerne
    message : description de la situation
    """
    alerte = {
        "id": len(alertes_session) + 1,
        "niveau": niveau,
        "service": service,
        "message": message,
        "horodatage": datetime.now().isoformat()
    }
    alertes_session.append(alerte)
    return json.dumps({
        "statut": "alerte creee",
        "alerte": alerte,
        "total_alertes_session": len(alertes_session)
    }, ensure_ascii=False)

@mcp.tool()
def calculer_score_risque(age: int, gravite_diagnostic: int, duree_sejour_jours: int) -> str:
    """
    Calcule un score de risque patient sur 100.
    age : age du patient en annees
    gravite_diagnostic : gravite du diagnostic principal (1 a 5)
    duree_sejour_jours : duree du sejour en jours
    """
    score_age = min(age / 100 * 30, 30)
    score_gravite = gravite_diagnostic / 5 * 50
    score_duree = min(duree_sejour_jours / 30 * 20, 20)
    score_total = round(score_age + score_gravite + score_duree, 1)

    if score_total >= 70:
        niveau = "critique"
    elif score_total >= 40:
        niveau = "modere"
    else:
        niveau = "faible"

    return json.dumps({
        "score": score_total,
        "niveau_risque": niveau,
        "detail": {
            "contribution_age": round(score_age, 1),
            "contribution_gravite": round(score_gravite, 1),
            "contribution_duree": round(score_duree, 1)
        }
    }, ensure_ascii=False)

@mcp.tool()
def calculer_score_criticite(code_cim: str, age: int, duree_sejour: int) -> str:
    """
    Calcule un score de criticité patient sur 100 à partir d'un diagnostic CIM,
    d'un âge et d'une durée de séjour. Aucune base de données requise.
    code_cim : code diagnostic CIM (ex: I21.0)
    age : age du patient en annees
    duree_sejour : duree du sejour en jours
    """
    # Table de correspondance CIM -> gravite (1 a 5)
    GRAVITES_CIM = {
        "I21": 5, "I21.0": 5, "I21.4": 5,
        "I63": 5, "I63.5": 5,
        "C34": 5, "C34.1": 5,
        "I50": 4, "I50.0": 4,
        "I48": 4,
        "G61": 4, "G61.0": 4,
        "G35": 3,
        "G40": 3, "G40.0": 3,
        "I10": 3,
        "G20": 3,
        "G43": 2, "G43.0": 2,
        "K57": 3, "K57.3": 3,
        "J18": 3, "J18.9": 3,
        "S06": 2, "S06.0": 2,
        "K40": 2, "K40.0": 2,
        "M16": 2, "M16.0": 2,
        "S52": 2, "S52.0": 2,
        "R07": 2, "R07.4": 2,
        "A09": 1,
        "T14": 1, "T14.1": 1,
        "J06": 1, "J06.9": 1,
        "L03": 1, "L03.0": 1,
        "R55": 1,
        "K80": 1, "K80.0": 1,
    }

    # Recherche de la gravite : code exact puis prefixe
    gravite = GRAVITES_CIM.get(code_cim.upper())
    if gravite is None:
        prefixe = code_cim.split(".")[0].upper()
        gravite = GRAVITES_CIM.get(prefixe, 3) # defaut : gravite 3

    # Calcul des composantes
    score_age = round(min(age / 100 * 25, 25), 1)
    score_gravite = gravite * 10
    score_duree = round(min(duree_sejour / 30 * 25, 25), 1)
    score_total = round(score_age + score_gravite + score_duree, 1)

    # Recommandation selon le score
    if score_total >= 75:
        recommandation = "Transfert en soins intensifs recommande"
    elif score_total >= 50:
        recommandation = "Surveillance renforcee requise"
    elif score_total >= 25:
        recommandation = "Suivi standard"
    else:
        recommandation = "Sortie envisageable"

    resultat = {
        "code_cim": code_cim,
        "age": age,
        "duree_sejour": duree_sejour,
        "gravite_cim": gravite,
        "score_total": score_total,
        "detail": {
            "score_age": score_age,
            "score_gravite": score_gravite,
            "score_duree": score_duree
        },
        "recommandation": recommandation
    }
    return json.dumps(resultat, ensure_ascii=False)

@mcp.tool()
def envoyer_rapport() -> str:
    """
    Simule l envoi d un rapport d alertes. Retourne le resume des alertes de la session.
    A appeler uniquement si au moins une alerte critique a ete creee.
    """
    nb_critiques = sum(1 for a in alertes_session if a["niveau"] == "critique")
    nb_warnings = sum(1 for a in alertes_session if a["niveau"] == "warning")
    nb_infos = sum(1 for a in alertes_session if a["niveau"] == "info")

    rapport = {
        "rapport_envoye": True,
        "horodatage": datetime.now().isoformat(),
        "resume": {
            "total": len(alertes_session),
            "critiques": nb_critiques,
            "warnings": nb_warnings,
            "infos": nb_infos
        },
        "alertes": alertes_session
    }
    return json.dumps(rapport, ensure_ascii=False)

if __name__ == "__main__":
    import uvicorn
    app = mcp.streamable_http_app()
    uvicorn.run(app, host="127.0.0.1", port=8001)
