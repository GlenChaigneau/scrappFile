import requests
from bs4 import BeautifulSoup
from Notary import Notary


def get_notary():

    try:
        # Envoi d'une requête GET à l'URL
        response = requests.get(baseUrl + uri)

        # Vérification de la réponse
        if response.status_code == 200:
            # Extraction du contenu HTML
            html_content = response.text

            # Création de l'objet BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Recherche des entrées d'annuaire de notaires
            content = soup.find("div", class_="professional-directory__results-list")
            entries = content.find_all("article", class_="notary-card notary-card--notary")
            # Boucle sur les entrées d'annuaire

            for entry in entries:
                try:
                    # Extraction du nom du notaire
                    name = entry.find("h2", class_="notary-card__title").text.strip()
                except:
                    name = "No Name"
                try:
                    # Extraction de l'adresse du notaire
                    address = entry.find("p", class_="notary-card__email field--email").text.strip()
                except:
                    address = "No Mail"
                try:
                    # Extraction du numéro de téléphone du notaire
                    phone = entry.find("p", class_="notary-card__phone field--telephone").text.strip()
                except:
                    phone = "No Phone"
                try:
                    # Extraction du numéro du site web du notaire
                    web = entry.find("p", class_="notary-card__url field--link").text.strip()
                except:
                    web = "No Website"

                return Notary(name, address, phone, web)
    except:
        pass


def scrapp():

    # Définition de l'Url
    baseUrl = "https://www.notaires.fr/fr"
    uri = "/directory/notaries?location=69000&page="

    for pageNb in range(0, 1929 + 1):

        uri = uri + str(pageNb)

        # Envoi d'une requête GET à l'URL
        response = requests.get(baseUrl+uri)

    notaryArray = [get_notary()]
    print(notaryArray)

    for notary in notaryArray:

        print("------[New Notary]------")
        print("Nom :", notary.get_name())
        print("Adresse Mail :", notary.get_address())
        print("Téléphone :", notary.get_phone())
        print("Site Web :", notary.get_web())

    return [notary for notary in notaryArray if notary]
    

