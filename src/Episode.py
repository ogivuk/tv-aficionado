# class Episode captures information about a single episode.
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

class Episode:
    "Contains information about a single episode."
    def __init__(self):
        self.name = ""
        self.releaseDate = None
        self.season = 0
        self.number =  0
        self.shortDesc = ""
        self.uid = ""
        self.season = None
        self.tvShow = None