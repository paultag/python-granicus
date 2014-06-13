from granicus.base import GranicusBase


class Events(GranicusBase):
    def get(self, **kwargs):
        return self.request('GET', 'events', params=kwargs)
