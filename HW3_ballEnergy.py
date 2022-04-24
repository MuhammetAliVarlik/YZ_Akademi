"""
Quick explanation

Let our starting energy be E0 and 3 legos on the number line.
Let the heights of the legos be h0 h1 h2, respectively.

Let's assume that E0 satisfies all the conditions.
If E0>h0 when it comes to the first obstacle, then energy E1 in the next step:
E1 = E0 + (E0 - h0 )= 2E0-h0
If E0<h0 then energy E1 in the next step:
E1 = E0 - (h0-E0 )= 2E0-h0
In both cases, the new energy formula is E(n)=2*E(n-1)+h(n-1)
If we keep on experimenting
E2=2E1-h1
E3=2E2-h2

The energy should not fall below 0. In this case
E0>=0
E1>=0
E2>=0
......
We can say E(n)>=0                                              (**1**)

E1=2E0-h0
E2=2E1-h1 //If we write 2E0-h0 instead of E1
E2=2(2E0-h0)-h1=4E0-2h0-h1
E3=2(2(2E0-h0)-h1)-h2=8E0-4h0-2h1-h2
If we formulate this
E(n)=(2^(n)*E0)-(2^(n-1)h0+2^(n-2)h1+.....+2^(n-n)h(n-1) )      (**2**)

from (**1**) and (**2**)

E(n)>=0
(2^(n)*E0)-(2^(n-1)h0+2^(n-2)h1+.....+2^(n-n)h(n-1)) >=0
(2^(n)*E0)>=(2^(n-1)h0+2^(n-2)h1+.....+2^(n-n)h(n-1))
E0>=(2^(n-1)h0+2^(n-2)h1+.....+2^(n-n)h(n-1))/(2^(n))           (**3**)

This formula guarantees that the energy will not go below 0 at any time n.

Proof:
E2=4E0-2h0-h1 ===> E0>=h0/2+h1/4 if this condition is met
E1=2E0-h0>=0 ===> E0>=h0/2 this condition must also be met
because
h0/2+h1/4>h0/2 (Height cannot be negative)

So we just need to calculate the nth value

E0 = (2^(n-1)h0+2^(n-2)h1+.....+2^(n-n)h(n-1))   /  (2^(n)) ===> total/divider  (**4**)
"""


# ceil function to round up fractional digits
def ceil(e):
    if (e - int(e)) != 0:
        return int(e) + 1


# minEnergyCalc function to round up fractional digits
def minEnergyCalc(arr, k):
    if k < 1 or k > 100000:
        print("Error,The lego numbers value entered must be between 1 and 100000!!")
        return 0
    if k < len(arr) or len(arr) < k:
        print("Error,The number of elements of the length array must be equal to the number of elements entered!!")
        return 0
    # Variables mentioned in (**4**).
    total = 0
    divider = pow(2, k)
    # Functionalized version of the formula given in (**3**).
    for i in range(0, k):
        if arr[i] < 1 or arr[i] > 100000:
            print("Error,The lego height value entered must be between 1 and 100000!!")
            return 0
        total = total + (arr[i] * pow(2, k - (1 + i)))
    print(ceil(total / divider))
    return ceil(total / divider)


# The output result may be fractional. Since we work with integers, we round the number to the larger integer with
# the ceil function.

# ----------------------------------------------------------------------------------------------------------------------
try:
    # number of elements
    n = int(input("Please enter the lego numbers on the number line from 1 to 100000:"))

    # Below line read inputs from user using map() function
    heights = list(
        map(int, input("Please enter the lego heights on the number line from 1 to 100000.The number of lego "
                       "heights must be equal to the value you entered in the first entry:").strip().split(

        )))

    # The minEnergyCalc function takes two values: the lego lengths of type list and the number of elements of type
    # integer

    minEnergyCalc(heights, n)
except ValueError:
    print("Error! The operation cannot be performed.All entered values must be integers")
