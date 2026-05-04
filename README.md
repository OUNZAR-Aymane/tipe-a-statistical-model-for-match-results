# Modélisation statistique des résultats de matchs de football

**TIPE 2023/2024 — OUNZAR Aymane**

Ce projet propose une approche statistique pour modéliser et prédire les résultats
des matchs de Premier League anglaise. Le nombre de buts marqués par chaque équipe
est modélisé par une loi de Poisson, dont les paramètres (force d'attaque, défense,
avantage du terrain) sont estimés par maximum de vraisemblance pondéré dans le temps.

Trois modèles sont comparés : un modèle de base (Modèle 0), un modèle avec
vraisemblance pondérée (Modèle 1), et un modèle intégrant une copule de Frank pour
capturer la dépendance entre les scores des deux équipes (Modèle 2). Les modèles sont
évalués via le critère d'Akaike et testés sur une stratégie de pariages sportifs
(marchés 1X2 et O/U 2.5 buts). Les trois modèles aboutissent à des profits positifs,
et le Modèle 1 s'avère le meilleur compromis entre complexité et performance.

## 📄 Présentation complète

[Voir le support de présentation (PDF)](https://github.com/OUNZAR-Aymane/tipe-a-statistical-model-for-match-results/blob/master/tipe_support.pdf)
