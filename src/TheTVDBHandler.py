# class TheTVDBHandler is a handler for the connection to thetvdb.com
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

import json
import urllib
import urllib2
import datetime
import TVSeries
import TVDBHandler

class TheTVDBHandler (TVDBHandler.TVDBHandler):
    "Handles the connection to thetvdb.com"
    def __init__(self, userName, userKey, apiKey):
        self.userName = userName
        self.userKey = userKey
        self.apiKey = apiKey
        self._urls = {
            "authentication_login" : "https://api.thetvdb.com/login",
            "authentication_refresh" : "https://api.thetvdb.com/refresh_token",
            "search_TVSeries" : "https://api.thetvdb.com/search/series?name=",
            "series_episodes" : "https://api.thetvdb.com/series/$uid/episodes?page=$pageNumber",
            "series_info" : "https://api.thetvdb.com/series/$uid"
        }
        self._authenticationToken = {
            "jwtToken" : "",
            "expiresOn" : None,
            "validity_inHours" : 24
        }

    def _checkAuthentication(self):
        "Takes care of authentication: checks if authenticated, first time or refresh"
        # 1. Check if the authentication needs to be done from scratch: first time, or expired
        if (self._authenticationToken["jwtToken"] == "") or (self._authenticationToken["expiresOn"] < datetime.datetime.now()):
            data = {
                "apikey": self.apiKey,
                "userkey": self.userKey,
                "username": self.userName
            }
            req = urllib2.Request(self._urls["authentication_login"])
            req.add_header('Accept', 'application/json')
            req.add_header('Content-Type', 'application/json')
            req.add_header('Accept-Language', 'en')
            try:
                response = urllib2.urlopen(req, json.dumps(data))
                self._authenticationToken["jwtToken"] = json.loads(response.read())[u"token"]
                "The token expires in 24h"
                self._authenticationToken["expiresOn"] = datetime.datetime.now() + datetime.timedelta(hours=self._authenticationToken["validity_inHours"])
                response.close()
            except (urllib2.HTTPError, urllib2.URLError), e:
                print('Error: ' + str(e.reason))
                self._authenticationToken = {
                    "jwtToken" : "",
                    "expiresOn" : ""
                }
        # 2. If not, check if the authentication is about to expire (within 1 hour) to refresh it
        else:
            if self._authenticationToken["expiresOn"] - datetime.datetime.now() < datetime.timedelta(hours=1):
                # Refresh the token
                req = urllib2.Request(self._urls["authentication_refresh"])
                req.add_header('Accept', 'application/json')
                req.add_header('Content-Type', 'application/json')
                req.add_header('Accept-Language', 'en')
                req.add_header('Authorization', 'Bearer '+self._jwtToken)
                try:
                    response = urllib2.urlopen(req)
                    self._authenticationToken["jwtToken"] = json.loads(response.read())[u"token"]
                    # The token expires in 24h
                    self._authenticationToken["expiresOn"] = datetime.datetime.now() + datetime.timedelta(hours=24)
                    response.close()
                except (urllib2.HTTPError, urllib2.URLError), e:
                    print('Authentication Error: ' + str(e.reason))
                    self._authenticationToken = {
                        "jwtToken" : "",
                        "expiresOn" : ""
                    }
        # 3. If not, the token is still valid for at least one more hour
            else:
                pass

    def getTVSeries(self, uid):
        url = self._urls["series_info"].replace("$uid",str(uid))
        data = self._getDataFromSource(url)
        tvSeries = TVSeries.TVSeries()
        tvSeries.uid = uid
        tvSeries.name = data[u"data"][u"seriesName"]
        tvSeries.shortDesc = data[u"data"][u"overview"]

        allEpisodesData = self.getAllEpisodesData(uid)
        for episodeData in allEpisodesData:
            episode = TVSeries.Episode()
            episode.name = episodeData["episodeName"]
            if episodeData["firstAired"]:
                episode.releaseDate = datetime.datetime.strptime(episodeData["firstAired"], '%Y-%m-%d').date()
            else:
                episode.releaseDate = None
            episode.uid = episodeData["id"]
            episode.shortDesc = episodeData["overview"]
            episodeNumInSeason = episodeData["airedEpisodeNumber"]
            episodeSeasonNum = episodeData["airedSeason"]
            # Do not consider episodes without release dates
            if episode.releaseDate != None:
                tvSeries.addEpisode(episodeSeasonNum, episodeNumInSeason, episode)

        return tvSeries

    def getTVSeriesUID(self, name):
        "Returns the UID of the TV Series on thetvdb.com"
        url = self._urls["search_TVSeries"]+urllib.quote_plus(name)
        data = self._getDataFromSource(url)[u"data"][0]
        return data[u"id"]

    def getAllEpisodesData(self, uid):
        episodes = []
        nextPage = 1
        while nextPage != None :
            url = self._urls["series_episodes"].replace("$uid",str(uid)).replace("$pageNumber",str(nextPage))
            data = self._getDataFromSource(url)
            episodes = episodes + data[u"data"]
            nextPage = data[u"links"][u"next"]
        return episodes

    def _getDataFromSource(self, requestUrl):
        "Returns data obtained from the source TVDB for given URL"
        self._checkAuthentication()
        req = urllib2.Request(requestUrl)
        req.add_header('Accept', 'application/json')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept-Language', 'en')
        req.add_header('Authorization', 'Bearer '+self._authenticationToken["jwtToken"])
        try:
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            response.close()
            return data
        except (urllib2.HTTPError, urllib2.URLError), e:
            print('Error: ' + str(e.reason))
            return json.dumps("{}")

if __name__ == "__main__":
    # Authenticate
    handler = TheTVDBHandler("Ognjen","EC797502870D09D4","1845172E818BDDF7")

    tvSeriesNamesAndIDs = {
        "Suits" : 247808,
        "Family Guy" : 75978,
        "Last Week Tonight with John Oliver" : 278518,
        "Game of Thrones" : 121361,
        "The Crown" : 305574,
        "Silicon Valley" : 277165,
        "The Americans (2013)" : 261690,
        "Vikings" : 260449,
        "Better Call Saul" : 273181,
        "Narcos" : 282670,
        "Outlander" : 270408
    }

    for (tvSeriesName, tvSeriesID) in tvSeriesNamesAndIDs.items():
        if not tvSeriesID:
            tvSeriesID = handler.getTVSeriesUID(tvSeriesName)
            print(tvSeriesName + ": " + str(tvSeriesID))
        
        tvSeries = handler.getTVSeries(tvSeriesID)
        print ("####################################################")
        print ("# " + tvSeries.name)
        if tvSeries.getLatestEpisodeDate():
            print ("# Latest episode was on: " + tvSeries.getLatestEpisodeDate().strftime('%Y-%b-%d') + " (" + \
                str((datetime.date.today() - tvSeries.getLatestEpisodeDate()).days) + " days ago).")
        else:
            print ("# No episode released yet.")
        if tvSeries.getNextEpisodeDate():
            print ("# Next episode is on:    " + tvSeries.getNextEpisodeDate().strftime('%Y-%b-%d') + " (in " + \
                str((tvSeries.getNextEpisodeDate() - datetime.date.today()).days + 1) + " days).")
        else:
            print ("# No next episode is scheduled.")

    print ("####################################################")
