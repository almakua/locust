from locust import HttpLocust, TaskSet, task
import time, logging, sys, csv, random
from bs4 import BeautifulSoup

global USER_CREDENTIALS
with open('credentials.csv', 'rb') as f:
    reader = csv.reader(f)
    USER_CREDENTIALS = list(reader)

#USERS = [
#    "marco.bianchi@neen.it,asparago",
#    "user01@neen.it,user01",
#    "user02@neen.it,user02",
#    "user03@neen.it,user03",
#    "user04@neen.it,user04",
#]

BROWSE = [
    "/accessories/eyewear.html",
    "/home-decor/books-music.html",
    "/women/pants-denim.html?occasion=31",
    "/accessories/eyewear.html?price=290-",
    "/accessories/eyewear/retro-chic-eyeglasses.html",
    "/vip.html",
    "/vip/flapover-briefcase.html",
    "/contacts/",
    "/men/shirts.html?color=17",
    "/men/shirts/plaid-cotton-shirt-476.html",
]

SEARCH_TERMS = [
    "glasses",
    "briefcase",
    "shorts",
    "demin",
    "plaid",
    "home",
]

PRODUCTS = [
    "/accessories/eyewear/aviator-sunglasses.html",
    "/accessories/bags-luggage/isla-crossbody-handbag.html",
    "/accessories/bags-luggage/leather-tablet-sleeve.html",
    "/accessories/bags-luggage/rolls-travel-wallet.html",
    "/accessories/bags-luggage/roller-suitcase.html",
    "/jackie-o-round-sunglasses.html",
    "/park-row-throw.html",
    "/vip/flapover-briefcase.html",
    "/vip/rolls-travel-wallet.html",
    "/vip/geometric-candle-holders.html",
    "/vip/madison-rx3400.html",
    "/accessories/bags-luggage/flapover-briefcase.html",
]

class UserBehavior(TaskSet):

    email = "NOT_FOUND"
    password = "NOT_FOUND"

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        if len(USER_CREDENTIALS) > 0:
            self.email, self.password = random.choice(USER_CREDENTIALS)
        #reader = csv.reader(USERS)
        #self.email, self.password  = reader[random.randint(0,len(reader)-1)]

        url = "/customer/account/loginPost"
        r = self.client.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        data = soup.find_all("input", {'name': 'form_key', 'type':'hidden'})
        for data in data:
            formid = (data.get('value'))
        r = self.client.post("/customer/account/loginPost", {
        #                 "login[username]": self.email, "login[password]": self.password , "form_key": formid , "send": "" } )
                         "login[username]": "user01@neen.it", 
                         "login[password]": "user01" , 
                         "form_key": formid , 
                         "send": "" } )
        #logging.info('Login with %s email and %s password', self.email, self.password)

    def logout(self):
        self.client.get("/customer/account/logout" )

    @task(1)
    def search(self):
        self.search = SEARCH_TERMS[random.randint(0,len(SEARCH_TERMS)-1)]
        self.client.post("/catalogsearch/result/", {
            "q": self.search } )


    @task(7)
    def browse(self):
        self.page = BROWSE[random.randint(0,len(BROWSE)-1)]
        self.client.get(self.page)


    @task(2)
    def addcart(self):
        url = PRODUCTS[random.randint(0,len(PRODUCTS)-1)]
        r = self.client.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        data = soup.find("form", {'id': 'product_addtocart_form', 'method':'post'})
        addtocart = (data.get('action'))
        self.client.post(addtocart)

    #@task(1)
    #def index(self):
    #    self.client.get("/")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 40000
    max_wait = 60000

