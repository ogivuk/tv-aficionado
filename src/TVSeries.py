# class TVSeries captures information about a single TV series.
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

class TVSeries:
    "Contains the information about a single TV series"
    def __init__(self):
        self.name = ""
        self.seasons = []
        self.shortDesc = ""
        self.uid = ""
    def getNextEpisode():
        todaysDate = datetime.date.today()
        print (todaysDate)