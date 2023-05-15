import re
import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.barreaudenice.com/annuaire/avocats/?fwp_paged=1")
print(r.status_code)

def get_all_pages():
    urls = []
    page_number = 1

    for i in range(104):
        i = f"https://www.barreaudenice.com/annuaire/avocats/?fwp_paged={page_number}"
        page_number += 1
        urls.append(i)
        #print(urls)

    return urls

def parse_attorney(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    avocats = soup.find_all('div', class_='callout secondary annuaire-single')
    #on met la balise "div" avec son attribut "class"
    #print(len(avocats))    on en aura 12

    for avocat in avocats:
        try:
            nom = avocat.find('h3').text.strip()   #on met ".text" pour avoir qu ele text choisi et non le code html, ".strip()permet de supprimer tous les espaces
        except AttributeError as e:
            nom = ""
        adresse = avocat.find('span', class_='adresse').text.strip()
        try:
            adresse_finale = re.sub(r"\s+", " ", adresse)     #"\s+"veut dire plus d un espace et le "r" c est pour utilise redex le 2eme element c est ceux par quoi on veut le remplacer al regex et le troisiemme c est sur quel element on veut la modifier en l occurence la notre variable adresse
        except AttributeError as e:
            adresse_finale = ""
        try:
            telephone = avocat.find('span', class_='telephone').text.strip()
        except AttributeError as e:
            telephone = ""
        try:
            email_avocat = avocat.find('span', class_='email').a.text.strip()
        except AttributeError as e:
            email_avocat = ""

        path = r"C:\Users\guela\Documents\SCRAPPING\PYCHARM\annuaire_avocat.txt" #le "r" pour row string inverse les back slash
        with open(path, "a") as f:
            f.write(f"{nom}\n") #le "\n" qui est rajoute c est pour la lisibilite du format txt sinon tout sur une ligne
            f.write(f"{adresse_finale}\n")
            f.write(f"{telephone}\n")
            f.write(f"{email_avocat}\n\n")

def parse_all_attorneys():
    pages = get_all_pages()
    for page in pages: #pour choisir son nombre de page a cette ligne preciser "pages[:2]
        parse_attorney(url=page)
        print(f"on scrape {page}") #nous permettra d avoir un element visuel lors de scrapping pour nous reperer dans la quantite de donnees


parse_all_attorneys()
