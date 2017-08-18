# class TheTVDBHandler is a handler for the connection to thetvdb.com
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

# TO DO:
# 3. Use classes, especially TVSeries,
#    it will be easier later for the backend writting into the DB
# 4. Handle error resonse messages
# 5. Create Unit tests

import json
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
            "episodes" : "https://api.thetvdb.com/series/$uid/episodes?page=$pageNumber"
        }
        self._authenticationToken = {
            "jwtToken" : "",
            "expiresOn" : None
        }

    def _checkAuthentication(self):
        "Performs authentication: first time or refresh"
        if (self._authenticationToken["jwtToken"] == "") or (self._authenticationToken["expiresOn"] < datetime.datetime.now()):
            "First authentication, or authentication has expired"
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
                self._authenticationToken["expiresOn"] = datetime.datetime.now() + datetime.timedelta(hours=24)
                response.close()
            except (urllib2.HTTPError, urllib2.URLError), e:
                print('Error: ' + str(e.reason))
                self._authenticationToken = {
                    "jwtToken" : "",
                    "expiresOn" : ""
                }
        else:
            # Check if the token is about to expire (within next 1 hour)
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
            else:
                # The token is still valid (at least for an hour longer)
                pass

    def _getDataFromSource(self, requestUrl):
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


    def getTVSeries(self, name):
        self._checkAuthentication()
        req = urllib2.Request(self._urls["search_TVSeries"]+name)
        req.add_header('Accept', 'application/json')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Bearer '+self._jwtToken)
        tvSeries = None

        try:
            response = urllib2.urlopen(req)
            tvSeries = TVSeries.TVSeries()
            data = json.loads(response.read())[u"data"][0]
            tvSeries.name = data[u"seriesName"]
            tvSeries.shortDesc = data[u"overview"]
            tvSeries.uid = data[u"id"]
            response.close()
        except (urllib2.HTTPError, urllib2.URLError), e:
            print('Error: ' + str(e.reason))
        # To Do: consider when token expired
        return tvSeries

    def getTVSeriesUID(self, name):
        "Returns the UID of the TV Series on thetvdb.com"
        url = self._urls["search_TVSeries"]+name.replace(" ","%20")
        data = self._getDataFromSource(url)[u"data"][0]
        return data[u"id"]

    def getNextEpisodeDate(self, uid):   
        "Returns the release date of the next episode"
        episodes = self.getAllEpisodes(uid)
        todaysDate = datetime.date.today()
        notAiredEpisodesDates = []
        for episode in episodes:
            if episode["firstAired"] != "" and datetime.datetime.strptime(episode["firstAired"], '%Y-%m-%d').date()>=todaysDate:
                notAiredEpisodesDates.append(episode["firstAired"])
        if len(notAiredEpisodesDates)>0:
            daysDifference = datetime.datetime.strptime(min(notAiredEpisodesDates), '%Y-%m-%d').date()-todaysDate
            return(min(notAiredEpisodesDates) + " (in " + str(daysDifference.days) + " days).")
        else:
            return "No episode scheduled"

    def getAllEpisodes(self, uid):
        episodes = []
        nextPage = 1
        lastPage = 1 #to be readjusted after the first received data
        while nextPage != None :
            url = self._urls["episodes"].replace("$uid",str(uid)).replace("$pageNumber",str(nextPage))
            data = self._getDataFromSource(url)
            episodes = episodes + data[u"data"]
            nextPage = data[u"links"][u"next"]
        return episodes

    def getLatestEpisodeDate(self, uid):   
        "Returns the release date of the most recent episode"
        episodes = self.getAllEpisodes(uid)
        todaysDate = datetime.date.today()
        airedEpisodesDates = []
        for episode in episodes:
            if episode["firstAired"] != "" and datetime.datetime.strptime(episode["firstAired"], '%Y-%m-%d').date()<todaysDate:
                airedEpisodesDates.append(episode["firstAired"])
        if len(airedEpisodesDates)>0:
            daysDifference = datetime.datetime.strptime(max(airedEpisodesDates), '%Y-%m-%d').date()-todaysDate
            return(max(airedEpisodesDates) + " (" + str(-daysDifference.days) + " days ago).")
        else:
            return("The series has not starte airing yet.")

if __name__ == "__main__":
    # Authenticate
    handler = TheTVDBHandler("Ognjen","EC797502870D09D4","1845172E818BDDF7")
#    handler.authenticate()
#    if handler.authenticated != 1:
#        print("Authentication failed")
#        exit()

    # Test getting a TV series
    uid = handler.getTVSeriesUID("Suits")
    print ("Suits latest:" + handler.getLatestEpisodeDate(uid))
    print ("Suits next:" + handler.getNextEpisodeDate(uid))
    uid = handler.getTVSeriesUID("Family Guy")
    print ("Family Guy latest:" + handler.getLatestEpisodeDate(uid))
    print ("Family Guy next:" + handler.getNextEpisodeDate(uid))
    uid = handler.getTVSeriesUID("Last Week Tonight with John Oliver")
    print ("Last Week Tonight latest: " + handler.getLatestEpisodeDate(uid))
    print ("Last Week Tonight next: " + handler.getNextEpisodeDate(uid))
    uid = handler.getTVSeriesUID("Game of Thrones")
    print ("Game of Thrones latest: " + handler.getLatestEpisodeDate(uid))
    print ("Game of Thrones next: " + handler.getNextEpisodeDate(uid))
    uid = handler.getTVSeriesUID("Crown")
    print ("Crown latest: " + handler.getLatestEpisodeDate(uid))
    print ("Crown next: " + handler.getNextEpisodeDate(uid))
    uid = handler.getTVSeriesUID("Silicon Valley")
    print ("Silicon Valley latest: " + handler.getLatestEpisodeDate(uid))
    print ("Silicon Valley next: " + handler.getNextEpisodeDate(uid))
    tvShow = "The Americans (2013)"
    uid = handler.getTVSeriesUID(tvShow)
    print (tvShow + " latest: " + handler.getLatestEpisodeDate(uid))
    print (tvShow + " next: " + handler.getNextEpisodeDate(uid))
    tvShow = "Vikings"
    uid = handler.getTVSeriesUID(tvShow)
    print (tvShow + " latest: " + handler.getLatestEpisodeDate(uid))
    print (tvShow + " next: " + handler.getNextEpisodeDate(uid))
    tvShow = "Better Call Saul"
    uid = handler.getTVSeriesUID(tvShow)
    print (tvShow + " latest: " + handler.getLatestEpisodeDate(uid))
    print (tvShow + " next: " + handler.getNextEpisodeDate(uid))
    tvShow = "Narcos"
    uid = handler.getTVSeriesUID(tvShow)
    print (tvShow + " latest: " + handler.getLatestEpisodeDate(uid))
    print (tvShow + " next: " + handler.getNextEpisodeDate(uid))