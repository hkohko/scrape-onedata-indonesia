# scrape-onedata-indonesia
[readme but english](README_EN.md)  
scrape link web dan json api link dari [katalog.data.go.id/dataset](https://katalog.data.go.id/dataset)  

**menggunakan database sqlite3**

scraping dilakukan secara sequential (halaman web terlebih dahulu, baru json link nya)

# Deskripsi

Aplikasi CLI ini mengumpukan link api json dan menyimpannya dalam database sqlite3  
Di dalam database `db\onedata_db.db`ada tiga table dengan skema:  

`CREATE TABLE halaman_web(halaman INTEGER,link TEXT, PRIMARY KEY(link))STRICT;`  
`CREATE TABLE json_api(link TEXT,json_link TEXT PRIMARY KEY)STRICT;`  
`CREATE TABLE json_metadata(json_api_rowid INTEGER,sumber_data TEXT,nama_file TEXT,deskripsi TEXT,link_download TEXT PRIMARY KEY)STRICT;`

# Cara pakai
Secara default, akan scraping 5 halaman pertama:
```
python start_scraping.py
```
menerima tiga keyword: `mulai`, `selesai`, `interval`  
`mulai, selesai` -> ketik nomor halaman disini  
`interval` -> float, untuk mengatur interval GET request
```
python start_scraping.py mulai=1 selesai=100 interval=0
```
scraping link api bisa dilakukan secara terpisah (jika scraping link web tidak selesai):
```
python .\src\json_links.py
```
(opsional) kompilasi link download file untuk masing-masing link api:  
```
python .\src\download_links.py
```

