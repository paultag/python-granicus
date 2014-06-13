from granicus.base import GranicusBase
from pupa.scrape.event import Event as OCDEvent


class Event(GranicusBase):
    def __init__(self, jurisdiction, id, data):
        super(Event, self).__init__(jurisdiction)
        self.id = id
        self.data = data

    def get(self, **kwargs):
        event = self.request("GET", 'events/%s' % (self.id), params=kwargs)
        ocde = OCDEvent(
            event['description'],
            event['when'],
            event.get('location', "unknown")
        )
        blacklisted = ("when", "description", "location")
        for k, v in event.items():
            if k in blacklisted:
                continue

            if k == 'id':
                k = '_id'

            if k == 'organization':
                # ocde.add_participant(id=v['id'], name=v['name'])
                continue

            setattr(ocde, k, v)
        ocde.validate()
        return ocde


class Events(GranicusBase):
    def _get(self, **kwargs):
        return self.request('GET', 'events', params=kwargs)

    def getall(self, **kwargs):
        page = -1
        max_pages = 0
        while page < max_pages:
            page += 1
            data = self._get(page=page)
            page = data.get("current_page")
            results = data.get("results", [])
            max_pages = (data.get("total_entries", 0) / data.get("per_page", 1))
            for el in results:
                yield Event(self.jurisdiction, el.get("id"), data)
