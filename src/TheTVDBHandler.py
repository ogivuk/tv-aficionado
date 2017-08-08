# class TheTVDBHandler is a handler for the connection to thetvdb.com
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

#import socket
import json
import urllib2

class TheTVDBHandler:
    "Handles the connection to thetvdb.com"
    def __init__(self, userName, userKey, apiKey):
        self.userName = userName
        self.userKey = userKey
        self.apiKey = apiKey

        self._authURL = "https://api.thetvdb.com/login"
        self._jwtToken = ""
        self.authenticated = 0

    def authenticate(self):
        "Initializes the connection (authentication)"
        self.authenticated = 0
        self._jwtToken = ""

        data = {
            "apikey": self.apiKey,
            "userkey": self.userKey,
            "username": self.userName
        }
        req = urllib2.Request(self._authURL)
        req.add_header('Accept', 'application/json')
        req.add_header('Content-Type', 'application/json')
        try:
            response = urllib2.urlopen(req, json.dumps(data))
            self._jwtToken = json.loads(response.read())[u"token"]
            self.authenticated = 1
            response.close()
        except (urllib2.HTTPError, urllib2.URLError), e:
            print('Authentication Error: ' + str(e.reason))

    def getNewEpisodeDate(self, name):
        pass
   
    def getNewEpisodeDate(self, uid):
        pass

if __name__ == "__main__":
    handler = TheTVDBHandler("Ognjen","EC797502870D09D4","1845172E818BDDF7")
    handler.authenticate()
    if handler.authenticated != 1:
        print("Authentication failed")
        exit()