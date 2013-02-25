import os
import re
import hashlib
import requests
import pickle
from BeautifulSoup import BeautifulSoup

def get_menu_text(href):
    filename = hashlib.md5(href).hexdigest() + ".html"
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return f.read()
    else:
        resp = requests.get("http://www.tourismvictoria.com" + href)
        with open(filename, "wb") as f:
            f.write(resp.text.encode('utf-8', 'replace'))
        return resp.text

def get_menus():
    resp = requests.get("http://www.tourismvictoria.com/events/dinearound/dinearound-menus-/")
    content = BeautifulSoup(resp.text)

    menus = {}
    for row in content.find(id="listingMenus").findAll('tr'):
        name = row.find('td')
        if not name:
            continue


        name = name.contents[0]
        print name

        menus[name] = {}
        n = 0
        for price, td in zip(('$20', '$30', '$40'), row.findAll('td')[1:4]):
            if td.text == '&nbsp;-&nbsp;':
                menus[name][price] = None
            else:
                menus[name][price] = get_menu(td.find('a')['href'], n)
                n += 1

    return menus

def get_menu(href, nth_menu=0):
    soup = BeautifulSoup(get_menu_text(href)).find('div', 'menuContainer')

    menu = {}
    category = None
    ii = 0
    in_correct_menu = False
    for n in soup.findAll(re.compile('(div|h3|h2)')):
        if n.name == 'h2':
            in_correct_menu = (ii == nth_menu)
            ii += 1
            continue

        if in_correct_menu:
            if n.name == 'h3':
                category = n.text
                menu[category] = []
            elif category and n['class'] == 'menuItem':
                menu[category].append(n.text)

    return menu

def main():
    with open("menus.pickle", "wb") as f:
        menus = get_menus()
        pickle.dump(menus, f)

if __name__ == "__main__":
    main()
