# Game Farming dan Mining
## Deskripsi Singkat
Project ini ini merupakan project game berbasis Command Line Interface (CLI) yang diprogram menggunakan bahasa pemrograman python.

Tujuan dari game ini yaitu mengumpulkan uang sebanyak-banyak nya yang dapat dihasilkan dengan bertani (Farming) ataupun Menambang (Mining), yang dimana hasil dari Farming dan Mining tersebut dapat dijual. Player juga bisa mendapatkan uang dari event-event yang terjadi selama sedang Mining.

## Fitur Utama
- **Farming:** Player dapat menanam tanaman yang dimana hasil panen nya dapat dijual untuk menambah uang. PLayer juga harus menyiram tanaman yang ditanam setiap hari agar tanamannya bisa tumbuh.
- **Mining:** Player dapat melakukan Mining untuk mendapatkan ore untuk dijual. Dalam sistem Mining juga terdapat beberapa event seperti fight dengan mob dan boss, chest, dan mercant.
- **Shop:** Player dapat membeli benih yang dapat digunakkan untuk Farming. Player juga dapat menjual hasil panen dan ore di sini. Selain itu Player dapat mengupgrade stats yang akan berguna dalam mining. 
- **Inventory:** Untuk menyimpan benih tanaman, hasil panen, dan ore dari hasil mining.
- **Tidur:** Fitur tidur ini digunakan untuk berganti hari, memulihkan stamina, serta menyimpan data game.
- **Reset:** Untuk mereset data game.

## Installation & Cara Menjalankan Program
- Pastikan python sudah terinstall di komputer.
- Clone Repository ini
```bash
# Clone Repository ini
git clone https://github.com/Umamusume-Project/repository-umamusume.git
```
- Pastikan semua file berada dalam satu folder yang sama
- Masuk ke Folder project
```bash
cd repository-umamusume
```
- Jalankan game di terminal dengan mengetik perintah berikut:
```bash
python MAIN.py
```
### Cara Bermain
- Baca perintah yang ditampilkan di menu
- Masukkan angka sesuai dengan angka perintah
- **Tujuan Awal:** Player bisa memulai dengan membeli benih di shop dengan uang yang sudah disediakan. Benih tersebut bisa digunakan untuk Farming. Selain itu Player juga bisa memulai dengan Mining untuk mendapatkan ore untuk dijual.

## Struktur Folder/File
```
├── MAIN.py            # Entry point game, menu utama dan loop game
├── farming.py         # Sistem Farming
├── inventory.py       # Sistem Inventory
├── mining.py          # Sistem Mining
├── player.py          # Logika player, untuk data uang, stamina, hari, inventory, dan stats untuk mining
├── savemanager.py     # Sistem unutk save data dan reset data
├── shop.py            # Sistem toko
├── save.txt           # File untuk data yang disimpan
└── README.md          # Dokumentasi Project
```

## Daftar Anggota Kelompok/Contributor
- Fairul Fadli (fadlilin)
- Nevan Zeffano Jeremia (NevanZJ)
- Kent Justin Kusuma (JustinKK11)
- Nicolas Peb Zolo (Xynicc23)
- Valentino Alfiyan (valentinoalfiyan255-hub)
