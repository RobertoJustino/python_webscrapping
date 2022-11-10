# Projet Web-Scraping

## Scrapper avec python

### Utilisation de BeautifulSoup et Pandas

  Les packages pour scrapper des pages HTML : 
- BeautifulSoup (pip3 install bs4)
- urllib 

  Le package pour travailler sur le dataset :
- pandas

## Problématique du projet  

### Site : https://www.tradergames.fr/fr/

#### La problématique du projet ici est de récupérer une certaine quantité des derniers arrivages du site via le scrapping et de vérifier la répartition des produits :  

- Provenance : répartition des régions sur les derniers arrivages
- Etats : répartition des produits Neuf et occasion sur les derniers arrivages

## Construction du dataset

#### Le dataset sera construit en récupérant les informations suivantes :  

- Id du produit
- Nom du produit
- Url de l'image du produit
- Prix du produit
- Region du produit : Zone Import
- Etat du produit : Occasion ou Neuf

#### Lien Jupyter Notebook : https://github.com/RobertoJustino/python_webscrapping/blob/main/python_scraping_trader_games.ipynb