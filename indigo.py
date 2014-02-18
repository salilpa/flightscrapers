from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta


class Indigo:
    url = "https://book.goindigo.in/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0",
        "Origin": "https://book.goindigo.in",
        "Referer": "https://book.goindigo.in/",
        }
    error = ""

    def __init__(self, source="BLR", destination="HYD", date=datetime.today() + timedelta(days=5)):
        self.source = source
        self.destination = destination
        self.date = date

    def request(self):
        request_data = {}
        request_data["indiGoOneWaySearch.Origin"] = self.source
        request_data["indiGoOneWaySearch.Destination"] = self.destination
        request_data["indiGoOneWaySearch.DepartureDate"] = self.date.strftime("%d %b %Y")
        request_data["indiGoOneWaySearch.PassengerCounts[0].Count"] = "1"
        request_data["indiGoOneWaySearch.PassengerCounts[0].PaxType"] = "ADT"
        request_data["indiGoOneWaySearch.PassengerCounts[1].Count"] = "0"
        request_data["indiGoOneWaySearch.PassengerCounts[1].PaxType"] = "CHD"
        request_data["indiGoOneWaySearch.InfantCount"] = "0"
        request_data["indiGoOneWaySearch.CurrencyCode"] = "INR"
        request_data["indiGoPromoAuthenticationData.PromoCode"] = ""
        request_data["indiGoPromoAuthenticationData.CustomerNumber"] = ""
        request_data["indiGoOneWaySearch.IsArmedForces"] = "false"
        request_data["indiGoOneWaySearch_Submit"] = "Search"
        try:
            r = requests.post(Indigo.url, request_data, headers=Indigo.headers)
        except requests.exceptions.RequestException as e:
            self.error = str(e)
            return False
        if r.status_code == 404:
            self.error = "404 error"
            return False
        elif r.text.find("price") > 0:
            soup = BeautifulSoup(r.text)
            self.__getDetails(soup)
            return True
        else:
            self.error = "Some other error"
            return False

    def __getDetails(self, soup):
        #set response_json here
        return False

    def get_json(self):
        return self.response_json


