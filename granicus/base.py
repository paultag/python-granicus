import requests
import time


class GranicusBase(object):
    GRANICUS_API_BASE = "http://demos.granicuslabs.com/v1"

    def __init__(self, jurisdiction):
        self.jurisdiction = jurisdiction

    def request(self, method, endpoint, params=None, data=None):
        url = "%s/%s/%s.json" % (
            self.GRANICUS_API_BASE,
            self.jurisdiction,
            endpoint
        )

        time.sleep(2)

        try:
            r = requests.request(
                method,
                url,
                params=params,
                data=data
            )
            if "We're sorry, but something went wrong." in r.text:
                raise ValueError("Something went wrong.")
            return r.json()
        except requests.exceptions.ConnectionError:
            print("  Uch, server broke. Backing off quickly.")
            time.sleep(5)
            print("    Retrying request.")
            return self.request(method, endpoint, params=params, data=data)
