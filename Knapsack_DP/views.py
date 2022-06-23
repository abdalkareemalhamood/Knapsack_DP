import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

class Item:
    def __init__(self, n = 0, v =0, w=0): #Constructor
        self.n = n
        self.v = v
        self.w = w

def cal(items,values,weights,limw):
    items = items.strip()
    items = items.split(" ")
    values = values.strip()
    values = values.split(" ")
    weights = weights.strip()
    weights = weights.split(" ")

    for i in range(0,len(items)):
        items[i] = int(items[i])

    for i in range(0,len(values)):
        values[i] = int(values[i])

    for i in range(0,len(weights)):
        weights[i] = int(weights[i])

    global a
    a=[]
    for i in range(0,len(items)): 
        a.append(Item(items[i],values[i],weights[i]))
    global N
    N = len(a)
    global b
    b = [[0 for i in range(0,limw+1)]for j in range(0,N+1)]

    c = [[0 for i in range(0,limw+1)]for j in range(0,N+1)]
    for i in range(1,N+1):
        for j in range(1,limw+1):
            w = a[i-1].w
            if(j-w<0):
                v1 = 0
            else:
                v1 = a[i-1].v + c[i-1][j-w]
            v2 = c[i-1][j]
            if (v1 > v2):
                c[i][j] = v1
                b[i][j] = j - w
            else:
                c[i][j] = v2
                b[i][j] = -1
    return c[i][j]; # c[n,limw]

def Prints(i, j):
    if (i == 0 or j == 0):
        return "";
    elif (b[i][j] == -1):
        return Prints(i - 1, j)
    else:
        return Prints(i - 1, b[i][j]) + str(a[i - 1].n) + ", "

def index(request):
    if request.method == 'GET' and 'items' in request.GET:
        items = request.GET.get('items')
        values = request.GET.get('values')
        weights = request.GET.get('weights')
        limW = int(request.GET.get('limW'))

        OptimalValue = cal(items,values,weights,limW)
        Solutions = Prints(N,limW)  

        return JsonResponse({
            'result': 'Dynamic Programming Knapsack Problem Solving: <br>' + 'The Optimal Solution is  ' + str(Solutions) + ' with Total Value: '+ str(OptimalValue) 
        },status=200,
        )

    return render(
        request,
        'Knapsack_DP.html'
    )
