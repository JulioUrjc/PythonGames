import turtle
import time

sleepTimer = 0.02

#ventana
wn = turtle.Screen()
wn.title("Pong by July")
wn.bgcolor("black")
wn.setup(width= 800, height= 600)
wn.tracer(0)

#Jugador 1
jugador1 = turtle.Turtle()
jugador1.speed(0)
jugador1.shape("square")
jugador1.color("white")
jugador1.penup()
jugador1.goto(-350,0)
jugador1.shapesize(stretch_wid= 5, stretch_len= 1)

#Jugador 2
jugador2 = turtle.Turtle()
jugador2.speed(0)
jugador2.shape("square")
jugador2.color("white")
jugador2.penup()
jugador2.goto(350,0)
jugador2.shapesize(stretch_wid= 5, stretch_len= 1)

#Pelota
pelota = turtle.Turtle()
pelota.speed(0)
pelota.shape("square")
pelota.color("white")
pelota.penup()
pelota.goto(0,0)
pelota.dx = 3
pelota.dy = 3

#Linea division
division = turtle.Turtle()
division.color("white")
division.goto(0,400)
division.goto(0,-400)

#Marcador
marcador = turtle.Turtle()
marcador.speed(0)
marcador.color("white")
marcador.penup()
marcador.hideturtle()
marcador.goto(0,260)
marcador.write("Jugador 1: 0        Jugador 2: 0", align= "center", font=("Courier",24,"normal"))

marcadorJ1= 0
marcadorJ2= 0

#Funciones Palas
def jugador1_up():
    if jugador1.ycor() > 250:
        return
    y = jugador1.ycor() + 20
    jugador1.sety(y)
def jugador1_down():
    if jugador1.ycor() < -250:
        return
    y = jugador1.ycor() - 20
    jugador1.sety(y)
def jugador2_up():
    if jugador2.ycor() > 250:
        return
    y = jugador2.ycor() + 20
    jugador2.sety(y)
def jugador2_down():
    if jugador2.ycor() < -250:
        return
    y = jugador2.ycor() - 20
    jugador2.sety(y)


#Teclado
wn.listen()
wn.onkeypress(jugador1_up,"w")
wn.onkeypress(jugador1_down,"s")
wn.onkeypress(jugador2_up,"Up")
wn.onkeypress(jugador2_down,"Down")

while True:
    wn.update()

    pelota.goto(pelota.xcor()+pelota.dx, pelota.ycor()+pelota.dy)

    #Rebote bordes y
    if  pelota.ycor() > 290 or pelota.ycor() < -290:
        pelota.dy *= -1

    #Puntos
    if pelota.xcor() > 390 or pelota.xcor() < -390:
        if pelota.xcor() > 0:
            marcadorJ1+= 1
        else:
            marcadorJ2+= 1 

        pelota.goto(0,0)
        marcador.clear()
        marcador.write("Jugador 1: {}        Jugador 2: {}".format(marcadorJ1,marcadorJ2), align= "center", font=("Courier",24,"normal"))
        time.sleep(1)

    #Rebote pala
    if ((pelota.xcor() > 340 and pelota.xcor() < 350) 
            and (pelota.ycor() < jugador2.ycor() + 50
            and pelota.ycor() > jugador2.ycor() - 50)):
        pelota.dx *=-1

    if ((pelota.xcor() < -340 and pelota.xcor() > -350) 
            and (pelota.ycor() < jugador1.ycor() + 50
            and pelota.ycor() > jugador1.ycor() - 50 )):
        pelota.dx *=-1

    time.sleep(sleepTimer)