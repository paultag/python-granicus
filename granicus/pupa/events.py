from granicus.events import Events
from pupa.scrape import Scraper


def make_event_scraper(jurisdiction):
    def _(*args, **kwargs):
        r = GranicusEventScraper(*args, **kwargs)
        r._granicus_jurisdiction = jurisdiction
        return r
    return _


class GranicusEventScraper(Scraper):
    def scrape(self):
        self.wrapper = Events(self._granicus_jurisdiction)
        for event in self.wrapper.getall():
            try:
                yield event.get()
            except ValueError:
                print("  => bad server response for {}".format(event.id))
                continue
