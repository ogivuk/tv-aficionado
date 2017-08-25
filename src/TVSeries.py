# class TVSeries captures information about a single TV series.
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

import datetime

class Episode:
    "Contains information about a single episode."
    def __init__(self):
        self.name = ""
        self.releaseDate = None
        self.shortDesc = ""
        self.uid = None

class Season:
    "Contains the information about a single season, including its eposides"
    def __init__(self):
        self.episodes = []
        self.uid = None
        self.status = None

class TVSeries:
    "Contains the information about a single TV series, including its seasons and episodes"
    def __init__(self):
        self.name = ""
        self.seasons = []
        self.shortDesc = ""
        self.sourceUID = ""

    def getNextEpisode(self):
        "Returns the next episode to be released, it would consider if it is on the today's date"
        currSeasonID, prevSeasonID, nextSeasonID = self._getOngoingSeason()
        if currSeasonID:
            # Find the episode to be released
            lastEpisodeIdx = len(self.seasons[currSeasonID].episodes)-1
            todaysDate = datetime.date.today()
            for cntEpisode in range(1, lastEpisodeIdx+1):
                if self.seasons[currSeasonID].episodes[cntEpisode].releaseDate >= todaysDate:
                    # found it!
                    return self.seasons[currSeasonID].episodes[cntEpisode]
        else:
            # Not currently airing, check the next season
            if nextSeasonID:
                # first episode in the next season
                return self.seasons[nextSeasonID].episodes[1]
            else:
                # no next season planed
                return None
        # If it comes here, something went wrong
        return None

    def getNextEpisodeDate(self):   
        "Returns the release date of the next episode"
        nextEpisode = self.getNextEpisode()
        if nextEpisode:
            return nextEpisode.releaseDate
        else:
            return None

    def getLatestEpisode(self):
        "Returns the latest episode that was released, it would not consider if it is on the today's date"
        currSeasonID, prevSeasonID, nextSeasonID = self._getOngoingSeason()
        if currSeasonID:
            # Find the episode that was last released
            lastEpisodeIdx = len(self.seasons[currSeasonID].episodes)-1
            todaysDate = datetime.date.today()
            for cntEpisode in range(1, lastEpisodeIdx+1):
                if self.seasons[currSeasonID].episodes[cntEpisode].releaseDate >= todaysDate:
                    # found it! The latest episode is the one before
                    return self.seasons[currSeasonID].episodes[cntEpisode-1]
        else:
            # Not currently airing, check the previous season
            if prevSeasonID:
                # last episode in the previous season
                return self.seasons[prevSeasonID].episodes[len(self.seasons[prevSeasonID].episodes)-1]
            else:
                # no episode aired
                return None
        # If it comes here, something went wrong
        return None

    def getLatestEpisodeDate(self):   
        "Returns the release date of the latest episode"
        latestEpisode = self.getLatestEpisode()
        if latestEpisode:
            return latestEpisode.releaseDate
        else:
            return None

    def addEpisode(self, episodeSeasonNum, episodeNumInSeason, episode):
        "Adds the episode object to the appropriate season in the appropriate place"
        # Check if the season already exists, and if not create it and all before that one
        if len(self.seasons)<=episodeSeasonNum:
            # extend the self.seasons array with seasons until and incl. the episode's season
            for cnt in range(len(self.seasons), episodeSeasonNum+1):
                self.seasons.append(Season())

        # Create any episode placeholders in the season until and incl. this episode
        for cnt in range(len(self.seasons[episodeSeasonNum].episodes), episodeNumInSeason + 1):
            self.seasons[episodeSeasonNum].episodes.append(Episode())

        # Append or update the existing episode
        self.seasons[episodeSeasonNum].episodes[episodeNumInSeason] = episode

    def _getOngoingSeason(self):
        "Returns (if exists) the indices of ongoing season, previous season, and next season"
        # Find the season that is currently airing (if exists)
        todaysDate = datetime.date.today()
        for cntSeason in range(1, len(self.seasons)):
            lastEpisodeIdx = len(self.seasons[cntSeason].episodes)-1
            if self.seasons[cntSeason].episodes[1].releaseDate < todaysDate and \
                self.seasons[cntSeason].episodes[lastEpisodeIdx].releaseDate >= todaysDate:
                # this is the ongoing season
                currSeason = cntSeason
                if currSeason > 1:
                    prevSeason = currSeason - 1
                else:
                    prevSeason = None
                if currSeason < len(self.seasons) - 1:
                    nextSeason = currSeason + 1
                else:
                    nextSeason = None
                return (currSeason, prevSeason, nextSeason)
            else:
                # check if we are waiting on the next season
                if self.seasons[cntSeason].episodes[1].releaseDate > todaysDate:
                    # cntSeason is actually next season, there is no current season
                    currSeason = None
                    nextSeason = cntSeason
                    if cntSeason > 1:
                        prevSeason = cntSeason - 1
                    else:
                        prevSeason = None
                    return (currSeason, prevSeason, nextSeason)
        # If it comes to here, it means that the show has no current season and no scheduled seasons
        # Check if it has any seasons (exclude the specials, Season 0)
        if len(self.seasons)>1:
            return (None, len(self.seasons)-1, None)
        else:
            return (None, None, None)