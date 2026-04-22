# Projet : Système d'Analyse Hospitalière Multi-Agents

Ce document résume les objectifs et l'architecture du projet d'analyse de données patients en langage naturel.

## Objectif
Développer une plateforme permettant au personnel médical d'interroger les données hospitalières (PostgreSQL sur Supabase) en langage naturel, d'obtenir des analyses structurées et de générer des alertes automatiques.

## Architecture Cible
L'architecture repose sur une pipeline en 7 étapes :
1. **Source** : Interface `dashboard.html` (Chart.js).
2. **Trigger** : n8n Webhook.
3. **Données (SQL Agent)** : Interroge la base via un serveur MCP PostgreSQL (Port 8000).
4. **Analyse (Analyste Agent)** : Analyse les données brutes extraites.
5. **Alertes (Alertes Agent)** : Génère des alertes et scores via un serveur MCP dédié (Port 8001).
6. **Formatage (Formatter Agent)** : Fusionne l'analyse et les alertes en un JSON final.
7. **Sortie** : Réponse JSON au dashboard et envoi vers un webhook externe (webhook.site).

## Composants Techniques
- **Base de données** : Supabase (Tables: `patients`, `sejours`, `diagnostics`, `services`, `medecins`).
- **Serveurs MCP** :
    - `mcp_server.py` : Accès SQL (FastMCP).
    - `mcp_alertes.py` : Logique métier médicale (Alertes, Scores de risque).
- **Automation** : n8n (Pipeline multi-agents).
- **IA** : Modèle `gpt-4o-mini`.

## Livrables attendus
- Base de données initialisée et vérifiée.
- Serveurs MCP opérationnels et testés.
- Pipeline n8n complète et fonctionnelle.
- Dashboard interactif affichant les analyses et graphiques.
