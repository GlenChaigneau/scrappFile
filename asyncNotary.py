import asyncio
import aiohttp
from bs4 import BeautifulSoup
from Notary import Notary
import pandas as pd
import time

baseUrl = 'https://www.notaires.fr'
uri = '/fr/directory/notaries?location=lyon&lat=45.758&lon=4.835&page='
pageNb = 5


async def swoup(session, url):
    async with session.get(url) as response:
        return BeautifulSoup(await response.text(), 'html.parser')


async def get_endpoints(session, cards):
    tasks = []
    for card in cards:
        link = card.find("a", class_="arrow-link")['href'].split('?')[0]
        task = asyncio.create_task(swoup(session, baseUrl + link))
        tasks.append(task)
    endpoints = []
    for task in asyncio.as_completed(tasks):
        soup = await task
        endpoints.append(soup)
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


def get_website(soup):
    try:
        website = soup.find("div", class_="office-sheet__url field--link").find("a")['href']
        if website.startswith("http"):
            return website
        else:
            return "https://" + website
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
                'mail': notary.get_mail(),
                'phone': notary.get_phone(),
                'website': notary.get_website(),
                'address': notary.get_address()
            }
            notary_data.append(notary_dict)

    return notary_data


async def main():
    async with aiohttp.ClientSession() as session:
        notaries = []
        for page in range(0, pageNb + 1):
            final_url = baseUrl + uri + str(page)
            soup = await swoup(session, final_url)
            cards = soup.findAll("article", class_="notary-card notary-card--notary")
            endpoints = await get_endpoints(session, cards)
            for endpoint in endpoints:
                nom = get_name(endpoint)
                phone = get_phone(endpoint)
                mail = get_mail(endpoint)
                website = get_website(endpoint)
                address = get_address(endpoint)
                notary = Notary(nom, phone, mail, website, address)
                notaries.append(notary)

        formated_notary = format_notary(notaries)
        df = pd.DataFrame(formated_notary)
        df.to_csv("notaries.csv", index=False)

        print(f"Le nombre de notaires récupérés est : {len(notaries)}")

start_time = time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
end_time = time.time()

print("Le temps d'exécution est de : ", end_time - start_time, " secondes.")
