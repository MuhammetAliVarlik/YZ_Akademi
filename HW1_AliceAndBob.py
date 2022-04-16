alice = list(map(int, input().split()))  # make a list of entered inputs
bob = list(map(int, input().split()))  # make a list of entered inputs
iterator = 0  # iterator of recursive function
points = [0, 0]  # comparison score

"""
recursive comparison function 
a= alice's 
b= bob's 
"""


def triplet(a, b, n):
    if n != len(a) or n != len(b):
        if a[n] > b[n]:
            points[0] += 1  # alice gets a point
        elif a[n] < b[n]:
            points[1] += 1  # bob gets a point
        triplet(a, b, n + 1)


triplet(alice, bob, iterator)  # run triplet function
print(points[0], points[1])  # print the result
