# class Episode captures information about a single episode.
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

class Episode:
    "Handles the connection to external source of TV Series Information"
    def __init__(self):
        self.name = ""
        self.releaseDate = Nothing
        self.season = 0
        self.number=  0
        self.shortDesc = ""
        self.uid = ""