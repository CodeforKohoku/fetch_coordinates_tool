from abc import ABCMeta, abstractmethod
import lib.utils as utils


class BaseDriver(metaclass=ABCMeta): # metaclass is "type class" by default

    def __init__(self):
        self._adds   = None
        self._coords = [] # [[x-cord, y-cord]] or [(x-cord, y-cord)]
        self._errs   = [] # failed to locate coords

        # update by subclass
        self.async_mode = False


    @property
    def fetched(self):
        if self._coords:
            return zip(self._adds, self._coords)
        # implicit None returned


    def run(self, adds):
        assert isinstance(adds, list)
        self._adds = adds

        if self.async_mode:
            self._coords = utils.async_run(self.async_fetch_coord, adds)

        else:
            self.run_adds()

        for err in self._errs:
            print(err)


    @abstractmethod 
    def __del__(self): # to clean up drivers and browsers
        pass

    @abstractmethod 
    def new_driver(self):
        pass

    @abstractmethod 
    def run_adds(self):
        pass

    @abstractmethod 
    def async_fetch_coord(self, add):
        pass

    @abstractmethod 
    def fetch_coord(self, add):
        pass
