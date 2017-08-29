# Information about latest and next release dates of favorite TV Series
#
# Author: Ognjen Vukovic (ognjen.m.vukovic@gmail.com)
# Date: August 2017
#

import datetime
import TheTVDBHandler

handler = TheTVDBHandler.TheTVDBHandler("Ognjen","EC797502870D09D4","1845172E818BDDF7")

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