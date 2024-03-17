# python-gTTS-SIMRS-Khanza-RSI-YATOFA
Aplikasi ini dibangun menggunakan bahasa pemerograman python sehingga membutuhkan beberapa library

=================== LANGKAH 1 ==================================

1. Library google text to speech
   pip install gTTS

2. Library pygame
   pip install pygame

3. Library mysql-connector-python
   pip install mysql-connector-python

4. jika menggunakan windows download python3+
   
5. jika menggunakan linux atau raspberry biasanya sudah terinstall python jika belum ketik perintah :

   => sudo apt-get update
   
   => sudo apt-get install python3.12

================== LANGKAH 2 ===============================

$ git clone https://github.com/krisnapranata/python-gTTS-SIMRS-Khanza-RSI-YATOFA.git

$ cd python-gTTS-SIMRS-Khanza-RSI-YATOFA
$ pip install -r requirements.txt
$ python3.12 pemanggil_windows.py <path-image> <untuk pemanggil poli>
$ python3.12 pemanggil_apotek_windows.py <path-image> <untuk pemanggil farmasi>

file konfigurasi :

kd_poli = "BED"

host = "localhost"

user = "sik"

password = "sik"

database = "sik"


kode poli / kd_poli disesuaikan dengan kode poli di SIMRS Khanza
host di sesuaikan dengan host Database
user di sesuaikan dengan dengan user database
password di sesuaikan dengan password database
database di sesuaikan dengan nama database

cara menjalankan aplikasinya copy file pemanggil poli = panggil_windows.py ke drive yang di inginkan

misal di drive C:

kemudian buka CMD lalu ketik : python3.12 C:\panggil_windows.py kemudian enter

lalu seperti biasa di SIMRS Khanza klik kanan dan antrian masuk poli
