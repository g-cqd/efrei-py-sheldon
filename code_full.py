import time
import sys
import asyncio
from threading import Thread

PLAYER_INFO_FILE = 'players_infos.csv'
ROUND_0_FILE = 'round_0.csv'
MATCHES_FILE = 'matches.csv'

# Sheldon Game

def test_file(test_number: 'int' = 1, file: 'str|None' = None) -> 'str':
    return f"./test_{test_number}/{file}"

class Tournament:

    WRITERS = []
    MATCHES_HEADER = 'Round,Winner,Player 1 name,Player 1 sign,Player 2 name,Player 2 sign'

    def write(self):
        result_file = open(test_file(self.test_number,MATCHES_FILE), 'w')
        result_file.write(Tournament.MATCHES_HEADER)
        for result in self.results:
            result_file.write(f'\n{result[0]},{result[1]},{result[2]},{result[3]},{result[4]},{result[5]}')
        result_file.close()

    async def write_async(self):
        result_file = open(test_file(self.test_number,MATCHES_FILE), 'w')
        result_file.write(Tournament.MATCHES_HEADER)
        for result in self.results:
            result_file.write(f'\n{result[0]},{result[1]},{result[2]},{result[3]},{result[4]},{result[5]}')
        result_file.close()
    
    def write_for_multithread(self):
        self.results.sort(key=lambda x: x[6])
        result_file = open(test_file(self.test_number,MATCHES_FILE), 'w')
        result_file.write(Tournament.MATCHES_HEADER)
        for result in self.results:
            result_file.write(f'\n{result[0]},{result[1]},{result[2]},{result[3]},{result[4]},{result[5]}')
        result_file.close()
    
    async def write_for_multithread_async(self):
        self.results.sort(key=lambda x: x[6])
        result_file = open(test_file(self.test_number,MATCHES_FILE), 'w')
        result_file.write(Tournament.MATCHES_HEADER)
        for result in self.results:
            result_file.write(f'\n{result[0]},{result[1]},{result[2]},{result[3]},{result[4]},{result[5]}')
        result_file.close()

    @staticmethod
    def compare(left: 'int', right: 'int') -> 'int':
        left_win = int((left + 1)%5 == right or (left + 3) % 5 == right)
        right_win = int((right + 1)%5 == left or (right + 3) % 5 == left)
        return left_win - right_win

    def __init__(self, test_number: 'int' = 1):
        self.test_number: 'int' = test_number
        self.players_map = {}
        self.players: 'list[int]' = []
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
        size: 'int' = int(len(self.players_map) / 2)
        self.players_map[player] = size
        self.players_map[size] = player
        return size

    def read_rounds(self) -> 'None':
        rounds = open(test_file(self.test_number,ROUND_0_FILE), 'r')
        rounds.readline()
        for line in rounds:
            line = line.strip().split(',')
            if len(line) > 1:
                player_1: 'int' = self.add_player(line[0])
                player_2: 'int' = self.add_player(line[1])
                self.players.extend([player_1,player_2])
        rounds.close()

    def read_info_file(self) -> 'None':
        info = open(test_file(self.test_number,PLAYER_INFO_FILE), 'r')
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

    @staticmethod
    def battle_unithread(tournament: 'Tournament', player_1: 'int', player_2: 'int', round: 'int') -> 'None':
        player_1_name: 'str' = tournament.players_map.pop(player_1)
        player_2_name: 'str' = tournament.players_map.pop(player_2)
        player_1_move: 'int' = tournament.moves[player_1].pop(0)
        player_2_move: 'int' = tournament.moves[player_2].pop(0)
        winner: 'int' = -1
        winner_name: 'str' = ''
        match Tournament.compare(player_1_move, player_2_move):
            case 1:
                winner = player_1
                winner_name = player_1_name
                tournament.players_map.pop(player_2_name)
                tournament.moves.pop(player_2)
                tournament.players.remove(player_2)
            case -1:
                winner = player_2
                winner_name = player_2_name
                tournament.players_map.pop(player_1_name)
                tournament.moves.pop(player_1)
                tournament.players.remove(player_1)
            case 0:
                if player_1_name < player_2_name:
                    tournament.players_map.pop(player_2_name)
                    tournament.moves.pop(player_2)
                    tournament.players.remove(player_2)
                    winner = player_1
                    winner_name = player_1_name
                else:
                    tournament.players_map.pop(player_1_name)
                    tournament.moves.pop(player_1)
                    tournament.players.remove(player_1)
                    winner = player_2
                    winner_name = player_2_name
        tournament.players_map[winner] = winner_name
        tournament.players_map[winner_name] = winner
        tournament.results.append((round,winner_name,player_1_name,tournament.moves_map[player_1_move],player_2_name,tournament.moves_map[player_2_move],player_1,player_2))
    
    def play(self,async_write=False) -> 'str':
        self.read_rounds()
        self.read_info_file()
        round_count: 'int' = 0
        while len(self.moves) > 1:
            keys: 'list[int]' = self.players.copy()
            size: 'int' = len(keys)
            for cursor in range(0,size,2):
                self.battle(keys[cursor],keys[cursor + 1],round_count)
            round_count += 1
        if async_write:
            Tournament.WRITERS.append( self.write_async() )
        else:
            self.write()
        winner: 'str' = self.players_map[self.players[0]]
        print(f"TOURNAMENT WINNER : {winner}")
        return winner

    async def play_async(self,async_write=False) -> 'str':
        self.read_rounds()
        self.read_info_file()
        round_count: 'int' = 0
        while len(self.moves) > 1:
            keys: 'list[int]' = self.players.copy()
            size: 'int' = len(keys)
            for cursor in range(0,size,2):
                self.battle(keys[cursor],keys[cursor + 1],round_count)
            round_count += 1
        if async_write:
            Tournament.WRITERS.append( self.write_async() )
        else:
            self.write()
        winner: 'str' = self.players_map[self.players[0]]
        print(f"TOURNAMENT WINNER : {winner}")
        return winner
        
    def play_multithreaded(self,async_write=False) -> 'str':
        self.read_rounds()
        self.read_info_file()
        round_count: 'int' = 0
        while len(self.moves) > 1:
            keys: 'list[int]' = self.players.copy()
            results: 'list[tuple[str,str,str,str,str,int,int]]' = []
            size: 'int' = len(keys)
            ranges: 'list[range]|None' = None
            if size >= 16:
                subpart: 'int' = int(size / 8)
                ranges = [range(x * subpart, x * subpart + subpart, 2) for x in range(8)] 
            elif size >= 8:
                subpart: 'int' = int(size / 4)
                ranges = [range(x * subpart, x * subpart + subpart, 2) for x in range(4)]
            elif size >= 4:
                subpart: 'int' = int(size / 2)
                ranges = [range(x * subpart, x * subpart + subpart, 2) for x in range(2)]
            else:
                ranges = [range(0,size,2)]
            for _range in ranges:
                threads = [
                    Thread(
                        target=lambda x,r,s,k,c: [r.append(Tournament.battle_unithread(s,k[i],k[i + 1],c)) for i in x],
                        args=[_range,results,self,keys,round_count]
                    )
                ]
                for thread in threads: thread.start()
                for thread in threads: thread.join()
            round_count += 1
        if async_write:
            Tournament.WRITERS.append( self.write_for_multithread_async() )
        else:
            self.write_for_multithread()
        winner = self.players_map[self.players[0]]
        print(f"TOURNAMENT WINNER : {winner}")
        return winner
    
    async def play_async_multithreaded(self,async_write=False) -> 'str':
        self.read_rounds()
        self.read_info_file()
        round_count: 'int' = 0
        while len(self.moves) > 1:
            keys: 'list[int]' = self.players.copy()
            results: 'list[tuple[str,str,str,str,str,int,int]]' = []
            size: 'int' = len(keys)
            ranges: 'list[range]|None' = None
            if size >= 16:
                subpart: 'int' = int(size / 8)
                ranges = [range(x * subpart, x * subpart + subpart, 2) for x in range(8)] 
            elif size >= 8:
                subpart: 'int' = int(size / 4)
                ranges = [range(x * subpart, x * subpart + subpart, 2) for x in range(4)]
            elif size >= 4:
                subpart: 'int' = int(size / 2)
                ranges = [range(x * subpart, x * subpart + subpart, 2) for x in range(2)]
            else:
                ranges = [range(0,size,2)]
            for _range in ranges:
                threads = [
                    Thread(
                        target=lambda x,r,s,k,c: [r.append(Tournament.battle_unithread(s,k[i],k[i + 1],c)) for i in x],
                        args=[_range,results,self,keys,round_count]
                    )
                ]
                for thread in threads: thread.start()
                for thread in threads: thread.join()
            round_count += 1
        if async_write:
            Tournament.WRITERS.append( self.write_for_multithread_async() )
        else:
            self.write_for_multithread()
        winner = self.players_map[self.players[0]]
        print(f"TOURNAMENT WINNER : {winner}")
        return winner

async def mode_11():
    t0: 'float' = time.perf_counter()
    for i in range(1, 14 + 1):
        Tournament(i).play()
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode_10():
    t0: 'float' = time.perf_counter()
    for i in range(1, 14 + 1):
        Tournament(i).play(async_write=True)
    await asyncio.gather(*Tournament.WRITERS)
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")


async def mode__9():
    t0: 'float' = time.perf_counter()
    for i in range(1, 14 + 1):
        Tournament(i).play_multithreaded()
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__8():
    t0: 'float' = time.perf_counter()
    for i in range(1, 14 + 1):
        Tournament(i).play_multithreaded(async_write=True)
    await asyncio.gather(*Tournament.WRITERS)
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__7():
    t0: 'float' = time.perf_counter()
    await asyncio.gather(*[Tournament(i).play_async() for i in range(1, 14 + 1)])
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__6():
    t0: 'float' = time.perf_counter()
    await asyncio.gather(*[Tournament(i).play_async(async_write=True) for i in range(1, 14 + 1)])
    await asyncio.gather(*Tournament.WRITERS)
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__5():
    t0: 'float' = time.perf_counter()
    threads: 'list[Thread]' = [Thread(target=lambda x: Tournament(x).play(), args=[i]) for i in range(1, 14 + 1)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__4():
    t0: 'float' = time.perf_counter()
    threads: 'list[Thread]' = [Thread(target=lambda x: Tournament(x).play(async_write=True), args=[i]) for i in range(1, 14 + 1)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    await asyncio.gather(*Tournament.WRITERS)
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__3():
    t0: 'float' = time.perf_counter()
    threads: 'list[Thread]'  = [Thread(target=lambda x: Tournament(x).play_multithreaded(), args=[i]) for i in range(1, 14 + 1)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__2():
    t0: 'float' = time.perf_counter()
    threads: 'list[Thread]'  = [Thread(target=lambda x: Tournament(x).play_multithreaded(async_write=True), args=[i]) for i in range(1, 14 + 1)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    await asyncio.gather(*Tournament.WRITERS)
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__1():
    t0: 'float' = time.perf_counter()
    await asyncio.gather(*[Tournament(i).play_async_multithreaded() for i in range(1, 14 + 1)])
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

async def mode__0():
    t0: 'float' = time.perf_counter()
    await asyncio.gather(*[Tournament(i).play_async_multithreaded(async_write=True) for i in range(1, 14 + 1)])
    await asyncio.gather(*Tournament.WRITERS)
    t1: 'float' = time.perf_counter()
    print(f"Total time : {t1-t0} s")

def main( args: 'list[str]' ):
    try:
        loop = asyncio.get_event_loop()
        test = int(args[:1][0])
        match test:
            case 0:
                loop.run_until_complete(mode__0())
            case 1:
                loop.run_until_complete(mode__1())
            case 2:
                loop.run_until_complete(mode__2())
            case 3:
                loop.run_until_complete(mode__3())
            case 4:
                loop.run_until_complete(mode__4())
            case 5:
                loop.run_until_complete(mode__5())
            case 6:
                loop.run_until_complete(mode__6())
            case 7:
                loop.run_until_complete(mode__7())
            case 8:
                loop.run_until_complete(mode__8())
            case 9:
                loop.run_until_complete(mode__9())
            case 10:
                loop.run_until_complete(mode_10())
            case 11:
                loop.run_until_complete(mode_11())
            case _:
                print("Invalid test number")
        loop.close()
    except:
        sys.exit(1)
    finally:
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
