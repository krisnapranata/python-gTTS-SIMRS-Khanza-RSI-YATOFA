#!/usr/bin/env python3
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from gtts import gTTS
from io import BytesIO
from datetime import datetime as date
import pygame
import os, time, sys
import mysql.connector
import socket

#kd_poli = "BED"
#kd_dokter = "D01"
host = "192.168.1.253"
user = "sik"
password = "00"
database = "sik"

#fungsi untuk memanggil google text to speech
def speak(text, language='id'):
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(mp3_fo)
    #mp3_fo.seek(0)
    #sound = pygame.mixer.Sound(mp3_fo)
    #sound.play()
    #time.sleep(8)
    return mp3_fo
    
#membuat koneksi ke database
def koneksi():
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
    return mydb

#Cek database tabel antriapotek3 untuk mendapatkan nilai 1 atau 0 
def cekdatabase():
        mydb = koneksi()
        mycursor = mydb.cursor()
        #mycursor.execute("SELECT * FROM antripoli WHERE kd_poli='" + str(kd_poli) + "' AND kd_dokter='" + str(kd_dokter) + "'")
        mycursor.execute("SELECT * FROM antriapotek3")
        myresult = mycursor.fetchone()
        #print(myresult)
        return(myresult)
    
#fungsi untuk melakukan update database tabel antri poli untuk merubah nilai 1 ke 0 supaya berhenti dipanggil    
def updatedatabase():
    no_rawat = cekdatabase()
    no_rawat = no_rawat[2]
    mydb = koneksi()
    mycursor = mydb.cursor()
    sql = "UPDATE antriapotek3 SET status='0' WHERE no_rawat='" + no_rawat + "'"
    mycursor.execute(sql)
    mydb.commit()

#fungsi ini dipakai untuk mendapatkan text yang akan di rubah ke suara
def antrian_panggil(no_rawat):
    mydb = koneksi()
    mycursor = mydb.cursor()
    #sql = "select antripoli.kd_dokter, antripoli.kd_poli, antripoli.no_rawat, pasien.nm_pasien, poliklinik.nm_poli, reg_periksa.no_reg, dokter.nm_dokter FROM antripoli inner join pasien inner join reg_periksa inner join poliklinik inner join dokter on antripoli.no_rawat=reg_periksa.no_rawat and reg_periksa.no_rkm_medis=pasien.no_rkm_medis and antripoli.kd_dokter=dokter.kd_dokter and antripoli.kd_poli=poliklinik.kd_poli where reg_periksa.no_rawat='" + no_rawat + "'"
    sql = "select antriapotek3.no_rawat, pasien.nm_pasien, pasien.alamat, poliklinik.nm_poli, dokter.nm_dokter FROM antriapotek3 inner join pasien inner join reg_periksa inner join poliklinik inner join dokter on antriapotek3.no_rawat=reg_periksa.no_rawat and reg_periksa.no_rkm_medis=pasien.no_rkm_medis and reg_periksa.kd_dokter=dokter.kd_dokter and reg_periksa.kd_poli=poliklinik.kd_poli where reg_periksa.no_rawat='" + no_rawat + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult
 

#fungsi ini digunakan untuk memberitahukan bahwa tidak ada koneksi, karena gTTS menggunakan internet supaya bisa berfungsi    
def check_internet_connection():
    remote_server = "www.google.com"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((remote_server, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()
    
print("Listening for Antrian...")

while True:
    try:
        hasil = cekdatabase()
        if hasil is False:
            print("Nomor resep tidak ditemukan")
            time.sleep(2)
        elif hasil[1] == str(0):
            print("Menunggu Antrin Selanjutnya")
            time.sleep(2)
        elif check_internet_connection():
            no_rawat = cekdatabase()
            no_rawat = no_rawat[2]
            panggil = antrian_panggil(no_rawat)
            print(panggil)
            pygame.init()
            pygame.mixer.init()
            if panggil[3] == "Unit IGD":
               sound = speak("Pasien atas nama " + str(panggil[1].lower()) + ", alamat " + str(panggil[2].lower()) + ", Unit I G D, silahkan ke loket untuk ambil obat ")
            else:
               sound = speak("Pasien atas nama " + str(panggil[1].lower()) + ", alamat " + str(panggil[2].lower()) + "," + str(panggil[3].lower()) + ", silahkan ke loket untuk ambil obat ")
            sound.seek(0)
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
            updatedatabase()
            time.sleep(1)
        else:
            print("Check Koneksi Internet Anda...!!!")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print('Program Selese')
        sys.exit(0)
        
