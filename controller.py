import control
import numpy as np

def calcLQR(mass=10,length=0.2*np.sqrt(2),Q=np.diag([5, 10]),R=np.diag([100])):
    M = mass*(length**2)
    
    A = np.array([[0, 1],
                 [mass*10.0*length/M, 0]])
    
    B = np.array([[0],
                  [1/M]])
        
    K, _, _ = control.lqr(A, B, Q, R)
    print(K)
    print(K.squeeze())
    return K, K.squeeze()

def calcLQRs(A,B,Q,R):
    K, _, _ = control.lqr(A, B, Q, R)
    print(K)
    print(K.squeeze())
    return K, K.squeeze()

def nonlinear(u):
    pass

def myController():
    pass
    