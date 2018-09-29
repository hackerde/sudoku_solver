class grid:
    def __init__(self, X, Y):
        #creating a grid
        self.state=0                                    #filled=1 and empty=0
        self.value=' '                                  #the value that the grid holda
        self.x=X                                        #x-coordinate of the grid in the board
        self.y=Y                                        #y-coordinate of the grid in the board
        self.pvalues=[1,2,3,4,5,6,7,8,9]                #list of possible values for that particular grid
    def fill(self, k):
        #filling a grid
        self.value=k                                    #set its value
        self.state=1                                    #change state to filled
        self.pvalues=[]                                 #empty possible values list
    def remvalue(self, r):
        #remove a value from the list of possible values of a grid
        self.pvalues.remove(r)

class sudoku:
    def __init__(self, brd=[]):
        #create a sudoku board which is a matrix
        self.state=0                                    #filled=1 and empty=0
        self.board=brd                                  #initialize with board if supplied in argument
    def statechecker(self):
        #check if the sudoku board is filled or not
        flag=1
        for i in self.board:
            for j in i:
                if j.state==0:
                    flag=0
                    break
            if flag==0:
                break
        else:
            self.state=1
        return self.state
    def display(self):
        #print the board
        b=self.board[::-1]                              #the board is stored with the bottom most row as the first row to make the board like a coordinate
        for i in b:
            for j in i:
                print (j.value, end=' ')
            print()
        print()
    def correct(self):
        for i in self.board:
            for j in i:
                if j.value==' ' and j.pvalues==[]:
                    return 0
        return 1

def newboard():
    S=sudoku()
    T=[]
    temp = open('sud.txt', 'r')                                 #using temporary input from file
    for i in range(9):
        row=[]
        f=list(temp.readline().rstrip())                        #input line
        for j in range(9):
            G=grid(j,i)
            if f[j]=='0':
                pass
            else:
                G.value=int(f[j])
                G.state=1
            row.append(G)
        T.append(row)
    S.board=T
    return S

def box(sud):
    box1=[sud.board[i][j] for i in range(3) for j in range(3)]
    box2=[sud.board[i][j] for i in range(3) for j in range(3,6)]
    box3=[sud.board[i][j] for i in range(3) for j in range(6,9)]
    box4=[sud.board[i][j] for i in range(3,6) for j in range(3)]
    box5=[sud.board[i][j] for i in range(3,6) for j in range(3,6)]
    box6=[sud.board[i][j] for i in range(3,6) for j in range(6,9)]
    box7=[sud.board[i][j] for i in range(6,9) for j in range(3)]
    box8=[sud.board[i][j] for i in range(6,9) for j in range(3,6)]
    box9=[sud.board[i][j] for i in range(6,9) for j in range(6,9)]
    return box1,box2,box3,box4,box5,box6,box7,box8,box9

def boxstate(b):
    flag=1
    for x in b:
        if x.state==0:
            flag=0
            break
    return flag

def showpv(S):
    for i in S.board:
        for j in i:
            print ('(', (j.x)+1, ',', (j.y)+1, ') - ', j.pvalues)
        print()

def mingrid(sud):
    mini=sud.board[0][0]
    for i in sud.board:
        for j in i:
            if (j.state==0 and len(j.pvalues)<len(mini.pvalues)) or (mini.state==1):
                mini=j
    return mini

def process1(sud, b):
    '''Process 1: Take a grid G. Make a list of values of the filled in grids which are either in the same row, column or box as G.
       Delete all those values from the pvalues of G.'''
    flag=0
    for i in sud.board:
        for j in i:
            if j.state==1:
                if j.pvalues!=[]:
                    j.pvalues=[]
                    flag=1
                continue
            elif len(j.pvalues)==1:                     #Check if any grid can be immediately filled in (one pvalue)
                j.fill(j.pvalues[0])
                flag=1
                continue
            else:
                p=[g.value for k in sud.board for g in k if g.state==1 and (j.x==g.x or j.y==g.y)]
                if j in b[0]:
                    p+=[g.value for g in b[0] if g.state==1]
                elif j in b[1]:
                    p+=[g.value for g in b[1] if g.state==1]
                elif j in b[2]:
                    p+=[g.value for g in b[2] if g.state==1]
                elif j in b[3]:
                    p+=[g.value for g in b[3] if g.state==1]
                elif j in b[4]:
                    p+=[g.value for g in b[4] if g.state==1]
                elif j in b[5]:
                    p+=[g.value for g in b[5] if g.state==1]
                elif j in b[6]:
                    p+=[g.value for g in b[6] if g.state==1]
                elif j in b[7]:
                    p+=[g.value for g in b[7] if g.state==1]
                else:
                    p+=[g.value for g in b[8] if g.state==1]
            pv=[]
            for v in j.pvalues:
                if v in p:
                    flag=1
                    continue
                else:
                    pv.append(v)
            j.pvalues=pv
    return flag
                
def process2(sud, b):
    '''Process 2: Take a grid G. Make a list L of the pvalues of the grid which are either in the same row, column or box as G.
       If there is a pvalue in G which is not in L, then fill G with that value.'''
    flag=0
    for i in sud.board:
        for j in i:
            if j.state==1:
                if j.pvalues!=[]:
                    j.pvalues=[]
                    flag=1
                continue
            elif len(j.pvalues)==1:                     #Check if any grid can be immediately filled in (one pvalue)
                j.fill(j.pvalues[0])
                flag=1
                continue
            else:
                r=[g for k in sud.board for g in k if g.y==j.y and not(g is j)]
                c=[g for k in sud.board for g in k if g.x==j.x and not(g is j)]
                if j in b[0]:
                    p=[g for g in b[0] if not(g is j)]
                elif j in b[1]:
                    p=[g for g in b[1] if not(g is j)]
                elif j in b[2]:
                    p=[g for g in b[2] if not(g is j)]
                elif j in b[3]:
                    p=[g for g in b[3] if not(g is j)]
                elif j in b[4]:
                    p=[g for g in b[4] if not(g is j)]
                elif j in b[5]:
                    p=[g for g in b[5] if not(g is j)]
                elif j in b[6]:
                    p=[g for g in b[6] if not(g is j)]
                elif j in b[7]:
                    p=[g for g in b[7] if not(g is j)]
                else:
                    p=[g for g in b[8] if not(g is j)]
                r1=[g.value for g in r if g.state==1]+[x for g in r if g.state==0 for x in g.pvalues]
                c1=[g.value for g in c if g.state==1]+[x for g in c if g.state==0 for x in g.pvalues]
                p1=[g.value for g in p if g.state==1]+[x for g in p if g.state==0 for x in g.pvalues]
                for v in j.pvalues:
                    if (v not in r1) or (v not in c1) or (v not in p1):
                        j.fill(v)
                        j.state=1
                        flag=1
                        break
                    
    return flag

def process3(sud, b):
    '''Process 3: Take a box. Check if a particular value P occurs in a particular row or column of the box.
       If yes, delete P from the pvalues of all the grids outside the box in the same row or column.'''
    flag=0
    for box in b:
        if boxstate(box)==1:
            continue
        E=[grid1 for grid1 in box if grid1.state==0]
        F=[grid2.value for grid2 in box if grid2.state==1]
        for value in range(1,10):
            if value in F:
                continue
            xvalues=[g1.x for g1 in E if value in g1.pvalues]
            yvalues=[g2.y for g2 in E if value in g2.pvalues]
            col=[c-xvalues[0] for c in xvalues]
            row=[r-yvalues[0] for r in yvalues]
            if not(any(col)):
                reqgridsx=[j for i in sud.board for j in i if j.x==xvalues[0] and (value in j.pvalues) and (j not in box)]
                if reqgridsx==[]:
                    continue
                else:
                    for rgx in reqgridsx:
                        rgx.pvalues.remove(value)
                        flag=1
            if not(any(row)):
                reqgridsy=[b for a in sud.board for b in a if b.y==yvalues[0] and (value in b.pvalues) and (b not in box)]
                if reqgridsy==[]:
                    continue
                else:
                    for rgy in reqgridsy:
                        rgy.pvalues.remove(value)
                        flag=1
    return flag
    

def process(S, B):
	flag1=process1(S, B)
	flag2=process2(S, B)
	flag3=process3(S, B)
	while (flag1+flag2+flag3 != 0):
		flag1=process1(S, B)
		flag2=process2(S, B)
		flag3=process3(S, B)

	return flag1, flag2, flag3

tracker=[]
S=newboard()
boxes=box(S)
S.display()
solved = process(S, boxes)
print ('\n------------------------------------------\n')
S.display()
