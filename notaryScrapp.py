import requests
from bs4 import BeautifulSoup
from Notary import Notary
import pandas as pd
import time

baseUrl = 'https://www.notaires.fr'
uri = '/fr/directory/notaries?location=lyon&lat=45.758&lon=4.835&page='
pageNb = 5


def swoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_endpoints(cards):
    endpoints = []
    for card in cards:
        link = card.find("a", class_="arrow-link")['href'].split('?')[0]
        endpoints.append(link)
    return endpoints


def get_name(soup):
    try:
        return soup.find("h1", class_="office-sheet__title text-center text-m-start").find("span").text.split(" : ")[0]
    except AttributeError:
        return ""


def get_phone(soup):
    try:
        return soup.find("div", class_="office-sheet__phone field--telephone").find("a").text
    except AttributeError:
        return ""


def get_mail(soup):
    try:
        return soup.find("div", class_="office-sheet__email field--email").find("a")['href'].replace("mailto:", "")
    except AttributeError:
        return ""


def get_address(soup):
    try:
        spans = soup.find("div", class_="office-sheet__address field--address").find("p", "address").findAll("span")
        address = " ".join([span.text for span in spans])
        return address
    except AttributeError:
        return ""


def format_notary(notary_array):
    notary_data = []
    for notary in notary_array:
        if notary:
            notary_dict = {
                'name': notary.get_name(),
                'phone': notary.get_phone(),
                'mail': notary.get_address(),
                'web': notary.get_web(),
            }
            notary_data.append(notary_dict)

    return notary_data


notaries = []
start_time = time.time()
for page in range(0, pageNb + 1):
    finalUrl = baseUrl + uri + str(page)
    soup = swoup(finalUrl)
    cards = soup.findAll("article", class_="notary-card notary-card--notary")
    endpoints = get_endpoints(cards)
    for endpoint in endpoints:
        finalUrl = baseUrl + endpoint
        soup = swoup(finalUrl)
        nom = get_name(soup)
        phone = get_phone(soup)
        mail = get_mail(soup)
        address = get_address(soup)
        notary = Notary(nom, phone, mail, address)

        notaries.append(notary)

formated_notary = format_notary(notaries)
df = pd.DataFrame(formated_notary)
df.to_csv("glen.csv", index=False)
end_time = time.time()
print("Le temps d'exécution est de : ", end_time - start_time, " secondes.")