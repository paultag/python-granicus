import requests


class GranicusAPIIterator(object):
    def __init__(self, method):
        self.method = method
        self.page = -1
        self.max_pages = 0

    # def iterpage(self):
    #     self.page += 1
    #     response = self.method(page=self.page)
    #
    # def iterate(self):
    #     while self.page < self.max_pages:
    #         yield from self.iterpage()

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

        return requests.request(
            method,
            url,
            params=params,
            data=data
        ).json()
