# SportsBetPy
Le projet SportsBetPy est un projet de Machine Learning sur le sujet des paris sportifs, l'objectif étant de développer un algorithme capable de battre les bookmakers.
Le code a été écrit en Python.

La réalisation du projet s'articule autour des 2 notebooks, du rapport et du Streamlit détaillés ci-contre :

## Création du jeu de donnees.ipynb
Ce notebook contient les phases de préprocessing: 
  - Traitement des données: récupération, nettoyage, création des variables explicatives nécessaires aux modèles de Machine Learning.
  - Dataviz: illustration des choix effectués et visualisation des données au travers de graphes.

Les données d'entrées utilisées sont à retrouver dans le dossier "Données d'entrée".

## Machine Learning.ipynb
Ce notebook contient la phase de Machine Learning. Nous avons utilisé les outils suivants:
  - Algorithmes: Random Forest Classifier, XGBoost, KNN, SVC, Voting Classifier.
  - Grilles de recherches d'hyperparamètres: GridSearchCV, Hyperopt.

## SportsBetPy.pdf
Ce rapport détaille l'ensemble du travail effectué au travers de ce projet.

## Streamlit
Ce dossier contient les éléments permettant de lancer le streamlit du projet, qui consiste en une simulation de site de pari sportif. Le script Streamlit a lancer est Sreamlit.py.

