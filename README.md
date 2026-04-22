# Systeme d'Analyse Hospitaliere Multi-Agents

Ce projet est une plateforme d'analyse de donnees medicales en temps reel utilisant une architecture multi-agents orchestree par n8n, alimentee par des serveurs MCP (Model Context Protocol) et une base de donnees PostgreSQL (Supabase).

## Fonctionnalites
- Interface Naturelle : Posez des questions sur les donnees hospitalieres en langage clair.
- Agents Specialises :
  - SQL Agent : Traduit les questions en requetes SQL securisees.
  - Analyste Agent : Genere des diagnostics statistiques et des graphiques.
  - Alertes Agent : Calcule les scores de risque et detecte les surcharges de services via une logique metier dediee.
- Dashboard Dynamique : Visualisation via Chart.js avec mise a jour temps reel.
- Export Automatique : Envoi des rapports vers des webhooks externes pour historisation.

## Architecture
1. Source : Dashboard HTML (Frontend).
2. Orchestrateur : n8n (Pipeline a 7 noeuds).
3. Services MCP (Python/FastMCP) :
   - Port 8000 : Acces SQL a Supabase.
   - Port 8001 : Logique metier medicale (Score de risque, alertes).
4. Base de donnees : Supabase (PostgreSQL).

## Installation

### Prerequis
- Node.js (pour n8n)
- Python 3.10+
- Un compte Supabase

### Configuration
1. Installer n8n :
   ```bash
   npm install n8n
   ```
2. Configurer Python :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn mcp psycopg2-binary python-dotenv
   ```
3. Variables d'environnement : Creer un fichier .env avec vos acces Supabase (Host, Port, User, Password).

## Lancement

1. Serveurs MCP (dans deux terminaux separes) :
   ```bash
   ./venv/bin/python3 mcp/mcp_server.py
   ./venv/bin/python3 mcp/mcp_alertes.py
   ```
2. n8n :
   ```bash
   npx n8n start
   ```
3. Dashboard :
   ```bash
   python3 -m http.server 3001
   ```
   Ouvrez ensuite http://localhost:3001/dashboard.html.

## Exemple de test
Saisissez dans le dashboard :
> "Analyse les services les plus charges et calcule l'age moyen des patients."

---

(c) 2026 - Projet d'Analyse Hospitaliere Multi-Agents
