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

kd_poli = "BED"
#kd_dokter = "D01"
host = "localhost"
user = "sik"
password = "00"
database = "yatofa27022024"

def speak(text, language='id'):
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(mp3_fo)
    mp3_fo.seek(0)
    sound = pygame.mixer.Sound(mp3_fo)
    sound.play()
    #time.sleep(8)
    
def koneksi():
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
    return mydb
    
def cekdatabase():
    kd_dokter = get_kddokter() 
    if kd_dokter is False:
        return False
    else:
        kd_dokter = kd_dokter[0]
        mydb = koneksi()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM antripoli WHERE kd_poli='" + str(kd_poli) + "' AND kd_dokter='" + str(kd_dokter) + "'")
        myresult = mycursor.fetchone()
        #print(myresult)
        return(myresult)
    
def updatedatabase():
    kd_dokter = get_kddokter() 
    kd_dokter = kd_dokter[0]
    mydb = koneksi()
    mycursor = mydb.cursor()
    sql = "UPDATE antripoli SET status='0' WHERE kd_poli='" + kd_poli + "' AND kd_dokter='" + kd_dokter + "'"
    mycursor.execute(sql)
    mydb.commit()

def antrian_panggil(no_rawat):
    mydb = koneksi()
    mycursor = mydb.cursor()
    sql = "select antripoli.kd_dokter, antripoli.kd_poli, antripoli.no_rawat, pasien.nm_pasien, poliklinik.nm_poli, reg_periksa.no_reg, dokter.nm_dokter FROM antripoli inner join pasien inner join reg_periksa inner join poliklinik inner join dokter on antripoli.no_rawat=reg_periksa.no_rawat and reg_periksa.no_rkm_medis=pasien.no_rkm_medis and antripoli.kd_dokter=dokter.kd_dokter and antripoli.kd_poli=poliklinik.kd_poli where reg_periksa.no_rawat='" + no_rawat + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult
    
def get_kddokter():
    hari_kerja = jadwal_hari_dokter()
    mydb = koneksi()
    mycursor = mydb.cursor()
    sql = "SELECT jadwal.kd_dokter FROM jadwal WHERE jadwal.kd_poli ='" + str(kd_poli) + "' AND jadwal.hari_kerja = '" + hari_kerja + "'"
    #sql = "SELECT jadwal.kd_dokter FROM jadwal WHERE jadwal.kd_poli ='" + str(kd_poli) + "' AND jadwal.hari_kerja = 'SENIN'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if myresult is not None:
        return myresult
    else:
        return False
    
    #return myresult
    
def jadwal_hari_dokter():
    hari = date.today().strftime("%A")
    if hari == "Monday":
       hari = "KAMIS"
    elif hari == "Tuesday":
         hari = "SELASA"
    elif hari == "Wednesday":
         hari = "RABU"
    elif hari == "Thursday":
         hari = "KAMIS"
    elif hari == "Friday":
         hari = "JUMAT"
    else:
        hari = "SABTU"

    return hari
    
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
            print("Periksa Jadwal Dokter")
            time.sleep(2)
        elif hasil[2] == str(0):
            print("Menunggu Antrin Selanjutnya")
            time.sleep(2)
        elif check_internet_connection():
            no_rawat = cekdatabase()
            no_rawat = no_rawat[3]
            panggil = antrian_panggil(no_rawat)
            print(panggil)
            pygame.init()
            pygame.mixer.init()
            speak("Antrian nomor " + str(panggil[5]) + "," + str(panggil[3].lower()) + "," + "silahkan masuk ke " + str(panggil[4]))
            updatedatabase()
            time.sleep(1)
        else:
            print("Check Koneksi Internet Anda...!!!")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print('Program Selese')
        sys.exit(0)
        