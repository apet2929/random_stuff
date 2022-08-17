from bs4 import BeautifulSoup

def convertDataToDict(data):

    soup = BeautifulSoup(data, 'html.parser')

    cards = soup.find_all("span", class_="TermText notranslate lang-en")

    for i in range(len(cards)):
        cards[i] = cards[i].text

    flashCards = {
        cards[1] : cards[0]
    }

    for i in range(2,len(cards), 2):
        flashCards[cards[i+1]] = cards[i]

    return flashCards
