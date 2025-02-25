# Latihan FastAPI
### Persiapan Menjalankan Program
1. Membuat database pada PostgreSQL untuk menyimpan data (nama database awal `databasesgt`)
2. Setup database pada `config/database.py`
```
"postgresql://postgres:12345@localhost/databasesgt"
```
(Nama user dan password juga perlu diatur dengan user default `postgres` dan password default `12345`)

### Cara Menjalankan Program
1. Membuat virtual environment dengan
```
python -m venv venv
```

2. Masuk ke virtual environment dengan
```
venv/Scripts/activate
```

3. Melakukan instalasi library yang dibutuhkan dengan
```
pip install fastapi uvicorn sqlalchemy pydantic psycopg2
```

4. Menjalankan program dengan
```
uvicorn main:app --reload
```

### Menggunakan Data Sampel
Data sampel dapat digunakan setelah program pertama kali dijalankan dan tabel berhasil dibuat program
1. Mengatur tabel agar dapat menghasilkan UUID dengan masuk ke database yang digunakan
2. Melakukan pengaturan untuk UUID dengan
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
ALTER TABLE books ALTER COLUMN id SET DEFAULT uuid_generate_v4();
ALTER TABLE members ALTER COLUMN id SET DEFAULT uuid_generate_v4();
```
3. Menjalankan file SQL untuk melakukan insert data

### Daftar API yang dibuat
1. GET /api/books
Memperlihatkan buku yang ada dalam database <br>
Input parameter (optional):
    - title (string case-insensitive)
    - author (string case-insensitive)
    - page (int)
    - limit (int)
  
2. POST /api/members
Membuat data member baru <br>
Body parameter (must be filled):
    - name (string)
    - email (string)
    - phone (string, 12 digits, start with 0)
    - address (string)
  
3. POST /api/borrowings
Membuat data borrowing baru <br>
Body parameter (must be filled):
    - book_id (string uuid)
    - member_id (string uuid)

4. PUT /api/borrowings/:id/return
Mengembalikan buku (edit data borrowing) <br>
Input parameter (must be filled):
    - id (string uuid, id data borrowing)
  
5. GET /api/members/:id/borrowings
Memperlihatkan sejarah borrowing seorang member <br>
Input parameter (must be filled):
    - id (string uuid, id data member)

    Input parameter lain (optional):
    - status (string)
    - page (int)
    - limit (int)


