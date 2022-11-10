from flask import Flask, render_template
import mysql.connector
import urllib
from urllib import request
import bs4
import pandas

app=Flask(__name__,template_folder='templates')


def getDataScrappingGames() :
    # Connexion à la page et récupération du code source

    url_trader_games = "https://www.tradergames.fr/fr/1091-derniers-arrivages"
    request_text = request.urlopen(url_trader_games).read()
    page = bs4.BeautifulSoup(request_text, "lxml")


    # Récupération des Ids des produits de la page dans le tableau list_ids
    list_ids = []
    articles = page.findAll('article')
    for div in articles :
        list_ids.append(div.get('data-id-product'))
    #-----------------------------------------------------------------------------    
    
    # Récupération des Images des produits de la page dans le tableau list_images_final (l'id est également récupéré pour vérifier la cohérence des données)
    list_images = {} # dictionnaire avec id + image
    articles = page.findAll('article')
    count = 0
    for div in articles :
        for d in div.findAll('div', {'class' : 'thumbnail-container'}) :
            for img in d.findAll('div', {'class' : 'product-image'}) :
                for i in img('img', {'class' : 'img-fluid'}) :
                    list_images[count] = div.get('data-id-product'), i.get("src")
                    count = count + 1
    list_images_final = []
    # On met nos données sous forme de tableau  
    for clé, valeur in list_images.items() :
        list_images_final.append(valeur[1])
    #-----------------------------------------------------------------------------

    # Récupération des Noms des produits de la page dans le tableau list_noms_final
    list_noms = {} # dictionnaire avec id + nom des produits
    articles = page.findAll('article')
    count = 0
    for div in articles :
        for h3 in div.findAll('div', {'class' : 'thumbnail-container'}) :
            for title in h3.findAll('h3', {'class' : 'h3 product-title'}) :
                list_noms[count] = div.get('data-id-product'), title.getText()
                count = count + 1
    list_noms_final = []
    #On met nos données sous forme de tableau  
    for clé, valeur in list_noms.items() :
        list_noms_final.append(valeur[1])
    #-----------------------------------------------------------------------------

    # Récupération des Prix des produits de la page dans le tableau list_prix_final
    list_prix = {} # dictionnaire avec id + prix
    articles = page.findAll('article')
    count = 0
    for div in articles :
        for span in div.findAll('div', {'class' : 'thumbnail-container'}) :
            for sp in span.findAll('span', {'itemprop' : 'price'}) :
                list_prix[count] = div.get('data-id-product'), sp.getText()
                count = count + 1
    list_prix_final = []
    #On met nos données sous forme de tableau  
    for clé, valeur in list_prix.items() :
        list_prix_final.append(valeur[1])
    #-----------------------------------------------------------------------------

    # Récupération  des stickers regions des produits de la page dans le tableau list_regions_final 
    list_regions = {} # dictionnaire avec id + regions
    articles = page.findAll('article')
    count = 0
    #On récupère toutes les images stickers sur les produits (regions + etats)
    for div in articles :
        for span in div.findAll('div', {'class' : 'thumbnail-container'}) :
            for sp in span.findAll('span', {'class' : 'fmm_sticker_base_span'}) :
                for i in sp.select('img[src*="/img/stickers/"]') :
                    list_regions[count] = div.get('data-id-product'), i.get("src")
                    count = count + 1
    
    count1 = 0
    list_regions1 = {}
    # On récupére les stickers qui ont un url avec rectangle dedans, il correspond au drapeau. 
    for clé, valeur in list_regions.items() : 
        if "Rectangle" in valeur[1] or "Réctangle" in valeur[1] :
            list_regions1[count1] =  valeur[0], valeur[1]
            count1 = count1 + 1
            
    list_regions2 = {}
    #On enlève les doublons
    for clé, valeur in list_regions1.items() :
            if valeur not in list_regions2.values() :
                list_regions2[clé] = valeur
    
    list_regions_final = []
    #On met nos données sous forme de tableau  
    for clé, valeur in list_regions2.items() :
        list_regions_final.append(valeur[1])
    # On comble les espaces et on rajoute l'url en préfixe
    for i,j in enumerate(list_regions_final) :
        list_regions_final[i] = list_regions_final[i].replace(" ", "%20")
        list_regions_final[i] = 'https://www.tradergames.fr' + list_regions_final[i]
    #-----------------------------------------------------------------------------

    # Récupération  des stickers regions des produits de la page dans le tableau list_regions_final 
    list_etats = {}
    articles = page.findAll('article')
    count = 0

    # On récupère toutes les images stickers sur les produits (regions + etats)
    for div in articles :
        for span in div.findAll('div', {'class' : 'thumbnail-container'}) :
            for sp in span.findAll('span', {'class' : 'fmm_sticker_base_span'}) :
                for i in sp.select('img[src*="/img/stickers/"]') :
                    list_etats[count] = div.get('data-id-product'), i.get("src")
                    count = count + 1

    count1 = 0
    list_etats1 = {}
    # On récupére l'url avec Neuf ou Occaz dedans, il correspond à l'état du produit. 
    for clé, valeur in list_etats.items() : 
        if "Neuf" in valeur[1] or "Occaz" in valeur[1] :
            list_etats1[count1] =  valeur[0], valeur[1]
            count1 = count1 + 1

    list_etats2 = {}
    #On enlève les doublons
    for clé, valeur in list_etats1.items() :
            if valeur not in list_etats2.values() :
                list_etats2[clé] = valeur

    list_etats_final = []

    #On met nos données sous forme de tableau  
    for clé, valeur in list_etats2.items() :
        list_etats_final.append(valeur[1])
    #On change la chaîne de caractère qui était un url en simple string avec l'info qu'on souhaite garder : Occasion ou Neuf 
    for i, j in enumerate(list_etats_final) :
        if "Occaz" in j :
            list_etats_final[i] = "Occasion"
        if "Neuf" in j :
            list_etats_final[i] = "Neuf"
    #-----------------------------------------------------------------------------

    df = pandas.DataFrame.from_dict( {'ID' : list_ids, 'nom_jeux' : list_noms_final, 'urls' : list_images_final, 'prix' : list_prix_final, 'zone_import' : list_regions_final, 'etat' : list_etats_final})
    return df


config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'gamesdb'
}

# READ ALL DATA
def games():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM games')
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return results

@app.route('/')
def index():
    return render_template('index.html', gamesSQL=games(), tables=[getDataScrappingGames().to_html(classes='data')], titles=getDataScrappingGames().columns.values)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


