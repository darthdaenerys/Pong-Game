import cv2
import numpy as np
from HandDetectionModule import MediapipeLandmark

# parameters
width=1280
height=720
paddlewidth=150
paddleheight=20
paddlecolor=(75, 153, 242)
lives=3
deltax=10
deltay=-10
xpos=640
ypos=400
level=1
ball=True
ballradius=8
highscore=0
bgcolor=(30,79,24)
scorecolor=(149, 129,252)

camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
camera.set(cv2.CAP_PROP_FPS,30)
camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('Classic Pong Game',cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Classic Pong Game',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

prevval=683
myscore=0
handData=MediapipeLandmark(1)

while True:
    _,frame=camera.read()
    val=handData.Coordinates(frame)
    background=np.zeros([720,1366,3],dtype=np.uint8)
    background[:,:]=bgcolor
    frameresize=cv2.resize(frame,(144,81))
    frameresize=cv2.flip(frameresize,1)
    background[639:720,1222:1366]=frameresize
    if val==0:
        val=prevval
    else:
        prevval=val
    cv2.rectangle(background,(1366-(val-paddlewidth//2),720-paddleheight),(1366-(val+paddlewidth//2),720),paddlecolor,-1)
    paddlerightcorner=(1366-(val-paddlewidth//2),720-paddleheight)
    paddleleftcorner=(1366-(val+paddlewidth//2),720-paddleheight)
    if ball==True:
        cv2.circle(background,(xpos,ypos),ballradius,(255,255,255),-1)
        xpos+=deltax
        ypos+=deltay
    if xpos>=1360 or xpos<=5:
        deltax=-deltax
    if ypos<=10:
        deltay=-deltay
    if xpos<=paddlerightcorner[0] and xpos>=paddleleftcorner[0]:
        if ypos>=695 and ypos<=710:
            deltay=-deltay
            myscore+=1
            if myscore%5==0 and myscore>=5:
                level+=1
                if deltax<0:
                    deltax-=2
                else:
                    deltax+=2
                if deltay<0:
                    deltay-=1
                else:
                    deltay+=1
    cv2.putText(background,'Lives: '+str(lives),(1200,35),cv2.FONT_HERSHEY_PLAIN,2,scorecolor,2)
    cv2.putText(background,'Level: '+str(level),(1200,68),cv2.FONT_HERSHEY_PLAIN,2,scorecolor,2)
    cv2.putText(background,'Score: '+str(myscore),(1200,101),cv2.FONT_HERSHEY_PLAIN,2,scorecolor,2)
    if ypos>=720:
        lives-=1
        temp=cv2.blur(background,(15,15))
        cv2.putText(temp,'You Lost a Life !',(300,360),cv2.FONT_HERSHEY_DUPLEX,3,(185,89,200),3,1)
        cv2.imshow('Classic Pong Game',temp)
        cv2.waitKey(2000)
        xpos=640
        ypos=400
        if deltay>0:
            deltay=-deltay
    if lives==0:
        ball=False
        deltax=10
        deltay=-10
        level=0
        background=cv2.blur(background,(20,20))
        cv2.waitKey(1000)
        for i in range(0,720,10):
            background[i:i+10,:]=(24,34,255)
            cv2.imshow('Classic Pong Game',background)
            cv2.waitKey(10)
        cv2.putText(background,'GAME OVER',(400,360),cv2.FONT_HERSHEY_DUPLEX,3,(0,255,255),2)
        cv2.putText(background,'Your Score: '+str(myscore),(420,420),cv2.FONT_HERSHEY_PLAIN,2,(0,255,35),2)
        if myscore>highscore:
            highscore=myscore
        cv2.putText(background,'HIGH SCORE: '+str(highscore),(420,480),cv2.FONT_HERSHEY_PLAIN,2,(0,255,56),2)
        cv2.putText(background,'Press q twice to exit or game restarts in 5 seconds',(300,550),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),2)
        cv2.imshow('Classic Pong Game',background)
        cv2.waitKey(5000)
        ball=True
        myscore=0
        lives=3
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
    cv2.imshow('Classic Pong Game',background)
camera.release()