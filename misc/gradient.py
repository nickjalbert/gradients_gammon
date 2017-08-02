# Toy backprop computation example
# f(x,y) = (x + sig(y)) / (sig(x) + (x+y)**2)
# http://cs231n.github.io/optimization-2/
import math

x = 3
y = 5 

sigy = 1.0 / (1 + math.exp(-1 * y)
num = x + sigy
sigx = 1.0 / (1 + math.exp(-1 * x))
xplusy = x + y
xplusy2 = xplusy**2
denom = sigx + xplusy2
invdenom = 1 / denom
f = num * invdenom


dnum = invdenom
dindvdenom = num
ddenom = -1/((denom)**2) * dinvdenom
dsigx = 1 * ddenom
dxplusy2 = 1 * ddenom
dxplusy = 2*xplusy * dxplusy2
dx = 1 * dxplusy
dy = 1 * dxplusy
dx += sigx * (1-sigx) * dsigx
dx += 1 * dnum
dsigy = 1 * dnum
dy +=  (sigy)*(1-sigy)*dsigy

