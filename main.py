from distutils.command.build import build
import cv2
import sqlite3
import liquidcrystal_i2c
from sys import exit
from random import seed, randint
from time import sleep
import numpy as np
import Adafruit_BBIO.GPIO as GPIO


def silnikrobibrr(enA='P9_23'):
    sleep(0.5)
    GPIO.output(enA, GPIO.HIGH)
    sleep(0.15)
    GPIO.output(enA, GPIO.LOW)


def countDots():
    sleep(1)
    minDist = 13
    param1 = 160
    param2 = 11
    minRadius = 5
    maxRadius = 10

    camera = cv2.VideoCapture(0)
    _, img = camera.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist=minDist, param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        return len(circles[0])


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

    # pins setup
    in1 = "P9_21"
    pwm = "P9_23"
    in2 = "P9_25"
    GPIO.setup(pwm, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)

    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)

    # lcd setup
    cols = 20
    rows = 2

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
            lcd.clear()
            conn, cur = establishConnection(db)
            silnikrobibrr()
            dots = countDots()
            result = "Ile " + str(dots)
            print(result)
            seed(dots)
            rand_number = randint(args[0], args[1])
            print(rand_number)
            lcd.printline(0, str(result).center(cols))
            lcd.printline(1, str(rand_number).center(cols))

            cur.execute("Insert into Kropeczki (suma) values (" + str(dots) + ");")
            conn.commit()
            conn.close()


        elif choice == 'W' and len(args) == 3:
            lcd.clear()
            conn, cur = establishConnection(db)
            cur.execute("select suma from Kropeczki order by id desc limit " + str(args[0]))
            records = cur.fetchall()
            total = sum([int(x[0]) for x in records])
            build_string = ""
            for x in records:
                print(int(x[0]))
                build_string += " {}".format(str(x[0]))


            seed(total)
            rand_number = randint(args[1], args[2])
            print("wylosowano ",rand_number)
            if len(build_string) >=15:
                lcd.printline(0, build_string[:15])
                print("Output nie zmieścił sie na wyświetlaczu")
            else:
                lcd.printline(0, build_string)

            lcd.printline(1,str(rand_number).center(cols))



            conn.close()


        elif choice == "H":
            printhelp()

        elif choice == 'E':
            exit(0);

        else:
            print("Musiałeś coś źle wpisać :(")



