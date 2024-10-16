
from Training.predict import bboxes_to_xy
from Training.dataset.annotate import draw
import numpy as np
import customtkinter as ctk
import cv2 
import time as t

def crop_frame(img, bbox=None, crop_info=(0, 0, 0), crop_pad=1.1) :
    if bbox is None:
        x, y, r = crop_info
        r = int(r * crop_pad)
        bbox = [y-r, y+r, x-r, x+r]
    crop = img[bbox[0]:bbox[1], bbox[2]:bbox[3]]
    return crop, bbox

class App(ctk.CTk):
    def __init__(self, board, pm, dm, cap, bbox, yolo, cfg):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.board = board
        self.pm = pm
        self.dm = dm
        self.cap = cap
        self.bbox = bbox
        self.yolo = yolo
        self.cfg = cfg 

        self.geometry("1110x600")
        self.minsize(400, 400)
        self.title("Darts Scorer")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master_frame = MasterFrame(master=self)
        self.master_frame.grid(row=0, column=0, sticky="NEW")
        self.update()

    def update_GUI(self): #updates the GUI based on the state of the darts and players objects
        players = self.pm.get_players()
        darts = self.board.get_darts()


        for p in players:
            if "1" in p.get_name():
                frame = self.master_frame.player_frame_1
            else:
                frame = self.master_frame.player_frame_2
                
            p.set_frame(frame)
            frame.player_label.configure(text=p.get_name())
            frame.player_score.configure(text=p.get_score())

            if p.get_active() : 

                bust = p.get_bust()
                won = p.get_won()
                active_player_frame = p.get_frame()

                if bust : 
                    dart_frame_color = "#c4000a"
                else : 
                    dart_frame_color = "#009933"

                if won :
                    dart_frame_color = "#D4AF37"
                    active_player_frame.configure(fg_color="#FFD700")
                else :
                    active_player_frame.configure(fg_color="white")


                dart_1 = darts[:1]
                dart_2 = darts[1:2]
                dart_3 = darts[2:]

                if len(dart_1) > 0: 
                    dart_score = dart_1[0].get_str_score()
                    active_player_frame.player_dart_1_label_num.configure(text=dart_score)
                    active_player_frame.player_dart_1_frame.configure(fg_color=dart_frame_color)
                else : 
                    active_player_frame.player_dart_1_label_num.configure(text="   ")
                    active_player_frame.player_dart_1_frame.configure(fg_color="#3d3d3d")

                if len(dart_2) > 0: 
                    dart_score = dart_2[0].get_str_score()
                    active_player_frame.player_dart_2_label_num.configure(text=dart_score)
                    active_player_frame.player_dart_2_frame.configure(fg_color=dart_frame_color)
                else : 
                    active_player_frame.player_dart_2_label_num.configure(text="   ")
                    active_player_frame.player_dart_2_frame.configure(fg_color="#3d3d3d")

                if len(dart_3) > 0:    
                    dart_score = dart_3[0].get_str_score()
                    active_player_frame.player_dart_3_label_num.configure(text=dart_score)
                    active_player_frame.player_dart_3_frame.configure(fg_color=dart_frame_color)
                else : 
                    active_player_frame.player_dart_3_label_num.configure(text="   ")
                    active_player_frame.player_dart_3_frame.configure(fg_color="#3d3d3d")
                

                 

            else : 
                p.get_frame().configure(fg_color="black")




    def update(self):
        
        board = self.board
        pm = self.pm
        dm = self.dm
        cap = self.cap
        bbox = self.bbox
        yolo = self.yolo
        cfg = self.cfg

        ret, frame = cap.read()

        cf, _ = crop_frame(frame, bbox)
        cf = cv2.cvtColor(cf, cv2.COLOR_BGR2RGB)
        cf = cv2.resize(cf, (800,800))

        bboxes = yolo.predict(cf)
        preds = bboxes_to_xy(bboxes, 3)

        xy = preds
        xy = xy[xy[:, -1] == 1]
        xy = xy[:, :2]
        xy = np.array(xy)

        est_cal = xy[:4, :]
        est_darts = xy[4:, :]

        if board.get_cal_points() is None: 
            board.set_cal_points(est_cal)
        else: 
            board.check_cal(board.get_cal_points(), est_cal)

        players = pm.get_players()

        for p in players: 
            if p.get_active(): 
                player = p
    
        dm.update_darts(est_darts, 0.01, board, cfg, player, pm, self)
        self.update_GUI()

        cf = cv2.cvtColor(cf, cv2.COLOR_BGR2RGB)
        
        cv2.imshow("test", cf)
        cv2.waitKey(10)

        self.schedule_update()

    def schedule_update(self):
        self.after(20, self.update)


class MasterFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, bg_color="black", fg_color="#4f4f4f")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.player_frame_1 = PlayerFrame(master=self, bg_color="black", fg_color="black")
        self.player_frame_1.grid(row=0, column=0, padx=20, pady=50, sticky="NEW")
        
        self.player_frame_2 = PlayerFrame(master=self, bg_color="black", fg_color="black")
        self.player_frame_2.grid(row=0, column=1, padx=20, pady=50, sticky="NEW")


class PlayerFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        
        self.player_frame_val = ctk.CTkFrame(master=self, bg_color="#303030", fg_color="#303030")
        self.player_frame_val.grid(row=0, column=0, sticky="NEW", padx=10, pady=10)
        self.player_frame_val.columnconfigure(0, weight=1)
        
        self.player_title_font = ctk.CTkFont(family="Helvetica", size=55, weight="bold", slant="roman", underline=True, overstrike=False)
        self.player_dart_num_font = ctk.CTkFont(family="Helvetica", size=55, weight="bold", slant="roman", underline=False, overstrike=False)
        self.player_score_font = ctk.CTkFont(family="Helvetica", size=100, weight="bold", slant="roman", underline=False,  overstrike=False)
        
        self.player_label = ctk.CTkLabel(master=self.player_frame_val, text="Player", fg_color="transparent", font=self.player_title_font)
        self.player_label.grid(row=0, column=0)
        
        self.player_score = ctk.CTkLabel(master=self.player_frame_val, text="501", fg_color="transparent", font=self.player_score_font)
        self.player_score.grid(row=1, column=0, pady=40, padx=10)
        
        self.player_darts = ctk.CTkFrame(master=self.player_frame_val, bg_color="#1c1c1c", fg_color="#1c1c1c")
        self.player_darts.grid(row=2, column=0, pady=20, padx=20, sticky="ew")
        
        self.player_dart_1_frame = ctk.CTkFrame(master=self.player_darts, bg_color="black", fg_color="#3d3d3d")
        self.player_dart_1_frame.grid(row=0, column=0, padx=15, pady=15, sticky="NSEW")

        self.player_dart_2_frame = ctk.CTkFrame(master=self.player_darts, bg_color="black", fg_color="#3d3d3d")
        self.player_dart_2_frame.grid(row=0, column=1, padx=15)

        self.player_dart_3_frame = ctk.CTkFrame(master=self.player_darts, bg_color="black", fg_color="#3d3d3d")
        self.player_dart_3_frame.grid(row=0, column=2, padx=15)

        self.player_dart_1_label_num  = ctk.CTkLabel(master=self.player_dart_1_frame, text="", fg_color="transparent", font=self.player_dart_num_font, width=100)
        self.player_dart_1_label_num.grid(row=0, column=0, padx=10, pady=20)

        self.player_dart_2_label_num  = ctk.CTkLabel(master=self.player_dart_2_frame, text="", fg_color="transparent", font=self.player_dart_num_font, width=100)
        self.player_dart_2_label_num.grid(row=0, column=0, padx=10, pady=20)

        self.player_dart_3_label_num  = ctk.CTkLabel(master=self.player_dart_3_frame, text="", fg_color="transparent", font=self.player_dart_num_font, width=100)
        self.player_dart_3_label_num.grid(row=0, column=0, padx=10, pady=20)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark") 
    ctk.set_default_color_theme("green") 
    app = App()

    app.master_frame.player_frame_2.player_label.configure(fg_color="white")

    app.mainloop()
