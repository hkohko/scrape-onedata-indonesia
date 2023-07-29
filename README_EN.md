# scrape-onedata-indonesia
webscrape page and json api link from [katalog.data.go.id/dataset](https://katalog.data.go.id/dataset)  

**uses sqlite3**

scraping is done sequentially (first the web pages, then the json api links)

# Description

This CLI app gathers and store json api links inside sqlite3 database.  

database schema:  
`CREATE TABLE halaman_web(halaman INTEGER,link TEXT, PRIMARY KEY(link))STRICT;`  
`CREATE TABLE json_api(link TEXT,json_link TEXT PRIMARY KEY)STRICT;`  
`CREATE TABLE json_metadata(json_api_rowid INTEGER,sumber_data TEXT,nama_file TEXT,deskripsi TEXT,link_download TEXT PRIMARY KEY)STRICT;`

# How to use
Scrapes the first 5 pages by default:
```
python start_scraping.py
```
accepts three keyword arguments: `mulai`, `selesai`, `interval`  
`mulai, selesai` -> `mulai` = starting page number, `selesai` = ending page number  
`interval` -> float, set GET request interval (in seconds) 
```
python start_scraping.py mulai=1 selesai=100 interval=0
```
json api link can be scraped separately (if web page scraping is terminated midway):
```
python .\src\json_links.py
```
(Optional) compile file download links from each json api link: 
```
python .\src\download_links.py
```

