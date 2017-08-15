# class TVDBHandler represents is a base class for handlers
# towards external databases with information about TV series.
# It is intended to be a virtual class that should not be used directly.
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

class TVDBHandler:
    "Handles the connection to external source of TV Series Information"
    def getNextEpisodeDate(self, name):
        pass
    def getNextEpisodeDate(self, uid):
        pass