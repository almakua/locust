from locust import HttpLocust, TaskSet, task, TaskSequence, seq_task
import time, logging, sys, csv, random
from bs4 import BeautifulSoup
from browse import *
from search_terms import *
from products import *

global USER_CREDENTIALS
with open('credentials.csv', 'rb') as f:
    reader = csv.reader(f)
    USER_CREDENTIALS = list(reader)

class UserBehavior(TaskSet):

    @task(1)
    def search(self):
        self.search = SEARCH_TERMS[random.randint(0,len(SEARCH_TERMS)-1)]
        self.client.post("/catalogsearch/result/", {
            "q": self.search } )


    @task(3)
    def browse(self):
        self.page = BROWSE[random.randint(0,len(BROWSE)-1)]
        self.client.get(self.page)

class pressureTest(TaskSequence):

    email = "NOT_FOUND"
    password = "NOT_FOUND"

    @seq_task(1)
    def index(self):
        self.client.get("/" )

    @seq_task(2)    
    def login(self):
        if len(USER_CREDENTIALS) > 0:
            self.email, self.password = random.choice(USER_CREDENTIALS)
        url = "/customer/account/login/"
        r = self.client.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        data = soup.find("input", {'name': 'form_key', 'type':'hidden'})
        #for data in data:
        formid = (data.get('value'))
        r = self.client.post("/customer/account/loginPost", {
                         "login[username]": self.email, "login[password]": self.password , "form_key": formid , "send": "" } )

        # enable it for debugging purpouse
        logging.info('Login with %s email and %s password', self.email, self.password)

    @seq_task(3)
    @task(7)
    def browse(self):
        self.page = BROWSE[random.randint(0,len(BROWSE)-1)]
        self.client.get(self.page)

    @seq_task(4)
    @task(2)
    def search(self):
        self.search = SEARCH_TERMS[random.randint(0,len(SEARCH_TERMS)-1)]
        self.client.post("/catalogsearch/result/", {
            "q": self.search } )

    @seq_task(5)
    @task(2)
    def addcart(self):
        url = PRODUCTS[random.randint(0,len(PRODUCTS)-1)]
        r = self.client.get(url)
        time.sleep(1)
        soup = BeautifulSoup(r.content, "html.parser")
        data = soup.find("form", {'id': 'product_addtocart_form', 'method':'post'})
        addtocart = (data.get('action'))
        self.client.post(addtocart)


    @seq_task(5)
    @task(1)
    def checkout(self):
        self.client.post("/gomage_checkout/onepage/ajax/", { "billing_address_id": "570201", "billing[firstname]": "aaa", "billing[lastname]": "aaa", "billing[fiscaleitalia_fiscalcode]": "aaa12345678", "billing[street][]": "aaa", "billing[street][]": "12", "billing[city]": "MilAno", "billing[region_id]": "610", "billing[region]": "", "billing[postcode]": "20000", "billing[country_id]": "IT", "billing[telephone]": "3333333333", "billing[company]": "", "billing[vat_id]": "", "billing[pec]": "", "billing[sdi_code]": "", "billing[use_for_shipping]": "1", "shipping_address_id": "570201", "shipping[firstname]": "aaa", "shipping[lastname]": "aaa", "shipping[street][]": "aaa", "shipping[street][]": "12", "shipping[city]": "MilAno", "shipping[region_id]": "610", "shipping[region]": "", "shipping[postcode]": "20000", "shipping[country_id]": "IT", "shipping[telephone]": "3333333333", "shipping_method": "owebiashipping1_case_1", "payment[method]": "bankpayment", "remove": "0", "coupon_code": "", "customer_comment": "", "accept_terms": "1" , "action": "save_payment_methods"} )
        self.client.post("/gomage_checkout/onepage/save/", { "billing_address_id": "570201", "billing[firstname]": "aaa", "billing[lastname]": "aaa", "billing[fiscaleitalia_fiscalcode]": "aaa12345678", "billing[street][]": "aaa", "billing[street][]": "12", "billing[city]": "MilAno", "billing[region_id]": "610", "billing[region]": "", "billing[postcode]": "20000", "billing[country_id]": "IT", "billing[telephone]": "3333333333", "billing[company]": "", "billing[vat_id]": "", "billing[pec]": "", "billing[sdi_code]": "", "billing[use_for_shipping]": "1", "shipping_address_id": "570201", "shipping[firstname]": "aaa", "shipping[lastname]": "aaa", "shipping[street][]": "aaa", "shipping[street][]": "12", "shipping[city]": "MilAno", "shipping[region_id]": "610", "shipping[region]": "", "shipping[postcode]": "20000", "shipping[country_id]": "IT", "shipping[telephone]": "3333333333", "shipping_method": "owebiashipping1_case_1", "payment[method]": "bankpayment", "remove": "0", "coupon_code": "", "customer_comment": "", "accept_terms": "1" } )

    @seq_task(6)
    @task(1)
    def logout(self):
        self.client.get("/customer/account/logout" )

class lurker(HttpLocust):
    task_set = UserBehavior
    weight = 1
    min_wait = 700
    max_wait = 1500

class loggedUser(HttpLocust):
    task_set = pressureTest
    weight = 2
    min_wait = 500
    max_wait = 1500