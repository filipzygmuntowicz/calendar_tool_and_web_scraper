import requests
from json.decoder import JSONDecodeError
import json
from task1_view import view


class Seller:

    def __init__(
            self, domain):
        self.domain = domain
        self.contractors = []

    def add_contractor(self, contractor):
        if contractor not in self.contractors:
            self.contractors.append(contractor)


class Sellers:

    def __init__(self):
        self.dictionary = {}

    def add_to_dictionary(self, seller_domain, seller):
        self.dictionary[seller_domain] = seller

    def add_contractor_to_url(self, seller_domain, contractor):
        self.dictionary[seller_domain].add_contractor(contractor)


class BadJsonError(Exception):
    pass


max_depth = 0
sellers = Sellers()


def get_sellers(url):
    global max_depth
    try:
        data = requests.get(
            "http://" + url + "/sellers.json", timeout=5).json()
        domains_to_check = []
        if isinstance(data, str) or isinstance(
                data, int) or isinstance(data, float):
            raise BadJsonError
        if "sellers" in data.keys():
            data = data["sellers"]
        else:
            data = [data]
        for seller in data:
            if "domain" in seller and seller["domain"] != "":
                domain = seller["domain"]
                if "name" in seller:
                    name = seller["name"]
                else:
                    name = "confidential"
                sellers.add_contractor_to_url(
                    url, {"name": name, "domain": domain})
                if "seller_type" in seller:
                    if ((seller["seller_type"] == "INTERMEDIARY" or
                            seller["seller_type"] == "BOTH") and
                            domain not in sellers.dictionary):
                        domains_to_check.append(domain)
                        sellers.add_to_dictionary(domain, Seller(domain))
                elif "directness" in seller:
                    if ((seller["directness"] == "RESELLER" or
                            seller["directness"] == "BOTH") and
                            domain not in sellers.dictionary):
                        domains_to_check.append(domain)
                        sellers.add_to_dictionary(domain, Seller(domain))
            else:
                sellers.add_contractor_to_url(
                    url, {
                        "name": "confidential",
                        "domain": "confidential"
                    })
        for index, domain in enumerate(domains_to_check):
            if index == 0:
                max_depth = max_depth + 1
                print(max_depth)
            get_sellers(domain)
            print(domain + " checked!\n" + str(len(domains_to_check) -
                  index) + " domains left to check.")
            print(domain + " checked!")


#    except (JSONDecodeError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.SSLError, BadJsonError, requests.exceptions.ChunkedEncodingError, requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL, AttributeError) as e:
# The data sources are flawed and inconsistent, I could list each and every exception like above but with time new flawed sites would spawn with new errors that I can't predict, that's why I used just a general Exception
    except Exception as e:
        n = str(type(e).__name__)
        print("failed: " + url + " with error" + n)


if __name__ == '__main__':
    sellers.add_to_dictionary("openx.com", Seller("openx.com"))
    print("program started")
    get_sellers("openx.com")
    final_data = []
    for seller in sellers.dictionary.values():
        final_data.append(
            {"domain": seller.domain, "contractors": seller.contractors})
    with open('finaldata.json', 'w') as outfile:
        json.dump({"items": final_data}, outfile)
    with open('maxdepth.txt', 'w', encoding="UTF-8") as file:
        file.write(str(max_depth))
    view(final_data, str(max_depth))
