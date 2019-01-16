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
    "Better Call Saul" : 273181,
    "Black Mirror" : 253463,
    "The Bridge (2011)" : 252019,
    "Family Guy" : 75978,
    "Fargo" : 269613,
    "Game of Thrones" : 121361,
    "Homeland" : 247897,
    "House of Cards (2013)" : 262980,
    "Last Week Tonight with John Oliver" : 278518,
    "Love (2016)" : 305378,
    "Modern Family" : 95011,
    "Mr. Robot" : 289590,
    "Narcos" : 282670,
    "Narcos: Mexico (2018)": 353232,
    "New Girl (2011-2018)" : 248682,
    "Norsemen (2016)" : 318009,
    "Outlander (2014)" : 270408,
    "Ozark (2017)" : 329089,
    "Peaky Blinders (2013)" : 270915,
    "Sherlock (2010)" : 176941,
    "Silicon Valley (2014)" : 277165,
    "Sneaky Pete (2015)" : 300166,
    "Suits (2011)" : 247808,
    "Taboo (2017)" : 292157,
    "The Big Bang Theory (2007)" : 80379,
    "The Blacklist (2013)" : 266189,
    "The Crown (2016)" : 305574,
    "The Marvelous Mrs. Maisel (2017)" : 326791,
    "True Detective (2014)" : 270633,
    "Vikings (2013)" : 260449,
    "Westworld (2016)" : 296762   
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