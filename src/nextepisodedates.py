# Information about latest and next release dates of favorite TV Series
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

import datetime
import json
import TheTVDBHandler

theTVDBHandler_config = {
    "userName" : "Ognjen",
    "userKey" : "EC797502870D09D4",
    "apiKey" : "1845172E818BDDF7",
    "token_validity" : 24,
    "urls": {
        "authentication_login" : "https://api.thetvdb.com/login",
        "authentication_refresh" : "https://api.thetvdb.com/refresh_token",
        "search_TVSeries" : {
                "url" : "https://api.thetvdb.com/search/series?name=$name",
                "param" : "$name"
        },
        "series_episodes" : {
            "url" : "https://api.thetvdb.com/series/$uid/episodes?page=$pageNumber",
            "param1" : "$uid",
            "param2" : "$pageNumber"
        },
        "series_info" : {
            "url" : "https://api.thetvdb.com/series/$uid",
            "param" : "$uid"
        }
    }
}

handler = TheTVDBHandler.TheTVDBHandler(json.dumps(theTVDBHandler_config))

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
    "Outlander" : 270408,
    "The Bridge (2011)" : 252019,
    "Homeland" : 247897,
    "Modern Family" : 95011,
    "House of Cards (2013)" : 262980,
    "Mr. Robot" : 289590,
    "Sherlock" : 176941,
    "Sneaky Pete" : 300166,
    "Taboo (2017)" : 292157,
    "The Mick" : 311818,
    "Westworld" : 296762
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