class Zelle:
    def __init__(self,x,y):
        self.x=x
        self.y=y

#3*3 matrix[0][0]
N = 3
matrix = []
for j in range(N):
    matrix.append([])
    print matrix
    for i in range(N):
        matrix[j].append(Zelle(i,j))


print matrix
