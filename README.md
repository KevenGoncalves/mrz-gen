# MRZ Gen API

![image](public/mrz.jpeg)

## Description

Machine Readable Zone generator and checker for official travel documents sizes
1, 2, 3, MRVA and MRVB (Passports, Visas, national id cards and other travel documents)

MRZ Generator and MRZ Checker are built according to International Civil Aviation
Organization specifications (ICAO 9303):

* [Specifications Common to all Machine Readable Travel Documents (MRTDs)](https://www.icao.int/publications/Documents/9303_p3_cons_en.pdf)
* [Specifications for Machine Readable Passports (MRPs)](https://www.icao.int/publications/Documents/9303_p4_cons_en.pdf)
* [Specifications for TD1 Size Machine Readable Official Travel Documents (MROTDs)](https://www.icao.int/publications/Documents/9303_p5_cons_en.pdf)
* [Specifications for TD2 Size Machine Readable Official Travel Documents (MROTDs)](https://www.icao.int/publications/Documents/9303_p6_cons_en.pdf)
* [Specifications for Machine Readable Visas (MRV)](https://www.icao.int/publications/Documents/9303_p7_cons_en.pdf)

## Fields Distribution of Official Travel Documents

![image](public/Fields_Distribution.png)

## Usage

1. install taskfile in your machine
2. create env `python -m venv venv`
3. active the venv for mac/linux `source ./venv/bin/activate` for windows `venv\Scripts\activate`
4. run `task install`
5. run `task dev` for development and `task start` for prod
6. visit `http://localhost:8000/api/v1/docs`
7. have fun :)
