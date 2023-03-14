PLAYER_INFO_FILE = './players_infos.csv'
ROUND_0_FILE = './round_0.csv'
MATCHES_FILE = './matches.csv'

# Sheldon Game

class Tournament:

    MATCHES_HEADER = 'Round,Winner,Player 1 name,Player 1 sign,Player 2 name,Player 2 sign'

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
        self.results = []
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

    def read_rounds(self) -> 'None':
        rounds = open(ROUND_0_FILE, 'r')
        rounds.readline()
        for line in rounds:
            line = line.strip().split(',')
            if len(line) > 1:
                player_1: 'int' = self.add_player(line[0])
                player_2: 'int' = self.add_player(line[1])
                self.players.extend([player_1,player_2])
        rounds.close()

    def read_info_file(self) -> 'None':
        info = open(PLAYER_INFO_FILE, 'r')
        info.readline()
        for line in info:
            line = line.strip().split(',')
            if len(line) > 1:
                player_id: 'int' = self.players_map[line[0]]
                if player_id in self.moves:
                    self.moves[player_id].append(self.moves_map[line[2]] )
                else:
                    self.moves[player_id] = [self.moves_map[line[2]]]
        info.close()

    def write(self):
        result_file = open(MATCHES_FILE, 'w')
        result_file.write(Tournament.MATCHES_HEADER)
        for result in self.results:
            result_file.write(f'\n{result[0]},{result[1]},{result[2]},{result[3]},{result[4]},{result[5]}')
        result_file.close()

    def battle(self, player_1: 'int', player_2: 'int', round: 'int') -> 'None':
        player_1_name: 'str' = self.players_map.pop(player_1)
        player_2_name: 'str' = self.players_map.pop(player_2)
        player_1_move: 'int' = self.moves[player_1].pop(0)
        player_2_move: 'int' = self.moves[player_2].pop(0)
        winner: 'int|None' = None
        winner_name: 'str|None' = None
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
        self.results.append((round,winner_name,player_1_name,self.moves_map[player_1_move],player_2_name,self.moves_map[player_2_move]))

    def play(self):
        self.read_rounds()
        self.read_info_file()
        round_count: 'int' = 0
        while len(self.moves) > 1:
            keys: 'list[int]' = self.players.copy()
            size: 'int' = len(keys)
            for cursor in range(0,size,2):
                self.battle(keys[cursor],keys[cursor + 1],round_count)
            round_count += 1
        self.write()
        winner: 'str' = self.players_map[self.players[0]]
        print(f"TOURNAMENT WINNER : {winner}")


def main():
    Tournament().play()

if __name__ == '__main__':
    main()
