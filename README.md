# Raspberryi-Pi-3-Sekil-Algilama-Sistemi
Bu çalışmada, Raspberry Pi 3B+ geliştirme kartı kullanılarak OpenCv, Tesseract ve OCR kütüphanelerinden yararlanılarak şekil ve renk algılama sistemi yapılmıştır. 
Tasarımda, görüntünün okunması için harici olarak USB Kamera kullanılmıştır. Kameradan okunan görüntü kayıt edilerek, OpenCv ve Tesseract kütüphanelerdeki 
görüntü işleme yöntemleri kullanılarak analiz edilmiştir. Analiz sonucunda şekil alanına göre karşılaştırma yapılmış ve bu sonuca göre şekil kenarları çizilmiştir. 
Arayüzden girilen HSV değerlerine göre renk tespiti yapılmıştır. Algılanan şekile göre çevre birimler aktif edilmiştir. 
Sistem bir arayüz ile kontrol edilmektedir. Bu arayüzden elde edilen sonuçlar bir “txt” dosyasına kaydedilebilmektedir. Aynı zamanda çevre birimler de kontrol edilmektedir.

Ortamda bulunan nesnelerin gerçek zamanlı tespit edilmesi, sınıflandırılması ve elde edilen sonuçlar sunulmaktadır.
Önerilen yönteme ait deneysel çalışmaların gerçekleştirilmesinde geometrik şekiller kullanılmaktadır. 
Fotoğraflar alındıktan sonra görüntü işleme teknikleri kullanılarak işlenmektedir. Şekillerin görüntü düzlemi üzerindeki kenar ve alan 
verileri hesaplanarak elde edilmektedir.

# IDE - Kütüphaneler ve Çevre Birimlerin Tanımlanması
Bu çalışmada kaynak kodun hazırlanmasında Thony IDE’ si kullanılmıştır. Bütün Raspberry Pi geliştirme kartlarında yüklü olarak gelmektedir. Hem esnek olmasından dolayı hem de gerekli kütüphanelerin yüklenmesi açısından oldukça kolaylık sağlamaktadır.
İlk olarak gerekli kütüphane tanımlamaları yapılmıştır. Thony IDE’ sinin mevcut LCD kütüphanesi ile GPIO pinleri çakıştığı için Adafriut Kütüphaneleri kullanılmıştır. Bu tanımlamalardan sonra çevre birimler tek tek test edilerek çalıştığı gözlemlenmiştir. Sonrasında sistemin ara yüzü oluşturulmaya başlanmıştır. Ara yüz oluşturmak için Python dilinin Tkhinder kütüphanesi kullanılmıştır.

*Kütüphane Tanımlamalarının Yapıldığı Program Bölümü;*
```python
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pytesseract
import datetime
from time import sleep
import board
import digitalio
import pwmio
import pulseio
from adafruit_motor import servo
import adafruit_character_lcd.character_lcd as characterlcd
#import RPi.GPIO as GPIO

```

*Çevre Birimlerinin Tanımlanımlandığı Program Bölümü;*

```python
#Buzzer
buzzer =pulseio.PWMOut(board.D26, variable_frequency=True)

#Ledler
led_yesil=digitalio.DigitalInOut(board.D20)
led_kirmizi=digitalio.DigitalInOut(board.D21)


#Servo
pwm = pwmio.PWMOut(board.D16, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm)


#16x2 LCD

lcd_columns =16
lcd_rows =2

lcd_rs=digitalio.DigitalInOut(board.D27)
lcd_en =digitalio.DigitalInOut(board.D22)
lcd_d4=digitalio.DigitalInOut(board.D25)
lcd_d5=digitalio.DigitalInOut(board.D24)
lcd_d6=digitalio.DigitalInOut(board.D23)
lcd_d7=digitalio.DigitalInOut(board.D18)


lcd = characterlcd.Character_LCD_Mono(lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7,lcd_columns,lcd_rows)
led_yesil.direction = digitalio.Direction.OUTPUT
led_kirmizi.direction = digitalio.Direction.OUTPUT
lcd.clear()

```
*Çevre Birimlerin Bağlandıktan Sonraki Sistemin Devre Modeli;*

Kamera, Klavye, 16x2 LCD, Servo – Motor, Led ve Buzzer breadboard üzerinde kurulmuştur. 
Servo – Motor, Led, 16x2 LCD ve Buzzer raspberry pi 3 kartında belirlenen ve uygun olan pinlere, 
Kamera ve Klavye ise raspberry pi 3 kartında USB portlarına bağlanmıştır.

![image](https://user-images.githubusercontent.com/70108497/130410546-42fb2c13-9274-4bf8-a181-1eff7dde0251.png)

# Sistem Arayüzü
Şekil ve Renk Tespitini gerçekleştirirken kameradan alınan verilerin kaydedilmesi, alınan verilerin görüntülenmesi ve ara yüzde bastırılması, servo – motor çalıştırılması, 
uyarıların kontrol edilmesi, elde edilen şekil ve renk değerlerinin kaydedilmesi, okunan şeklin bastırılması ve renginin görüntülenmesi işlemleri aşağıda görüldüğü gibi 
Python da Tkhinder kütüphanesi ile tasarlanmıştır.

“Kamerayı Çalıştır” butonuna basıldığında Kamera modülü ile ara yüz Raspberry Pi USB Portu üzerinden seri haberleşme tabanlı yapılmaktadır. 
Okunan görüntüyü kaydetmek için klavyeden ” S” tuşuna basılması gerekmektedir. “Şekli Algıla” butonunun aktif olmasıyla kaydedilen görüntü okunduktan 
sonra arayüzde en son okunan şekil ayrı bir pencerede açılarak, pencere üzerindeki şekil üzerinde ve LCD ekranda bastırılmaktadır. “Sisteme Kaydet” butonunun 
aktif edilmesiyle şablonlardan veriler çekilerek “txt” uzantılı dosyaya kaydedilebilmektedir. “Temizle” butonun aktif edilmesiyle ara yüzdeki bütün veriler ve paneller 
temizlenmektedir. 






