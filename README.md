# 🛒 Analyse des Performances E-commerce — ElecMart Retail

> Projet portfolio Data Analyst · Secteur Retail & E-commerce · 2024

---

## 🎯 Contexte & Problématique

### Contexte métier

Dans le secteur du retail e-commerce, comprendre le comportement des visiteurs est essentiel pour optimiser le tunnel de conversion et maximiser la rentabilité. Les données clickstream, combinées aux données de ventes et de profils clients, permettent d'identifier les points de friction et les leviers de croissance.

### Problématique

**"Comment optimiser les performances d'un e-commerce retail en analysant le comportement des visiteurs, les sources de trafic et la rentabilité produit ?"**

### Objectifs

- Analyser l'entonnoir de conversion de bout en bout (sessions → achat)
- Identifier les devices et sources de trafic les plus performants
- Segmenter les clients par statut de fidélité et mesurer leur rentabilité
- Identifier les produits les plus rentables et les leviers d'optimisation

---

## 📊 Résultats & KPIs Clés

| KPI | Valeur |
|-----|--------|
| 🔍 Sessions analysées | 500 000 |
| 🛒 Taux de conversion | 2.40% |
| 🧺 Taux d'ajout panier | 9.21% |
| ❌ Taux d'abandon panier | 74% |
| 💰 Chiffre d'affaires total | 884M€ |
| 📈 Marge brute totale | 165M€ |
| 💹 Taux de marge | 18.7% |

---

## 🔍 Analyses & Insights

### 1. Entonnoir de Conversion
- 49.5% des sessions visitent une page produit → fort intérêt initial
- Seulement 9.2% ajoutent au panier → friction UX entre produit et panier
- 2.40% finalisent l'achat → taux standard e-commerce (2–3%)
- **74% des paniers sont abandonnés** → levier prioritaire d'optimisation

### 2. Performance par Device 📱
- Mobile = 45% du trafic mais conversion la plus basse (1.93%)
- Desktop = 25% du trafic mais meilleure conversion (3.04%) — **57% supérieure**
- Tablet = position intermédiaire (2.57%)
- → **Optimiser l'UX mobile est le levier numéro 1**

### 3. Sources de Trafic 🔗
- Organic = 1ère source en volume (39%) → SEO performant
- Campaign = meilleur taux de conversion → trafic qualifié
- Direct = 2ème source en volume (22%)
- → **Augmenter le budget campagnes pour maximiser les conversions**

### 4. Segmentation Clients 👥
- Elite dépense **3x plus par client** que Basic/Silver (2 361€ vs ~750€)
- Gold génère le plus grand volume de revenus total
- → **Programme de montée en gamme Basic → Gold à développer**

### 5. Top Produits 🏆
- Identification des 10 produits avec la meilleure marge brute
- Analyse croisée marge brute vs taux de marge par produit
- → **Maximiser la visibilité des produits à forte marge**

### 6. Heatmap Segment × Canal 🔥
- Croisement segment produit (Entry/Mid/Premium) × canal d'acquisition
- Identification des combinaisons les plus rentables
- → **Orienter les budgets marketing vers les segments les plus rentables**

---

## 💡 Recommandations Actionnables

| # | Recommandation | Impact estimé |
|---|---------------|---------------|
| 1 | **Optimiser l'UX mobile** — A/B test checkout mobile | +30% conversion mobile |
| 2 | **Relance panier abandonné** — email J+1 avec promo 5% | -20% abandon panier |
| 3 | **Augmenter budget campagnes** — meilleur ROI publicité | +15% conversions qualifiées |
| 4 | **Programme fidélité Elite** — avantages exclusifs montée en gamme | +25% LTV clients |
| 5 | **Mettre en avant top produits** — homepage + push notifications | +10% marge brute |

---

## 🗄️ Dataset

**Source :** [Kaggle — ECommerce Retail Analytics Dataset (ElecMart)](https://www.kaggle.com/datasets/ajibsss/elecmart-retail-analytics-dataset)

**Architecture en étoile — 14 tables · 1.8M+ lignes**

| Fichier | Disponible | Description | Volume |
|---------|-----------|-------------|--------|
| `fact_clickstream.csv` | ⬇️ Kaggle | Sessions web et comportement visiteurs | 1.7M lignes |
| `fact_sale.csv` | ⬇️ Kaggle | Transactions de vente ligne par ligne | 1.8M lignes |
| `fact_transaction.csv` | ⬇️ Kaggle | Transactions agrégées | — |
| `dim_customer.csv` | ✅ repo | Profil et segmentation clients | 150K lignes |
| `dim_product.csv` | ✅ repo | Catalogue produits et prix | 470 lignes |
| `dim_store.csv` | ⬇️ Kaggle | Magasins et points de vente | — |
| `dim_location.csv` | ⬇️ Kaggle | Géographie | — |
| `dim_campaign.csv` | ⬇️ Kaggle | Campagnes marketing | — |
| `dim_date.csv` | ⬇️ Kaggle | Calendrier | — |
| `inventory.csv` | ⬇️ Kaggle | Niveaux de stock | — |

> ⚠️ Les fichiers `fact_` dépassent 100MB — à télécharger directement sur [Kaggle](https://www.kaggle.com/datasets/ajibsss/elecmart-retail-analytics-dataset) et à placer dans le même dossier que le notebook.

---

## 🛠️ Stack technique

- **Python 3** — langage principal
- **Pandas** — manipulation et agrégation des données
- **Matplotlib** — visualisations personnalisées
- **Seaborn** — heatmap et graphiques statistiques
- **Jupyter Notebook** — présentation interactive de l'analyse
- **Kaggle** — source de données publique réelle
- **GitHub** — versioning et présentation portfolio

---

## 📁 Structure du repo

```
ecommerce-retail-analytics/
├── README.md
├── requirements.txt
├── analyse_ecommerce_elecmart.ipynb   ← Notebook Jupyter complet
├── analyse_ecommerce.py               ← Script Python standalone
├── dim_customer.csv                   ← 150K clients
└── dim_product.csv                    ← 470 produits
```

---

## 🚀 Lancer le projet

```bash
# 1. Cloner le repo
git clone https://github.com/TON_USERNAME/ecommerce-retail-analytics
cd ecommerce-retail-analytics

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Télécharger les fichiers fact_ sur Kaggle
# https://www.kaggle.com/datasets/ajibsss/elecmart-retail-analytics-dataset
# Placer fact_clickstream.csv, fact_sale.csv dans le dossier

# 4. Lancer le notebook
jupyter notebook analyse_ecommerce_elecmart.ipynb
```

---

## 👤 Auteur

**Thierry** · Candidat Data Analyst Junior · Paris Île-de-France
Master Big Data — Paris 8 · Licence Informatique — Sorbonne Paris Nord

> 💼 En reconversion depuis un poste opérationnel en logistique — ce projet démontre ma capacité à analyser des données comportementales e-commerce et à produire des insights actionnables pour des équipes marketing et produit.
