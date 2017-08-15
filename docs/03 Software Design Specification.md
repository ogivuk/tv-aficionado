# Software Design Specification

## Class Diagram
![Class Diagram](https://yuml.me/diagram/scruffy/class/%20[TVDBHandler%7C%7C+getNextEpisode(name:%20string):%20Episode;+getNextEpisode(uid:%20string):%20Episode],%20[TheTVDBHandler%7C+apiKey:%20string;+userName:%20string;%20+userKey:%20string;+authenticated:%20int;-jwtToken:%20string;_authURL:%20string%7C+TheTVDBHandler(userName:%20string;userKey:%20string;apiKey:%20string);+authenticate():%20void;+getNextEpisode(name:%20string):%20Episode;+getNextEpisode(uid:%20int):%20Episode],%20[Episode%7C+name:%20string;%20+releaseDate:%20Datetime;%20+season:%20int;%20+number:%20int;%20+shortDesc:%20string;%20+uid:%20string],%20[PythonLib::Datetime],%20[TheTVDB.com],%20[TVDBHandler]%5E[TheTVDBHandler],%20[TVDBHandler]%3C%3E-%3E[Episode],%20[Episode]uses-.-%3E[PythonLib::Datetime],%20[TheTVDBHandler]uses-.-%3E[TheTVDB.com])

Source code of the Class Diagram:
```
![Class Diagram](
https://yuml.me/diagram/scruffy/class/
[TVDBHandler||+getNextEpisode(name: string): Episode;+getNextEpisode(uid: string): Episode],
[TheTVDBHandler|+apiKey: string;+userName: string; +userKey: string;+authenticated: int;-jwtToken: string;_authURL: string|+TheTVDBHandler(userName: string;userKey: string;apiKey: string);+authenticate(): void;+getNextEpisode(name: string): Episode;+getNextEpisode(uid: int): Episode],
[TVSeries|+name: string;+shortDesc: string;+uid: string|+getNextEpisode(): Episode],
[Season|+number: int;+tvSeries: TVSeries],
[Episode|+name: string;+releaseDate: Datetime;+season: int;+number: int;+shortDesc: string;+uid: string],
[PythonLib::Datetime],
[TheTVDB.com],
[TVDBHandler]^[TheTVDBHandler],
[TVDBHandler]<>->[TVSeries],
[TVSeries]++tvSeries-seasons 1..*>[Season],
[Season]++season-episodes 1..*>[Episode],
[Episode]uses-.->[PythonLib::Datetime],
[TheTVDBHandler]uses-.->[TheTVDB.com]
)
```