import numpy as np

class Kalman:

    def __init__(self, property_arr):
        #set up necessary matricies
        self.x_noise = 1.
        self.y_noise = 1.
        self.dt = 1
        self.u = .01
        #position uncertainty
        self.initial_pos_uncertainty = np.matrix([[self.dt^4/4, 0, self.dt^3/2, 0], [0, self.dt^4/4, 0, self.dt^3/2], [self.dt^3/2, 0, self.dt^2, 0],  [0, self.dt^3/2, 0, self.dt^2]])
        # measurement uncertainty
        self.R =  np.matrix([[self.x_noise, 0.], [0., self.y_noise]])
        # next state function
        self.F =  np.matrix([[1., 0., self.dt, 0.], [0., 1., 0., self.dt], [0., 0., 1., 0.], [0., 0., 0., 1.]])
        # external motion (ie acceleration)
        self.G = np.matrix([[self.dt^2/2], [self.dt^2/2], [self.dt], [self.dt]])
        # measurement function
        self.H =  np.matrix([[1., 0., 0., 0.], [0., 1., 0., 0.]])
        #identity matrix
        dim = len(property_arr[0])
        self.I = np.eye(dim, dim)

        #store our property array
        self.property_arr = property_arr

    def filter(self, cutoff_idx=None, number_frames_to_predict=60):
        if not cutoff_idx: cutoff_idx = len(self.property_arr) - number_frames_to_predict
        predict_arr= []
        P = self.initial_pos_uncertainty
        x = self.property_arr[0]
        for Z in self.property_arr[:cutoff_idx]:
            x, P = self.predict(x, P)
            x, P = self.update(x, P, Z)
            predict_arr.append([x.item(0,0), x.item(0,1)])
        predict_arr = predict_arr[-10:]
        for n in range(number_frames_to_predict):
            x, P = self.predict(x, P)
            predict_arr.append([x.item(0,0), x.item(0,1)])
        return predict_arr

    def predict(self, x, P):
        x = self.F.dot(x) + self.G.dot(self.u)
        P = self.F.dot(P).dot(self.F.transpose()) + self.G
        return x, P

    def update(self, x, P, Z):
        y = Z.transpose() - self.H.dot(x)
        S = self.H.dot(P).dot(self.H.transpose()) + self.R
        K = P.dot(self.H.transpose()).dot(np.linalg.inv(S))
        x = x + K.dot(y)
        P = (self.I - K.dot(self.H)).dot(P)
        return x, P
