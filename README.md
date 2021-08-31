# Raspberryi-Pi-3-Sekil-Algilama-Sistemi
Bu çalışmada, Raspberry Pi 3B+ geliştirme kartı kullanılarak OpenCv, Tesseract ve OCR kütüphanelerinden yararlanılarak şekil algılama, alan hesaplama ve renk algılama sistemi yapılmıştır. Tasarımda, görüntünün okunması için harici olarak USB Kamera kullanılmıştır. Kameradan okunan görüntü kayıt edilerek, OpenCv ve Tesseract kütüphanelerdeki 
görüntü işleme yöntemleri kullanılarak analiz edilmiştir. Analiz sonucunda şekil alanına göre karşılaştırma yapılmış ve bu sonuca göre şekil kenarları çizilmiştir. Alan hesaplama kısımında ise şekil algılanıp kenarları çizilerek, çizilen kenarlara göre orta noktası işaretlenmiştir. İşaretlenen orta noktaya göre x ve y eksen değerleri alınarak alan hesabı yapılmıştır. 

Arayüzden girilen HSV değerlerine göre renk tespiti yapılmıştır. Algılanan şekile göre çevre birimler aktif edilmiştir. Sistem bir arayüz ile kontrol edilmektedir. Bu arayüzden elde edilen sonuçlar bir “txt” dosyasına kaydedilebilmektedir. Aynı zamanda çevre birimler de kontrol edilmektedir.

Ortamda bulunan nesnelerin gerçek zamanlı tespit edilmesi, sınıflandırılması ve elde edilen sonuçlar sunulmaktadır. Önerilen yönteme ait deneysel çalışmaların gerçekleştirilmesinde geometrik şekiller kullanılmaktadır. Fotoğraflar alındıktan sonra görüntü işleme teknikleri kullanılarak işlenmektedir. Şekillerin görüntü düzlemi üzerindeki kenar ve alan verileri hesaplanarak elde edilmektedir.

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
Şekil, Alan ve Renk Tespitini gerçekleştirirken kameradan alınan verilerin kaydedilmesi, alınan verilerin görüntülenmesi ve ara yüzde bastırılması, servo – motor çalıştırılması, 
uyarıların kontrol edilmesi, elde edilen şekil ve renk değerlerinin kaydedilmesi, okunan şeklin bastırılması ve renginin görüntülenmesi işlemleri aşağıda görüldüğü gibi 
Python da Tkhinder kütüphanesi ile tasarlanmıştır.

“Kamerayı Çalıştır” butonuna basıldığında Kamera modülü ile ara yüz Raspberry Pi USB Portu üzerinden seri haberleşme tabanlı yapılmaktadır. 
Okunan görüntüyü kaydetmek için klavyeden ” S” tuşuna basılması gerekmektedir. “Şekli Algıla” butonunun aktif olmasıyla kaydedilen görüntü okunduktan 
sonra arayüzde en son okunan şekil ayrı bir pencerede açılarak, pencere üzerindeki şekil üzerinde ve LCD ekranda bastırılmaktadır. “Sisteme Kaydet” butonunun 
aktif edilmesiyle şablonlardan veriler çekilerek “txt” uzantılı dosyaya kaydedilebilmektedir. “Temizle” butonun aktif edilmesiyle ara yüzdeki bütün veriler ve paneller 
temizlenmektedir. 

![sk_1_k](https://user-images.githubusercontent.com/70108497/131489243-985c7678-cf14-428d-a496-ec5c928512a7.jpeg)

# Sistem Algoritması
“Kamerayı Çalıştır” butonuna basıldığında Okunan görüntüyü kaydetmek için klavyeden ” S” tuşuna basılması gerekmektedir.
Şekil algılama fonksiyonunda ilk olarak arayüzden kayıt edilen görüntüyü çağırılmıştır. OpenCv kütüphanesinde görüntü rengini değiştirerek threshold işlemi uygulayarak
findContours fonksiyonu ile kenarları tespit edilmiştir. For döngüsü ile tespit edilen kenarlar çizilmiştir. Devamında ise if koşul bloğunda approx değeri kontrol edilmiştir.
Bu duruma göre şeklin üçgen mi ya da kare mi olduğu tespit edilmiştir.

*Şeklin Algılanması ;*
```python
def sekil_algilama():    
    
        img = cv2.imread("/home/pi/Raspberryi-Pi-3-Sekil-Algilama-Sistemi/p3.png")
        font=cv2.FONT_HERSHEY_COMPLEX
        imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thrash = cv2.threshold(imgGrey, 145,255,cv2.THRESH_BINARY)
        blur = cv2.GaussianBlur(thrash,(11,11),0)
        contours, _ =cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        i =0
            
        for contour in contours:                
                
                if i ==0:
                    i=1
                    continue
            
                approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
                cv2.drawContours(img, [contour],0,(0,255,0),5)                
                
                M = cv2.moments(contour)
                if M['m00'] != 0.0:
                    x= int(M['m10']/M['m00'])
                    y= int(M['m01']/M['m00'])         
                            
                
                if  len(approx) == 3 or len(approx) == 4 :
                    cv2.putText(img,"Ucgen",(x,y),font,0.6,(0,255,0))
                    lcd.clear()
                    lcd.message = ("Ucgen")
                                     
                                
                elif len(approx) == 5 or len(approx) == 6 :
                    cv2.putText(img,"Kare",(x,y),font,0.6,(0,255,0))
                    lcd.clear()
                    lcd.message = ("Kare")                                        
                   
                else:
                    cv2.putText(img,"Cember",(x,y),font,0.6,(0,255,0))
                    lcd.clear()
                    lcd.message = ("Cember")
                              
       

```
 
V1

![sk_2_k](https://user-images.githubusercontent.com/70108497/131493588-f88edaaa-3c5a-4db3-81a2-778b45741ecd.png)

V2

![sk3_k](https://user-images.githubusercontent.com/70108497/131494565-59abc959-2a1d-409c-8cab-c2c05b9401f3.png)


*Şeklin Orta Noktasının Tespit Edilmesi ve Alan Hesabı Yapılması ;*

Devamında ise tespit edilen şeklin alanı, şeklin orta noktası tespit edilerek hesaplanmıştır. Bu hesaplama işlemi şu şekilde düşünülmüştür ;
İlk olarak kayıt edilen görüntü açılmış ve threshold işlemleri uygulanarak kenarları tespit edilmiştir. Moments fonksiyonu ile orta noktası işaretlenmiştir.
Moments fonksiyonun x ve y ekseni değerleri alınarak şekile göre alan hesabı yapılmıştır. Yapılan bu hesap arayüz ve LCD ekranda bastırılmıştır.

```python

def alan_hesaplama():
    img = cv2.imread("/home/pi/Raspberryi-Pi-3-Sekil-Algilama-Sistemi/p3.png")
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thrash = cv2.threshold(imgGrey, 145,255,cv2.THRESH_BINARY)
    blur = cv2.GaussianBlur(thrash,(11,11),0)
    contours, _ =cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    i = 0
    for contour in contours:
        
        
        if i ==0:
            i=1
            continue
    
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
        cv2.drawContours(img, [contour],0,(0,255,0),5)
        
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            cX= int(M['m10']/M['m00'])
            cY= int(M['m01']/M['m00'])
        
        cv2.circle(img, (cX,cY),7,(0,0,0),-1)
        cv2.putText(img, "Center",(cX+10,cY-5),cv2.FONT_HERSHEY_PLAIN,1,(100,200,0),2)
        cv2.putText(img, "Genislik {}".format(round(cX,2)),(cX-100,cY-20),cv2.FONT_HERSHEY_PLAIN,1,(100,200,0),2)
        cv2.putText(img, "Yukseklik {}".format(round(cY,2)),(cX-100,cY+20),cv2.FONT_HERSHEY_PLAIN,1,(100,200,0),2)
        
        if  len(approx) == 3 or len(approx) == 4 :
                    
                    lcd.clear()
                    lcd.message = ("Alani : {}".format(round((cX*cY)/2)))
                    entry['state']='normal'
                    entry.insert(0,round((cX*cY)/2))
                    entry['state']='disabled'                    
                 
               
        elif len(approx) == 5 or len(approx) == 6 :
                    
                    lcd.clear()
                    lcd.message = ("Kare")
                    entry['state']='normal'
                    entry.insert(0,round((cX*cX)))
                    entry['state']='disabled'
                    
        else:
                    yari_cap=float(cX)/2
                    c_alan =float(3.14*((yari_cap*yari_cap)))
                    sonuc = round(c_alan)
                    lcd.clear()
                    lcd.message = ("Cember")
                    entry['state']='normal'
                    entry.insert(0,sonuc)
                    entry['state']='disabled'
```

V1

![s2_2_2_kk](https://user-images.githubusercontent.com/70108497/131493324-3958d2e7-8ade-4913-a29e-fd6f39821af1.png)

V2

![sk_3_2_k](https://user-images.githubusercontent.com/70108497/131494876-963ea666-3b91-4c4a-ba85-13b92875e8db.png)

V3

![sk_4_k](https://user-images.githubusercontent.com/70108497/131495390-913bca14-966c-4a50-b03b-0f10bf2ad6dc.png)


*Şeklin Renginin Tespit Edilmesi*

Şeklin renk tespiti yapılırken ilk olarak kayıt edilen görüntü açılarak görüntü üzerinde maske işlemleri uygulanmaktadır. Arayüzde HSV değerleri girilmesi gerekmektedir. HSV değerleri bulunan ortama ve ortamın ışık açısına göre değişmektedir. Girilen HSV değerinden sonra "Rengini Bul" butonona basıldığında ilk olarak if koşuluna sokularak şekil tespit edilmektedir. Sonrasında şekile göre rengi tespit edilip, rengine göre LED, arayüz ve LCD ekranda bastırılmaktadır.

V1

![sk_6_k](https://user-images.githubusercontent.com/70108497/131498694-10bb5866-7a88-4737-9996-07cf5e0ab680.png)

V2

![sk_7_k](https://user-images.githubusercontent.com/70108497/131498932-6434dd02-4538-4e2a-be60-a598cfa3ccdd.png)

*Tespit Edilen Şekil ve Renginin LCD Ekranda Bastırılması ;*

V1

![sk_5_k](https://user-images.githubusercontent.com/70108497/131497061-e0e9ddb2-4807-4f79-84fa-e05b847ea1b2.png)

V2

![sk_8_k](https://user-images.githubusercontent.com/70108497/131499498-bde1b5eb-d52b-4308-8dda-67b85383e1fa.png)


# Sonuç
Raspberry Pi 3B+ geliştirme kartı ile görüntü işleme yöntemleri kullanılarak Şekil Algılama Sistemi başarı ile çalıştırılmıştır. Tasarımda Thony IDE yani Python derleyicisi kullanılarak kaynak kodu hazırlanmıştır. Gerçek zamanlı hazırlanan bu sistemin gerekli çevre birimleri montajları breadboard üzerine yapılarak sistem çalışır hale getirilmiştir. Bu çalışmada Raspberry Pi geliştirme kartı kullanılarak bir sistem tasarımı sunulmuştur.









