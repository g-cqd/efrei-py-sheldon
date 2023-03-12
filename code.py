PLAYER_INFO_FILE = './players_infos.csv'
ROUND_0_FILE = './round_0.csv'
MATCHES_FILE = './matches.csv'

# Sheldon Game

class Tournament:

    # static method
    @staticmethod
    def compare(left: 'int', right: 'int') -> 'int':
        left_win = int((left + 1)%5 == right or (left + 3) % 5 == right)
        right_win = int((right + 1)%5 == left or (right + 3) % 5 == left)
        return left_win - right_win

    def __init__(self):
        self.players_map = {}
        self.players =[]
        self.moves = {}
        self.matches = []
        self.results = open(MATCHES_FILE, 'w')
        self.results.write('Round,Winner,Player 1 name,Player 1 sign,Player 2 name,Player 2 sign\n')
        self.moves_map = {
            'SCISSORS': 0,
            'PAPER': 1,
            'ROCK': 2,
            'LIZARD': 3,
            'SPOCK': 4,
            0: 'SCISSORS',
            1: 'PAPER',
            2: 'ROCK',
            3: 'LIZARD',
            4: 'SPOCK'
        }

    def add_player(self, player: 'str') -> 'int':
        size = int(len(self.players_map) / 2)
        self.players_map[player] = size
        self.players_map[size] = player
        return size

    def read_info_file(self, file: 'str'):
        info = open(file, 'r')
        info.readline()

        for line in info:
            line = line.strip().split(',')
            player_id = self.players_map[line[0]]
            if player_id in self.moves:
                self.moves[player_id].append(self.moves_map[line[2]] )
            else:
                self.moves[player_id] = [self.moves_map[line[2]]]

        info.close()
    
    def read_rounds(self, file: 'str'):
        rounds = open(file, 'r')
        rounds.readline()
        for line in rounds:
            line = line.strip().split(',')
            player_1 = self.add_player(line[0])
            player_2 = self.add_player(line[1])
            self.matches.append((player_1,player_2))
            self.players.extend([player_1,player_2])
        rounds.close()

    def battle(self, player_1: 'int', player_2: 'int',round) -> 'int':
        player_1_name = self.players_map.pop(player_1)
        player_2_name = self.players_map.pop(player_2)
        player_1_move = self.moves[player_1].pop(0)
        player_2_move = self.moves[player_2].pop(0)
        winner = None
        winner_name = None
        match Tournament.compare(player_1_move, player_2_move):
            case 1:
                winner = player_1
                winner_name = player_1_name
                self.players_map.pop(player_2_name)
                self.moves.pop(player_2)
                self.players.remove(player_2)
            case -1:
                winner = player_2
                winner_name = player_2_name
                self.players_map.pop(player_1_name)
                self.moves.pop(player_1)
                self.players.remove(player_1)
            case 0:
                if player_1_name < player_2_name:
                    self.players_map.pop(player_2_name)
                    self.moves.pop(player_2)
                    self.players.remove(player_2)
                    winner = player_1
                    winner_name = player_1_name
                else:
                    self.players_map.pop(player_1_name)
                    self.moves.pop(player_1)
                    self.players.remove(player_1)
                    winner = player_2
                    winner_name = player_2_name
        self.players_map[winner] = winner_name
        self.players_map[winner_name] = winner
        self.results.write(f'{round},{winner_name},{player_1_name},{self.moves_map[player_1_move]},{player_2_name},{self.moves_map[player_2_move]}\n')
    
    def play(self):
        self.read_rounds(ROUND_0_FILE)
        self.read_info_file(PLAYER_INFO_FILE)
        round_count = 0
        while len(self.moves) > 1:
            keys = self.players.copy()
            for cursor in range(0,len(keys), 2):
                player_1 = keys[cursor]
                player_2 = keys[cursor + 1]
                self.battle(player_1,player_2,round_count)
            round_count += 1
        self.results.close()
        print(f"TOURNAMENT WINNER : {self.players_map[list(self.moves.keys())[0]]}")



Tournament().play()
