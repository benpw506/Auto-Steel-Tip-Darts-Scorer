import numpy as np

# A class to track the number to track the darts currently in the dart board

class DartBoard : 
    def __init__(self, cal_points): 
        self.cal_points = cal_points # A list of the coordinates of the 4 quandrants of the dartboard
        self.darts = [] # A list of Dart objects currently in the board
        self.timer = 0 # An intger used to detect when a player removes their darts 

    def get_cal_points(self) :
        return self.cal_points
    
    def set_cal_points(self, value) : 
        self.cal_points = value

    #Used to constantly update the callibration points on the board. This allows for darts to still be accuratley detected when the board moves on impact and when a dart occuldes a calibration point.
    def check_cal(self, prev, new) :  
        threshold = 0.005 # Error threshold between predictions
        temp = np.array([])

        if new.shape[0] < 4: 
            self.set_cal_points(prev)
        else : 
            for i in range(4):
                comp = new[i] - prev[i]
                temp = np.append(temp, comp)
                
            temp = np.abs(temp)

            for i in range(len(temp)) : 
                if threshold < temp[i] : 
                    self.set_cal_points(prev)

                else: 
                    self.set_cal_points(new)
    
    def add_dart_to_board(self, dart):
        self.darts.append(dart)
    
    def get_darts(self) :
        return self.darts
    
    def get_timer(self) : 
        return self.timer
    
    def increment_timer(self): 
        self.timer += 1

    def reset_timer(self):
        self.timer = 0

    def reset_board(self) : 
        self.darts = []
    

    
  
