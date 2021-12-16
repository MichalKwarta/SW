import cv2
import sqlite3
# import liquidcrystal_i2c
from sys import exit
from random import seed,randint
from time import sleep
# import Adafruit_BBIO.GPIO as GPIO

# class LCD:
#     def __init__(self): 
#         self.cols = 20
#         rows = 4
#         self.lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 2, numlines=rows)
#     def print(self,text,row):
#         self.lcd.printline(row,text.center(self.cols))
        




def silnikrobibrr(enA,in1,in2):
    
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    sleep(1)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    



def countDots(pins):
    silnikrobibrr(*pins)
    camera = cv2.VideoCapture(0)
    _, img = camera.read()
    _,_,blue = cv2.split(img)
    _, thresh = cv2.threshold(blue, 100, 255, cv2.THRESH_BINARY)
    contours,_ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    dots = 0
    for c in contours:
        dots +=1 if 300<cv2.contourArea(c)<=1500 else 0
    return dots

def countDotsMock():
    num = randint(1,10)
    return num

def establishConnection(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor() 
    if conn is not None:
        cur.execute(""" CREATE TABLE IF NOT EXISTS Kropeczki (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    suma NUMBER
                    ); """)
    else:
        print("Baza danych nie istnieje :(")
        exit() 
    return conn,cur



if __name__ == '__main__':
    # lcd = LCD()
    db = r'Kropeczki.db'
    enA ='jakis_pin'
    in1 = 'inny pin'
    in2 = 'jeszcze inny pin'
    GPIO.setup(enA, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    
                
    
    print('''L o S o W a Ń s K O
          q L U- losuj ziarno i wygeneruj liczbę z zakresu <L;U>
          w N L U - pobierz z bazy danych ostanie N wyników i wygeneruj liczbę z zakresu <L;U>  
          e - exit
          ''')
    
    while True:
        choice,*args = input(">").split()
        choice = choice.upper()
        try:
            args = list(map(int,args))
        except ValueError:
            print("Podano błędne argumenty :(")
            exit(1)
        
        
        if choice == 'Q' and len(args)==2:
            conn,cur = establishConnection(db)
                
            dots = countDots((enA,in1,in2))
            seed(dots)
            print(randint(args[0],args[1]))
            cur.execute(f"Insert into Kropeczki (suma) values ({str(dots)});")
            conn.commit()
            conn.close()
            
            
        elif choice == 'W' and len(args)==3:
            conn,cur = establishConnection(db)
            cur.execute(f"select suma from Kropeczki order by id desc limit {args[0]} ")
            records = cur.fetchall()
            total = sum([int(x[0]) for x in records])
            print(f"list = {[int(x[0]) for x in records]}")
            seed(total)
            print(randint(args[1],args[2]))
            conn.close()
            
        elif choice == 'E':
            exit();
        else:
            print("Musiałeś coś źle wpisać :(")
        
            
        
    