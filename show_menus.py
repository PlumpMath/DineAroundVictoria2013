import pickle

with open("menus.pickle", "rb") as f:
    menus = pickle.load(f)

with open("rundown.txt", "wb") as f:
    for place in sorted(menus.keys()):
        f.write(place.encode('utf-8', 'replace') + "\n")
        for price in sorted(menus[place].keys()):
            if menus[place][price] is None:
                continue
            f.write("\t" + price.encode('utf-8', 'replace') + "\n")
            for course in menus[place][price]:
                f.write("\t\t" + course.encode('utf-8', 'replace') + "\n")
                for item in menus[place][price][course]:
                    f.write("\t\t\t" + item.encode('utf-8', 'replace') + "\n")
