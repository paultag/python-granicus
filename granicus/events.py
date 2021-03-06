from granicus.base import GranicusBase
from pupa.scrape.event import Event as OCDEvent
import dateutil.parser


def parsedatetime(date):
    return dateutil.parser.parse(date)


def fix_participant(participant):
    participant['type'] = {
        "meeting body": "organization",
    }[participant.pop('participant_type')]
    participant['id'] = participant.pop('participant_id')
    participant['name'] = participant.pop('participant')
    return participant


def fix_agenda(item):
    if 'media' in item:
        if item['media'] == {}:
            item['media'] = []
        else:
            item['media'] = [item['media']]
    if item['description'] == "":
        item['description'] = "unknown"
    return item


def fix_location(location):
    if 'coordinates' in location:
        if location['coordinates'] == []:
            location['coordinates'] = {}
        else:
            location['coordinates'] = dict(location['coordinates'])
    return location


class Event(GranicusBase):
    def __init__(self, jurisdiction, id, data):
        super(Event, self).__init__(jurisdiction)
        self.id = id
        self.data = data

    def get(self, **kwargs):
        event = self.request("GET", 'events/%s' % (self.id), params=kwargs)
        if event['description'] == '':
            event['description'] = "unknown"

        ocde = OCDEvent(
            event['description'],
            parsedatetime(event['when']),
            "",
        )
        ocde.location = fix_location(event.get('location', {"name": "unknown"}))
        blacklisted = ("when", "description", "location")
        for k, v in event.items():
            if k in blacklisted:
                continue

            if k == 'id':
                k = '_id'

            if k == 'organization':
                # ocde.add_participant(id=v['id'], name=v['name'])
                continue

            if k == 'participants':
                for p in v:
                    fix_participant(p)

            if k == 'agenda':
                for p in v:
                    fix_agenda(p)

            if k == 'status':
                try:
                    v = {"scheduled": "tentative"}[v]
                except KeyError:
                    pass

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
