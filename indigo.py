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
    response_json = {}

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
        elif r.text.find("<div class=\"price-itinerary\">") > 0:
            soup = BeautifulSoup(r.text)
            self.__getDetails(soup)
            return True
        else:
            self.error = "Some other error"
            return False

    def __getDetails(self, soup):
        #set response_json here
        self.response_json["source"] = self.source
        self.response_json["destination"] = self.destination
        self.response_json["checked_time"] = datetime.today()
        self.response_json["date"] = self.date
        result_table = soup.find("table", {"class":"availability-result-table group"})
        flights = []
        for row in result_table.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) > 3:
                flight_object = {
                    "flight_number" : [],
                    "departure_time" : [],
                    "arrival_time" : []
                }
                for flight_number in tds[0].text.split("\n"):
                    if len(flight_number.strip()) > 0:
                        flight_object["flight_number"].append(flight_number.strip())
                flight_object["flight_number"] = self.get_multiple_data_from_text(tds[0].text.strip())
                flight_object["departure_time"] = self.get_multiple_data_from_text(tds[1].text.strip())
                flight_object["arrival_time"] = self.get_multiple_data_from_text(tds[2].text.strip())
                flight_object["regular_fare"] = float(re.sub(',','',re.findall('[\d,.]+',tds[3].text.strip())[0]))
                flights.append(flight_object)
        self.response_json["flights"] = flights

    def get_multiple_data_from_text(self, text):
        result = []
        for ind_object in text.split("\n"):
            if len(ind_object.strip()) > 0:
                result.append(re.sub(' +',' ',ind_object.strip()))
        return result

    def get_json(self):
        return self.response_json


