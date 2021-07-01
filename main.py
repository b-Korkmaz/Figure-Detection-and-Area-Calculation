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


def nothing(x):
    # any operation
    pass
cap = cv2.VideoCapture(0)



font=cv2.FONT_HERSHEY_COMPLEX

#Buzzer
buzzer =pulseio.PWMOut(board.D26, variable_frequency=True)

#Ledler
led_yesil=digitalio.DigitalInOut(board.D20)
led_kirmizi=digitalio.DigitalInOut(board.D21)


#Servo#
pwm = pwmio.PWMOut(board.D16, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm)

my_servo.angle = 0


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

led_kirmizi.value =False
led_yesil.value =False

pencere = tk.Tk()

#Alan
entry = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=27,font="bold")
entry.place(x=280, y=300)

#Rengi
entry2 = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=27,font="bold")
entry2.place(x=280, y=360)

entry3 = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=5,font="bold")
entry3.place(x=10, y=445)

entry4 = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=5,font="bold")
entry4.place(x=85, y=445)

entry5 = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=5,font="bold")
entry5.place(x=160, y=445)

entry6 = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=27,font="bold")
entry6.place(x=280, y=500)


######################################################




######################################################
def kamera():
    
    while 1:
    
        _,frame= cap.read()
        cv2.imshow("Kamera", frame)
    
    
        key= cv2.waitKey(1)
        if key == ord("s"):
                cv2.imwrite("/home/pi/Raspberryi-Pi-3-Sekil-Algilama-Sistemi/p3.png",frame)
                
                b2['state']='normal'
                cv2.destroyAllWindows()
                break

######################################################
            
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
                    entry2['state']='normal'
                    entry2.insert(0,"ÜÇGEN")
                    entry2['state']='disabled'
                    
                
                
                
                elif len(approx) == 5 or len(approx) == 6 :
                    cv2.putText(img,"Kare",(x,y),font,0.6,(0,255,0))
                    lcd.clear()
                    lcd.message = ("Kare")
                    entry2['state']='normal'
                    entry2.insert(0,"KARE")
                    entry2['state']='disabled'
                    
                   
                else:
                    cv2.putText(img,"Cember",(x,y),font,0.6,(0,255,0))
                    lcd.clear()
                    lcd.message = ("Cember")
                    entry2['state']='normal'
                    entry2.insert(0,"ÇEMBER")
                    entry2['state']='disabled'
            
        cv2.imshow("Sekil", img)
        cv2.moveWindow("Sekil",620,80)
        cv2.waitKey(0)
        b3['state']='normal'
        cv2.destroyAllWindows()
            
    
    
######################################################
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
         
         
         
    cv2.imshow("Alan", img)
    cv2.moveWindow("Alan",620,80)
    cv2.waitKey(0)
    b4['state']='normal'
    entry3['state']='normal'
    entry4['state']='normal'
    entry5['state']='normal'
    
    cv2.destroyAllWindows()        
            
            
            
            
            
            
            
                    
######################################################
    
def renk_bulma():
    lcd.clear()       
    img = cv2.imread("/home/pi/Raspberryi-Pi-3-Sekil-Algilama-Sistemi/p3.png")
    l_h =int(entry3.get())
    l_s =int(entry4.get())
    l_v =int(entry5.get())
    font=cv2.FONT_HERSHEY_COMPLEX
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([180, 255, 255])
    
    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    
    
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        
        if area > 400:
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
        if len(approx) == 3:
            #cv2.putText(img, "Ucgen", (x, y), font, 1, (0, 0, 0))
            
            if l_h==0 and l_s==75 and l_v==0:
                                    
                    led_kirmizi.value =True
                    led_yesil.value =False
                    
                    renk_durumu=tk.Label(text=('-----------'), bg="red",font="Verdana 15 bold")
                    renk_durumu.place(x=90, y=500)
                    
                    entry6['state']='normal'
                    entry6.insert(0,"Kırmızı Üçgen")
                    entry['state']='disabled'
                    
                    lcd.clear()
                    lcd.message = ("Kirmizi Ucgen")
                    
                    
                        
                    
            elif l_h==0 and l_s==50 and l_v==0:
                    led_kirmizi.value =False
                    led_yesil.value =True
                    
                    renk_durumu=tk.Label(text=('-----------'), bg="green",font="Verdana 15 bold")
                    renk_durumu.place(x=90, y=500)
                    
                    entry6['state']='normal'
                    entry6.insert(0,"Yeşil Üçgen")
                    entry6['state']='disabled'
                    
                    lcd.clear()
                    lcd.message = ("Yesil Ucgen")
        
        elif len(approx) == 4:
            #cv2.putText(img, "Kare", (x, y), font, 1, (0, 0, 0))
            
            if l_h==0 and l_s==75 and l_v==0:
                
                    led_kirmizi.value =True
                    led_yesil.value =False
                    
                    renk_durumu=tk.Label(text=('-----------'), bg="red",font="Verdana 15 bold")
                    renk_durumu.place(x=90, y=500)
                    
                    entry6['state']='normal'
                    entry6.insert(0,"Kırmızı Kare")
                    entry['state']='disabled'
                    
                    lcd.clear()
                    lcd.message = ("Kirmizi Kare")
                        
                    
            elif l_h==0 and l_s==50 and l_v==0 or l_h==0 and l_s==68 and l_v==0:
                    led_kirmizi.value =False
                    led_yesil.value =True
                    
                    renk_durumu=tk.Label(text=('-----------'), bg="green",font="Verdana 15 bold")
                    renk_durumu.place(x=90, y=500)
                    
                    entry6['state']='normal'
                    entry6.insert(0,"Yeşil Kare")
                    entry6['state']='disabled'
                    
                    lcd.clear()
                    lcd.message = ("Yesil Kare")
        
        
    
        else:
            #cv2.putText(img, "Cember", (x, y), font, 1, (0, 0, 0))
            if l_h==0 and l_s==30 and l_v==0 or l_h==0 and l_s==59 and l_v==0 or l_h==0 and l_s==55 and l_v==0:
                
                    led_kirmizi.value =False
                    led_yesil.value =False
                    
                    renk_durumu=tk.Label(text=('-----------'), bg="purple",font="Verdana 15 bold")
                    renk_durumu.place(x=90, y=500)
                    entry6['state']='normal'
                    entry6.insert(0,"Mor Çember")
                    entry['state']='disabled'
                    
                    lcd.clear()
                    lcd.message = ("Mor Cember")
                        
                    
            elif l_h==0 and l_s==60 and l_v==0:
                    led_kirmizi.value =False
                    led_yesil.value =False
                    
                    renk_durumu=tk.Label(text=('-----------'), bg="orange",font="Verdana 15 bold")
                    renk_durumu.place(x=90, y=500)
                    
                    entry6['state']='normal'
                    entry6.insert(0,"Turuncu Çember")
                    entry6['state']='disabled'
                    
                    lcd.clear()
                    lcd.message = ("Turuncu Cember")
                    
    cv2.imshow("Renk", img)
    cv2.moveWindow("Renk",620,80)
    cv2.waitKey(0)
    b7['state']='normal'
    cv2.destroyAllWindows()
                     
######################################################
def veri_kaydet():
    
    v2=entry.get()
    v3=entry2.get()
    v4=entry6.get()
    b6['state']='normal'
    
    
    
    dosya_2 = open("sekil_verileri.txt", "a", encoding="utf-8")

    
    dosya_2.write("Şekil "+v3+" ALANI-->"+v2+" Rengi-->"+v4)
    dosya_2.write("\n")
    
    dosya_2.write("--------------------------------")
    dosya_2.write("\n")
    
    buzzer.duty_cycle=300
    sleep(0.5)
    buzzer.duty_cycle=600
    sleep(0.5)
    buzzer.duty_cycle=300
    sleep(0.5)
    buzzer.duty_cycle=600
    sleep(0.5)
    buzzer.duty_cycle=300
    sleep(0.5)
    buzzer.duty_cycle=600
    sleep(0.5)
    buzzer.duty_cycle=300
    sleep(0.5)
    
    buzzer.duty_cycle=0
    
    
    
    dosya_2.close()
    messagebox.showinfo("Kayıt","BİLGİLER KAYIT EDİLDİ")

######################################################
def temizle():
    temizle_cevap=messagebox.askyesno("Temizleme","Bütün Verileri Temizlemek İstediğinizden\n Eminmisiniz ?")
    if temizle_cevap==1:
        entry['state']='normal'
        entry.delete(0,tk.END)
        entry['state']='disabled'
    
        entry2['state']='normal'
        entry2.delete(0,tk.END)
        entry2['state']='disabled'
        
        
        entry3.delete(0,tk.END)
        entry3['state']='disabled'
        
        
        entry4.delete(0,tk.END)
        entry4['state']='disabled'
        
        
        entry5.delete(0,tk.END)
        entry5['state']='disabled'
        
        entry6['state']='normal'
        entry6.delete(0,tk.END)
        entry6['state']='disabled'
    
        
        b2['state']='disabled'
        b3['state']='disabled'
        b4['state']='disabled'
        b7['state']='disabled'
        
        led_kirmizi.value =False
        led_yesil.value =False
        
        lcd.clear()
    
        renk_durumu=tk.Label(text=('-----------'), bg="white",font="Verdana 15 bold")
        renk_durumu.place(x=90, y=500)
        
        my_servo.angle = 180
        sleep(0.5)
        my_servo.angle = 75
        sleep(0.5)
        my_servo.angle = 180
        sleep(0.5)
        my_servo.angle = 75
        
        
        
        cv2.destroyAllWindows()
    else:
        pass

######################################################
def sistemi_kapat():
    cevap=messagebox.askyesno("Çıkış","Programı Kapatmak İstediğinizden\n Eminmisiniz ?")
    if cevap==1:
        exit()
    else:
        pass


######################################################

pencere.title("Şekil Okuma Sistemi -Anasayfa")
pencere.geometry("600x700+0+0")


baslik=tk.Label(text="Şekil OKUMA SİSTEMİ",font="Verdana 22 bold",bg="white")
baslik.place(x=10,y=10)

b1 = tk.Button(text ="Kamerayı Çalıştır",bg="white",command=kamera)
b1.place(x=10,y=100)

kam_yazi=tk.Label(text="Görüntüyü Kaydetmek için\n Klavyeden 'S' Tuşuna Basınız",font="Verdana 10 bold",bg="white")
kam_yazi.place(x=165,y=100)


b2=tk.Button(text="Şekli Algıla", bg="white",state='disabled',command = sekil_algilama)
b2.place(x=10,y=150)

b3=tk.Button(text="Alanı Hesapla", bg="white",state='disabled',command = alan_hesaplama)
b3.place(x=10,y=200)

b4=tk.Button(text="Rengini Bul", bg="white", state='disabled',command = renk_bulma)
b4.place(x=10,y=240)

b5=tk.Button(text="Programı Kapat",command=sistemi_kapat)
b5.place(x=430,y=635)

b6=tk.Button(text="Temizle", command = temizle)
b6.place(x=330,y=590)

b7=tk.Button(text="Sisteme Kaydet", state='disabled',command = veri_kaydet)
b7.place(x=430,y=590)


sekil_alani = tk.Label(text=("ALANI               "),bg="white" ,font="Verdana 15 bold")
sekil_alani.place(x=10, y=300)

sekil_durumu  = tk.Label(text=('ŞEKİL     '), bg="white",font="Verdana 15 bold")
sekil_durumu.place(x=10, y=360)

renk  = tk.Label(text=('RENGİ'), bg="white",font="Verdana 15 bold")
renk.place(x=10, y=500)

renk_durumu=tk.Label(text=('-----------'), bg="white",font="Verdana 15 bold")
renk_durumu.place(x=90, y=500)

hsv_deger  = tk.Label(text=('HSV DEĞERLERİ'), bg="white",font="Verdana 15 bold")
hsv_deger.place(x=10, y=405)

"""
s2=datetime.datetime.now()
s3=datetime.datetime.strftime(s2,'%d.%m.%Y')
sistem_saati2=tk.Label(text=(s3), bg="white",font="Verdana 10 bold")
sistem_saati2.place(x=450,y=10)
"""
pencere.mainloop()

cap.release()
cv2.destroyAllWindows()

            
            
            
######################################################
            
            
            
            

