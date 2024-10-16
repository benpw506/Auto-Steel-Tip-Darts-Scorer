import numpy as np

from Training.dataset.annotate import get_dart_scores

class Dart_Manager: #Processes the predictions from the YOLO model and updates the Dart objects accordingly.
    def __init__(self):
        self.darts = []
    
    def get_num_darts(self):
        return len(self.darts)

    def add_dart(self, dart):
        self.darts.append(dart)

    def get_darts(self):
        return self.darts
    
    def reset_darts(self):
        self.darts = []
    
    def update_darts(self, est_darts, accuracy, board, cfg, player, pm, app): 
        current_darts = self.get_darts()
        
        if not len(est_darts) == 0:
            if self.get_num_darts() == 0:
                dart = Dart(est_darts[0], 1, False)
                self.add_dart(dart)
            else :
                for est_dart in est_darts :
                    prev_dart_found = False
                    for cur_dart in current_darts : 
                        cur_xy = cur_dart.get_xy()
                        est_xy = est_dart

                        comp_xy = cur_xy - est_xy
                        comp_xy = np.abs(comp_xy)

                        if accuracy > comp_xy[0] and accuracy > comp_xy[1] :
                            cur_dart.set_frequency(1)
                            prev_dart_found = True
                            break
                    if not prev_dart_found: 
                        dart = Dart(est_dart, 1, False)
                        self.add_dart(dart)
        
        bust = player.get_bust()

        if not bust : 
            for dart in current_darts: 
                dart_frequency = dart.get_frequency()
                dart_active = dart.get_active()

                if not dart_active : 
                    if dart_frequency > 6:
                        if len(board.get_darts()) <= 3:
                            dart_xy = dart.get_xy()
                            cal_xy = board.get_cal_points()
                            dart.set_str_score(cal_xy, dart_xy, cfg)
                            board.add_dart_to_board(dart)
                            player.update_score(dart, board)
                            dart.set_active(True)
        
        num_darts_in_board = len(board.get_darts())
  

        if num_darts_in_board >= 1 : 
            if len(est_darts) == 0: 
                board.increment_timer()
            if len(est_darts) > 0:
                board.reset_timer()
            if board.get_timer() > 15: 
                self.reset_darts()
                board.reset_board()
                player.set_bust(False)
                app.update_GUI()
                pm.swap_players()


                    



        
#Represents a dart on the dartboard
class Dart:
    def __init__(self, xy, frequency, active): #
        self.xy = xy
        self.frequency = frequency
        self.active = active
        self.str_score = 0
        self.int_score = 0
    
    def get_xy (self) : 
        return self.xy
    
    def set_frequency(self, value) : 
        self.frequency += value

    def get_frequency(self):
        return self.frequency
    
    def get_active(self): 
        return self.active
    
    def set_active(self, value):
        self.active = value

    def get_str_score(self):
        return self.str_score
    
    def get_int_score(self): 
        return self.int_score
    
    def set_str_score(self, cal_xy, dart_xy, cfg): 
        xy = np.append(cal_xy, dart_xy)
        xy = xy.reshape((-1,2))
        score = get_dart_scores(xy, cfg)
        self.str_score = score
        self.set_int_score()

    def set_int_score(self):
        str_score = self.get_str_score()[0]
        int_score = 0

        try: 
            int_score = int(str_score)
        except ValueError: 
            if str_score == "DB" : 
                int_score = 50
            elif str_score == "B" :
                int_score = 25
            elif str_score[0] == "D" :
                int_score = int(str_score[1:]) * 2
            elif str_score[0] == "T" :
                int_score = int(str_score[1:]) * 3

        self.int_score = int_score
