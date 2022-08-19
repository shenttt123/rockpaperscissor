import itertools

num_of_pairs=3
a=[1,2,3]
b=[4,5,6]
c=[7,8,9]

rbox=[0] * num_of_pairs
pbox=[0] * num_of_pairs
sbox=[0] * num_of_pairs



for i in range(num_of_pairs):
    rbox[i] = 1
    pbox[i] = 2
    sbox[i] = 3
all = rbox+pbox+sbox
print(all)

def compare(a,b):
    print(a,b)

for a, b in itertools.combinations(all, 2):
    compare(a, b)
