class PlayerManager: #Constucts an array of two player objects
    def __init__(self): 
        self.players = []
        self.construct_players()
    
    def add_player(self, player):
        self.players.append(player)

    def get_players(self):
        return self.players
    
    def construct_players(self) :
        player1 = Player("Player 1", True)
        self.add_player(player1)

        player2 = Player("Player 2", False)
        self.add_player(player2)

        player1.set_active(True)
    
    def swap_players(self):
        players = self.players

        for p in players: 
            p.set_active(not p.get_active)



    

class Player:
    def __init__(self, name, active) : #Represents a player, keeping track of their score, whether they have bust or won the game and whether it is there turn to throw. 
        self.name = name
        self.active = active
        self.bust = False
        self.won = False
        self.score = 121
        self.frame = None


    def update_score(self, new_dart, board): 
        dart_score = new_dart.get_int_score()
        player_score = self.score
        darts = board.get_darts()

        if ((player_score - dart_score) < 0) or ((player_score - dart_score) == 1): 
            if len(darts) > 1 :
                for dart in darts[:-1] : 
                    dart_score = dart.get_int_score()
                    self.score += dart_score
                    self.bust = True
            else: 
                self.bust = True
        elif (player_score - dart_score) == 0: 
            dart_score_str = new_dart.get_str_score()[0]
            if dart_score_str[0] == "D" : 
                 self.set_won(True)
            
            elif len(darts) > 1 :
                for dart in darts[:-1] : 
                    dart_score = dart.get_int_score()
                    self.score += dart_score
                    self.bust = True
            else : 
                self.bust = True

        else : 
            self.score -= dart_score

        


    def set_bust(self, value): 
        self.bust = value

    def set_won(self, value): 
        self.won = value

    def get_won(self) : 
        return self.won 
    
    def get_bust(self): 
        return self.bust

    def get_score(self):
        return self.score
    
    def get_active(self):
        return self.active

    def set_active(self, value): 
        self.active = value

    def get_name(self): 
        return self.name
    
    def get_frame(self): 
        return self.frame
    
    def set_frame(self, value): 
        self.frame = value


