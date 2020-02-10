from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "bakugan.csv"
f = open(filename,"w",encoding="utf-8")
headers = "Title, ,,Price, ,,Shipping, ,,Link\n"

f.write(headers)

#class conatining listing information
class Listing:
    def __init__(self,title, price, shipping, link):
        self.title = title
        self.price = price
        self.shipping = shipping
        self.link = link



    def __str__(self):
        if "New Listing" in self.title:
            self.title = self.title.replace("New Listing", "")
        return "{} {} {} {}".format("Title: " + str(self.title)+"\n", "Price: " + str(self.price)+"\n", "Shipping Cost: " + str(self.shipping)+"\n", "Link: " + str(self.link)+"\n")

pgNum = 1
lastPage = 10
link = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=bakugan+lot&_sacat=0&LH_TitleDesc=0&LH_BIN=1&_pgn="
my_url =link + str(pgNum)

#opens url and gets page
uClient = uReq(my_url)

#html of page
page_html = uClient.read()

#html parsing
page_soup = soup(page_html, "html.parser")
containers = []

#loops through pages
for i in range (pgNum+1, lastPage):
    #loop for adding items on page to array
    for j in range(0,len(page_soup.findAll("li", {"class":"s-item"}))):
        #gets all listings on url
        containers.append(page_soup.findAll("li", {"class":"s-item"})[j])
    #goes to next page
    pgNum = pgNum+1
    myUrl = link + str(pgNum)
    uClient = uReq(my_url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")


#close connection
uClient.close();
listings = []


for i in range (0,len(containers)):
    try:
        listing = Listing(containers[i].h3.text, containers[i].find("span",{"class":"s-item__price"}).text,containers[i].find("span",{"class":"s-item__shipping s-item__logisticsCost"}).text, containers[i].find("a",{"href":True})['href'])
        listings.append(listing)
    except:
        print("")

for i in range(0, len(listings)):
    #print(listings[i])
    c = listings[i]
    f.write(c.title.replace(",", " ") + ",,," + c.price + ",,," + c.shipping + ",,," + c.link + "\n")

f.close()
print(len(listings))
