from locust import HttpLocust, TaskSet, task
import time, logging, sys, csv, random
from bs4 import BeautifulSoup
import browse, search_terms, products

global USER_CREDENTIALS
with open('credentials.csv', 'rb') as f:
    reader = csv.reader(f)
    USER_CREDENTIALS = list(reader)

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

        url = "/customer/account/loginPost"
        r = self.client.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        data = soup.find_all("input", {'name': 'form_key', 'type':'hidden'})
        for data in data:
            formid = (data.get('value'))
        r = self.client.post("/customer/account/loginPost", {
                         #"login[username]": self.email, "login[password]": self.password , "form_key": formid , "send": "" } )
                         "login[username]": "aaa@aaa.com", 
                         "login[password]": "asparago" , 
                         "form_key": formid , 
                         "send": "" } )
        # enable it for debugging purpouse
        # logging.info('Login with %s email and %s password', self.email, self.password)

    def logout(self):
        self.client.get("/customer/account/logout" )

    @task(5)
    def search(self):
        self.search = SEARCH_TERMS[random.randint(0,len(SEARCH_TERMS)-1)]
        self.client.post("/catalogsearch/result/", {
            "q": self.search } )


    @task(35)
    def browse(self):
        self.page = BROWSE[random.randint(0,len(BROWSE)-1)]
        self.client.get(self.page)


    @task(10)
    def addcart(self):
        url = PRODUCTS[random.randint(0,len(PRODUCTS)-1)]
        r = self.client.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        data = soup.find("form", {'id': 'product_addtocart_form', 'method':'post'})
        addtocart = (data.get('action'))
        self.client.post(addtocart)
        
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 7000

