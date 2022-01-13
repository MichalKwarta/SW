import cv2
import sqlite3
# import liquidcrystal_i2c
from sys import exit
from random import seed, randint
from time import sleep

import Adafruit_BBIO.GPIO as GPIO




def silnikrobibrr(enA='P9_25', in1='P9_23', in2='P9_21'):

    GPIO.output(enA, GPIO.HIGH)
    # GPIO.output(in1, GPIO.HIGH)
    # GPIO.output(in2, GPIO.LOW)
    print("BRRRR")
    sleep(2)
    GPIO.output(enA, GPIO.LOW)
    # GPIO.output(in1, GPIO.LOW)
    # GPIO.output(in2, GPIO.HIGH)


# import Adafruit_BBIO.GPIO as GPIO

# class LCD:
#     def __init__(self):
#         self.cols = 20
#         rows = 4
#         self.lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 2, numlines=rows)
#     def print(self,text,row):
#         self.lcd.printline(row,text.center(self.cols))




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


if __name__ == '__main__':
    # lcd = LCD()
    db = r'Kropeczki.db'

    GPIO.setup("P9_21", GPIO.OUT)
    GPIO.setup("P9_23", GPIO.OUT)
    GPIO.setup("P9_25", GPIO.OUT)
    GPIO.output('P9_25', GPIO.LOW)
    GPIO.output('P9_23', GPIO.HIGH)
    GPIO.output('P9_21', GPIO.LOW)
    print('''L o S o W a Ń s K O
          q L U- losuj ziarno i wygeneruj liczbę z zakresu <L;U>
          w N L U - pobierz z bazy danych ostanie N wyników i wygeneruj liczbę z zakresu <L;U>  
          e - exit
          ''')

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
            silnikrobibrr()
            dots = countDots()
            print("ilosc kostek ",dots)
            seed(dots)
            print(randint(args[0], args[1]))
            cur.execute("Insert into Kropeczki (suma) values ("+ str(dots)+ ");")
            conn.commit()
            conn.close()


        elif choice == 'W' and len(args) == 3:
            conn, cur = establishConnection(db)
            cur.execute("select suma from Kropeczki order by id desc limit " + str(args[0]))
            records = cur.fetchall()
            total = sum([int(x[0]) for x in records])
            for i, x in enumerate(records):
                print(i, int(x[0]))

            seed(total)
            print(randint(args[1], args[2]))
            conn.close()

        elif choice == 'E':
            exit();
        else:
            print("Musiałeś coś źle wpisać :(")



