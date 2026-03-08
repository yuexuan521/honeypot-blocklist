[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [Français](README_FR.md) | [Español](README_ES.md)

# Flux de renseignement sur les menaces HFish Honeypot

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yuexuan521/honeypot-blocklist)
[![Source](https://img.shields.io/badge/Source-HFish-blue.svg)](https://hfish.net/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Data Quality Check](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml/badge.svg)](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml)
[![Release](https://img.shields.io/github/v/release/yuexuan521/honeypot-blocklist)](https://github.com/yuexuan521/honeypot-blocklist/releases)

Flux d’adresses IP malveillantes à haute fiabilité, généré automatiquement à partir de la **télémétrie des honeypots HFish**, conçu pour les environnements **pare-feu / WAF / SIEM / IPSet / EDL**.

Ce projet collecte en continu les adresses IP sources observées par des honeypots HFish exposés à Internet, applique un filtrage automatique ainsi qu’une liste blanche, puis publie un flux propre et simple à intégrer dans des systèmes de défense et des pipelines d’automatisation.

> **Avertissement**
> Ce flux est généré automatiquement. Même si un filtrage et une liste blanche sont appliqués, il est fortement recommandé d’évaluer son impact dans votre propre environnement avant de l’utiliser en production.

---

## Pourquoi ce projet existe

Les honeypots exposés à Internet reçoivent en permanence des tentatives de brute force, des scans de vulnérabilités, des essais d’identifiants faibles et d’autres trafics d’attaque automatisés.  
L’objectif de ce dépôt est de transformer ces observations réelles en un **flux de renseignement défensif** réutilisable afin d’aider les utilisateurs à :

- bloquer rapidement les IP malveillantes récentes à la périphérie du réseau
- enrichir les détections SIEM / SOAR avec un signal de menace supplémentaire
- générer automatiquement des règles de blocage pour des pare-feu Linux, des services Web et des environnements edge
- construire leur propre flux privé de renseignement sur les menaces à partir de HFish

---

## Principales caractéristiques

- **Flux glissant d’IP malveillantes sur 24 heures**
- **Mise à jour automatique toutes les 2 à 4 heures**
- **URL d’abonnement en texte brut**
- **SDK Python et CLI inclus**
- **Prise en charge de Docker**
- **Exemples d’intégration pour Nginx, Linux Firewall, Cloudflare et Palo Alto**
- **Projet open source sous licence MIT**

---

## URL du flux

Vous pouvez intégrer directement l’URL suivante dans vos équipements de sécurité, scripts ou workflows automatisés :

| Format | URL | Cas d’usage |
|---|---|---|
| TXT | `https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt` | EDL de pare-feu, Linux IPSet, WAF, enrichissement SIEM |

---

## Profil du flux

| Élément | Valeur |
|---|---|
| Source de données | HFish Honeypot (V3+) |
| Périmètre d’observation | Internet public |
| Activités incluses | brute force SSH/RDP, scans Web / exploitation de vulnérabilités, sondes sur services non autorisés |
| Fenêtre temporelle | 24 dernières heures |
| Fréquence de mise à jour | toutes les 2 à 4 heures |
| Traitement des données | nettoyage automatique et filtrage de base par liste blanche |
| Exclusions courantes | GoogleBot, BingBot, services GitHub, Cloudflare et autres infrastructures légitimes connues lorsque cela s’applique |

---

## Pourquoi ce flux est crédible

Ce projet est conçu pour être **simple, transparent, auditable et facile à automatiser**.

- **Format de données ouvert** : une IP par ligne, facile à vérifier, analyser et intégrer
- **Chaîne d’outils ouverte** : la logique de génération, le client et la CLI sont publics dans le dépôt
- **Limites clairement documentées** : le risque de faux positifs est explicitement indiqué
- **Orienté usage réel** : pensé pour des environnements de défense concrets, pas seulement pour une démonstration

Cela dit, aucun flux automatisé de renseignement sur les menaces n’est parfait.  
Des sorties réseau partagées, du NAT, des hôtes compromis ou une réattribution dynamique d’IP peuvent introduire du bruit ou des faux positifs. En production, il est conseillé d’observer et de tester avant d’appliquer un blocage strict.

---

## Cas d’usage recommandés

Ce flux convient notamment pour :

- bloquer rapidement des IP malveillantes connues à la périphérie du réseau
- alimenter une **EDL (External Dynamic List)** sur des pare-feu d’entreprise
- enrichir des plateformes **SIEM / SOAR**
- générer automatiquement des règles **Linux IPSet / iptables**
- produire des règles de refus pour **Nginx**
- mettre en place une logique légère de blocage sur **Cloudflare Workers** ou d’autres environnements edge

---

## Démarrage rapide

### Linux IPSet + iptables

```bash
# 1) Télécharger le flux le plus récent
wget -O /tmp/blacklist.txt https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt

# 2) Créer un ensemble IPSet
ipset create honeypot_blacklist hash:ip hashsize 4096

# 3) Importer les IP
while read ip; do
  ipset add honeypot_blacklist "$ip"
done < /tmp/blacklist.txt

# 4) Bloquer le trafic correspondant
iptables -I INPUT -m set --match-set honeypot_blacklist src -j DROP
```

------

## Utilisation pour les développeurs

### SDK Python

```python
from tools.client import ThreatFeedClient

feed = ThreatFeedClient()
feed.fetch_data()

if feed.is_malicious("1.2.3.4"):
    print("Cette IP devrait être bloquée")
else:
    print("Cette IP n’est pas actuellement présente dans le flux")
```

### CLI

```bash
# Mettre à jour les données locales
python3 tools/cli.py --update

# Vérifier si une IP est présente dans le flux
python3 tools/cli.py --check 1.2.3.4

# Exporter en JSON
python3 tools/cli.py --export json

# Exporter en TXT
python3 tools/cli.py --export txt
```

### Docker

```bash
docker build -t hfish-feed .
docker run --rm hfish-feed --check 1.1.1.1
```

------

## Exemples d’intégration

Le répertoire `integrations/` contient des exemples prêts à l’emploi pour plusieurs plateformes :

| Plateforme     | Type          | Usage                                           |
| -------------- | ------------- | ----------------------------------------------- |
| Nginx          | Script        | Génération de règles de refus pour serveurs Web |
| Linux Firewall | Script        | Blocage efficace avec `ipset` + `iptables`      |
| Cloudflare     | Worker        | Logique de blocage à la périphérie              |
| Palo Alto      | Documentation | Intégration avec External Dynamic List (EDL)    |

------

## Construire votre propre flux HFish

Si vous exploitez votre propre environnement HFish, vous pouvez réutiliser les outils de ce projet pour générer un flux privé ou spécifique à votre organisation.

Outils concernés :

- `tools/generate_feed.py`
- `tools/update_feed.sh`

Article de référence :

- **Guide pratique pour construire une source automatisée de renseignement sur les menaces avec HFish + Python + GitHub Pages**

------

## Structure du dépôt

```text
.
├── .github/workflows/       # vérification qualité des données et automatisation
├── integrations/            # exemples d’intégration par plateforme
├── tools/                   # générateur, SDK client, CLI, scripts de mise à jour
├── tests/                   # tests
├── ip_list.txt              # flux publié
└── README*.md               # documentation multilingue
```

------

## Niveau de maturité du projet

Ce projet est maintenu comme un utilitaire de sécurité destiné à des usages défensifs concrets, et non comme une simple démonstration.

Éléments actuels montrant sa maturité :

- dépôt public
- licence open source explicite
- documentation claire sur la sémantique du flux
- méthodes d’accès via CLI et SDK
- exemples d’intégration
- workflow automatisé de contrôle qualité des données

Avant une adoption en production, il est recommandé d’évaluer :

- la portée du blocage
- la gestion des faux positifs
- les attentes en matière de fréquence de mise à jour
- la stratégie de retour arrière
- la nécessité d’une liste blanche locale

------

## Signalement des faux positifs

Les faux positifs ne peuvent pas être totalement éliminés.

Si vous pensez qu’une IP a été ajoutée par erreur au flux, veuillez ouvrir une Issue et fournir autant que possible :

- l’adresse IP concernée
- la raison de la contestation
- des éléments justificatifs
- un horodatage approximatif si disponible

Ces informations aident à améliorer la qualité du flux au fil du temps.

------

## Sécurité

Ce dépôt publie un flux de renseignement sur les menaces ainsi que des outils associés.
**Il ne constitue pas une solution de prévention complète et ne doit pas être utilisé comme unique base de blocage.**

Bonnes pratiques recommandées :

- l’utiliser comme un signal parmi d’autres
- le combiner avec des listes blanches locales
- le tester d’abord en mode observation ou sur un périmètre limité
- faire preuve de prudence avec les plages IP partagées ou dynamiques

Si vous découvrez un problème de sécurité lié au code du dépôt, à l’automatisation ou aux scripts d’intégration, vous pouvez d’abord utiliser GitHub Issues. Pour un sujet sensible, un canal privé peut également être mis en place.

------

## Contribution

Les contributions en code, documentation et idées d’amélioration sont les bienvenues.

Exemples de contributions utiles :

- amélioration de la qualité du flux
- réduction des faux positifs
- amélioration du parseur, du client ou de la CLI
- ajout de nouvelles intégrations
- corrections documentaires et traductions
- amélioration des tests et du CI

Pour les changements importants, il est recommandé d’ouvrir d’abord une Issue afin de discuter du périmètre et de l’approche avant de soumettre une Pull Request.

------

## Feuille de route

Axes d’amélioration envisageables :

- formats de flux avec métadonnées plus riches
- suppression plus stricte des faux positifs
- davantage d’intégrations pour pare-feu / SIEM
- meilleure couverture de tests
- ajout de statistiques et d’éléments de transparence

------

## Clause de non-responsabilité

1. **Précision**
   Les données sont collectées et traitées automatiquement. Nous essayons de réduire le bruit, mais des hôtes compromis, des infrastructures partagées ou des IP dynamiques peuvent tout de même apparaître dans le flux.
2. **Utilisation à vos risques**
   Vous êtes responsable de vérifier si ce flux convient à votre environnement avant de l’utiliser en production.
3. **Absence de responsabilité**
   Le mainteneur ne peut être tenu responsable d’une interruption de service, d’une perte de connectivité, d’un impact opérationnel ou d’une perte de données causés par l’utilisation de ce flux.

------

## Licence

Ce projet est publié sous **MIT License**.

------

Propulsé par [HFish](https://hfish.net/) et l’automatisation Python.
