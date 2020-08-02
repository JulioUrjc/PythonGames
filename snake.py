import turtle
import time
import random

sleepTimer = 0.1

#Marcador
score = 0
high_score = 0

#Configuracion de la ventana
wn = turtle.Screen()
wn.title("Juego de Snake")
wn.bgcolor("black")
wn.setup(width = 600, height = 600)
wn.tracer(0)

#Cabeza serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("white")
cabeza.penup() #movimiento sin rastro
cabeza.goto(0,0)
cabeza.direction = "stop"

#Cuerpo serpiente
cuerpo = []

#Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup() #movimiento sin rastro
comida.goto(0,100)

#Marcador
marcador = turtle.Turtle()
marcador.speed(0)
marcador.color("white")
marcador.penup()
marcador.hideturtle()
marcador.goto(0, 260)
marcador.write("Score: 0    High Score: 0", align = "center", font = ("Courier", 18, "normal"))

#Funciones
def arriba():
    cabeza.direction = "up"
def abajo():
    cabeza.direction = "down"
def izquierda():
    cabeza.direction = "left"
def derecha():
    cabeza.direction = "right"


def mov():
    if cabeza.direction == "up":
        y = cabeza.ycor()
        cabeza.sety(y + 20)
    if cabeza.direction == "down":
        y = cabeza.ycor()
        cabeza.sety(y - 20)
    if cabeza.direction == "left":
        x = cabeza.xcor()
        cabeza.setx(x - 20)
    if cabeza.direction == "right":
        x = cabeza.xcor()
        cabeza.setx(x + 20)

def perder():
    time.sleep(1)
    #borrar segmentos
    for segmento in cuerpo:
        segmento.goto(400,400)
        del segmento
    #Borrar lista
    cuerpo.clear()

    cabeza.goto(0,0)
    cabeza.speed(0)
    cabeza.direction = "stop"
    score = 0
    marcador.clear()
    marcador.write("Score: {}    High Score: {}".format(score, high_score), align = "center", font = ("Courier", 18, "normal"))

#Teclado
wn.listen()
wn.onkeypress(arriba,"Up")
wn.onkeypress(abajo,"Down")
wn.onkeypress(izquierda,"Left")
wn.onkeypress(derecha,"Right")

#Bucle del juego
while True:
    wn.update()

    #Colisiones bordes
    cabezaX = cabeza.xcor()
    cabezaY = cabeza.ycor()
    if cabezaX > 280 or cabezaX < -280 or cabezaY > 280 or cabezaY < -280:
        perder()

    #Colisiones comida
    if cabeza.distance(comida) < 20:
        comidaX = random.randint(-280,280)
        comidaY = random.randint(-280,280)
        comida.goto(comidaX, comidaY)

        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")
        nuevo_segmento.color("grey")
        nuevo_segmento.penup() #movimiento sin rastro
        cuerpo.append(nuevo_segmento)

        #Aumentar marcador
        score+= 10
        if score > high_score:
            high_score = score

        marcador.clear()
        marcador.write("Score: {}    High Score: {}".format(score, high_score), align = "center", font = ("Courier", 18, "normal"))

    #mover cuerpo
    totalSeg = len(cuerpo)
    for index in range(totalSeg-1, 0, -1):
        x = cuerpo[index-1].xcor()
        y = cuerpo[index-1].ycor()
        cuerpo[index].goto(x, y)
    if totalSeg > 0:
        cuerpo[0].goto(cabezaX, cabezaY)

    mov()

    #Colisiones con el cuerpo
    for segmento in cuerpo:
        if cabeza.distance(segmento) < 20:
            perder() 

    time.sleep(sleepTimer)