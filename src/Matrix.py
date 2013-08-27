import functions
from numpy import array,zeros
from random import randint

class Matrix():
    Main_matrix=zeros((9,9),dtype=int)
    score=0
    next_colors=list()

    def __init__(self):
        self.Main_matrix=zeros((9,9),dtype=int)
        self.X1=0
        self.X2=0
        self.Y1=0
        self.Y2=0

        i=0
        self.Get_NextColors()
        while i!=3:
            m=randint(0,8)
            n=randint(0,8)
            color=randint(1,7)
            if(self.Main_matrix[m,n]==0):
                self.Main_matrix[m,n]=color
                i=i+1

    def Get_NextColors(self):
        self.next_colors=[randint(1,7) for i in range(3)]


    def Check(self):
        disapear_list=list()
        for i in range(9):
            li=[self.Main_matrix[i,n] for n in range(9)]
            START,END=Check_line(li)
            if END-START >0:
                self.score=self.score+(END-START+1)
                for s in range(END-START+1):
                    disapear_list.append([i,s+START,self.Main_matrix[i,s+START]])
                    self.Main_matrix[i,s+START]=0
#                print disapear_list

            lj=[self.Main_matrix[n,i] for n in range(9)]
            START,END=Check_line(lj)
            if END-START >0:
                self.score=self.score+(END-START+1)
                for s in range(END-START+1):
                    disapear_list.append([s+START,i,self.Main_matrix[s+START,i]])
                    self.Main_matrix[s+START,i]=0
#                return disapear_list

        for i in [0,1,2,3,4]:
            lm=[self.Main_matrix[i+m,m] for m in range(9-i)]
            START,END=Check_line(lm)
            if END-START>0:
                self.score=self.score+(END-START+1)
                for s in range(END-START+1):
                    disapear_list.append([i+s+START,s+START,self.Main_matrix[i+s+START,s+START]])
                    self.Main_matrix[i+s+START,s+START]=0
#                return disapear_list

            ln=[self.Main_matrix[m,i+m] for m in range(9-i)]
            START,END=Check_line(ln)
            if END-START>0:
                self.score=self.score+(END-START+1)
                for s in range(END-START+1):
                    disapear_list.append([s+START,i+s+START,self.Main_matrix[s+START,i+s+START]])
                    self.Main_matrix[s+START,i+s+START]=0
#                return disapear_list

            lp=[self.Main_matrix[8-m,i+m] for m in range(9-i)]
            START,END=Check_line(lp)
            if END-START>0:
                self.score=self.score+(END-START+1)
                for s in range(END-START+1):
                    disapear_list.append([8-(s+START),i+s+START,self.Main_matrix[8-(+s+START),i+s+START]])
                    self.Main_matrix[8-(s+START),i+s+START]=0
#                return disapear_list

        for i in [4,5,6,7,8]:
            lq=[self.Main_matrix[i-m,m] for m in range(i+1)]
            START,END=Check_line(lq)
            if END-START>0:
                self.score=self.score+(END-START+1)
                for s in range(END-START+1):
                    disapear_list.append([i-(s+START),s+START,self.Main_matrix[i-(s+START),s+START]])
                    self.Main_matrix[i-(s+START),s+START]=0
#                return disapear_list

        return disapear_list

    def update(self):
        i=0
        new_ball=list()
        while i!=3:
            m=randint(0,8)
            n=randint(0,8)
            color=self.next_colors[i]
            if(self.Main_matrix[m,n]==0):
                self.Main_matrix[m,n]=color
                new_ball.append([m,n,color])
 #               print m,n,color
                i=i+1
        self.Get_NextColors()
        return new_ball



    def move(self,x1,y1,x2,y2):
        trace=functions.FindPath(self.Main_matrix,x1,y1,x2,y2)
#        if trace!=False:
#            self.Main_matrix[x2,y2]=self.Main_matrix[x1,y1]
#            self.Main_matrix[x1,y1]=0
        return trace


    def get_space(self):
        number=0
        for i in range(9):
            for j in range(9):
                if self.Main_matrix[i,j]==0:
                    number=number+1
        return number


def Check_line(line_list):
    num=len(line_list)
    START=0
    END=0

    for i in range(num-4):
        if line_list[i]==line_list[i+4] and line_list[i]!=0:
            if line_list[i]==line_list[i+3]:
                if line_list[i]==line_list[i+2]:
                    if line_list[i]==line_list[i+1]:
                        START=i
                        END=i+4
                        if i+5 < num and line_list[i]==line_list[i+5]:
                            END=i+5
                            if i+6 < num and line_list[i]==line_list[i+6]:
                                END=i+6
                                if i+7 < num and line_list[i]==line_list[i+7]:
                                    END=i+7
                                    if i+8 < num and line_list[i]==line_list[i+8]:
                                        END=i+8
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
    return START,END


