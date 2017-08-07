# Software Design Specification

## Class Diagram
![Class Diagram](https://yuml.me/diagram/scruffy/class/%20[TVDBHandler%7C%7C+getNextEpisode(name:%20string):%20Datetime;+getNextEpisode(uid:%20int):%20Datetime],%20[TheTVDBHandler%7C-apiKey:%20string;-userName:%20string;%20-userKey:%20string;%20-jwtToken:%20string%7C+getNextEpisode(name:%20string):%20Datetime;+getNextEpisode(uid:%20int):%20Datetime],%20[PythonLib::Datetime],%20[TheTVDB.com],%20[TVDBHandler]%5E[TheTVDBHandler],%20[TVDBHandler]uses-.-%3E[PythonLib::Datetime],%20[TheTVDBHandler]uses-.-%3E[TheTVDB.com])

Source code of the Class Diagram:
```
![Class Diagram](
https://yuml.me/diagram/scruffy/class/
[TVDBHandler||+getNextEpisode(name: string): Datetime;+getNextEpisode(uid: int): Datetime],
[TheTVDBHandler|-apiKey: string;-userName: string; -userKey: string; -jwtToken: string|+getNextEpisode(name: string): Datetime;+getNextEpisode(uid: int): Datetime],
[PythonLib::Datetime],
[TheTVDB.com],
[TVDBHandler]^[TheTVDBHandler],
[TVDBHandler]uses-.->[PythonLib::Datetime],
[TheTVDBHandler]uses-.->[TheTVDB.com]
)
```