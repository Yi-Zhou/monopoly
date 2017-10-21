# Subject: COMP 1001
# Name: Zhou Yi
# Student ID: 14109328D

from graphics import *
from random import *
from datetime import datetime
from datetime import timedelta
import calendar
import os

#***********************************************************************************************
#
# http://www.gulps.cyc.edu.tw/tncyfkks/2/color.htm  get color
#
#************************************************************************************************
#
# This game is called Monopoly
#
#************************************************************************************************
#
# I have used try-except and while loop to prevent the game from player's bad-inputs
# in every human-computer interactive interfaces below
#
# A breif introduction of Rules and Playing Methods of this game are as follows:
#
# 1. At the beginning of the game, The interface will ask the player to input the infomation and 
# the wanted initial settings, including the shape and color of their Chess Pieces, initial Cash,
# initial Coupon, the number of players
#
# 2. After entering the main game, the players will throw a die (which is a random integer) and 
# walk corresponding number of steps from one block to another. Each round will counts for one
# "day" in the game. The starting date is 2015 Jan. 14 in this game.
# (I imported functions(classes) from datetime.py and calendar.py to conduct with dates)
#
#************************************************************************************************
#
# 3. Before a player throwing a dice, he or she may choose to do things as follws:
#                                               (It is called preparation period)
#
# (1). Look at infomation of each players
#     *In this choice, the interface will print out each player's infomation including
#      Cash, Coupon, Props, Cards, the number of grounds he or she have etc.
# 
# (2). Use Props or Cards
#     *There are total number of 19 kind of Card and 7 kind of Prop in this game
#      Different prop or card has different functions
#      It is one of the most colorful and difficult part of this programme
#      (Functions of each kind of card or prop vide infra)
#
# (3). Save or Load game records
#     *The player may choose to either save or load game here
#      If the user chooses to save, this programme will create a file and write the game 
#      infomations into it
#      elif the user chooses to load, he or she just need to input the name of the file which 
#      contains his or her game infomation.
#      (I have used a combination of while loop and try-except in this part to prevent FileNotFoundError)
#
# (4). Throw the die
#     *The Chess piece representing the player will move on the chess board and trigger events
#      according the block he or she falls on.
#      After the player chooses this, he or she will not be able to do other things until next round.
#
# (5). Quit the game
#     *In case the player chooses this option carelessly, the interface will ask the player
#      "Are you sure to quit the game?" to confirm his or her choice.
#      If the player is sure to quit the game, he or she will be regard as "bankrupt"
#      All of the infomation related to him or her will be erased.
#
#************************************************************************************************
#
# 4. Blocks
#
#    When a player's chess piece goes on a certain block, a event will ensue.
#    There are totally 8 different kinds of blocks.
#
# (1). Grounds
#     *Gounds are main sites where players exchange their game money.
#      The rule of exchangement is as follows:
#
#   (i). Vacant ground
#       At the beginning of the game, every grond on the chess board is vacant.
#       If the player falls on this site, he or she will be asked whether to "buy" this ground.
#       If the player chooses "yes", the ground will be considered "belongs to" that player.
#       And the ground will turn to be occupied.
#       The price of the ground is caculated by this formular:
#
#           price=round(houseprice*(houselevel+1)*priceindex)
#
#       where "houseprice" is the initial houseprice of each gronud.
#             "priceindex" is a parameter which is initialize to 1 at the beginning of the game
#                          and it will rise by 12% per month. This parameter can accelerate the
#                          process of the game. (In case the game lasts too long.)
#             "houselevel" is the level of the ground and can be upgraded by the owner.
#
#   (ii). Occupied ground
#
#       ******** Toll ********
#
#       If the certain ground has been bought by a certain player, every other palyers falling on
#       this block have to pay some money as "toll" to the ground owner.
#       The formular caculating the "toll" is:
#
#           price=round(houseprice*(houselevel+1)*priceindex)
#           addition=∑price1*0.1
#           toll=int(price*0.3+addition)
#             
#       where "price1" is the price of the ground which is in the same "street" with the event block
#       and is owned by the same owner. It is caculated by the same formular for price.
#
#       For example:
#       Bob bought a ground in the street "Hung Hom". Several rounds later, John falls on this ground.
#       Because Bob simultaneously owns some other gronds in "Hung Hom" which in the same "street", 
#       during the caculation of "toll", John will have to pay Bob not only the toll for this single ground,
#       but also additional fees caused by other grounds in the same "street".
#
#       *The unlucky toll payer will pay the toll in Cash first.
#        If his or her Cash is not enough, he or she will pay it by Deposit.
#        And if his or her total assets is 0, he or she will be declared "Bankrupt".
#
#       ******** Upgrading ********
#
#       If the guy falling on an occupied ground is the owner per se, the player will be asked whether
#       to upgrade this ground. If his or her Cash is enough, houselevel will increase by 1 where the max
#       level of a ground is 6(initial level is 0). The cost of upgrading is just the initial houseprice. 
#       As we can see in the formular of toll above, a higher level will cause a higher toll.
#

# (2). Coupon Points
#      *Players can get complimentary coupons from these points.
#       Players can use these coupons to buy Props and Cards from groceries.
#
# (3). Groceries
#      *In this map, there are totally two groceries. Players can buy Props or Cards using their coupon here.
#
# (4). Banks
#      *In this map, there are two banks, one Bank of China and one Heng Seng Bank.
#       The player PASS or FALLS ON this block will be able to save or withdraw money here.
#
#      *Bank doesn't work on Sunday
#
# (5). Lottery points
#      *Players can buy lottery in this block
#
# (6). News Block:
#      *A random event will ensue if a player falls on this block.
#       Possible events are as follows:
#
#     (i). 公開表揚第一地主,獎勵$5000
#          The player who owns most grounds will get $5000.
#    (ii). 公開補助土地最少者$5000
#          The player who owns least grounds will get $5000.
#   (iii). 銀行加發儲金紅利所有人得到存款8.0%
#          Deposit of each player increases by 8.0%.
#    (iv). 豪雨特報行人停走一回
#          Every player have to stop for a round.
#     (v). 八號風球席捲香港摧毀房屋一棟
#          A random house will be destoryed and its houselevel decreases by 1.
#          There are no houses on the map, nobody will be influenced.
#    (vi). 所有人交個人所得稅10%'
#          Deposit of each player decreases by 10.0%.
#
# (7). Complimentary Card(Prop) Point
#      Player will get one random Card(Prop) here.
#
# (8). Park and blocks marked by nothing or "空"
#      Nothing will happen.
#
#   *If the player's inventory is full (have more than 12 Cards or more than 12 Props),
#    He or she will not be able to get Free Card or Prop at block (7) or (8)
#
# (9). PolyU
#      *Player will get a scholarship of $5000 at this point.
#************************************************************************************************
# 
# 5. Props and Cards can be used to do harm to others or benifit yourself, or both simultaneously.
#    Here are the effects of Cards and Props
#
#  ******************************** Cards ********************************
#
# (1). 陷害卡(Framing Card)
#     It can be used at a player who is at most 5 steps away from the user(excluding the user per se).
#     The victim will have to be imprisoned for 3 "days".
#
#     *Other players needn't pay toll to him or her if he or she is in prison.
#     *It's effect can be offset by 免罪卡(Exoneration Card)
#     *or be transfered to another player by 嫁禍卡(CalamityShift Card).
#
# (2). 轉向卡(Veer Card)
#     It can be used at a player who is at most 5 steps away from the user(including the user per se).
#     The target player will veer back(change his or her direction of moving).
#
# (3). 免費卡(Free Card)
#     It can be used when a player have to pay a bill exceeding $2000.
#     The player will not need to pay the money as long as he or she uses this card.
#
# (4). 停留卡(Stop Card)
#     It can be used to a player who is at most 5 steps away from the user(including the user per se).
#     The target player have to stop for a round.
#
# (5). 天使卡(Angle Card)
#     It can be used when the user is standing on a ground.
#     A very powerful card. It can upgrade all of the houses in a whole street.
#
# (6). 惡魔卡(Devil Card)
#     It can be used when the user is standing on a ground.
#     Which is oppisite to Angle Card, It can degrade all of the houses in a whole street.
#
# (7). 拆除卡(Demolition Card)
#     It can be used at a ground which is at most 5 steps away from the user.
#     Degrade a house(houselevel-=1).
#
# (8). 烏龜卡(Turtle Card)
#     It can be used at a player who is at most 5 steps away from the user(including the user per se).
#     The target player can only walk 1 step each round for 3 rounds.
#
# (9). 購地卡(Purchase Card)
#     It can be used when the user is standing on a ground which is owned by others
#     The owner of the ground is forced to sell this ground to the card user.
#     *The Card user have to pay the money to the original owner to buy this ground.
#      If his or her Cash is not enough, he will not be able to use this card.
#
# (10). 怪獸卡(Monster Card):
#     It can be used at a ground which is at most 5 steps away from the user.
#     The houselevel of the target ground will be lowered to 0 after using this card.
#
# (11). 搶奪卡(Rob Card)
#     It can be used at a player who is at most 5 steps away from the user(excluding the user per se).
#     The user may get a Card or Prop from the target player by using this card.
#
# (12). 冬眠卡(Hibernation Card)
#     It can be used at any preparation time
#     Every Player except the user per se will have to sleep for 5 rounds.
#     During sleeping, they can not charge tolls from the user if the user falls on their grounds.
#
# (15). 夢遊卡(DreamWalk Card)
#     It can be used at a player who is at most 5 steps away from the user(excluding the user per se).
#     The target player have to Dream Walk for 5 days in which he can not trigger any events on
#     functional blocks but he or she have to pay the toll when falling on other player's ground.
#
#     *Other players needn't pay toll to him or her if he or she is Dream Walking.
#     *It's effect can be offset by 免罪卡(Exoneration Card)
#     *or be transfered to another player by 嫁禍卡(CalamityShift Card).
#
# (14). 免罪卡(Exoneration Card)
#     It cannot be used actively.
#     This Card can offset an attack from other's 陷害卡(Framing Card) or 夢遊卡(DreamWale Card).
#
# (15). 嫁禍卡(CalamityShift Card)
#     It cannot be used actively.
#     This Card can transfer the effect of 陷害卡(Framing Card) or 夢遊卡(DreamWale Card) to another player.
#     *Transfers can occur more than once if the target player also has 嫁禍卡(CalamityShift Card).
#
# (16). 均富卡(AverageRich Card)
#     It can be used at any preparation time.
#     To sum up the Cashes of all the players and redistribute it to each player evenly.
#
#     *For example:
#      Player A,B,C,D have Cash $10000,$20000,$30000,$40000 respectively
#      If Player A uses AverageRich Card, Cash of each player will be $25000,$25000,$25000,$25000.
#      which is the average of the sum.
#
# (17). 均貧卡(AveragePoor Card)
#     It can be used at a player who is at most 5 steps away from the user(excluding the user per se).
#     Different from AverageRich Card, only the Cash of the user and the target player will be averaged.
#
# (18). 查稅卡(Tax Card)
#     It can be used at a player who is at most 5 steps away from the user(excluding the user per se).
#     The user will get 10% of the Cash of the target player
#
# (19). 復仇卡(Revenge Card)
#     It cannot be used actively but used atomatically
#     When the player is framed to prison or have to Dream Walk, if he or she has Revenge Card, the Card user
#     who contributes to this will have be sent to prison or Dream Walk together with him or her.
#
#  ******************************** Props ********************************
#
# (1). 遙控骰子(Wishful Dice)
#    The user will be asked to input a number. Then, after he or she throw the dice,
#    the dice will come up this number. (Players can control his number of steps by using this prop2).
#
# (2). 路障(Barrier Block)
#    This prop can be put on a block which is at most 5 steps away from the position of the user.
#    A Barrier will display on the chosen block in the graphics window.
#    Later, any player who PASSES BY or FALLS ON this block will be blocked by the barrier.
#    Once the barrier has blocked one player, the barrier will be erased.
#
# (3). 地雷(LandMine)
#    This prop can be put on a block which is at most 5 steps away from the position of the user.
#    A Land Mine will display on the chosen block in the graphics window.
#    Later, once a player FALLS ON this block, the Mine will explode and the player will be sent to the hospital.
#    And stay there for 3 days.
#    The event on that block will not be triggered.
#
# (4). 定時炸彈(TimeBomb)
#    This prop can be put on a block which is at most 5 steps away from the position of the user.
#    A TimeBomb will desplay on the chosen block in the graphics window.
#    Later, once a player FALLS ON this block, he or she will be attached by the TimeBomb.
#    The TimeBomb will explode once the unlucky player has walked 30 steps.
#    TimeBomb can be passed between players when the one who is attached by a TimeBomb pass by another player.
#
#    For example:
#    A TimeBomb attaching on Player A will be passed to Player B if Player A pass by Player B.
#
#    *One player can only carry one TimeBomb.
#     (If Player A falls on a block where there is a TimeBomb, he will not be attached by the TimeBomb again)
#     (If Player B above has already been attached by a TimeBomb, TimeBomb attached on A will not be passed to B)
#
#    *Once a TimeBomb is attached on a player, the number on the up-left coner of the graphics window for that
#     player will turn red and the number is just the number of steps left before the explosion of TimeBomb.
#
#    *If Player A above (attached by a TimeBomb) happen to fall on a LandMine, the TimeBomb will also
#     explode due to the explosion of LandMine. So he or she will have to stay in the hosipital for more days.
#
#    *One block can only contain one object (Barrier Block \ LandMine \ TimeBomb)
#
# (5). 機器工人(Mechanic Workers)
#    This prop can be used at a ground which is at most 5 steps away from the user.
#    The houselevel of that ground will be increased by 1 if it is not at the highest level(6)
#    *If the house has been the highest level, this prop cannot be used.
#
# (6). 機器娃娃(Street Cleaner)
#    A Street Cleaner will be dispatched and the objects (Barrier Block / LandMine / TimeBomb)
#    on 10 steps of blocks in front of the user will be erased.
#
#************************************************************************************************
#
# Interest distributed by the Bank:
# On the first day of every month, the bank will give out interests.
# The interst for each player is 10.0% of his or her Deposit.
# At the same time, the price index will increase by 15.0%.
#
#************************************************************************************************
#
# Draw the winning number for the lottery
# At the middle of every month, a number will be draw as the winning number of the lottery.
# The initial prize of lottery is $4000.
# If no one win the prize in a month, the prize will be accumulated to next month.
# The amount of prize can also be affected by priceindex.
#
#************************************************************************************************
#
# Functions of this programme can be divided into 3 main parts
#
# Part I:
# Chess Board Drawing functions
# These are a pile of functions which can draw a chess board for the players to play on

#
# Part II:
# Game Operation functions
# These pile of functions will create a player-computer interface
# which enables the players to play the game according to the game rules
#
# Part III:
# File Conducting functions
# These functions conduct with Saving and Loading game history records
#
#************************************************************************************************
#
# ★ Remarks: 
#
# Actually, the number of Cards or Props a player can carry has a upper limit (12).
# Every player should have no Cards at the beginning of the game.
#
# However, for the convenience of testers, every player in this version will have every kind of Cards
# even if it has exceeded the upper limit.
# (This may cause the event that the players cannot get complimentary card
#  because "inventory is full" at the block "Free Card Point".)
#
# Please notice that it is just for tester's convenience but not a bug.
#
# In case the user of this programme may enter bad-inputs carelessly,
# users can answer questions like "(Y/N)?" affirmatively just by input any key except "N" and "n"
#
# Pls be reminded that for your convenience of remarking, every one has a CalamityShift Card(嫁禍卡) and
# an Exoneration Card(免罪卡) at the beginning of the game when testing Framing Card.
#
#************************************************************************************************
#
#

'''def Coordinates(win):   #Help me to determine the position of objects.  #Line 4
    for i in range(100):
        P=Point(10*(i+1),1)
        P.draw(win)
    for i in range(100):
        P=Point(1,10*(i+1))
        P.draw(win)
    for i in range(20):
        P1=Point(50*(i+1),10)
        P2=Point(50*(i+1),700)
        message=Text(P1,50*(i+1))
        message.draw(win)
        line=Line(P1,P2)
        line.draw(win)
        line.setFill('silver')
    for i in range(35):
        P1=Point(18,50*(i+1))
        P2=Point(1000,50*(i+1))
        message=Text(P1,50*(i+1))
        message.draw(win)
        line=Line(P1,P2)
        line.setFill('silver')
        line.draw(win) '''

def Rectan(x,y,width,height):   #Line 27                             
    rect=Rectangle(Point(x-width/2,y+height/2),Point(x+width/2,y-height/2))
    return rect

# This function is used to draw blocks of the chess board
# It can simplify the process of drawing blocks
# (Only need the position of the center point, length, width to draw a rectangle.) 


def Trian(x,y,a):   #Line 31
    P1=Point(x-a,y+a/2*(3**0.5))
    P2=Point(x+a,y+a/2*(3**0.5))
    P3=Point(x,y-a/(3**0.5))
    tri=Polygon(P1,P2,P3)
    return tri

# Somewhat similar to the function Rectan()
# Draw a isosceles Triangle directly

def kiosk(win,x,y,a):
    P1=Point(x-a,y+a/4)
    P2=Point(x,y+a)
    P3=Point(x+a,y+a/4)
    P4=Point(x+a,y)
    P5=Point(x-a,y)
    roof=Polygon(P1,P2,P3,P4,P5)
    roof.setFill('sandybrown')
    roof.draw(win)
    rect1=Rectan(x-32.5*a/40,y-a/2,3*a/8,a)
    rect1.setFill('darkred')
    rect1.draw(win)
    rect2=Rectan(x+32.5*a/40,y-a/2,3*a/8,a)
    rect2.setFill('darkred')
    rect2.draw(win)
    text=Text(Point(100,530),'PARK')
    text.draw(win)

# Draw a kiosk for the block "park"
    
def Cross(x,y,a):   #Line 38
    P1=Point(x+a/2,y+a/2)
    P2=Point(x+a/2,y+3*a/2)
    P3=Point(x-a/2,y+3*a/2)
    P4=Point(x-a/2,y+a/2)
    P5=Point(x-3*a/2,y+a/2)
    P6=Point(x-3*a/2,y-a/2)
    P7=Point(x-a/2,y-a/2)
    P8=Point(x-a/2,y-3*a/2)
    P9=Point(x+a/2,y-3*a/2)
    P10=Point(x+a/2,y-a/2)
    P11=Point(x+3*a/2,y-a/2)
    P12=Point(x+3*a/2,y+a/2)
    cross=Polygon(P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12)
    return cross

# Draw a cross using a as wdith of each edge

def DrawBarrier(p,win):   #Line 54
    x=p.getX()
    y=p.getY()
    R1=rect1=Rectan(x,y+5,30,6)
    R2=rect2=Rectan(x-13,y-3,4,9)    
    R3=rect3=Rectan(x+13,y-3,4,9)
    rect1.setFill('orangered')
    rect2.setFill('peru')
    rect3.setFill('peru')
    return R1,R2,R3

# Draw a barrier

def DrawLandMine(p,win):  #Line 65
    x=p.getX()
    y=p.getY()
    cir=Circle(p,10)
    cir.setFill('black')
    line1=Line(Point(x-5,y),Point(x+5,y))
    line2=Line(Point(x,y+5),Point(x,y-5))
    line1.setFill('red')
    line2.setFill('red')
    line3=Line(Point(x,y+10),Point(x,y+15))
    line4=Line(Point(x,y+15),Point(x+3,y+15))
    line3.setFill('saddlebrown')
    line4.setFill('saddlebrown')
    return [cir,line1,line2,line3,line4]

# Draw a LandMine for prop using

def DrawTimeBomb(p,win):    #Line 80
    x=p.getX()
    y=p.getY()
    S=[]
    rec=Rectan(x-3,y,2,12)
    for i in range(6):
        rec=Rectan(x-7.5+3*i,y,3,25)
        rec.setFill('red')
        S.append(rec)
    line=Line(Point(x-9,y),Point(x+9,y))
    line.setFill('saddlebrown')   
    S.append(line)
    cir=Circle(p,1.7)
    cir.setFill('saddlebrown')
    S.append(cir)
    return S

# Draw a TimeBomb for prop using

def DrawStreetCleaner(p,win):
    x=p.getX()
    y=p.getY()
    p0=Point(x-2.5,y+5)
    p1=Point(x-2.5,y+10)
    p2=Point(x+2.5,y+10)
    p3=Point(x+2.5,y+5)
    p4=Point(x+0.5,y+5)
    p5=Point(x+0.5,y+2)
    p6=Point(x+4,y)
    p7=Point(x+3.5,y-0.5)
    p8=Point(x+0.5,y)
    p9=Point(x+0.5,y-5)
    p10=Point(x+4,y-9.5)
    p11=Point(x+3.5,y-10.5)
    p12=Point(x,y-5)
    p13=Point(x-3.5,y-10.5)
    p14=Point(x-4,y-9.5)
    p15=Point(x-0.5,y-5)
    p16=Point(x-0.5,y)
    p17=Point(x-3.5,y-0.5)
    p18=Point(x-4,y)
    p19=Point(x-0.5,y+2)
    p20=Point(x-0.5,y+5)
    baby=Polygon(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20)
    baby.setFill('black')
    return baby
    
# Draw a little lovely guy as the StreetCleaner for prop using

def cp(x,y,t,s,color):    #draw 'ten' coupon points   #Line 98
    tex=Text(Point(x,y),s)
    tex.setFill(color)
    t.append(tex)
    
# Draw coupon points

def CreateChessBoard():      #Line 104
    win=GraphWin('Chess Board',1000,700)
    win.setCoords(0.0,0.0,1000.0,700.0)
    win.setBackground('powderblue')
    #Coordinates(win)   # Can change this line into presudu code when playing
    S=[]   # collect the blocks
    T=[]   # collect the coordinates
    recA=Rectan(100,150,100,100)
    recA.setFill('gold')
    S.append(recA)
    T.append(Point(100,150))
    for i in range(5):
        rect=Rectan(75,230+i*60,50,60)
        S.append(rect)
        T.append(Point(75,230+i*60))
    recB=Rectan(100,550,100,100)
    recB.setFill('lawngreen')
    S.append(recB)
    T.append(Point(100,550))
    for i in range(3):
        cir=Circle(Point(175+i*50,575),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(175+i*50,575))
    squareA=Rectan(310,525,50,50)
    squareA.setFill('lawngreen')
    S.append(squareA)
    T.append(Point(310,525))
    for i in range(2):
        cir=Circle(Point(275-50*i,475),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(275-50*i,475))
    for i in range(2):
        rect=Rectan(170,460-i*60,50,60)
        S.append(rect)
        T.append(Point(170,460-i*60))
    squareB=Rectan(170,345,50,50)
    S.append(squareB)
    T.append(Point(170,345))
    rect=Rectan(225,345,60,50)
    S.append(rect)
    T.append(Point(225,345))
    squareC=Rectan(280,345,50,50)
    squareC.setFill('bisque')
    S.append(squareC)
    T.append(Point(280,345))
    for i in range(2):
        rect=Rectan(280,290-i*60,50,60)
        S.append(rect)
        T.append(Point(280,290-i*60))
    for i in range(2):
        cir=Circle(Point(340+i*50,230),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(340+i*50,230))
    for i in range(2):
        cir=Circle(Point(390,280+i*50),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(390,280+i*50))
    squareD=Rectan(390,382,50,50)
    squareD.setFill('lightblue')
    S.append(squareD)
    T.append(Point(390,382))
    for i in range(2):
        cir=Circle(Point(390,436+i*50),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(390,436+i*50))
    recC=Rectan(425,565,100,100)
    decolor=['dodgerblue','forestgreen','#DC143C']
    for i in range(3):
        deco=Rectan(425,615-(2*i+1)*100/6,100,100/3)
        deco.setFill(decolor[i])
        deco.setOutline('white')
        deco.draw(win)
    S.append(recC)
    T.append(Point(425,565))
    for i in range(5):
        rect=Rectan(505+60*i,590,60,50)
        S.append(rect)
        T.append(Point(505+60*i,590))
    squareE=Rectan(800,590,50,50)
    S.append(squareE)
    T.append(Point(800,590))
    recD=Rectan(875,565,100,100)
    recD.setFill('white')
    S.append(recD)
    T.append(Point(875,565))
    squareF=Rectan(850,490,50,50)
    squareF.setFill('gold')
    S.append(squareF)
    T.append(Point(850,490))
    for i in range(2):
        rect=Rectan(795-i*60,490,60,50)
        S.append(rect)
        T.append(Point(795-i*60,490))
    squareG=Rectan(680,490,50,50)
    squareG.setFill('greenyellow')
    S.append(squareG)
    T.append(Point(680,490))
    for i in range(2):
        rect=Rectan(625-i*60,490,60,50)
        S.append(rect)
        T.append(Point(625-i*60,490))
    for i in range(3):
        cir=Circle(Point(510,490-50*i),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(510,490-50*i))
    for i in range(5):
        rect=Rectan(565+60*i,390,60,50)
        S.append(rect)
        T.append(Point(565+60*i,390))
    squareH=Rectan(860,390,50,50)
    squareH.setFill('bisque')
    S.append(squareH)
    T.append(Point(860,390))
    for i in range(2):
        cir=Circle(Point(860,340-50*i),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(860,340-50*i))
    cir=Circle(Point(815,270),22)
    cir.setFill('seashell')
    S.append(cir)
    T.append(Point(815,270))
    recE=Rectan(735,300,100,100)
    recE.setFill('peru')
    S.append(recE)
    T.append(Point(735,300))
    for i in range(3):
        rect=Rectan(655-60*i,325,60,50)
        S.append(rect)
        T.append(Point(655-60*i,325))
    squareI=Rectan(530,275,50,50)
    squareI.setFill('indianred')
    S.append(squareI)
    T.append(Point(530,275))
    for i in range(2):
        rect=Rectan(535+60*i,225,60,50)
        S.append(rect)
        T.append(Point(535+60*i,225))
    cir=Circle(Point(650,225),22)
    cir.setFill('seashell')
    S.append(cir)
    T.append(Point(650,225))
    cir=Circle(Point(700,200),22)
    cir.setFill('seashell')
    S.append(cir)
    T.append(Point(700,200))
    cir=Circle(Point(750,190),22)
    cir.setFill('seashell')
    S.append(cir)
    T.append(Point(750,190))
    recF=Rectan(830,150,100,100)
    S.append(recF)
    for i in range(3):
        deco=Rectan(830,200-(2*i+1)*100/6,100,100/3)
        deco.setFill(decolor[i])
        deco.setOutline('white')
        deco.draw(win)
    T.append(Point(830,150))
    for i in range(3):
        rect=Rectan(750-60*i,125,60,50)
        S.append(rect)
        T.append(Point(750-60*i,125))
    recG=Rectan(550,125,100,100)
    recG.setFill('lightskyblue')
    S.append(recG)
    T.append(Point(550,125))
    for i in range(3):
        rect=Rectan(470-60*i,125,60,50)
        S.append(rect)
        T.append(Point(470-60*i,125))
    squareJ=Rectan(295,125,50,50)
    squareJ.setFill('lightgreen')
    S.append(squareJ)
    T.append(Point(295,125))
    for i in range(2):
        cir=Circle(Point(237-54*i,125),22)
        cir.setFill('seashell')
        S.append(cir)
        T.append(Point(237-54*i,125))
    t=[]
    polyu=Text(Point(530,275),'PolyU')
    polyu.setFill('white')
    t.append(polyu)
    t.append(Text(Point(620,275),'紅磡(Hung Hom)'))
    t.append(Text(Point(675,425),'九龍灣(Kowloon Bay)'))
    t.append(Text(Point(675,525),'沙田(Sha Tin)'))
    t.append(Text(Point(650,625),'荃灣(Tsuen Wan)'))
    t.append(Text(Point(260,380),'旺角(Mong Kok)'))
    atext=Text(Point(150,225),'(Tsim Sha Tsui)')
    atext.setSize(10)
    t.append(atext)
    atext=Text(Point(150,250),'尖沙咀')
    atext.setSize(10)
    t.append(atext)
    t.append(Text(Point(410,90),'金鐘(Admiralty)'))
    t.append(Text(Point(700,90),'銅鑼灣(Causeway Bay)'))
    t.append(Text(Point(550,140),'中銀大廈'))
    t.append(Text(Point(550,110),'(BOC Tower)'))
    t.append(Text(Point(210,70),'西區海底隧道'))
    t.append(Text(Point(210,90),'Western Harbor Tunnel'))
    t.append(Text(Point(235,517),'彌敦道'))
    t.append(Text(Point(232,537),'Nathan Road'))
    t.append(Text(Point(430,350),'青\n山\n公\n路'))
    t.append(Text(Point(650,175),'海底隧道'))
    t.append(Text(Point(910,220),'公主道'))
    t.append(Text(Point(910,250),'Princess Margaret\nRoad'))
    t.append(Text(Point(475,440),'大\n老\n山\n公\n路'))
    t.append(Text(Point(735,300),'壁屋監獄'))
    t.append(Text(Point(100,620),"九龍公園\n(Kowloon Park)"))
    cp(175,575,t,'10','brown')
    cp(275,575,t,'10','brown')
    cp(390,330,t,'10','brown')
    cp(510,490,t,'10','brown')
    cp(860,340,t,'10','brown')
    cp(225,475,t,'20','tomato')
    cp(340,230,t,'20','tomato')
    cp(390,486,t,'20','tomato')
    cp(510,440,t,'20','tomato')
    cp(860,290,t,'20','tomato')
    cp(750,190,t,'20','tomato')
    cp(650,225,t,'30','tomato')
    cp(237,125,t,'30','tomato')
    cp(390,436,t,'50','chocolate')
    cp(815,270,t,'50','chocolate')
    cp(390,280,t,'50','chocolate')
    cp(225,575,t,'50','chocolate')
    cp(275,475,t,'空','sienna')
    cp(700,200,t,'空','sienna')
    cp(390,230,t,'空','sienna')
    cp(510,390,t,'空','sienna')
    cp(183,125,t,'空','sienna')
    rect=Rectan(875,640,100,50)
    rect.setFill('white')
    t.append(rect)
    text=Text(Point(875,640),'SickRoom')
    text.setSize(15)
    t.append(text)
    for i in S:
        i.draw(win)
    for i in t:
        i.draw(win)
    cro=Cross(875,565,30)
    cro.setFill('red')
    cro.draw(win)
    text=Text(Point(335,568),'京士柏公園\n(Kings Park)')
    text.setSize(10)
    text.draw(win)
    text=Text(Point(309.8,515),'PARK')
    text.setSize(7)
    text.draw(win)
    text=Text(Point(100,150),'Mark\nSix\nLottery!!')
    text.setFill('mediumblue')
    text.draw(win)
    text=Text(Point(850,490),'Lottery!')
    text.setFill('mediumblue')
    text.setSize(10)
    text.draw(win)
    text=Text(Point(425,565),'TVB\nNews')
    text.draw(win)
    text=Text(Point(830,148),'TVB\nNews')
    text.draw(win)
    text=Text(Point(680,490),'Hang\nSeng\nBank')
    text.setSize(9)
    text.draw(win)
    text=Text(Point(875,565),'沙田醫院\nShatin Hospital')
    text.setFill('lightgrey')
    text.setSize(9)
    text.draw(win)
    text=Text(Point(280,345),'PARKn\nSHOP')
    text.setSize(9)
    text.draw(win)
    text=Text(Point(860,390),'Wellcome\nSuper\nmarket')
    text.setSize(8)
    text.draw(win)
    rect=Rectan(735,270,100,40)
    rect.setFill('sienna')
    rect.draw(win)
    text=Text(Point(295,125),'Free\nProp\nPoint')
    text.setSize(10)
    text.draw(win)
    text=Text(Point(390,382),'Free\nCard\nPoint')
    text.setSize(10)
    text.draw(win)
    kiosk(win,100,550,40)
    kiosk(win,310,525,20)
    houseposition=[1,2,3,4,5,13,14,16,18,19,28,29,30,31,32,36,37,39,40,44,45,46,47,48,54,55,56,58,59,64,65,66,68,69,70]
    for i in houseposition:
            S[i].setFill('lemonchiffon')
    return(win,S,T)

# A large function to draw the chess board and return the points and block objects for future use
# The map of the chessboard is based on the map of Hong Kong.

def getint(question,requirement):
    print(question)
    while True:
        try:
            integer=int(input(requirement))
            break
        except ValueError:
            print('Error!Please enter again.')
    return integer

# get an integer from a player

def GetPlayerInfo(color0):       #Line 320
    while True:
        try:
            print('The maximum number of players is ',len(color0),'.',sep='')
            pn=int(input('How many players are there?\n'))
            if pn>len(color0):
                print('\nError! Please enter again.')
                continue
            break
        except ValueError:
            print('\nError! Please enter again.')
    namelist=[]
    for i in range(pn):
        print('The name of the player',i+1,'is:')
        name=input()
        namelist.append(name)
    return pn,namelist

# Create the namelist

def initialsettings():    #Line 336
    print('\nSuggestive number of possetion for each person are (1),(2)and(3):\n')
    print('(1) Cash: $40000    Deposit: $40000')
    print('(2) Cash: $70000    Deposit: $70000')
    print('(3) Cash: $100000    Deposit: $100000')
    print('(4) Let me determine it!')
    while True:
        print('\nHow much initial possession do you want? (Enter the number above please.)')
        try:
            choi2=int(input('Please enter your choice: '))
        except ValueError:
            print('\nYour input is not valid.')
            continue
        if choi2==1 or choi2==2 or choi2==3:
            Cash=10000+choi2*30000
            Deposit=10000+choi2*30000
            break
        elif choi2==4:
            Cash=-1
            Deposit=-1
            while Cash<=0 or Deposit<=0:
                print('\nYour input should be positive integers.')
                try:
                    Cash=int(input('\nWhat is the number of cash you expect?\n'))
                    Deposit=int(input('\nWhat is the number of deposit you expect?\n'))
                except ValueError:
                    Cash=-1
                    print('Your input should be positive integers.')
                    continue
            break
        else:
            print('\nYour input is not valid.')
    print('\nSuggestive values of coupons are: 40,80 or 120\n')
    print('(1) 40 Coupons per player')
    print('(2) 80 Coupons per player')
    print('(3) 120 Coupons per player')
    print('(4) Let me determine it!')
    while True:
        print('\nHow many initial coupons do you want? (Enter the above number please.)')
        try:
            try:
                choi1=int(input('Please enter your choice: '))
            except ValueError:
                print('Your input is not valid.')
                continue
            if choi1 ==1 or choi1==2 or choi1==3:
                Coupon=choi1*40
                break
            elif choi1==4:
                Coupon=-1
                while Coupon<0:
                    try:
                        print('\nYour input should be a positive integer.')
                        Coupon=int(input('\nEnter your expected number of coupons please: '))
                    except ValueError:
                        print('Your input should be a positive integer.')
                break
            else:
                print('\nYour input is not valid.')
        except ValueError:
            print('\nYour input is not valid.')
    return Coupon,Cash,Deposit

# Set initial parameters of the game

def printinventory(prop,card,i):
    print('\n{0:<30}'.format('Cards'),'{0:<30}'.format('Props'))
    if len(prop[i])>len(card[i]):
        a=0
        for j in card[i]:
            k=prop[i][a]
            a+=1
            print('{0:<28}'.format(j),'{0:<30}'.format(k))
        for k in prop[i][a:]:
            print('{0:<30}'.format(''),'{0:<30}'.format(k))
    if len(prop[i])<=len(card[i]):
        b=0
        for k in prop[i]:
            j=card[i][b]
            b+=1
            print('{0:<28}'.format(j),'{0:<30}'.format(k))
        for j in card[i][b:]:
            print('{0:<30}'.format(j),'{0:<30}'.format(''))

#used to print the Props and Cards of a player

def printpropscards(prop,card,namelist,pn):
    for i in range(pn):
        print('\nPlayer',namelist[i])
        printinventory(prop,card,i)
             
def YourInfo(num,namelist,Cash,Deposit,Coupon,hpro,prop,card,pn):     #Line 396
    print('\nPlayer ',namelist[num],', your infomation are as follows: ',sep='')
    print('  Name       Cash       Deposit      Coupon      Ground')
    print('{0:^8}'.format(namelist[num]),'{0:^14}'.format(Cash[num]),'{0:^11}'.format(Deposit[num]),'{0:^14}'.format(Coupon[num]),'{0:^10}'.format(len(hpro[num])),sep='')
    print('\nYour Props and Cards are as follows: ')
    printinventory(prop,card,num)
    return None

# At the beginning of a player's round,
# he or she can see his or her own infomation including Props, Cards, Cash etc.
    
def PlayerInfo(pn,namelist,Cash,Deposit,Coupon,hpro,Hospital,prop,card):   #Line 402
    printpropscards(prop,card,namelist,pn)
    print("\nAll players' property infomation are as follows:")
    print('  Name       Cash       Deposit      Total      Coupon      Ground     ')
    for i in range(pn):
        print('{0:^8}'.format(namelist[i]),'{0:^14}'.format(Cash[i]),'{0:^11}'.format(Deposit[i]),'{0:^13}'.format(Cash[i]+Deposit[i]),'{0:^10}'.format(Coupon[i]),'{0:^14}'.format(len(hpro[i])),sep='')

# The first choice    
    
def Operation(namelist,num,direction):       #Line 408
    if direction[num]==0:
        print('\nplayer ',namelist[num],', Your moving direction is clockwise',sep='')
    else:
        print('\nplayer ',namelist[num],', Your moving direction is anti-clockwise',sep='')
    print('\nYou can do things as follows: \n',sep='')
    print('(1) View player infomations.')
    print('(2) Use cards or props.')
    print('(3) Save or load the game.')
    print('(4) Throw the dice!')
    print('(5) Good Game, I quit!\n')
    while True:
        try:
            cho=int(input('What do you want to do? \n'))
            return cho
        except ValueError:
            print('\nError! Please enter again.')
            continue
            print('\nError! Please enter again.')
    return cho

# Get player's choice for preparation period

def getshapecolor(pn,i,point,name,color0,color,shapecho,Load):        #Line 430
    if not Load:
        print('\nWe have 4 kinds of different shapes you can choose:\n')
        print('(1) Square\n(2) Triangle\n(3) Circle\n(4) Cross')
        print('\nPlayer',name,',',' please choose one shape representing you:',sep='')
        shapecho=input()
        co=[]  #collect the color infomations
        while shapecho!='1' and shapecho!='2'and shapecho!='3'and shapecho!='4':
            print('\nError! Please enter again!\n')
            print(name,',',' please choose one shape representing you:',sep='')
            shapecho=input()
        print('\nPlayer',name,',','please choose a color representing you.')
        for i in range(len(color0)):
            print('(',i+1,') ',color0[i],sep='')
        while True:
            try:
                print('\n',name,',',' Which color do you want?',sep='')
                j=int(input())
                if j>len(color0):
                    print('\nError! Please enter again!\n')
                    continue
                break
            except ValueError:
                print('\nError! Please enter again!\n')
    x=point.getX()
    y=point.getY()
    shapedict={'1':Rectan(x,y,22,22),'2':Trian(x,y,15),'3':Circle(Point(x,y),13),'4':Cross(x,y,10)}
    shape=shapedict[shapecho]
    if Load:
        shape.setFill(color[i])
        co=color[i]
    else:
        shape.setFill(color0[j-1])
        co=color0[j-1]
    
    return shape,co,shapecho

# Get initial settings of color and shape for the users

def personon(pnum,position):     #Line 480
    if position in pnum:
        return True
    else:
        return False

# A function detecting whether there is a person on a certain block

def mfptp(o,p1,p2,TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,timer,StrClean,Dream):  #move from a point to a point  #Line 486
    x1=p1.getX()
    y1=p1.getY()
    x2=p2.getX()
    y2=p2.getY()
    for i in range(20):
        o.move((x2-x1)/20,(y2-y1)/20)
        time.sleep(0.012)
    pnum[num]=pSet.index(p2)
    if TBstate[num]:
        if (p2!=pSet[74] and p2!=pSet[75]): #pSet[74,75]: Sickroom and Prison
            TBnum[num]-=1
            TBinfo[num].setText('%02d'%TBnum[num])
        if TBnum[num]==0:
            TBinfo[num].setFill('black')
            print('The Time Bomb exploded. You were sent to hospital by ambulence.')
            non=input('Press enter key to continue.')
            TBstate[num]=False
            pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(o,p2,pSet[74],TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,timer,StrClean,Dream)
            Hospital[num]+=4
        elif personon(pnum,pSet.index(p1)):
            num1=pnum.index(pSet.index(p1))
            if not TBstate[num1]:
                TBnum[num1]=TBnum[num]+1
                TBinfo[num1].setText('%02d'%TBnum[num1])
                TBinfo[num1].setFill('red')
                TBstate[num1]=True
                TBnum[num]=0
                TBinfo[num].setText('%02d'%TBnum[num])
                TBinfo[num].setFill('black')
                TBstate[num]=False     ###### TB exchange #####
    if not StrClean and not Dream[num]:
        if pnum[num]==67 or pnum[num]==38:
            if str(timer.theweekday())=='Sun':
                print("Sorry, today is Sunday, the Bank doesn't work.")
                non=input('\nPress enter key to continue.')
            else:
                print('Welcome to Bank.')
                while True:
                    money=-1
                    print('Your account infomation is as follows:')
                    print('{0:^14}'.format('Cash'),'{0:^14}'.format('Deposit'),sep='')
                    print('{0:^14}'.format(Cash[num]),'{0:^14}'.format(Deposit[num]),sep='')
                    print('You can save or withdraw money from your account')
                    mcho=getchoice('Go out','Save Money','Withdraw Money')
                    if mcho=='0':
                        break
                    elif mcho=='1':
                        while money<0:
                            money=getint('How much money do you want to save?','Please enter the number of money.\n')
                            if money<0:
                                print('\nNegative amount of money is illegal.\n')
                        if money>Cash[num]:
                            print("Sorry, you don't have so much money.")
                            time.sleep(1)
                        else:
                            Cash[num]-=money
                            Deposit[num]+=money
                            print('You saved $%d into your account at the bank.'%(money))
                            time.sleep(1)
                        continue
                    elif mcho=='2':
                        while money<0:
                            money=getint('How much money do you want to withdraw?','Please enter the number of money.\n')
                            if money<0:
                                print('\nNegative amount of money is illegal.\n')
                        if money>Deposit[num]:
                            print("Sorry, you don't have so much money.")
                            time.sleep(1)
                        else:
                            Cash[num]+=money
                            Deposit[num]-=money
                            print('You withdrawed $%d from your account at the bank.'%(money))
                            time.sleep(1)
                        continue
    return pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit

# Enable the chess piece to move from a point to another smoothly and slowly
        

def msbs(o,pSet,step,start,direction,num,passway,BBon,BBobj,TBstate,TBinfo,TBnum,pnum,Hospital,Cash,Deposit,timer,StrClean,Dream):    #move step by step   #Line 504
    if direction[num]==0:
        for i in range(step):
            pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(o,pSet[(pSet.index(start)+i)%74],pSet[(pSet.index(start)+i+1)%74],TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,timer,StrClean,Dream)
            passway.append((pSet.index(start)+i+1)%74)       #From Line 486
            if Hospital[num]!=0:
                break
            if BBon[pnum[num]]:  ##BB detection                                                                                           
                for i in BBobj[pnum[num]]:                             
                    i.undraw()                                            
                BBon[pnum[num]]=False                                         
                break                                              
         ###output pnum                      
    if direction[num]==1:                              
        for i in range(step):         
            pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(o,pSet[(pSet.index(start)-i)%74],pSet[(pSet.index(start)-i-1)%74],TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,timer,StrClean,Dream)
            passway.append((pSet.index(start)-i-1)%74)      #From Line 486
            if Hospital[num]!=0:
                break
            if BBon[pnum[num]]:  ##BB detection
                for i in BBobj[pnum[num]]:
                    i.undraw()
                BBon[pnum[num]]=False
                break
    return passway,pnum,BBon,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit

    
def detectstreet(pnum,num):     #Line 529
    a=[1,2,3,4,5]
    b=[13,14,16,18,19]
    c=[28,29,30,31,32]
    d=[36,37,38,39,40]
    e=[44,45,46,47,48]
    f=[54,55,56,58,59]
    g=[64,65,66]
    h=[68,69,70]
    S=[a,b,c,d,e,f,g,h]
    for i in S:
        if pnum[num] in i:
            return S.index(i)

# Detect the street number for a certain place

def couponbonus(num,pnum,Coupon):   #Line 543
    ten=[7,9,23,41,50]
    twenty=[12,20,26,42,51,62]
    thirty=[60,72]
    fifty=[8,22,25,52]
    i=pnum
    if i in ten:
        Coupon[num]+=10
        print('\n10 Coupons. Have fun!\n')
        n=input('Press enter to continue.')
    elif i in twenty:
        Coupon[num]+=20
        print('\n20 Coupons. Good luck!\n')
        n=input('Press enter to continue.')
    elif i in thirty:
        Coupon[num]+=30
        print('\n30 Coupons! You are lucky!\n')
        n=input('Press enter to continue.')
    elif i in fifty:
        Coupon[num]+=50
        print('\nCongratulations! You get 50 Coupons!!\n')
        n=input('Press enter to continue.')
    return Coupon

def propcardchoice():    #Line 567
    print('What kind of inventory do you want to use?\nProps or Cards?\n(1)Props\n(2)Cards')
    cho=0
    cho=input('enter your choice: (Enter 0 to turn back)\n')
    while cho!='1' and cho!='2' and cho!='0':
        print('\nError! Please enter again.')
        cho=input('enter your choice:\n')
    return cho

#Get the player's choice for Cards or Props

def ChooseProp(prop,num,PC):       #Line 576
    if PC=='1':
        name='props'
    elif PC=='2':
        name='cards'
    print('Here are the ',name,': (Enter 0 to turn back.)',sep='')
    while True:
        try:
            for i in range(len(prop[num])):
                print('(',i+1,')',prop[num][i],sep='')
            print('Which one would you like to choose?')
            cho=int(input())
            while cho not in range(len(prop[num])+1):
                print('\nError! Please enter again.')
                cho=int(input())
            return cho
        except ValueError:
            print('\nError! Please enter again.')

# Choose a Prop OR Card

def propUse(prop,procho,num,Wdice,BB,LM,TB,MW,StrClean,cho):     # make a function from the choice of the user to the prop #Line 591
    if prop[num][procho-1]=='遙控骰子(Wishful Dice)':           
        Wdice=True
    elif prop[num][procho-1]=='路障(Barrier Block)':          
        BB=True
    elif prop[num][procho-1]=='地雷(LandMine)':
        LM=True
    elif prop[num][procho-1]=='定時炸彈(TimeBomb)':
        TB=True
    elif prop[num][procho-1]=='機器工人(Mechanic Workers)':
        MW=True
    elif prop[num][procho-1]=='機器娃娃(Street Cleaner)':
        StrClean=True
    return Wdice,BB,LM,TB,MW,StrClean   ###

def cardUse(card,carcho,num,FC,VC,FreeC,StopC,AngleC,DevilC,DemoC,TurtleC,PurC,MonsterC,RobC,HiberC,ExonerC,ShiftC,ARC,APC,TaxC,RevengeC,DreamC):
    if card[num][carcho-1]=='陷害卡(Framing Card)':
        FC=True
    elif card[num][carcho-1]=='轉向卡(Veer Card)':
        VC=True
    elif card[num][carcho-1]=='免費卡(Free Card)':
        FreeC=True
    elif card[num][carcho-1]=='停留卡(Stop Card)':
        StopC=True
    elif card[num][carcho-1]=='天使卡(Angle Card)':
        AngleC=True
    elif card[num][carcho-1]=='惡魔卡(Devil Card)':
        DevilC=True
    elif card[num][carcho-1]=='拆除卡(Demolition Card)':
        DemoC=True
    elif card[num][carcho-1]=='烏龜卡(Turtle Card)':
        TurtleC=True
    elif card[num][carcho-1]=='購地卡(Purchase Card)' :
        PurC=True
    elif card[num][carcho-1]=='怪獸卡(Monster Card)':
        MonsterC=True
    elif card[num][carcho-1]=='搶奪卡(Rob Card)':
        RobC=True
    elif card[num][carcho-1]=='冬眠卡(Hibernation Card)':
        HiberC=True
    elif card[num][carcho-1]=='免罪卡(Exoneration Card)':
        ExonerC=True
    elif card[num][carcho-1]=='嫁禍卡(CalamityShift Card)':
        ShiftC=True
    elif card[num][carcho-1]=='均富卡(AverageRich Card)':
        ARC=True
    elif card[num][carcho-1]=='均貧卡(AveragePoor Card)':
        APC=True
    elif card[num][carcho-1]=='查稅卡(Tax Card)':
        TaxC=True
    elif card[num][carcho-1]=='復仇卡(Revenge Card)':
        RevengeC=True
    elif card[num][carcho-1]=='夢遊卡(DreamWalk Card)':
        DreamC=True
    return FC,VC,FreeC,StopC,AngleC,DevilC,DemoC,TurtleC,PurC,MonsterC,RobC,HiberC,ExonerC,ShiftC,ARC,APC,TaxC,RevengeC,DreamC

def CanUseCard(pnum,num,num1,namelist,f):
    if abs(pnum[num1]-pnum[num]) in [0,1,2,3,4,5,69,70,71,72,73]:
        if f:
            print('The player',namelist[num1],'{}'.format(f))
        non=input('\nPress enter key to continue.')
        return True
    else:
        return False

# Return whether the player can use a certain Card OR Prop

def ChoosePerson(direction,namelist1,pnum,num,pn,cardname):  #The namelist here may be newnamelist, according to what card you use
    if cardname!='CalamityShift Card':
        if direction[num]==0:
            print('\nYour moving direction is clockwise.')
        else:
            print('\nYour moving direction is anti-clockwise.')
        
        print('\nYou can use your',cardname,'at the person\nwho is at most 5 steps away from you')
        print('\nPlease enter the number of that player:')
    else:
        print('Please enter the number of the player who you want to shift your calamity to.')
    a=0
    for i in range(0,len(namelist1),2):
        a+=1
        print('(',a,') ',namelist1[2*a-1],sep='')
    print('Which one would you like to use your card to? (enter 0 to turn back)')
    percho=''
    while percho not in range(int(len(namelist1)/2)+1):     
        try:
            percho=int(input('Please choose the Player to use your %s.\n'%cardname))
        except ValueError:
            print('\nError. Please enter your choice again')
            continue
        if pnum[namelist1[2*percho-2]] not in range(0,74):
            print('\nThat person has already been in the prison or the hospital.')
            print("You can't shift your calamity to him or her.")
            percho=-1 #continue
            non=input('\nPress enter key to continue.')
            continue
    return percho

# Choose the person to use card        

def putprop(direction,num,pSet,pnum,win,Aon,Aobj,Bon,Con,propname):     #Line 604
    if direction[num]==0:
        print('\nYour moving direction is clockwise.')
    else:
        print('\nYour moving direction is anti-clockwise.')
    print('\nYou can put your',propname,'at the position which is at most 5 steps away from you')
    while True:
        print('\nWhich direction will you choose to put down your ',propname,'?',sep='')
        print('(1) Forward\n(2) Backward')
        dcho=input() 
        while dcho!='1' and dcho!='2' and dcho!='0':
            print('\nError! Please enter again.')
            print('\nWhich direction will you choose to put down your ',propname,'?',sep='')
            print('(1) Forward\n(2) Backward')
            dcho=input()
        if dcho!='0':
            print('How many steps forward/backward from you?(enter number 1-5, enter 0 to turn back)')
            scho=input()
            while scho not in ['0','1','2','3','4','5']:
                print('\nError! Please enter again.')
                print('How many steps forward/backward from you?(enter number 1-5, enter 0 to turn back)')
                scho=input()
            if scho=='0':
                continue
        break
    #### Consider the different definitions of 'Forward' and 'Backward' ####
    if (direction[num]==0 and dcho=='2') or (direction[num]==1 and dcho=='1'):
        pnum2=(pnum[num]-int(scho))%74
        if not (Aon[pnum2] or Bon[pnum2] or Con[pnum2] or (pnum2 in pnum)):
            p=pSet[pnum2]
            for i in Aobj[pnum2]:
                i.draw(win)
            Aon[pnum2]=True
            x=p.getX()
            y=p.getY()
        else:
            print("\nThere has already been an object there,\nyou can't put your %s there."%propname)
            dcho='0'
            non=input('\nPress enter key to continue.')
    elif (direction[num]==1 and dcho=='2') or (direction[num]==0 and dcho=='1'):
        pnum2=(pnum[num]+int(scho))%74
        if not (Aon[pnum2] or Bon[pnum2] or Con[pnum2] or (pnum2 in pnum)):
            p=pSet[pnum2]
            for i in Aobj[pnum2]:
                i.draw(win)
            Aon[pnum2]=True
            x=p.getX()
            y=p.getY()
        else:
            print("\nThere has already been an object there,\nyou can't put your %s there."%propname)
            dcho='0'
            non=input('\nPress enter key to continue.')
    return Aon,dcho

# Put a prop on a certain place

def useMW(direction,num,pSet,pnum,win,MW,houselevel,hpro,Levelobj,f):
    #Both machinic worker and democ
    if direction[num]==0:
        print('\nYour moving direction is clockwise.')
    else:
        print('\nYour moving direction is anti-clockwise.')
    print('\nYou can choose a house(ground) which is at most 5 steps away from you to',f)
    while True:
        print('\nWhich direction will you choose to use your prop or card?')
        print('(1) Forward\n(2) Backward\n(3) Just the ground where I am standing.')
        dcho=input()
        scho='' # in case of error
        while dcho!='1' and dcho!='2' and dcho!='3' and dcho!='0':
            print('\nError! Please enter again.')
            print('\nWhich direction will you choose to use your prop or card?')
            print('(1) Forward\n(2) Backward\n(3) Just the ground where I am standing.')
            dcho=input()
        if dcho!='0' and dcho!='3':
            print('How many steps forward/backward from you?(enter number 1-5, enter 0 to turn back)')
            scho=input()
            while scho not in ['0','1','2','3','4','5']:
                print('\nError! Please enter again.')
                print('How many steps forward/backward from you?(enter number 1-5, enter 0 to turn back)')
                scho=input()
        if scho=='0':
            continue
        if dcho=='3':   # A little bit tricky
            scho='0'   
        break
    whetherin=False
    #### Consider the different definitions of 'Forward' and 'Backward' ####
    if (direction[num]==0 and dcho=='2') or (direction[num]==1 and dcho=='1'):
        pnum1=(pnum[num]-int(scho))%74
    elif (direction[num]==1 and dcho=='2') or (direction[num]==0 and dcho=='1'):
        pnum1=(pnum[num]+int(scho))%74
    elif dcho=='3':
        pnum1=pnum[num]
    if dcho!='0':
        if f=='upgrade.':
            for i in hpro:
                if pnum1 in i:
                    if houselevel[pnum1]<=5:
                        x=pSet[pnum1].getX()
                        y=pSet[pnum1].getY()
                        Levelobj[pnum1][houselevel[pnum1]].draw(win)
                        houselevel[pnum1]+=1
                        print('Congratulations! Building upgraded successfully!')
                        non=input('Press enter key to continue.')
                        whetherin=True
                    else:
                        print("\nSorry, this house has been at the highest level.You can't upgrade it.\n")
                        MW=False       
            if not whetherin:
                print('\nThis ground can not be upgraded.')
                non=input('\nPress enter key to continue.')
                MW=False
        elif f=='destory.':
            for i in hpro:
                if pnum1 in i:
                    if houselevel[pnum1]>0:
                        x=pSet[pnum1].getX()
                        y=pSet[pnum1].getY()
                        houselevel[pnum1]-=1
                        Levelobj[pnum1][houselevel[pnum1]].undraw()
                        print('This ground has been destoryed.')
                        non=input('Press enter key to continue.')
                        whetherin=True
                    else:
                        print("\nSorry, this ground has no houses.")
                        MW=False
            if not whetherin:
                print('\nThis ground can not be destoryed.')
                non=input('\nPress enter key to continue.')
                MW=False
        elif f=='send your Monster to.':
            for i in hpro:
                if pnum1 in i:
                    if houselevel[pnum1]>0:
                        x=pSet[pnum1].getX()
                        y=pSet[pnum1].getY()
                        for i in Levelobj[pnum1]:
                            i.undraw()
                        houselevel[pnum1]=0
                        print('This ground has been destoryed.')
                        non=input('Press enter key to continue.')
                        whetherin=True
            if not whetherin:
                print('\nThis ground can not be destoryed.')
                non=input('\nPress enter key to continue.')
                MW=False
    return MW,houselevel,dcho

                    ############### step on the bomb ###############        
def steponbomb(LMon,pnum,num,LMobj,pSet,shapes,Hospital,TBstate,TBinfo,TBnum,Cash,Deposit,timer,StrClean,Dream):          #Line 658
    if LMon[pnum[num]]:
        print('\nAaAaaaaAaaaahhhhhhhhhhh!!\nOhhhOOOhhhhhhhhhhh!!!')
        time.sleep(0.5)
        LMon[pnum[num]]=False
        print('\nYou were carried to Shatin Hospital by ambulence')
        non=input('Press enter key to continue')
        for i in LMobj[pnum[num]]:
            i.undraw()
        if TBstate[num]:
            Hospital[num]+=3
            TBstate[num]=False
            TBnum[num]=0
            TBinfo[num].setFill('black')
            TBinfo[num].setText('%02d'%TBnum[num])
        pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(shapes[num],pSet[pnum[num]],pSet[74],TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,timer,StrClean,Dream)             ###From Line 486
        Hospital[num]+=4
    return LMon,pnum,Hospital,TBinfo,TBnum,TBstate

def buyhouse(place,pnum,num,Eng,houseprice,bSet,color,Cash,Vacancy,hpro,houselevel,priceindex):     #Line 677
    if Cash[num]>=houseprice[pnum[num]]*(houselevel[pnum[num]]+1)*priceindex:
        for i in place:
            if pnum[num] in i:   #買地手續
                print('\nA Vacancy in,',Eng[place.index(i)],'the price is',round(houseprice[pnum[num]]*(houselevel[pnum[num]]+1)*priceindex),'would you like to purchase it? (Y/N)')
                try:
                    decision=input()
                    if decision[0]!='N' or 'n':
                        if Cash[num]>=houseprice[pnum[num]]*(houselevel[pnum[num]]+1)*priceindex:
                            bSet[pnum[num]].setFill(color[num])
                            Cash[num]=Cash[num]-round(houseprice[pnum[num]]*(houselevel[pnum[num]]+1)*priceindex)
                            Vacancy[pnum[num]]=False
                            hpro[num].append(pnum[num])
                            print('Congratulations! You bought this estate successfully!')
                        else:
                            print('Your Cash is not enough.')
                            non=input('Press enter key to continue.')
                except IndexError:
                    bSet[pnum[num]].setFill(color[num])
                    Cash[num]=Cash[num]-round(houseprice[pnum[num]]*(houselevel[pnum[num]]+1)*priceindex)  #Just need to press 'enter' to buy the ground
                    Vacancy[pnum[num]]=False
                    hpro[num].append(pnum[num])
                    print('Congratulations! You bought this estate successfully!')
    else:
        print('\nSorry, your money is not enough.')
        non=input('\nPress enter key to continue.')
    return Cash,Vacancy,hpro,bSet

def upgradehouse(houselevel,pnum,num,pSet,Cash,houseprice,win,Levelobj):    #Line 697
    if Cash[num]>=houseprice[pnum[num]]:   
        if houselevel[pnum[num]]<=5:    # the maximum level is 6
            print('\nWould you like to upgrade your ground? (Y/N)\n')
            try:
                decision=input()
                if decision[0]!='N' or 'n':
                    x=pSet[pnum[num]].getX()
                    y=pSet[pnum[num]].getY()
                    Levelobj[pnum[num]][houselevel[pnum[num]]].draw(win)
                    Cash[num]-=houseprice[pnum[num]]
                    houselevel[pnum[num]]+=1
                    print('Congratulations! Building upgraded successfully!')
            except IndexError:                     # The player just need to press 'enter'
                x=pSet[pnum[num]].getX()
                y=pSet[pnum[num]].getY()
                Levelobj[pnum[num]][houselevel[pnum[num]]].draw(win)
                Cash[num]-=houseprice[pnum[num]]
                houselevel[pnum[num]]+=1
                print('Congratulations! Building upgraded successfully!')
        else:
            print("\nSorry, your house has been at the highest level.You can't upgrade it.\n")
            non=input('Press enter key to continue.\n')
    else:
        print('\nSorry, Your money is not enough.')
        non=input('\nPress enter key to continue.')
    return houselevel,Cash

def tollgiving(hpro,pnum,num,Hospital,houseprice,houselevel,Cash,Deposit,namelist,place,Prison,Hiberstate,card,Dream,priceindex):    #Line 724
    for i in hpro:
        if pnum[num] in i:
            num1=hpro.index(i)  #get the number of the player
    if Hospital[num1]==0 and Prison[num1]==0 and num!=num1 and Dream[num1]==0 and Hiberstate[num1]==0:
        price=round(houseprice[pnum[num]]*(houselevel[pnum[num]]+1)*priceindex)
        addition=0
        print('\nThis ground is owned by ',namelist[num1],'.',sep='')
        street=detectstreet(pnum,num)     #From Line 529
        for i in hpro[num1]:
            if i in place[street]:
                if i != pnum[num]:
                    price1=round(houseprice[i]*(houselevel[i]+1)*priceindex)
                    addition+=price1*0.1
        toll=int(price*0.3+addition)
        if toll>2000:
            if '免費卡(Free Card)' in card[num]:
                Freecho=input('\nWould you like to use your Free Card?(Y/N)')
                if Freecho=='N' or Freecho=='n':
                    print('You have to give him/her $',toll,' as toll.\n',sep='')
                    non=input('Press enter key to continue.')
                    if Cash[num]>=toll:
                        Cash[num]-=toll
                    elif Cash[num]<toll:
                        toll1=toll-Cash[num]
                        Deposit[num]-=toll1
                        Cash[num]=0
                    Deposit[num1]+=toll
                else:
                    print('You have used the Free Card. You need not pay the toll now.')
                    non=input('Press enter key to continue.')
                    del card[num][card[num].index('免費卡(Free Card)')]
            else:
                if Cash[num]>=toll:
                    Cash[num]-=toll
                elif Cash[num]<toll:
                    toll1=toll-Cash[num]
                    Cash[num]=0
                    Deposit[num]-=toll1
                Deposit[num1]+=toll
                print('You have to give him/her $',toll,' as toll.\n',sep='')
                non=input('Press enter to continue.')
        else:       
            if Cash[num]>=toll:
                Cash[num]-=toll
            elif Cash[num]<toll:
                toll1=toll-Cash[num]
                Deposit[num]-=toll1
                Cash[num]=0
            Deposit[num1]+=toll
            print('You have to give him/her $',toll,' as toll.\n',sep='')
            non=input('Press enter to continue.')
    elif num!=num1:
        if Hospital[num1]>0:
            print('Player',namelist[num1],"is in the hospital.\nYou needn't pay the toll.")
            non=input('\nPress enter key to continue.')
        elif Prison[num1]>0:
            print('Player',namelist[num1],"is in the prison.\nYou needn't pay the toll.")
            non=input('\nPress enter key to continue.')
        elif Hiberstate[num1]>0:
            print('Player',namelist[num1],"is still sleeping now.\nYou needn't pay the toll.")
            non=input('\nPress enter key to continue.')
        elif Dream[num1]:
            print('Player',namelist[num1],"is DreamWalking.\nYou needn't pay the toll.")
            non=input('\nPress enter key to continue.')
    return Cash,Deposit,card

# Toll System

def detecthpro(pnum,num,hpro):
    num1=0
    for i in hpro:
        for j in i:
            if pnum[num]==j:
                return num1
        num1+=1

def UseExonerCard(card,num1,namelist):
    ExonerC=False
    if '免罪卡(Exoneration Card)' in card[num1]:
        print('\nPlayer ',namelist[num1],', you have Exoneration Card.',sep='')
        print('Would you like to use it?(Y/N)')
        ifexon=input()
        if ifexon!='N' and ifexon!='n':
            del card[num1][card[num1].index('免罪卡(Exoneration Card)')]
            ExonerC=True
    return ExonerC

def UseShiftCard(namelist,num1,card,pn,pnum,direction):
    shiftcho=False
    if '嫁禍卡(CalamityShift Card)' in card[num1]:   #if no CSC, jump out
        print('\nPlayer',namelist[num1],', you have CalamityShift Card.')
        print('Would you like to use it?(Y/N)')
        ifshift=input()
        if ifshift!='N' and ifshift!='n':
            shiftcho=True
            #re-build newnamelist
            newnamelist2=[]
            for i in range(pn):
                if i!=num1:
                    newnamelist2.append(i)
                    newnamelist2.append(namelist[i])
            percho=ChoosePerson(direction,newnamelist2,pnum,num1,pn,cardname='CalamityShift Card')
            percho-=1
            if percho==-1:
                print('\nPlayer',namelist[num1],'refuses to use the CalamityShift Card.')
                non=input('\nPress enter key to continue.')
            else:
                del card[num1][card[num1].index('嫁禍卡(CalamityShift Card)')]
                num1=newnamelist2[2*percho]
    return num1,shiftcho

def machinelist(rawlist,inted):
    try:
        finallist=[]
        rawlist1=rawlist.strip('\n')
        print(rawlist1)
        rawlist2=rawlist1.strip('[').strip(']')
        print(rawlist2)
        rawlist3=rawlist2.split(', ')
        print(rawlist3)
        for i in rawlist3:
            i=i.strip('\'')
            if inted:
                i=int(i)
            finallist.append(i)
    except ValueError:
        finallist=[]
    print(finallist)
    return finallist

def Boolmachine(rawlist):
    finallist=[]
    rawlist1=machinelist(rawlist,False)
    for i in rawlist1:
        if i=='True':
            finallist.append(True)
        elif i=='False':
            finallist.append(False)
        else:
            raise ValueError
    return finallist

def ifondraw(Xon,Xobj,win):
    for i in range(len(Xon)):
        if Xon[i]:
            for j in Xobj[i]:
                j.draw(win)

def load(afile,Levelobj,pSet,bSet,win,LMobj,TBobj,BBobj,shapes,color,shapecholist,Namebook,hpro,prop,card,TBinfo,Load,lotteries):
    Vacancy=[True]*76
    Quitnum1=afile.readline()
    Quitnum=int(Quitnum1)
    pn1=afile.readline()   ##'1':raw infomation
    pn=int(pn1)   #get pn!
    num1=afile.readline()
    loadnum=int(num1)  #get num! to specify it, loadnum
    shapecholist1=afile.readline()
    shapecholist=machinelist(shapecholist1,False) #get shapecholist!
    color1=afile.readline()
    color=machinelist(color1,False)  #get color!
    pnum1=afile.readline() #get pnum!
    pnum=machinelist(pnum1,True)
    namelist1=afile.readline()
    namelist=machinelist(namelist1,False)
    direction1=afile.readline()
    direction=machinelist(direction1,True)
    Cash1=afile.readline()
    Cash=machinelist(Cash1,True)
    Deposit1=afile.readline()
    Deposit=machinelist(Deposit1,True)
    Coupon1=afile.readline()
    Coupon=machinelist(Coupon1,True)
    Hospital1=afile.readline()
    Hospital=machinelist(Hospital1,True)
    Prison1=afile.readline()
    Prison=machinelist(Prison1,True)
    TBnum1=afile.readline()
    TBnum=machinelist(TBnum1,True)
    houselevel1=afile.readline()
    houselevel=machinelist(houselevel1,True)
    for i in range(len(houselevel)):
        if houselevel[i]!=0:
            for j in range(houselevel[i]):
                Levelobj[i][j].draw(win)
    BBon1=afile.readline()
    BBon=Boolmachine(BBon1)
    ifondraw(BBon,BBobj,win)
    LMon1=afile.readline()
    LMon=Boolmachine(LMon1)
    ifondraw(LMon,LMobj,win)
    TBon1=afile.readline()
    TBon=Boolmachine(TBon1)
    ifondraw(TBon,TBobj,win)
    TBstate1=afile.readline()
    TBstate=Boolmachine(TBstate1)
    Stopstate1=afile.readline()
    Stopstate=Boolmachine(Stopstate1)
    Turtlenum1=afile.readline()
    Turtlenum=machinelist(Turtlenum1,True)
    Hiberstate1=afile.readline()
    Hiberstate=machinelist(Hiberstate1,True)
    Dream1=afile.readline()
    Dream=machinelist(Dream1,True)
    Wdiceused1=afile.readline()
    Wdiceused2=Wdiceused1.strip('\n')
    if Wdiceused2=='True':
        Wdiceused=True
    elif Wdiceused2=='False':
        Wdiceused=False
    else:
        raise ValueError
    Wstep1=afile.readline()
    Wstep=int(Wstep1)
    thedate1=afile.readline()
    thedate=thedate1.strip('\n')
    loccupy1=afile.readline()
    loccupy=Boolmachine(loccupy1)
    bonus1=afile.readline()
    bonus=int(bonus1)
    priceindex1=afile.readline()
    priceindex=float(priceindex1)
    priceindex=round(priceindex,2)
    for i in range(pn):
        text=Text(Point(100+i*100,650),'%02d'%TBnum[i])
        if TBnum[i]:
            text.setFill('red')
        TBinfo.append(text)#
    for i in TBinfo:
        i.draw(win)
    for i in range(pn):
        lhpro1=afile.readline()
        lhpro=machinelist(lhpro1,True)
        hpro.append(lhpro)#
    for i in range(len(hpro)):
        for j in hpro[i]:
            bSet[j].setFill(color[i])
    for i in hpro:
        for j in i:
            Vacancy[j]=False
    for i in range(pn):
        lprop1=afile.readline()
        lprop=machinelist(lprop1,False)
        prop.append(lprop)
    for i in range(pn):
        lcard1=afile.readline()
        lcard=machinelist(lcard1,False)
        card.append(lcard)
    for i in range(pn):
        llotteries1=afile.readline()
        llotteries=machinelist(llotteries1,True)
        lotteries.append(llotteries)
    for i in range(pn):
        text=Text(Point(100+i*100,680),namelist[i])
        text.setFill(color[i])
        Namebook.append(text)
        text.draw(win)
    for i in range(pn):
        shape,co,shapecho=getshapecolor(pn,i,pSet[pnum[i]],'',[],color,shapecholist[i],Load)
        shapes.append(shape)
    for j in shapes:
        j.draw(win)
    
    return Vacancy,Quitnum,pn,loadnum,shapecholist,\
        color,pnum,namelist,direction,Cash,Deposit,Coupon,\
        Hospital,Prison,TBnum,houselevel,BBon,LMon,TBon,TBstate,\
        Stopstate,Turtlenum,Hiberstate,TBinfo,hpro,prop,card,Namebook,\
        shapes,Dream,Wdiceused,Wstep,thedate,lotteries,loccupy,bonus,priceindex
    
################################################################################

class grocery():
    def __init__(self,prop=[],card=[]):
        self.prop=prop
        self.card=card
        self.propdict={'遙控骰子(Wishful Dice)':40,'路障(Barrier Block)':40,'地雷(LandMine)':35,
                         '定時炸彈(TimeBomb)':35,'機器工人(Mechanic Workers)':50,'機器娃娃(Street Cleaner)':30}
        self.spropdict={'遙控骰子(Wishful Dice)':20,'路障(Barrier Block)':20,'地雷(LandMine)':17,
                         '定時炸彈(TimeBomb)':17,'機器工人(Mechanic Workers)':25,'機器娃娃(Street Cleaner)':15}
        self.carddict={'陷害卡(Framing Card)':40,'轉向卡(Veer Card)':40,'免費卡(Free Card)':50,\
                '停留卡(Stop Card)':40,'天使卡(Angle Card)':170,'惡魔卡(Devil Card)':170,\
                '拆除卡(Demolition Card)':40,'烏龜卡(Turtle Card)':100,'購地卡(Purchase Card)':50,\
                '怪獸卡(Monster Card)':100,'搶奪卡(Rob Card)':50,'冬眠卡(Hibernation Card)':150,\
                '免罪卡(Exoneration Card)':40,'嫁禍卡(CalamityShift Card)':50,\
                  '均富卡(AverageRich Card)':250,'均貧卡(AveragePoor Card)':250,\
                  '查稅卡(Tax Card)':35,'復仇卡(Revenge Card)':30,'夢遊卡(DreamWalk Card)':40}
        self.scarddict={'陷害卡(Framing Card)':20,'轉向卡(Veer Card)':20,'免費卡(Free Card)':25,\
                '停留卡(Stop Card)':20,'天使卡(Angle Card)':85,'惡魔卡(Devil Card)':85,\
                '拆除卡(Demolition Card)':20,'烏龜卡(Turtle Card)':50,'購地卡(Purchase Card)':25,\
                '怪獸卡(Monster Card)':50,'搶奪卡(Rob Card)':25,'冬眠卡(Hibernation Card)':75,\
                '免罪卡(Exoneration Card)':20,'嫁禍卡(CalamityShift Card)':25,\
                  '均富卡(AverageRich Card)':125,'均貧卡(AveragePoor Card)':125,\
                  '查稅卡(Tax Card)':17,'復仇卡(Revenge Card)':15,'夢遊卡(DreamWalk Card)':20}
    def getcards(self):  # choose with replacement
        self.card=[]
        cardlist=['陷害卡(Framing Card)','轉向卡(Veer Card)','免費卡(Free Card)',\
                '停留卡(Stop Card)','天使卡(Angle Card)','惡魔卡(Devil Card)',\
                '拆除卡(Demolition Card)','烏龜卡(Turtle Card)','購地卡(Purchase Card)',\
                '怪獸卡(Monster Card)','搶奪卡(Rob Card)','冬眠卡(Hibernation Card)',\
                '免罪卡(Exoneration Card)','嫁禍卡(CalamityShift Card)',\
                  '均富卡(AverageRich Card)','均貧卡(AveragePoor Card)',\
                  '查稅卡(Tax Card)','復仇卡(Revenge Card)','夢遊卡(DreamWalk Card)']
        cardnum=randint(7,9)
        for i in range(cardnum):
            self.card.append(choice(cardlist))
        return self.card
    def getprops(self):
        self.prop=[]
        self.prop=['遙控骰子(Wishful Dice)','路障(Barrier Block)','地雷(LandMine)',\
                    '定時炸彈(TimeBomb)','機器工人(Mechanic Workers)','機器娃娃(Street Cleaner)']
        return self.prop

def getchoice(do0,do1,do2):
    print('%s or %s?'%(do1,do2))
    print('(1) %s\n(2) %s\n(0) %s '%(do1,do2,do0))
    print('Please enter your choice: ')
    docho=input()
    while docho!='0' and docho!='1' and docho!='2':
        print('Error,Please enter your choice again:')
        docho=input()
    return docho

def buysellcard(cardlist,cardcho,card,Coupon,num,carddict,f):
    while cardcho!=0:
        if f=='buy':
            print('The commodity here are as follows:')
        elif f=='sell':
            cardlist=card[num].copy()
            print('Your inventory is as follows:')
        print('(0) Turn back')
        for i in range(len(cardlist)):
            print('{0:<30}'.format('(%d) %s'%(i+1,cardlist[i])),'-%d Coupons'%carddict[cardlist[i]])
        print('\nYou have %d Coupons.'%Coupon[num])
        print('\nWhat do you want to %s?\nPlease enter your choice:'%f)
        cardcho='0'
        while cardcho not in range(len(cardlist)+1):
            if cardcho!='0':
                print('Error,Please enter again.')
            try:
                cardcho=int(input())
            except ValueError:
                print('Error,Please enter again.')
                continue
        if len(card[num])>=12 and cardcho!=0 and f=='buy':
            print('\nSorry. Your inventory is full.')
            print('You only can carry no more than 12 Cards or Props.')
            cardcho=0
            non=input('\nPress enter key to continue.')
        if cardcho!=0:
            cprice=carddict[cardlist[cardcho-1]]
            print('Are you sure to %s %s?(Y/N)'%(f,cardlist[cardcho-1]))
            YN=input()
            if YN!='N' and YN!='n':
                if f=='buy':
                    if Coupon[num]>=cprice:
                        print('You bought one %s from the grocery.'%cardlist[cardcho-1])
                        non=input('Press enter key to continue.')
                        Coupon[num]-=cprice
                        card[num].append(cardlist[cardcho-1])
                        del cardlist[cardcho-1]
                        continue
                    else:       #elif Coupon[num]<cprice:
                        print('Sorry, Your Coupon is not enough.')
                        non=input('Press enter key to continue.')
                        continue
                    '''elif len(card[num]>=10:
                        print('Inventory is Full.')
                        continue'''
                elif f=='sell':
                    print('You sold one %s to the grocery.'%cardlist[cardcho-1])
                    non=input('Press enter key to continue.')
                    Coupon[num]+=cprice
                    del cardlist[cardcho-1]
                    del card[num][cardcho-1]
    return cardcho,cardlist,Coupon,card

class timer():
    
    def __init__(self,StartTime='15-01-14'):
        self.StartTime=StartTime
        self.Date=datetime.strptime(self.StartTime,'%y-%m-%d')
        self.datelist=str(self).split('-')
        
    def __str__(self):
        self.strDate=str(self.Date).strip('00:00:00')
        return self.strDate
    
    def addaday(self):
        self.Date=self.Date+timedelta(days=1)
        self.datelist=str(self).split('-')

    def interest(self):   ###### unfinished ######
        if self.datelist[2]=='01 ':
            return True
        else:
            return False

    def lotterytime(self):
        if self.datelist[2]=='15 ':
            return True
        else:
            return False

    def theweekday(self):  # return the abbriviate of the weekday of a certain day
        daynum=calendar.weekday(int(self.datelist[0]),int(self.datelist[1]),int(self.datelist[2]))
        self.theday=calendar.day_abbr[daynum]
        return self.theday

class lottery():

    def __init__(self,occupy=[False]*36,bonus=4000):
        self.occupy=occupy
        self.bonus=bonus

    def initial(self):
        self.__init__(occupy=[False]*36,bonus=4000)

    def addbonus(self):
        self.bonus+=4000

    def bought(self,num):
        self.occupy[num-1]=True #start from 1

    def debought(self,num):
        self.occupy[num-1]=False
                
def winprint(astr):
    for i in astr:
        print(i,end='')
        time.sleep(0.04)
    print()

def Bankrupt(Vacancy,Quitnum,namelist,Cash,Deposit,Coupon,shapes,\
            pnum,hpro,color,TBinfo,direction,Hospital,Prison,\
            prop,card,TBnum,TBstate,Stopstate,Turtlenum,\
            Namebook,Hiberstate,shapecholist,pn,num,lotteries,Dream,bSet):                  
    Quitnum+=1   # Synchronize turns of Players
    non=input('Press enter key to continue.')
    #del all the infos
    del namelist[num]
    del Cash[num]
    del Deposit[num]
    del Coupon[num]
    shapes[num].undraw()
    del shapes[num]
    del pnum[num]
    for i in hpro[num]:
        Vacancy[i]=True
        bSet[i].setFill('white')
    del hpro[num]
    del color[num]
    TBinfo[num].undraw()
    del TBinfo[num]
    del direction[num]
    del Hospital[num]
    del Prison[num]
    del prop[num]
    del card[num]
    del TBnum[num]
    del TBstate[num]
    del Stopstate[num]
    del Turtlenum[num]
    Namebook[num].undraw()
    del Namebook[num]
    del Hiberstate[num]
    del shapecholist[num]
    del lotteries[num]
    del Dream[num]
    pn-=1
    #delete all the infomation about the player
    return pn,Vacancy,Quitnum

def winner(namelist,pn):
    if pn==1:
        winprint('!@#$%^&*()_+!@#$%^&*()_+!@#$%^&*()_+!@#$%^&*()_+!@#$%^&*()_+')
        winprint('####################### Game Over ##########################')
        winprint('!@#$%^&*()_+!@#$%^&*()_+!@#$%^&*()_+!@#$%^&*()_+!@#$%^&*()_+\n\n')
        winprint('✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿')
        winprint('✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿')
        winprint('The Winner is:                                              ')
        winprint(namelist[0]+'!!!!!! Congratulations!!')
        winprint('✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿')
        winprint('✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿✿')
        return True
    else:
        return False

# Decoration
                
def main():     #Line 748
    Cloud=[]
    print('\nYou can start a new game or load a past game.')
    print('(1) Start a New Game!\n(2) Load game')
    firstcho=input('Please enter your choice.\n')
    while firstcho!='1' and firstcho!='2':
        print('\nError! Please enter again.')
        firstcho=input('\nPlease enter your choice.\n')
    win,bSet,pSet=CreateChessBoard()   #From Line 104 [1]
    Timer=timer()
    Lottery=lottery()
    pHos=Point(875,640)
    pSet.append(pHos)
    pPri=Point(735,270)
    pSet.append(pPri)
    BBobj=[]
    LMobj=[]
    TBobj=[]
    shapes=[]
    Levelobj=[]
    shapecholist=[]
    pnum=[]  
    hpro=[]
    direction=[]
    Cash=[]
    Deposit=[]
    Coupon=[]
    passway=[]
    prop=[]
    card=[]
    TBinfo=[]
    color=[]
    Namebook=[]
    oldnamelist=[]
    lotteries=[]
    lwinner=''
    houseprice=[0,1800,1900,2000,1700,1800,0,0,0,0,0,0,0,2500,2400,0,2700,0,2600,2500,0,0,0,0,0,0,0,0,1500,1700,1600,1700,1500,0,0,0,2000,1900,0,2100,2000,0,0,0,2300,2100,2200,2300,2400,0,0,0,0,0,2300,2100,2200,0,2300,2200,0,0,0,0,4200,3800,4000,0,3300,3300,3500,0,0,0]    
    houseposition=[1,2,3,4,5,13,14,16,18,19,28,29,30,31,32,36,37,39,40,44,45,46,47,48,54,55,56,58,59,64,65,66,68,69,70]
    houselevel=[0]*76
    Vacancy=[True]*76
    BBon=[False]*76
    LMon=[False]*76
    TBon=[False]*76
    Wstep=0
    priceindex=1
    Allprop=['遙控骰子(Wishful Dice)','路障(Barrier Block)','地雷(LandMine)',
            '定時炸彈(TimeBomb)','機器工人(Mechanic Workers)','機器娃娃(Street Cleaner)']
    Allcard=['陷害卡(Framing Card)','轉向卡(Veer Card)','免費卡(Free Card)',
            '停留卡(Stop Card)','天使卡(Angle Card)','惡魔卡(Devil Card)',
            '拆除卡(Demolition Card)','烏龜卡(Turtle Card)','購地卡(Purchase Card)',
            '怪獸卡(Monster Card)','搶奪卡(Rob Card)','冬眠卡(Hibernation Card)',
            '免罪卡(Exoneration Card)','嫁禍卡(CalamityShift Card)','均富卡(AverageRich Card)',
            '均貧卡(AveragePoor Card)','查稅卡(Tax Card)','復仇卡(Revenge Card)','夢遊卡(DreamWalk Card)']
    尖沙咀=[1,2,3,4,5]
    旺角=[13,14,16,18,19]
    荃灣=[28,29,30,31,32]
    沙田=[36,37,38,39,40]
    九龍灣=[44,45,46,47,48]
    紅磡=[54,55,56,58,59]
    銅鑼灣=[64,65,66]
    金鐘=[68,69,70]
    place=[尖沙咀,旺角,荃灣,沙田,九龍灣,紅磡,銅鑼灣,金鐘]
    Eng=['尖沙咀(Tsim Sha Tsui)','旺角(Mong Kok)','荃灣(Tsuen Wan)','沙田(Sha Tin)','九龍灣(Kowloon Bay)','紅磡(Hung Hom)','銅鑼灣(Causeway Bay)','金鐘(Admiralty)']
    Load=False
    lotterywin=False
    for p in pSet:
        R1,R2,R3=DrawBarrier(p,win)    #From Line 54 [4]
        BBobj.append([R1,R2,R3])
        LMobj.append(DrawLandMine(p,win))############### props ############### #From Line 65 [5]
        TBobj.append(DrawTimeBomb(p,win))   #From Line 80 [6]
        Levelobj.append([])
    for i in range(6):
        for p in pSet:
            x=p.getX()
            y=p.getY()
            rect=Rectan(x,y,50-i*10,50-i*10)
            rect.setOutline('grey')
            Levelobj[pSet.index(p)].append(rect)
    Newsdict={1:'公開表揚第一地主%s獎勵$5000',\
              2:'公開補助土地最少者%s $5000',\
              3:'銀行加發儲金紅利所有人得到存款8.0%',\
              4:'豪雨特報行人停走一回',\
              5:'八號風球席捲香港摧毀房屋一棟',\
              6:'所有人交個人所得稅10%'}
    if firstcho=='1':
        color0=['red','darkorange','yellow','#BFFF00','deepskyblue','violet']
        pn,namelist=GetPlayerInfo(color0)     #From Line 320 [2]
        iCoupon,iCash,iDeposit=initialsettings()    #From Line 336 [3]
        Hospital=[0]*pn
        Prison=[0]*pn
        TBnum=[0]*pn
        Dream=[0]*pn
        for i in range(pn):
            prop.append(['遙控骰子(Wishful Dice)','路障(Barrier Block)','地雷(LandMine)',
                         '定時炸彈(TimeBomb)','機器工人(Mechanic Workers)','遙控骰子(Wishful Dice)','機器娃娃(Street Cleaner)'])
            card.append(['陷害卡(Framing Card)','轉向卡(Veer Card)','免費卡(Free Card)',
                         '停留卡(Stop Card)','天使卡(Angle Card)','惡魔卡(Devil Card)',
                         '拆除卡(Demolition Card)','烏龜卡(Turtle Card)','購地卡(Purchase Card)',
                         '怪獸卡(Monster Card)','搶奪卡(Rob Card)','冬眠卡(Hibernation Card)',
                         '免罪卡(Exoneration Card)','嫁禍卡(CalamityShift Card)','均富卡(AverageRich Card)',
                         '均貧卡(AveragePoor Card)','查稅卡(Tax Card)','復仇卡(Revenge Card)','夢遊卡(DreamWalk Card)'])
        TBstate=[False]*pn
        Stopstate=[False]*pn
        Hiberstate=[0]*pn
        Turtlenum=[0]*pn
        for i in range(pn):
            text=Text(Point(100+i*100,650),'%02d'%TBnum[i])
            TBinfo.append(text)
        for i in TBinfo:
            i.draw(win)
        Quitnum=0
        #determine whether a houseproperty is vacancy.
        
                #####################################
        for i in range(pn):
            shapecho=0
            hpro.append([])
            lotteries.append([])
            IP=choice(pSet[0:74])  #get a point from the pSet randomly
            shape,co,shapecho=getshapecolor(pn,0,IP,namelist[i],color0,color,shapecho,Load)   #From Line 430 [7]
            shapecholist.append(shapecho)
            shapes.append(shape)
            pnum.append(pSet.index(IP))
            color.append(co)
            del color0[color0.index(co)]
            direction.append(randint(0,1))
            Cash.append(iCash)
            Deposit.append(iDeposit)
            Coupon.append(iCoupon)
        for i in shapes:
            i.draw(win)
        for i in range(pn):
            text=Text(Point(100+i*100,680),namelist[i])
            text.setFill(color[i])
            Namebook.append(text)
            text.draw(win)
    elif firstcho=='2':
        print('Please enter the name of the file of your record.')
        while True:
            try:
                filename=input()
                if not filename:
                    filename='default.txt' ##in case of error
                afile=open(filename,'r')
                break
            except FileNotFoundError:
                print('Error, File can Not be Found.')
                continue
        Load=True
        Vacancy,Quitnum,pn,loadnum,shapecholist,\
                            color,pnum,namelist,direction,Cash,Deposit,\
                            Coupon,Hospital,Prison,TBnum,houselevel,BBon,\
                            LMon,TBon,TBstate,Stopstate,Turtlenum,Hiberstate,\
                            TBinfo,hpro,prop,card,Namebook,shapes,Dream,\
                            Wdiceused,Wstep,thedate,lotteries,loccupy,bonus,priceindex=load(afile,Levelobj,\
                            pSet,bSet,win,LMobj,TBobj,BBobj,shapes,color,\
                            shapecholist,Namebook,hpro,prop,card,TBinfo,Load,lotteries)
        print(type(loccupy),loccupy,type(bonus),bonus)
        Lottery=lottery(loccupy,bonus)
        Timer=timer(thedate)

    #print(Cash,Deposit,Coupon)
    #PlayerInfo(pn,namelist,Cash,Deposit,Coupon)
    print('\n\n========================NOW GAME START!!!========================\n\n')
    gameover=False
    while True:
        if Timer.lotterytime() and not Load:
            time.sleep(0.5)
            winprint(('It is lottery time!!!'))
            winprint('The bonus this month is: $%d!!!'%round(Lottery.bonus*priceindex))
            time.sleep(1.3)
            winprint('Here are the lottery numbers of each Player:')
            for i in range(pn):
                print('%s:\t%s'%(namelist[i],str(lotteries[i])))
            winnum=randint(1,36)
            winprint('The winning number is:                                    ')
            winprint('%02d!!!!!'%winnum)
            time.sleep(1)
            for i in range(len(lotteries)):
                for j in lotteries[i]:
                    if j==winnum:
                        lwinner=namelist[i]
                        winprint('Congratulations!!The winner is %s!!!!!!!!'%lwinner)
                        winprint('%s wins the bonus $%d!!!!!'%(lwinner,round(Lottery.bonus*priceindex)))
                        non=input('\nPress enter key to continue.')
                        Cash[i]+=round(Lottery.bonus*priceindex)
                        Lottery.initial()
                        lotteries=[]
                        for i in range(pn):
                            lotteries.append([]) #initialize
                        lotterywin=True
            if not lotterywin:
                print('\nSorry. No one win the bonus this month.')
                time.sleep(0.5)
                print('The bonus will be accumulated to next month.')
                time.sleep(0.5)
                print('Have fun!!!')
                non=input('\nPress enter key to continue.')
                Lottery.addbonus()
            else:
                lotterywin=False
        elif Timer.interest() and not Load:
            time.sleep(0.5)
            print('Today is the day the Bank give out interests.')
            time.sleep(1)
            for i in range(pn):
                interest=int(Deposit[i]*0.10)
                print('Player %s got $%d.'%(namelist[i],interest))
                Deposit[i]+=interest
                priceindex+=0.12
                priceindex=round(priceindex,2)
            non=input('Press enter key to continue.')
        for num in range(pn):
            Loaded=False
            if Load:
                if num!=loadnum:
                    continue
                Load=False
                Loaded=True
            # Save & Load System
            for i in range(pn):
                oldnamelist.append(i)
                oldnamelist.append(namelist[i])
            if Quitnum>0:
                num-=Quitnum
            name=namelist[num]     
            print('\n==============Now, it is the turn for player ',name,'.==============',sep='')
            print('\nToday is: ',str(Timer),Timer.theweekday())
            YourInfo(num,namelist,Cash,Deposit,Coupon,hpro,prop,card,pn)   #From Line 396 [8]
            newnamelist=[]
            newpnum=[]
            houses=[]
            Ground=[]
            for i in range(len(houselevel)):
                if houselevel[i]!=0:
                    houses.append(i)
            for i in range(pn):
                j=len(hpro[i])
                Ground.append(j)
            for i in range(pn):
                if i!=num:
                    newnamelist.append(i)
                    newnamelist.append(namelist[i]) #Get ready for card use
            
            ######################################### Hospital System ###########################################
            
            if Hospital[num]>0:
                Hospital[num]-=1
                if Dream[num]:
                    Dream[num]-=1
                    if Dream[num]==0:
                        print('Dreamwalk finished.')
                    else:
                        print('You still have to Dreamwalk for %d days'%(Dream[num]))
                        time.sleep(0.5)
                if Hospital[num]>0:
                    print('\nSorry, you can not check out of the hospital now.')
                    print('\nYou still have to wait for',Hospital[num],'days.')
                    non=input('\nPress enter key to continue')
                elif Hospital[num]==0:
                    print('You can check out now!')
                    non=('Press enter key to continue')
                    pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(shapes[num],pSet[74],pSet[34],TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,Timer,StrClean,Dream)   #From Line 486 [9]    #simplify it
                    #################### step on the bomb #####################
                    Lmon,pnum,Hospital,TBinfo,TBnum,TBstate=steponbomb(LMon,pnum,num,LMobj,pSet,shapes,Hospital,TBstate,TBinfo,TBnum,Cash,Deposit,Timer,StrClean,Dream) #even just go out of hospital...
                    ###########################################################     #From Line 658 [10]
                    if TBon[pnum[num]]:
                        if not TBstate[num]:
                            print('Unluckily, you are attached by a TimeBomb.')
                            print('The bomb will explode in 30 steps.')
                            non=input('\nPress enter key to continue.')
                            TBinfo[num].setFill('red')
                            TBinfo[num].setText('%02d'%30)
                            for i in TBobj[pnum[num]]:
                                i.undraw()
                            TBon[pnum[num]]=False
                            TBstate[num]=True
                            TBnum[num]=30
                        else:
                            print('You have already been carrying a TimeBomb.')
                            non=input('\nPress enter key to continue.')
                    elif BBon[pnum[num]]:  ##BB detection
                        for i in BBobj[pnum[num]]:
                            i.undraw()
                        BBon[pnum[num]]=False
            elif Prison[num]>0:
                Prison[num]-=1
                if Dream[num]>0:
                    Dream[num]-=1
                    if Dream[num]==0:
                        print('Dreamwalk finished.')
                        Dreamstate[num]=False
                    elif Dream[num]>0:
                        print('You still have to Dreamwalk for %d days'%(Dream[num]))
                        time.sleep(0.5)
                    else:
                        raise ValueError
                    
                if Prison[num]>0:
                    print('\nSorry, you can not check out of the prison now.')
                    print('\nYou still have to wait for',Prison[num],'days.')
                    non=input('\nPress enter key to continue')
                elif Prison[num]==0:
                    print('You can check out now!')
                    non=('Press enter key to continue')
                    pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(shapes[num],pSet[75],pSet[53],TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,Timer,StrClean,Dream)   #From Line 486 [9]    #simplify it
                    #################### step on the bomb #####################
                    Lmon,pnum,Hospital,TBinfo,TBnum,TBstate=steponbomb(LMon,pnum,num,LMobj,pSet,shapes,Hospital,TBstate,TBinfo,TBnum,Cash,Deposit,Timer,StrClean,Dream) #even just go out of prison...
                    if TBon[pnum[num]]:
                        if not TBstate[num]:
                            print('Unluckily, you are attached by a TimeBomb.')
                            print('The bomb will explode in 30 steps.')
                            non=input('\nPress enter key to continue.')
                            TBinfo[num].setFill('red')
                            TBinfo[num].setText('%02d'%30)
                            for i in TBobj[pnum[num]]:
                                i.undraw()
                            TBon[pnum[num]]=False
                            TBstate[num]=True
                            TBnum[num]=30
                        else:
                            print('You have already been carrying a TimeBomb.')
                            non=input('\nPress enter key to continue.')
                    elif BBon[pnum[num]]:  ##BB detection
                        for i in BBobj[pnum[num]]:
                            i.undraw()
                        BBon[pnum[num]]=False
                else:
                    raise ValueError
            
            elif Hiberstate[num]:
                Hiberstate[num]-=1
                if Hiberstate[num]:
                    print('You still have to sleep for',Hiberstate[num],'days.')
                    non=input('\nPress enter key to continue.')
                elif Hiberstate[num]==0:
                    print('Sleep finished.')
                              
            elif Dream[num]:
                Dream[num]-=1
                if Dream[num]==0:
                    print('Dreamwalk finished.')
                elif Dream[num]:
                    print('You still have to Dreamwalk for %d days'%(Dream[num]))
                    time.sleep(0.5)
                    step=randint(1,6)
                    if Stopstate[num]:
                        step=0
                        Stopstate[num]=False
                    elif Turtlenum[num]>0:
                        step=1
                        Turtlenum[num]-=1
                    else:
                        print('\nThe dice comes up with\n',step)
                    passway,pnum,BBon,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=msbs(shapes[num],pSet,step,pSet[pnum[num]],direction,num,passway,BBon,BBobj,TBstate,TBinfo,TBnum,pnum,Hospital,Cash,Deposit,Timer,StrClean,Dream)
                    ############### step on timebomb ###############                  #From Line 504 [19]
                    if TBon[pnum[num]]:
                        if not TBstate[num]:
                            print('Unluckily, you are attached by a TimeBomb.')
                            print('The bomb will explode in 30 steps.')
                            non=input('Press enter key to continue.')
                            TBinfo[num].setFill('red')
                            TBinfo[num].setText('%02d'%30)
                            for i in TBobj[pnum[num]]:
                                i.undraw()
                            TBon[pnum[num]]=False
                            TBstate[num]=True
                            TBnum[num]=30
                        else:
                            print('You have already been carrying a TimeBomb.')
                            non=input('Press enter key to continue.')
                    
                    ################## steponbomb ####################
                                    
                    Lmon,pnum,Hospital,TBinfo,TBnum,TBstate=steponbomb(LMon,pnum,num,LMobj,pSet,shapes,Hospital,TBstate,TBinfo,TBnum,Cash,Deposit,Timer,StrClean,Dream)
                    ###################################################################
                    if not LMon[pnum[num]]:
                        for i in hpro:
                            if pnum[num] in i:
                                Cash,Deposit,card=tollgiving(hpro,pnum,num,Hospital,houseprice,houselevel,Cash,Deposit,namelist,place,Prison,Hiberstate,card,Dream,priceindex)
                                                                                            #From Line 724 [24]
                
            if Hospital[num]==0 and Prison[num]==0 and Hiberstate[num]==0 and Dream[num]==0:
                Wdice=False
                if not Loaded:  # protect 'Wdiceused'
                    Wdiceused=False
                BB=False  #Barrier Block
                LM=False  #LandMine
                TB=False  #TimeBomb
                MW=False  #Mechanic Workers
                StrClean=False #Street Cleaner
                FC=False  #Framing Card
                VC=False  #Veer Card
                FreeC=False #Free Card
                StopC=False #Stop Card
                DemoC=False #
                AngleC=False #Angle Card
                DevilC=False #Devil Card
                TurtleC=False #Turtle Card
                PurC=False #Purchase Card
                MonsterC=False #Monster Card
                RobC=False #Rob Card
                HiberC=False #Hiber Card
                ExonerC=False #Exoneration Card
                ShiftC=False #Calamity Shifting Card
                ARC=False #AverageRich Card
                APC=False #AveragePoor Card
                TaxC=False #Tax Card
                RevengeC=False #Revenge Card
                DreamC=False #Dreaming Card
                step=randint(1,6)     ### get the random int before 'throwing the die' because of Wdice
                while True:
                    cho=Operation(namelist,num,direction)      #From Line 408 [11]
                    if cho==1:
                        PlayerInfo(pn,namelist,Cash,Deposit,Coupon,hpro,Hospital,prop,card)     #From Line 402 [12]
                        non=input('Press enter to continue.')          
                             #From Line 408 [13]
                        
                    ######################################### Props & Cards #######################################

                    elif cho==2:              
                        PC=propcardchoice()    #get the choice   #From Line 567  [14]
                        if PC=='0':
                            continue
                        elif PC=='1':          ############## props ###############
                            procho=ChooseProp(prop,num,PC)     #From Line 576 [15]
                            if procho==0:
                                continue           #turn back
                            Wdice,BB,LM,TB,MW,StrClean=propUse(prop,procho,num,Wdice,BB,LM,TB,MW,StrClean,PC)    #From Line 591 [16]
                            if Wdice:
                                if Wdiceused:
                                    print("You have used Wishful Dice, you needn't use it again.")
                                    non=input('Press enter to continue.')
                                    Wdice=False
                                    continue
                                try:
                                    a=int(input('How many steps would you like to walk? (1-6) (Press enter to turn back)\n'))
                                    while a not in [1,2,3,4,5,6]:
                                        print('\nError! Please enter again.')
                                        a=int(input('How many steps would you like to walk? (1-6) (Press enter to turn back)\n'))
                                    Wstep=a
                                    del prop[num][procho-1]
                                    Wdice=False       #debug
                                    Wdiceused=True       ##in case the user use Wdice twice
                                except ValueError:
                                    Wdice=False
                                    Wdiceused=False
                                    continue    
                            if BB:
                                BBon,dcho=putprop(direction,num,pSet,pnum,win,BBon,BBobj,LMon,TBon,propname='Barrier Block')
                                BB=False
                                if dcho!='0':                                                  #From Line 604 [17]
                                    del prop[num][procho-1]
                                else:       #dcho=='0' (Fail to use)
                                    continue
                            if LM:
                                LMon,dcho=putprop(direction,num,pSet,pnum,win,LMon,LMobj,BBon,TBon,propname='LandMine')
                                LM=False
                                if dcho!='0':                                                   #From Line 604 [17]
                                    del prop[num][procho-1]
                                else:       #dcho=='0' (Fail to use)
                                    continue
                            if TB:
                                TBon,dcho=putprop(direction,num,pSet,pnum,win,TBon,TBobj,BBon,LMon,propname='TimeBomb')
                                if dcho!='0':                                                   #From Line 604 [17]                              
                                    del prop[num][procho-1]
                                    TB=False
                                else:       #dcho=='0' (Fail to use)
                                    TB=False
                                    continue
                            if MW:
                                MW,houselevel,dcho=useMW(direction,num,pSet,pnum,win,MW,houselevel,hpro,Levelobj,f='upgrade.')
                                if dcho=='0':
                                    MW=False
                                    continue
                                if MW:
                                    del prop[num][procho-1]
                                    MW=False
                                else:
                                    MW=False
                                    continue
                            if StrClean:
                                baby=DrawStreetCleaner(pSet[pnum[num]],win)
                                rinfo=TBstate[num]
                                TBstate[num]=False  #protect
                                for i in range(1,11):
                                    if direction[num]==0:
                                        BBon[(pnum[num]+i)%74]=False
                                        LMon[(pnum[num]+i)%74]=False
                                        TBon[(pnum[num]+i)%74]=False
                                    if direction[num]==1:
                                        BBon[(pnum[num]-i)%74]=False
                                        LMon[(pnum[num]-i)%74]=False
                                        TBon[(pnum[num]-i)%74]=False
                                a=pnum[num]
                                baby.draw(win)
                                passway,pnum,BBon,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=msbs(baby,pSet,10,pSet[pnum[num]],direction,num,passway,BBon,BBobj,TBstate,TBinfo,TBnum,pnum,Hospital,Cash,Deposit,Timer,StrClean,Dream)
                                time.sleep(0.3)
                                baby.undraw()
                                pnum[num]=a
                                TBstate[num]=rinfo
                                if direction[num]==0:
                                    if 74 in range(pnum[num]+1,pnum[num]+11):
                                        for j in BBobj[(pnum[num]+1):]:
                                            for k in j:
                                                k.undraw()
                                        for j in LMobj[(pnum[num]+1):]:
                                            for k in j:
                                                k.undraw()
                                        for j in TBobj[(pnum[num]+1):]:
                                            for k in j:
                                                k.undraw()
                                        for j in BBobj[:(pnum[num]+11)%74]:
                                            for k in j:
                                                k.undraw()
                                        for j in LMobj[:(pnum[num]+11)%74]:
                                            for k in j:
                                                k.undraw()
                                        for j in TBobj[:(pnum[num]+11)%74]:
                                            for k in j:
                                                k.undraw()
                                    else:
                                        for j in BBobj[(pnum[num]+1)%74:(pnum[num]+11)%74]:
                                            for k in j:
                                                k.undraw()
                                        for j in LMobj[(pnum[num]+1)%74:(pnum[num]+11)%74]:
                                            for k in j:
                                                k.undraw()
                                        for j in TBobj[(pnum[num]+1)%74:(pnum[num]+11)%74]:
                                            for k in j:
                                                k.undraw()
                                if direction[num]==1:
                                    if 0 in range((pnum[num]-10),pnum[num]):
                                        for j in BBobj[:pnum[num]]:
                                            for k in j:
                                                k.undraw()
                                        for j in BBobj[(pnum[num]-10)%74:]:
                                            for k in j:
                                                k.undraw()
                                        for j in LMobj[:pnum[num]]:
                                            for k in j:
                                                k.undraw()
                                        for j in LMobj[(pnum[num]-10)%74:]:
                                            for k in j:
                                                k.undraw()
                                        for j in TBobj[:pnum[num]]:
                                            for k in j:
                                                k.undraw()
                                        for j in TBobj[(pnum[num]-10)%74:]:
                                            for k in j:
                                                k.undraw()
                                    else:
                                        for j in BBobj[pnum[num]-10:pnum[num]]:
                                            for k in j:
                                                k.undraw()
                                        for j in TBobj[pnum[num]-10:pnum[num]]:
                                            for k in j:
                                                k.undraw()
                                        for j in LMobj[pnum[num]-10:pnum[num]]:
                                            for k in j:
                                                k.undraw()
                                del prop[num][procho-1]
                                StrClean=False
                                            
                    ############################ cards ############################
                        elif PC=='2':
                            carcho=ChooseProp(card,num,PC)
                            if carcho==0:
                                continue
                            FC,VC,FreeC,StopC,AngleC,DevilC,DemoC,TurtleC,PurC,MonsterC,RobC,HiberC,ExonerC,ShiftC,ARC,APC,TaxC,RevengeC,DreamC=cardUse(card,carcho,num,FC,VC,FreeC,StopC,AngleC,DevilC,DemoC,TurtleC,PurC,MonsterC,RobC,HiberC,ExonerC,ShiftC,ARC,APC,TaxC,RevengeC,DreamC)    #From Line 591
                            if FC:
                                FC=False
                                percho=ChoosePerson(direction,newnamelist,pnum,num,pn,cardname='Framing Card')  #From Line
                                percho-=1  # Habit of human
                                if percho==-1:
                                    continue
                                num1=newnamelist[2*percho]
                                if pnum[num1]//74==0: #in case the person has been in hospital or prison
                                    if CanUseCard(pnum,num,num1,namelist,f='was condemned to be arrested for 3 days.'):
                                        del card[num][carcho-1]
                                        while '嫁禍卡(CalamityShift Card)' in card[num1]:      ##Here should be a while loop because Shift Card is transferable
                                            num1,shiftcho=UseShiftCard(namelist,num1,card,pn,pnum,direction)
                                            if not shiftcho:  #if shiftcho==True, num1 must have changed
                                                break           #if Player num1 haven't CSC, the condition of the loop can't be satisfied, the loop breaks
                                                                #else, ask the player whether to use
                                        ExonerC=UseExonerCard(card,num1,namelist)
                                        if not ExonerC:
                                            Prison[num1]+=4
                                            pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(shapes[num1],pSet[pnum[num1]],pSet[75],TBstate,num1,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,Timer,StrClean,Dream)
                                            if '復仇卡(Revenge Card)' in card[num1] and num1!=num:
                                                del card[num1][card[num1].index('復仇卡(Revenge Card)')]
                                                print('\nThe Revenge Card takes its effect.\nYou have to go prison together with him or her.')
                                                time.sleep(1.3)
                                                Prison[num]+=4
                                                pnum,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit=mfptp(shapes[num],pSet[pnum[num]],pSet[75],TBstate,num,TBinfo,TBnum,pnum,pSet,Hospital,Cash,Deposit,Timer,StrClean,Dream)
                                                time.sleep(1.3)
                                            if Prison[num]:
                                                break     #in this case he or she should have been in the prison. So break
                                        else:
                                            print('The Exoneration Card takes its effect')
                                            print("You needn't go to prison then.")
                                            time.sleep(1.5)
                                            ExonerC=False   #re-false
                                    else:
                                        print("That player is too far from you, you can't frame him or her")
                                        non=input('Press enter key to continue.')
                                else:
                                    print("\nThat player has already been in prison or hospital, you can't frame him or her")
                                    non=input('Press enter key to continue.')
                            if VC:
                                percho=ChoosePerson(direction,oldnamelist,pnum,num,pn,cardname='Veer Card')
                                percho-=1
                                VC=False
                                if percho==-1:
                                    continue
                                num1=oldnamelist[2*percho]
                                if pnum[num1]//74==0:
                                    if CanUseCard(pnum,num,num1,namelist,f='has turned back.'):
                                        if direction[num1]==0:
                                            direction[num1]=1
                                        elif direction[num1]==1:
                                            direction[num1]=0
                                        del card[num][carcho-1]
                                    else:
                                        print("That player is too far from you. \nYou can't apply your card to him or her")
                                        time.sleep(0.3)
                                else:
                                    print("That player is in prison or hospital. \nYou can't use your card to him or her.")
                            if FreeC:
                                print("\nYou can't use Free Card actively")
                                non=input('\nPress enter key to continue.')
                                FreeC=False
                            if StopC:
                                StopC=False
                                percho=ChoosePerson(direction,oldnamelist,pnum,num,pn,cardname='Stop Card')
                                percho-=1
                                if percho==-1:
                                    continue
                                num1=oldnamelist[2*percho]
                                if pnum[num1]//74==0:
                                    if CanUseCard(pnum,num,num1,namelist,f='has to stop for a round.'):
                                        Stopstate[num1]=True
                                        del card[num][carcho-1]
                                    else:
                                        print("That player is too far from you. \nYou can't apply your card to him or her")
                                        non=input('\nPress enter key to continue.')
                            if AngleC:
                                AngleC=False
                                if pnum[num] in houseposition:
                                    streetnum=detectstreet(pnum,num)
                                    print('\nThe whole street is upgrated')
                                    non=input('Press enter key to continue.')
                                    for i in place[streetnum]:
                                        p=pSet[i]
                                        x=p.getX()
                                        y=p.getY()
                                        if houselevel[i]<=5:
                                            Levelobj[i][houselevel[i]].draw(win)
                                            houselevel[i]+=1
                                    del card[num][carcho-1]
                                else:
                                    print('\nYou must be on a ground when using a Angel Card.')
                                    non=input('Press enter key to continue.')
                            if DevilC:
                                DevilC=False
                                if pnum[num] in houseposition:
                                    streetnum=detectstreet(pnum,num)
                                    print('\nThe whole street is destoryed.')
                                    non=input('Press enter key to continue.')
                                    for i in place[streetnum]:
                                        p=pSet[i]
                                        x=p.getX()
                                        y=p.getY()
                                        if houselevel[i]>0:
                                            houselevel[i]-=1
                                            Levelobj[i][houselevel[i]].undraw()
                                    del card[num][carcho-1]
                                else:
                                    print('\nYou must be on a ground when using a Devil Card.')
                                    non=input('Press enter key to continue.')
                            if DemoC:
                                DemoC,houselevel,dcho=useMW(direction,num,pSet,pnum,win,DemoC,houselevel,hpro,Levelobj,f='destory.')
                                if dcho=='0':
                                    DemoC=False
                                if DemoC:
                                    del card[num][carcho-1]
                                    DemoC=False
                                else:
                                    DemoC=False
                            if TurtleC:
                                TurtleC=False
                                percho=ChoosePerson(direction,oldnamelist,pnum,num,pn,cardname='Turtle Card')
                                percho-=1
                                if percho==-1:
                                    continue
                                num1=oldnamelist[2*percho]
                                if pnum[num1]//74==0:
                                    if CanUseCard(pnum,num,num1,namelist,f='has been turtled.'):
                                        Turtlenum[num1]=3
                                        del card[num][card[num].index('烏龜卡(Turtle Card)')]
                                    else:
                                        print("That player is too far from you, you can't apply your card to him or her")
                                        non=input('\nPress enter key to continue.')
                                else:
                                    print("\nThat player is in prison or hospital, you can't use your card to him or her.")
                            if PurC:
                                PurC=False
                                price=houseprice[pnum[num]]*(houselevel[pnum[num]]+1)
                                if Cash[num]>=price:
                                    if pnum[num] in houseposition:
                                        num1=detecthpro(pnum,num,hpro)
                                        if num1!=num:
                                            del card[num][carcho-1]
                                            del hpro[num1][hpro[num1].index(pnum[num])]
                                            hpro[num].append(pnum[num])
                                            bSet[pnum[num]].setFill(color[num])
                                            Cash[num]-=price
                                        else:
                                            print("It is your own ground, you needn't use your Purchase Card")
                                            non=input('Press enter key to continue.')
                                    else:
                                        print('You must be on a ground to use your Purchase Card.')
                                        non=input('Press enter key to continue.')
                                else:
                                    print("\nSorry, you don't have enough money to pay for this ground.")
                                    non=input('Press enter key to continue.')
                            if MonsterC:
                                MonsterC,houselevel,dcho=useMW(direction,num,pSet,pnum,win,MonsterC,houselevel,hpro,Levelobj,f='send your Monster to.')
                                if dcho=='0':
                                    MonsterC=False
                                if MonsterC:
                                    del card[num][carcho-1]
                                    MonsterC=False
                                else:
                                    MonsterC=False
                            if RobC:
                                RobC=False
                                percho=ChoosePerson(direction,newnamelist,pnum,num,pn,cardname='Rob Card')
                                percho-=1
                                if percho==-1:
                                    continue
                                num1=newnamelist[2*percho]
                                if pnum[num1]//74==0:
                                    if not CanUseCard(pnum,num,num1,namelist,f=''):
                                        print("That player is too far from you, you can't apply your card to him or her")
                                        non=input('\nPress enter key to continue.')
                                    else:
                                        print('\nThe Player ',namelist[num1],"'s props and cards are as follows.",sep='')
                                        printinventory(prop,card,num1)
                                        print('\nWhat kind of inventory do you want?')
                                        print('\n(1)Card\n(2)Prop')
                                        pccho=input('Please enter your choice: \n')          #the choice of props or cards
                                        while pccho!='1' and pccho!='2':
                                            print('Error. Please enter your choice again.')
                                            print('\nWhat kind of inventory do you want?')
                                            print('\n(1)Card\n(2)Prop')
                                            pccho=input('Please enter your choice: \n')
                                        if pccho=='2':
                                            procarcho=ChooseProp(prop,num1,pccho)
                                            if procarcho==0:
                                                continue
                                            else:
                                                del card[num][carcho-1]
                                                prop[num].append(prop[num1][procarcho-1])
                                                print('\nYou robbed the',prop[num1][procarcho-1],'from Player',namelist[num1],'successfully.')
                                                non=input('Press enter key to continue.')
                                                del prop[num1][procarcho-1]
                                        elif pccho=='1':
                                            procarcho=ChooseProp(card,num1,pccho)
                                            if procarcho==0:
                                                continue
                                            else:
                                                del card[num][carcho-1]
                                                card[num].append(card[num1][procarcho-1])
                                                print('\nYou robbed the',card[num1][procarcho-1],'from Player',namelist[num1],'successfully.')
                                                non=input('Press enter key to continue.')
                                                del card[num1][procarcho-1]
                                else:
                                    print("\nThat player is in prison or hospital, you can't use your card to him or her.")
                                    non=input('Press enter key to continue.')
                            if HiberC:
                                Hiberstate=[6]*pn
                                Hiberstate[num]=0
                                del card[num][carcho-1]
                                print('You used your Hiberation Card successfully.\nEvery Player except you will have to sleep for 5 days.')
                                time.sleep(1.3)
                            if ExonerC:
                                print("\nYou can't use Exoneration Card actively")
                                non=input('\nPress enter key to continue.')
                                ExonerC=False
                            if ShiftC:
                                print("\nYou can't use Exoneration Card actively")
                                non=input('\nPress enter key to continue.')
                                ShiftC=False
                            if ARC:
                                ARC=False
                                almoney=sum(Cash)
                                for i in range(len(Cash)):
                                    Cash[i]=int(almoney/pn)
                                print('\nYou used AverageRich Card successfully.\nNow Cashes of each Player are averaged.')
                                del card[num][carcho-1]
                                time.sleep(1.2)
                            if APC:
                                APC=False
                                percho=ChoosePerson(direction,newnamelist,pnum,num,pn,cardname='AveragePoor Card')
                                percho-=1
                                if percho==-1:
                                    continue
                                num1=newnamelist[2*percho]
                                if pnum[num1]//74==0:
                                    if not CanUseCard(pnum,num,num1,namelist,f=''):
                                        print("That player is too far from you, you can't apply your card to him or her")
                                        non=input('\nPress enter key to continue.')
                                    else:
                                        avmoney=int((Cash[num1]+Cash[num])/2)
                                        Cash[num]=avmoney
                                        Cash[num1]=avmoney
                                        print('\nYou used AveragePoor Card successfully.\nNow Cashes of you two are averaged.')
                                        del card[num][carcho-1]
                                        time.sleep(1.3)
                                else:
                                    print("\nThat player is in prison or hospital, you can't use your card to him or her.")
                            if TaxC:
                                TaxC=False
                                percho=ChoosePerson(direction,newnamelist,pnum,num,pn,cardname='AveragePoor Card')
                                percho-=1
                                if percho==-1:
                                    continue
                                num1=newnamelist[2*percho]
                                if pnum[num1]//74==0:
                                    if not CanUseCard(pnum,num,num1,namelist,f=''):
                                        print("That player is too far from you, you can't apply your card to him or her")
                                        non=input('\nPress enter key to continue.')
                                    else:
                                        del card[num][carcho-1]
                                        money=int(Cash[num1]*0.10)
                                        Cash[num]+=money
                                        Cash[num1]-=money
                                        print('You used your Tax Card successfully.\nYou got $%d from Player %s'%(money,namelist[num1]))
                                        time.sleep(1.3)
                                else:
                                    print("That player is too far from you. \nYou can't apply your card to him or her")
                                    non=input('\nPress enter key to continue.')
                            if RevengeC:
                                RevengeC=False
                                print("You can't use Revenge Card actively.")
                                non=input('Press enter key to continue.')
                            if DreamC:
                                DreamC=False
                                percho=ChoosePerson(direction,newnamelist,pnum,num,pn,cardname='Rob Card')
                                percho-=1
                                if percho==-1:
                                    continue
                                num1=newnamelist[2*percho]
                                if pnum[num1]//74==0:
                                    if not CanUseCard(pnum,num,num1,namelist,f='will fall into asleep.'):
                                        print("That player is too far from you, you can't apply your card to him or her")
                                        non=input('\nPress enter key to continue.')
                                    else:
                                        del card[num][carcho-1]
                                        while '嫁禍卡(CalamityShift Card)' in card[num1]:      ##Here should be a while loop because Shift Card is transferable
                                            num1,shiftcho=UseShiftCard(namelist,num1,card,pn,pnum,direction)
                                            if not shiftcho:  #if shiftcho==True, num1 must have changed
                                                break           #if Player num1 haven't CSC, the condition of the loop can't be satisfied, the loop breaks
                                                                #else, ask the player whether to use
                                        ExonerC=UseExonerCard(card,num1,namelist)
                                        if not ExonerC:
                                            Dream[num1]+=6
                                            if '復仇卡(Revenge Card)' in card[num1] and num1!=num:
                                                del card[num1][card[num1].index('復仇卡(Revenge Card)')]
                                                print('\nThe Revenge Card takes its effect.\nYou have to SleepWalk together with him or her.')
                                                time.sleep(1.3)
                                                Dream[num]+=6
                                                cho=4   # move directly
                                                print('Player %s starts to DreamWalk, too.'%(namelist[num]))
                                                time.sleep(1.3)
                                        else:
                                            print('The Exoneration Card takes its effect')
                                            print("You needn't DreamWalk then.")
                                            time.sleep(1)
                                            ExonerC=False   #re-false
                                else:
                                    print("That player is too far from you. \nYou can't apply your card to him or her")
                                    non=input('\nPress enter key to continue.')
                            
                        ############################### Save and Load System #############################
                    elif cho==3:
                        print('Load or Save?(enter 0 to turn back)')
                        print('(1) Load\n(2) Save')
                        LScho=input()
                        while LScho!='0' and LScho!='1' and LScho!='2':
                            print('Error! Please enter again.')
                            LScho=input()
                        if LScho=='0':
                            continue
                        if LScho=='1':
                            print('Please enter the name of the file of your record.')
                            while True:
                                try:
                                    filename=input()
                                    if not filename:  # if filename=''
                                        filename='default.txt' ##in case of error
                                    afile=open(filename,'r')
                                    break
                                except FileNotFoundError:
                                    print('Error, File can Not be Found.')
                                    continue
                            Load=True
                            ########### initialize ###########
                            for i in shapes:
                                i.undraw()
                            for i in TBinfo:
                                i.undraw()
                            for i in TBobj:
                                for j in i:
                                    j.undraw()
                            for i in LMobj:
                                for j in i:
                                    j.undraw()
                            for i in BBobj:
                                for j in i:
                                    j.undraw()
                            for i in Namebook:
                                i.undraw()
                            for i in houseposition:  #re-paint
                                bSet[i].setFill('lemonchiffon') 
                            shapes=[]
                            color=[]
                            shapecholist=[]
                            Namebook=[]
                            hpro=[]
                            prop=[]
                            card=[]
                            BBon=[]
                            TBinfo=[]
                            lotteries=[]
                            for i in range(len(houselevel)):
                                if houselevel[i]!=0:
                                    for j in Levelobj[i]:
                                        j.undraw()
                            #############################################
                            loadnum=''
                            Vacancy,Quitnum,pn,loadnum,shapecholist,\
                            color,pnum,namelist,direction,Cash,Deposit,\
                            Coupon,Hospital,Prison,TBnum,houselevel,BBon,\
                            LMon,TBon,TBstate,Stopstate,Turtlenum,Hiberstate,\
                            TBinfo,hpro,prop,card,Namebook,shapes,Dream,\
                            Wdiceused,Wstep,thedate,lotteries,loccupy,bonus,priceindex=load(afile,Levelobj,\
                            pSet,bSet,win,LMobj,TBobj,BBobj,shapes,color,\
                            shapecholist,Namebook,hpro,prop,card,TBinfo,Load,lotteries)
                            Lottery.__init__(loccupy,bonus)
                            Timer.__init__(thedate)
                            break
                        elif LScho=='2':
                            #hpro
                            
                            Cloud=[Quitnum,pn,num,shapecholist,color,pnum,namelist,
                                   direction,Cash,Deposit,Coupon,Hospital,Prison,
                                   TBnum,houselevel,BBon,LMon,TBon,TBstate,Stopstate,
                                   Turtlenum,Hiberstate,Dream,Wdiceused,Wstep,str(Timer)[2:-1],Lottery.occupy,Lottery.bonus,priceindex] # all of the infos are here
                            print('Please enter the name of the save file.')
                            filename=input()
                            if not filename:
                                filename='default.txt'
                            afile=open(filename,'w')
                            for i in Cloud:
                                p=str(i)
                                afile.write(p+'\n')
                            for i in hpro:
                                p=str(i)
                                afile.write(p+'\n')
                            for i in prop:
                                p=str(i)
                                afile.write(p+'\n')
                            for i in card:
                                p=str(i)
                                afile.write(p+'\n')
                            for i in lotteries:
                                p=str(i)
                                afile.write(p+'\n')
                            afile.close()
                        
                    ########################################### End ###############################################

                    if cho==4:   # should be if because of DreamWalk Card
                        if Wdiceused:
                            step=Wstep
                        if Stopstate[num]:
                            step=0
                            Stopstate[num]=False
                        elif Turtlenum[num]>0:
                            step=1
                            Turtlenum[num]-=1
                        else:
                            print('\nThe dice comes up with\n',step)
                        passway,pnum,BBon,TBinfo,TBnum,TBstate,Hospital,Cash,Deposit\
                        =msbs(shapes[num],pSet,step,pSet[pnum[num]],direction,num,passway,\
                        BBon,BBobj,TBstate,TBinfo,TBnum,pnum,Hospital,Cash,Deposit,Timer,StrClean,Dream)
                        ############### step on TimeBomb ###############                  #From Line 504 [19]
                        if TBon[pnum[num]]:
                            if not TBstate[num]:
                                print('Unluckily, you are attached by a TimeBomb.')
                                print('The bomb will explode in 30 steps.')
                                non=input('\nPress enter key to continue.')
                                TBinfo[num].setFill('red')
                                TBinfo[num].setText('%02d'%30)
                                for i in TBobj[pnum[num]]:
                                    i.undraw()
                                TBon[pnum[num]]=False
                                TBstate[num]=True
                                TBnum[num]=30
                            else:
                                print('You have already been carrying a TimeBomb.')
                                non=input('\nPress enter key to continue.')
                        ################################################
                        ################## steponbomb ####################
                                    
                        Lmon,pnum,Hospital,TBinfo,TBnum,TBstate=steponbomb(LMon,pnum,num,LMobj,pSet,shapes,Hospital,TBstate,TBinfo,TBnum,Cash,Deposit,Timer,StrClean,Dream)
                                                                                                    #From Line 658 [20]
                        ###############Couponbonus ###############
                        if Dream[num]:
                            print('Player %s: You are DreamWalking. \nYou cannot get the Coupon bonus.'%namelist[num])
                            non=input('\nPress enter key to continue.')
                        else:
                            Coupon=couponbonus(num,pnum[num],Coupon)        #From Line 543 [21]

                        ################## PolyU ##################
                                        
                        if not LMon[pnum[num]]:
                            if Dream[num]==0:
                                if pnum[num]==17 or pnum[num]==49: # Grocery
                                    cardcho='0'
                                    print('\nWelcome to %s!'%('grocery'))
                                    time.sleep(1)
                                    shop=grocery([],[])
                                    cardlist=shop.getcards()
                                    proplist=shop.getprops()
                                    scardlist=card[num].copy()
                                    sproplist=prop[num].copy()
                                    while True:
                                        print('\nYou can buy or sell your Props and Cards here.')
                                        print('Your Props and Cards are as follows:')
                                        printinventory(prop,card,num)
                                        print()
                                        docho=getchoice('Go out','Buy','Sell')
                                        if docho=='0':
                                            time.sleep(0.3)
                                            break
                                        elif docho=='1':
                                            while True:
                                                print('Props and Cards here are as follows.')
                                                print('\n{0:<30}'.format('Cards'),'{0:<30}'.format('Props'))
                                                b=0
                                                if len(cardlist)>len(proplist):
                                                    for k in proplist:
                                                        j=cardlist[b]
                                                        b+=1
                                                        print('{0:<28}'.format(j),'{0:<30}'.format(k))
                                                    for j in cardlist[b:]:
                                                        print('{0:<28}'.format(j),'{0:<30}'.format(''))
                                                elif len(cardlist)<=len(proplist):
                                                    for j in cardlist:
                                                        k=proplist[b]
                                                        b+=1
                                                        print('{0:<28}'.format(j),'{0:<30}'.format(k))
                                                    for k in proplist[b:]:
                                                        print('{0:<30}'.format(''),'{0:<30}'.format(k))
                                                print('\nWhat do you want to buy?')
                                                PC=getchoice('Turn back','Cards','Props')
                                                if PC=='0':
                                                    break
                                                elif PC=='1':
                                                    carddict=shop.carddict
                                                    cardcho='0'
                                                    cardcho,cardlist,Coupon,card=buysellcard(cardlist,cardcho,card,Coupon,num,carddict,'buy')
                                                    if cardcho==0:
                                                        continue
                                                elif PC=='2':
                                                    propdict=shop.propdict
                                                    cardcho='0'
                                                    cardcho,proplist,Coupon,prop=buysellcard(proplist,cardcho,prop,Coupon,num,propdict,'buy')
                                                    if cardcho==0:
                                                        continue
                                            if PC=='0':   #catch PC=='0'
                                                continue
                                        elif docho=='2':
                                            while True:
                                                print('Your Props and Cards are as follows:')
                                                printinventory(prop,card,num)
                                                print('\nWhat do you want to sell')
                                                PC=getchoice('Turn back','Cards','Props')
                                                if PC=='0':
                                                    break
                                                elif PC=='1':
                                                    carddict=shop.scarddict
                                                    cardcho='0'
                                                    cardcho,scardlist,Coupon,card=buysellcard(scardlist,cardcho,card,Coupon,num,carddict,'sell')
                                                elif PC=='2':
                                                    propdict=shop.spropdict
                                                    cardcho='0'
                                                    cardcho,sproplist,Coupon,prop=buysellcard(sproplist,cardcho,prop,Coupon,num,propdict,'sell')
                                                if cardcho==0:
                                                    continue
                                            if PC=='0':   # catch PC=='0'
                                                continue
                                            continue
                                                
                                elif pnum[num]==57: # PolyU
                                    print("\nWelcome to PolyU!!!\nBecause of your outstanding performance,\nyou get the Principal's Scholarship $5000!!")
                                    Deposit[num]+=5000
                                    non=input('\nPress enter key to continue.')
                                elif pnum[num]==24: # Complimentary Card Point
                                    winprint('Welcome to Complimentary Card Point!')
                                    if not len(card[num])>=12:
                                        time.sleep(1)
                                        randcard=choice(Allcard)
                                        winprint('Congratulations! You get a %s for free!\n'%randcard)
                                        card[num].append(randcard)
                                        non=input('Press enter key to continue.')
                                    else:
                                        print('Sorry, Your Card inventory is full. You cannot get the card.')
                                        non=input('\nPress enter key to continue.')
                                elif pnum[num]==71: # Complimentary Prop Pont
                                    winprint('Welcome to Complimentary Prop Point!')
                                    if not len(prop[num])>=12:
                                        time.sleep(1)
                                        randprop=choice(Allprop)
                                        winprint('Congratulations! You get a %s for free!'%randprop)
                                        prop[num].append(randprop)
                                        non=input('Press enter key to continue.')
                                    else:
                                        print('Sorry, Your Prop inventory is full. You cannot get the prop.')
                                        non=input('\nPress enter key to continue.')
                                elif pnum[num]==0 or pnum[num]==35: #Lottery Points
                                    print('You can buy lottery here!')
                                    if Cash[num]>=1000:
                                        while True:
                                            lotterycho=getchoice('Go out','Buy a lottery','See the lottery list')
                                            if lotterycho=='0':
                                                break
                                            elif lotterycho=='1':
                                                luckynum=-1
                                                print('\nA lottery will cost you $1000')
                                                while luckynum not in range(1,37):
                                                    try:
                                                        luckynum=int(input('\nPlease enter your lucky number: (1-36)\n'))
                                                    except ValueError:
                                                        print('\nError, please enter again.')
                                                    if luckynum not in range(1,37):
                                                        print('\nThe nuber you input should be in range (1-36).')
                                                if not Lottery.occupy[luckynum-1]:
                                                    print('You bought a lottery numbered %02d'%luckynum)
                                                    non=input('\nPress enter key to continue.')
                                                    Cash[num]-=1000
                                                    Lottery.bought(luckynum)
                                                    lotteries[num].append(luckynum)
                                                    break
                                                else:
                                                    print('Sorry, this number has been occupied.\nYou can choose another number.')
                                                    time.sleep(1.3)
                                                    continue
                                            elif lotterycho=='2':
                                                for i in range(6):
                                                    for j in range(1,7):
                                                        lnum=i*6+j
                                                        if Lottery.occupy[lnum-1]:
                                                            AorO='O'
                                                        else:
                                                            AorO='A'
                                                        print('%02d : %s'%(lnum,AorO),end='  ')
                                                    print()
                                                print('\n"A" means "Available",\n"O" means "Occupied"')
                                                non=input('\nPress enter key to continue.')
                                    else:
                                        print('Sorry, your money is not enough.')
                                        non=input('\nPress enter key to continue.')
                                                
                                elif pnum[num]==63 or pnum[num]==27: # News Points
                                    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                                    print('#################### TVB NEWS ###################')
                                    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
                                    non=input('Press enter to watch the News.\n')
                                    newskey=randint(1,6)
                                    if newskey==1:
                                        if Ground.count(max(Ground))>1:
                                            print(Newsdict[1]%'')
                                            print('No Player got the prize.')
                                            non=input('\nPress enter key to continue.')
                                        else:
                                            num1=Ground.index(max(Ground))
                                            print(Newsdict[1]%namelist[num1])
                                            Deposit[num1]+=5000
                                            non=input('\nPress enter key to continue.')
                                    elif newskey==2:
                                        if Ground.count(min(Ground))>1:
                                            print(Newsdict[2]%'')
                                            print('No Player got the subsidy.')
                                            non=input('\nPress enter key to continue.')
                                        else:
                                            num1=Ground.index(min(Ground))
                                            print(Newsdict[2]%namelist[num1])
                                            Deposit[num1]+=5000
                                            non=input('\nPress enter key to continue.')
                                    elif newskey==3:
                                        print(Newsdict[3])
                                        nDeposit=[]
                                        for i in range(pn):
                                            j=int(Deposit[i]*1.08)
                                            print('Player %s gained $%d'%(namelist[i],j-Deposit[i]))
                                            nDeposit.append(j)
                                        Deposit=nDeposit
                                        non=input('\nPress enter key to continue.')
                                    elif newskey==4:
                                        print(Newsdict[4])
                                        Stopstate=[True]*pn
                                        non=input('\nPress enter key to continue.')
                                    elif newskey==5:
                                        print(Newsdict[5])
                                        if houselevel==[0]*len(houselevel):
                                            print('\nNo Player has a house,\nso Players are not influenced.')
                                            non=input('\nPress enter key to continue.')
                                        else:
                                            pnum1=choice(houses)
                                            for i in range(len(place)):
                                                if pnum1 in place[i]:
                                                    street=Eng[i]
                                            print('The house is in %s.'%street)
                                            non=input('\nPress enter key to continue.')
                                            houselevel[pnum1]-=1
                                            Levelobj[pnum1][houselevel[pnum1]].undraw()
                                    elif newskey==6:
                                        print(Newsdict[6])
                                        nDeposit=[]
                                        for i in range(pn):
                                            j=int(Deposit[i]*0.9)
                                            print('Player %s lost $%d'%(namelist[i],Deposit[i]-j))
                                            nDeposit.append(j)
                                        Deposit=nDeposit
                                        non=input('\nPress enter key to continue.')
                                elif pnum[num]in houseposition:
                                    
                                ############################################# House Property System ##########################################
                                            
                                #################### Buy the Vacancy ####################

                                    if Vacancy[pnum[num]] is True:
                                        Cash,Vacancy,hpro,bSet=buyhouse(place,pnum,num,Eng,houseprice,bSet,color,Cash,Vacancy,hpro,houselevel,priceindex)
                                                                                            #From Line 677 [22]
                                ################ Stop ##################

                                    ################# Upgrade owned ground ###################
                                                           
                                    elif pnum[num] in hpro[num]:      #upgrade the house
                                        houselevel,Cash=upgradehouse(houselevel,pnum,num,pSet,Cash,houseprice,win,Levelobj)    #From Line 697 [23]

                                #################### End ####################
                                        
                            ##################### Toll System #######################
                                    
                                    else:
                                        Cash,Deposit,card=tollgiving(hpro,pnum,num,Hospital,houseprice,houselevel,Cash,Deposit,namelist,place,Prison,Hiberstate,card,Dream,priceindex)
                                        for i in range(pn):
                                            if Deposit[i]<=0 and Cash[i]<=0:
                                                print('Player %s has bankrupted...'%namelist[i])
                                                for i in lotteries[num]:
                                                    Lottery.debought(num)
                                                    assert Lottery.occupy[num-1]==False
                                                pn,Vacancy,Quitnum=Bankrupt(Vacancy,Quitnum,namelist,Cash,Deposit,Coupon,shapes,\
                                                 pnum,hpro,color,TBinfo,direction,Hospital,Prison,\
                                                 prop,card,TBnum,TBstate,Stopstate,Turtlenum,\
                                                 Namebook,Hiberstate,shapecholist,pn,num,lotteries,Dream,bSet)
                                                break
                                                                                            
                            elif Dream[num]>0:
                                for i in hpro:
                                    if pnum[num] in i:
                                        Cash,Deposit,card=tollgiving(hpro,pnum,num,\
                                                                     Hospital,houseprice,\
                                                                     houselevel,Cash,Deposit,\
                                                                     namelist,place,Prison,\
                                                                     Hiberstate,card,Dream,priceindex)
                                        non=input('Press enter key to continue.')
                                
                        break
                                ########################## end ###########################

                        ##################################### Quit the Game ###############################
                            
                    elif cho==5:
                        quitcho=input('Are you truly going to quit the game?(Y/N)')
                        if quitcho!='Y' and quitcho!='y':
                            continue
                        print('\nPlayer',i,'has quit the game.\n')
                        for i in lotteries[num]:
                            Lottery.debought(num)
                            assert Lottery.occupy[num-1]==False
                        pn,Vacancy,Quitnum=Bankrupt(Vacancy,Quitnum,namelist,Cash,Deposit,Coupon,shapes,\
                                     pnum,hpro,color,TBinfo,direction,Hospital,Prison,\
                                     prop,card,TBnum,TBstate,Stopstate,Turtlenum,\
                                     Namebook,Hiberstate,shapecholist,pn,num,lotteries,Dream,bSet)
                        print(namelist)
                        break   #renew
                    else:
                        continue
                                
     
                ####################################################################################
                    
                passway=[]  #re-emptify
                if not Load:
                    Wdiceused=False
                newnamelist=[] #re-emptify   It's very important!!!
                newpnum=[]
                oldnamelist=[] #re-emptify
                print('===========================================================================')
                if winner(namelist,pn):
                    gameover=True
                    break
            continue
        if gameover:
            break
        Quitnum=0
        if not Load:
            Timer.addaday()
    print('Thank you for playing this Game!')
    non=input('\nPress enter key to close the game window.')
            
main()
