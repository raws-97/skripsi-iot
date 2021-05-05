#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import os
from pyfingerprint.pyfingerprint import PyFingerprint
import base64
import requests

#Default Settings
url = "http://10.1.0.133:8045/api/absen/"
kampus = 1
location = "V205"
fingerNumber = 4

def get_finger_image():


    ## Reads image and download it
    ##

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Tries to read image and download it
    try:
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
    
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)


def read_finger_data():


    ## Reads image and download it
    ##

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Tries to read image and download it
    try:
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        
        #saving image from sensor to local
        imageDestination =  os.getcwd() + '/fingerprint.bmp'
        f.downloadImage(imageDestination)
        with open("fingerprint.bmp", "rb") as image_file:
            baseImageData = base64.b64encode(image_file.read()).decode('ascii')
        
        #payload format to send to server
        basePayload = {"file": baseImageData, "kampus": kampus, "lokasi": location}

        try :

            #Send data to Server
            baseData = requests.get(url+"finger", json=basePayload)
            #Result from Server
            baseResult = baseData.json()



            #Get Lecturer Photo based on kode
            #get_photo = url+"foto?kode="+baseResult['kode']+"&institusi="+baseResult['institusi']
            # get_photo = url+"foto?kode=00670&institusi=1"
            get_photo = url+"foto?kode="+baseResult['kode']+"&institusi=1"
            
            #Converting Image to base64, decode to ascii to get string, not bytes
            photo_encode = base64.b64encode(requests.get(get_photo).content).decode('ascii')


            return {
                "result": 'success',
                "data": baseResult,
                "finger": baseImageData,
                "lecturer_photo": photo_encode

                }
        except :

            return { 
                "result": 'failed'

            }


    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def searchDosen(id):
    parameter = url+"data?"

    try:
        val = int(id)
        req = requests.get(parameter+"kode="+id+"&nama=")
        data = req.json()

        return {
            "data": data,
            "status": 200
        }

    except ValueError:
        req = requests.get(parameter+"kode=&nama="+id)
        data = req.json()

        return {
            "data": data,
            "status": 200
        }

def register_finger():
    ## Reads image and download it
    ##

    ## Tries to initialize the sensor
    for i in range(fingerNumber):
        get_finger_image()
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)

        ## Tries to read image and download it
        try:
            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass
            
            finger =  os.getcwd() + '/registerFinger'+str(i+1)+'.bmp'
            f.downloadImage(finger)
            print("Finger "+str(i+1)+" Success")

        
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)

def registerFingerAPI(payload):
    register_finger()

    with open('registerFinger1.bmp', "rb") as image_file:
            finger1 = base64.b64encode(image_file.read()).decode('ascii')
    with open('registerFinger2.bmp', "rb") as image_file:
            finger2 = base64.b64encode(image_file.read()).decode('ascii')
    with open('registerFinger3.bmp', "rb") as image_file:
            finger3 = base64.b64encode(image_file.read()).decode('ascii')
    with open('registerFinger4.bmp', "rb") as image_file:
            finger4 = base64.b64encode(image_file.read()).decode('ascii')
    
    basePayload = {
    "gelar_belakang_dosen": payload['gelar_belakang_dosen'],
    "gelar_depan_dosen": payload['gelar_depan_dosen'],
    "id_dosen": payload['id_dosen'],
    "id_fakultas": payload['id_fakultas'],
    "id_institusi": payload['id_institusi'],
    "id_prodi": payload['id_prodi'],
    "id_status_dosen": payload['id_status_dosen'],
    "nama_dosen": payload['nama_dosen'],
    "nama_fakultas": payload['nama_fakultas'],
    "nama_institusi": payload['nama_institusi'],
    "nama_jenis_kelamin": payload['nama_jenis_kelamin'],
    "nama_prodi": payload['nama_prodi'],
    "nama_status_dosen": payload['nama_status_dosen'],
    "nidn": payload['nidn'],
    "sidik_jari_1": finger1,
    "sidik_jari_2": finger2,
    "sidik_jari_3": finger3,
    "sidik_jari_4": finger4,
    "status_aktif": payload['status_aktif']
    }

    try:
        baseData = requests.post(url+"daftar", json=basePayload)
        result = baseData.json()

        return 'Success'
    except:
        return 'Failed'