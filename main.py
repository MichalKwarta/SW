from distutils.command.build import build
import cv2
import sqlite3
import liquidcrystal_i2c
from sys import exit
from random import seed, randint
from time import sleep

import Adafruit_BBIO.GPIO as GPIO




def silnikrobibrr(enA='P9_25', in1='P9_23', in2='P9_21'):

    GPIO.output(enA, GPIO.HIGH)
    print("BRRRR")
    sleep(2)
    GPIO.output(enA, GPIO.LOW)







def countDots():
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()
    cv2.imwrite("nowe.jpg",frame)

    _, _, red = cv2.split(frame)
    _, threshh = cv2.threshold(red, 50, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(threshh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    suma = 0
    for c in contours[1]:
        (_, _, w, h) = cv2.boundingRect(c)
        if 100 < cv2.contourArea(c) <= 300 and 0.8 < w / h < 1.2:
            suma += 1
    return suma


def establishConnection(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    if conn is not None:
        cur.execute("CREATE TABLE IF NOT EXISTS Kropeczki (id INTEGER PRIMARY KEY AUTOINCREMENT, suma NUMBER);")
    else:
        print("Baza danych nie istnieje :(")
        exit()
    return conn, cur

def printhelp():
        print('''L o S o W a Ń s K O
          q L U- losuj ziarno i wygeneruj liczbę z zakresu <L;U>
          w N L U - pobierz z bazy danych ostanie N wyników i wygeneruj liczbę z zakresu <L;U>  
          h - help
          e - exit
          ''')
        
        
if __name__ == '__main__':
    db = r'Kropeczki.db'

    #pins setup
    enA = "P9_21"
    in1 = "P9_23"
    in2 = "P9_25"
    GPIO.setup(enA, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    
    GPIO.output(enA, GPIO.LOW)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    
    
    #lcd setup
    cols = 20
    rows = 4

    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 2, numlines=rows)
    lcd.backlight()

   
    
    
    
    
    printhelp()

    while True:
        choice, *args = input(">").split()
        choice = choice.upper()
        try:
            args = list(map(int, args))
        except ValueError:
            print("Podano błędne argumenty :(")
            exit(1)

        if choice == 'Q' and len(args) == 2:
            conn, cur = establishConnection(db)
            silnikrobibrr()
            dots = countDots()
            result = "ilosc kostek " + str(dots)
            print(result)
            seed(dots)
            rand_number = randint(args[0], args[1])
            print(rand_number)
            lcd.printline(0, result.center(cols))
            lcd.printline(1,rand_number.center(cols ))
            
            
            cur.execute("Insert into Kropeczki (suma) values ("+ str(dots)+ ");")
            conn.commit()
            conn.close()


        elif choice == 'W' and len(args) == 3:
            conn, cur = establishConnection(db)
            cur.execute("select suma from Kropeczki order by id desc limit " + str(args[0]))
            records = cur.fetchall()
            total = sum([int(x[0]) for x in records])
            build_string = ""
            for i, x in enumerate(records):
                print(i, int(x[0]))
                build_string+=" {}".format(str(x[0]))
            
            split_string = [build_string[i:i+20] for i in range(0, len(build_string), 20)]
            
            seed(total)
            rand_number = randint(args[1], args[2])
            if len(split_string)<=4:
                
                for i,string in enumerate(split_string):
                    lcd.printline(i,string)
            else:
                lcd.printline(0,"za duzy output")
                lcd.printline(1,str(rand_number))
            conn.close()
            
            
        elif choice == "H" or "HELP":
            printhelp()
            
        elif choice == 'E':
            exit();
        else:
            print("Musiałeś coś źle wpisać :(")



