import numpy as np
import matplotlib.pyplot as plt

# points are in the format (t, (x, y))

# numerically computes int_{0}^1 e^{k2\pi it} f(t)dt

def fint(pts, k):
  ret = 0
  for i in range(len(pts) - 1):
    t = pts[i][0]
    delta_t = pts[i + 1][0] - pts[i][0]

    pt1 = pts[i][1][0] + 1j * pts[i][1][1]
    pt2 = pts[i + 1][1][0] + 1j * pts[i + 1][1][1]

    ret += (delta_t) * (np.exp(-2 * np.pi * 1j * k * t) * pt1 + (np.exp(-2 * np.pi * 1j * k * (t + 1))) * pt2) / 2
    #ret += (delta_t) * np.exp(-2 * np.pi * 1j * k * t) * pt1
  return ret

def ft(pts, m):
  with open("ft", "w") as f:
    for k in range(-m, m + 1):
      c_k = fint(pts, k)
      #print(f"{np.real(c_k):.3f}, {np.imag(c_k):.3f}")
      f.write(f"{np.real(c_k):.3f}, {np.imag(c_k):.3f}\n")
      #f.write("")

def ft2(pts, m):
  coeffs = []
  for k in range(-m, m + 1):
    c_k = fint(pts, k)
    print(f"{np.real(c_k):.3f}, {np.imag(c_k):.3f}")
    coeffs.append(fint(pts, k))
  return coeffs

def evalu(coeffs, m, t):
  ret = 0
  for k in range(-m, m + 1):
    ret += np.exp(2 * np.pi * 1j * k * t) * coeffs[k + m]
    print(np.exp(2 * np.pi * 1j * k * t))
  return ret

def trace(coeffs, m):
  x = []
  y = []
  for t in np.linspace(0, 1, 100):
    val = evalu(coeffs, m, t)
    x.append(np.real(val))
    y.append(np.imag(val))
    if len(x) > 1:
      plt.plot([x[-1],x[-2]], [y[-1],y[-2]])
  plt.show()

#ft([(0,(-2,-2)), (0.25, (2,-2)), (0.5, (2,2)), (0.75, (-2, 2)), (1, (-2, -2))], 3)
#coeffs = ft2([(0,(0,0)), (0.25,(1,0)), (0.5,(0,0)), (0.75,(-1,0)),(1,(0,0))], 5)
coeffs = ft2([(0,(-2,-2)), (0.125, (-2,0)), (0.25,(-2,2)), (0.375,(0,2)), (0.5,(2,2)), (0.625, (2,0)), (0.75,(2,-2)),(0.875,(0,-2)),(1,(-2,-2))], 4)
#print(coeffs)
#print(evalu(coeffs, 5, 0.25))
trace(coeffs, 4)
