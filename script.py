import requests
from bs4 import BeautifulSoup

url = "http://www.century21.com"
r = requests.get(url)
c = r.content

# This gives us all the information (html) from the site
soup = BeautifulSoup(c, "html.parser")

# This will give all the divs that have the property information
all = soup.find_all("div", {"class": "propertyRow"})

# This will give us the info of each property
l=[]
for item in all:
    d={}
    d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text # Gives us the address
    d["Locality"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text # Gives us the neighborhood
    d["Price"] = item.find("h4", {"class", "propPrice"}).text.replace("\n","").replace(" ", "")
    try:
        d["Beds"] = item.find("span", {"class", "infoBed"}).find('b').text #Number of beds
    except:
        d["Beds"] = None  # We have to do a try-except in cases where there are no info on the item. We print them to better process information
    try:
        d["Area"] = item.find("span", {"class", "infoSqFt"}).find('b').text
    except:
        d["Area"] = None
    try:
        d["Baths"] = item.find("span", {"class", "infoValueFullBath"}).find('b').text
    except:
        d["Baths"] = None
    try:
        d["Half Baths"] = item.find("span", {"class", "infoValueHalfBath"}).find('b').text
    except:
        d["Half Baths"] = None
    for column_group in item.find_all("div", {"class": "columnGroup"}):
        for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}), column_group.find_all("span", {"class": "featureName"})):
            if "Lot Size" in feature_group.text:
                d["Lot Size"] = feature_name.text
    l.append(d)

