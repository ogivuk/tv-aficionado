# class Season captures information about a single season.
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

class Season:
    "Contains the information about a single season"
    def __init__(self, tvSeries):
        self.number = 0
        self.tvSeries = tvSeries
        self.episodes = []
        self.number =  0
        self.shortDesc = ""
        self.uid = ""