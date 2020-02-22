

import math

########################
# Question 1
########################

def repeat(s1,n,s2):
    fx=("_"+n*(s1+s2)+"_")
    return fx

#######################
# Question 2
#######################

def is_prime(n):
     for i in range(2,n):
          if (n%i)==0:
               return False
          else:
               return True


#######################
# Question 3
#######################
'''int-->(str)
'''
def points(x1,y1,x2,y2):

     d=math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     s=(y2-y1)/(x2-x1)
     print('The slope is',s,'and the distance is',d)


#######################
# Question 4
#######################

def month_apart(m1,d1,m2,d2):
     m=['None','January','February','March','April','May','June','July','August','September','October','November','December']
     if m1<m2<m1+2 and d1>d2:
          print('should return False',',','because', m[m1] ,d1,'isn\'t at least a month before', m[m2],d2)
     if m1>=m2:
          print('should return False',',','because', m[m1] ,d1,'isn\'t at least a month before', m[m2],d2)
     elif m1<m2:
          print('should return True',',','because', m[m1] ,d1,'is at least a month before', m[m2],d2)
#######################
# Question 5
#######################
     
def reverse_int(num):
     se = 0
     while num > 0:
          se = (10*se) + num%10
          num //= 10
     
     return se

#######################
# Question 6
#######################
'''(str)-->int--->(str)
'''
def vowelCount(sent):
     cont1=0
     cont2=0
     cont3=0
     cont4=0
     cont5=0
     vowl1='Aa'
     vowl2='Ee'
     vowl3='Ii'
     vowl4='Oo'
     vowl5='Uu'
     for l in sent:
          if l in vowl1:
               cont1+=1
          if l in vowl2:
               cont2+=1
          if l in vowl3:
               cont3+=1
          if l in vowl4:
               cont4+=1
          if l in vowl5:
               cont5+=1
     print ('a, e , i, o, and u appear',',',' respectively',',', cont1,',', cont2,',',cont3,',', cont4,',', cont5,' times')


#######################
# Question 7
#######################

def allTheSame(x, y, z):
     if y == x and x == z:
        return True
     else:
        return False
def allDifferent(x, y, z):
     if x != y and x != z and y != z:
          return True
     else:
          return False

def sortedFunc(x, y, z):
     if x > z and z > y:
        return True
     if x > y and y > z:
        return True
     if z > x and x > x:
        return True
     if y > x and x > z:
        return True
     if y > z and z > x:
        return True
     elif z > y and y > x:
        return True
     else:
        return False

#######################
# Question 8
#######################

def leap(y):
     if ((y % 4 == 0 and y % 100 != 0) or (y % 400 == 0 and y % 3200 != 0)):
          return True
     else:
          return False


#######################
# Question 9
#######################
'''(str)-->int
'''
def letter2number(g):
    if g == 'A+':
        return 4.3
    if g == 'A':
        return 4.0
    if g == 'A-':
        return 3.7
    if g == 'B+':
        return 3.3
    if g == 'B':
        return 3.0
    if g == 'B-':
        return 2.7
    if g == 'C+':
        return 2.3
    if g == 'C':
        return 2.0
    if g == 'C-':
        return 1.7
    if g== 'D+':
        return 1.3
    elif g == 'D':
        return 1.0
    elif g== 'D-':
        return 0.7
    elif g == 'F':
        return 0



#######################
# Question 11
#######################

def is_nneg_float(numb):
     numb=float(numb)
     if numb>0:
          return True
     if numb in 'qwertyuiopasdefrgthjklzxcvbnm':
          return False
     else:
          return False
     


#######################
# Question 12
#######################
'''(str)-->int
'''
def rps(a,b):
     if a ==b:
       return 0
     if a=="R" and b=="P":
          return 1
     if a=="R" and b=="S":
          return -1
     if a=="P" and b=="R":
          return-1
     if a=="P" and b=="S":
          return 1
     if a=="S" and b=="R":
          return 1
     if a=="S" and b=="P":
          return -1

#######################
# Question 13
#######################

def alogical(number):
     resu= 0
     while(number>1):
          number = number/2
          resu = resu + 1
     return resu



#######################
# Question 14
#######################
'''int-->int
'''
def count_even_digits(n, legh):
     cout = 0
     for i in range(0,legh):
          digt = n % 10
          n = n // 10
          if (digt % 2 == 0):
               cout += 1
     return cout

