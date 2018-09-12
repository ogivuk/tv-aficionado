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
    "Handles the connection to thetvdb.com, receives config in JSON format."
    def __init__(self, config):
        # make the dependency on urllib2 explicit to help unit testing (Dependency Injection)
        self._http_client = urllib2
        # parse the configuration parameters
        cfg = json.loads(config)
        self.userName = cfg["userName"]
        self.userKey = cfg["userKey"]
        self.apiKey = cfg["apiKey"]
        self._urls = {
            "authentication_login" : cfg["urls"]["authentication_login"],
            "authentication_refresh" : cfg["urls"]["authentication_refresh"],
            "search_TVSeries" : {
                "url" : cfg["urls"]["search_TVSeries"]["url"],
                "param" : cfg["urls"]["search_TVSeries"]["param"]
            },
            "series_episodes" : {
                "url": cfg["urls"]["series_episodes"]["url"],
                "param1" : cfg["urls"]["series_episodes"]["param1"],
                "param2" : cfg["urls"]["series_episodes"]["param2"]
            },
            "series_info" : {
                "url" : cfg["urls"]["series_info"]["url"],
                "param" : cfg["urls"]["series_info"]["param"]
            }
        }
        self._authenticationToken = {
            "jwtToken" : "",
            "expiresOn" : None,
            "validity_inHours" : cfg["token_validity"]
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
            req = self._http_client.Request(self._urls["authentication_login"])
            req.add_header('Accept', 'application/json')
            req.add_header('Content-Type', 'application/json')
            req.add_header('Accept-Language', 'en')
            try:
                response = self._http_client.urlopen(req, json.dumps(data))
                self._authenticationToken["jwtToken"] = json.loads(response.read())[u"token"]
                #The token expires in 24h
                self._authenticationToken["expiresOn"] = datetime.datetime.now() + datetime.timedelta(hours=self._authenticationToken["validity_inHours"])
                response.close()
            except (self._http_client.HTTPError, self._http_client.URLError), e:
                print('Error: ' + str(e.reason))
                self._authenticationToken = {
                    "jwtToken" : "",
                    "expiresOn" : ""
                }
        # 2. If not, check if the authentication is about to expire (within 1 hour) to refresh it
        else:
            if self._authenticationToken["expiresOn"] - datetime.datetime.now() < datetime.timedelta(hours=1):
                # Refresh the token
                req = self._http_client.Request(self._urls["authentication_refresh"])
                req.add_header('Accept', 'application/json')
                req.add_header('Content-Type', 'application/json')
                req.add_header('Accept-Language', 'en')
                req.add_header('Authorization', 'Bearer '+self._jwtToken)
                try:
                    response = self._http_client.urlopen(req)
                    self._authenticationToken["jwtToken"] = json.loads(response.read())[u"token"]
                    # The token expires in 24h
                    self._authenticationToken["expiresOn"] = datetime.datetime.now() + datetime.timedelta(hours=24)
                    response.close()
                except (self._http_client.HTTPError, self._http_client.URLError), e:
                    print('Authentication Error: ' + str(e.reason))
                    self._authenticationToken = {
                        "jwtToken" : "",
                        "expiresOn" : ""
                    }
        # 3. If not, the token is still valid for at least one more hour
            else:
                pass

    def getTVSeries(self, uid):
        url = self._urls["series_info"]["url"]\
            .replace(self._urls["series_info"]["param"],str(uid))
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
        url = self._urls["search_TVSeries"]["url"]\
            .replace(self._urls["search_TVSeries"]["param"],urllib.quote_plus(name))
        #url = self._urls["search_TVSeries"]+urllib.quote_plus(name)
        data = self._getDataFromSource(url)[u"data"][0]
        return data[u"id"]

    def getAllEpisodesData(self, uid):
        episodes = []
        nextPage = 1
        while nextPage != None :
            url = self._urls["series_episodes"]["url"]\
                .replace(self._urls["series_episodes"]["param1"],str(uid))\
                .replace(self._urls["series_episodes"]["param2"],str(nextPage))
            data = self._getDataFromSource(url)
            episodes = episodes + data[u"data"]
            nextPage = data[u"links"][u"next"]
        return episodes

    def _getDataFromSource(self, requestUrl):
        "Returns data obtained from the source TVDB for given URL"
        self._checkAuthentication()
        req = self._http_client.Request(requestUrl)
        req.add_header('Accept', 'application/json')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept-Language', 'en')
        req.add_header('Authorization', 'Bearer '+self._authenticationToken["jwtToken"])
        try:
            response = self._http_client.urlopen(req)
            data = json.loads(response.read())
            response.close()
            return data
        except (self._http_client.HTTPError, self._http_client.URLError), e:
            print('Error: ' + str(e.reason))
            return json.dumps("{}")
