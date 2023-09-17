import json
import unittest
import datetime

import pydash
from dateutil.tz import tzutc

from src.datatypes.game import Game
from src.datatypes.goal import Goal
from src.datatypes.period import Period
from src.datatypes.shootout import Shootout
from src.datatypes.team_stats import TeamStats
from src.datatypes.teams import Team
from src.utils import constants, nhl_api_client

FEED_LIVE_TEST_FILE_PATH = f"{constants.TEST_RES_PATH}/2022020158_feed_live.json"
SCHEDULED_FEED_LIVE_TEST_FILE_PATH = f"{constants.TEST_RES_PATH}/2023010001_feed_live.json"


class TestNhlApiClient(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        with open(FEED_LIVE_TEST_FILE_PATH, "r") as file:
            json_string = file.read()
            self.feed_live = json.loads(json_string)
        with open(SCHEDULED_FEED_LIVE_TEST_FILE_PATH, "r") as file:
            json_string = file.read()
            self.scheduled_feed_live = json.loads(json_string)

    def test_parse_goals(self):
        expected = [Goal(period='1st', time='05:16', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (1) Wrist Shot, assists: Kevin Shattenkirk ' '(3)'), Goal(period='1st', time='06:18', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (7) Wrist Shot, assists: Evgeny Svechnikov ' '(3), Tomas Hertl (6)'), Goal(period='1st', time='06:41', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (8) Slap Shot, assists: Jaycob Megna (4), ' 'Nico Sturm (1)'), Goal(period='1st', time='10:52', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Frank Vatrano (4) Wrist Shot, assists: Isac Lundestrom (4), ' 'Jakob Silfverberg (1)'), Goal(period='1st', time='19:45', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (2) Backhand, assists: Trevor Zegras (2), ' 'Kevin Shattenkirk (4)'), Goal(period='2nd', time='03:28', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Power Play', goalie='Stolarz', description='Timo Meier (2) Backhand, assists: Alexander Barabanov (4), ' 'Erik Karlsson (6)'), Goal(period='2nd', time='15:10', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Ryan Strome (2) Deflected, assists: John Klingberg (3), ' 'Troy Terry (7)'), Goal(period='2nd', time='15:31', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Timo Meier (3) , assists: none'), Goal(period='3rd', time='11:31', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Max Comtois (2) Wrist Shot, assists: Troy Terry (8), Nathan ' 'Beaulieu (1)'), Goal(period='3rd', time='17:48', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (9) Wrist Shot, assists: Alexander Barabanov ' '(5), Tomas Hertl (7)'), Goal(period='SO', time='00:00', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Logan Couture - Wrist Shot'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Trevor Zegras - Backhand'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Troy Terry - Backhand')]
        goals = nhl_api_client.parse_goals(self.feed_live)
        print(goals)
        self.assertEqual(goals, expected)

    def test_parse_game(self):
        expected = Game(id=2022020158, away_team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), home_team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzutc()), end_time=datetime.datetime(2022, 11, 2, 5, 35, 23, tzinfo=tzutc()), game_clock='Final', away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins='55.4', giveaways=10, takeaways=10, pp_opportunities=4, pp_goals=0, pp_percentage='0.0', periods=[Period(goals=3, shots=17, period_number=1, ordinal_number='1st'), Period(goals=1, shots=15, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=9, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=3, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=2, attempts=2, has_been_played=True)), home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins='44.6', giveaways=10, takeaways=10, pp_opportunities=3, pp_goals=1, pp_percentage='33.3', periods=[Period(goals=2, shots=10, period_number=1, ordinal_number='1st'), Period(goals=2, shots=18, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=14, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=2, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=1, attempts=3, has_been_played=True)), goals=[Goal(period='1st', time='05:16', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (1) Wrist Shot, assists: Kevin Shattenkirk (3)'), Goal(period='1st', time='06:18', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (7) Wrist Shot, assists: Evgeny Svechnikov (3), Tomas Hertl (6)'), Goal(period='1st', time='06:41', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (8) Slap Shot, assists: Jaycob Megna (4), Nico Sturm (1)'), Goal(period='1st', time='10:52', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Frank Vatrano (4) Wrist Shot, assists: Isac Lundestrom (4), Jakob Silfverberg (1)'), Goal(period='1st', time='19:45', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (2) Backhand, assists: Trevor Zegras (2), Kevin Shattenkirk (4)'), Goal(period='2nd', time='03:28', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Power Play', goalie='Stolarz', description='Timo Meier (2) Backhand, assists: Alexander Barabanov (4), Erik Karlsson (6)'), Goal(period='2nd', time='15:10', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Ryan Strome (2) Deflected, assists: John Klingberg (3), Troy Terry (7)'), Goal(period='2nd', time='15:31', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Timo Meier (3) , assists: none'), Goal(period='3rd', time='11:31', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Max Comtois (2) Wrist Shot, assists: Troy Terry (8), Nathan Beaulieu (1)'), Goal(period='3rd', time='17:48', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (9) Wrist Shot, assists: Alexander Barabanov (5), Tomas Hertl (7)'), Goal(period='SO', time='00:00', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Logan Couture - Wrist Shot'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Trevor Zegras - Backhand'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Troy Terry - Backhand')])
        game = nhl_api_client.parse_game(self.feed_live)
        print(game)
        self.assertEqual(game, expected)

    def test_parse_scheduled_game(self):
        expected = Game(id=2023010001, away_team=Team(id=26, abbreviation='LAK', city='Los Angeles', name='Kings', logo_url='https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png'), home_team=Team(id=53, abbreviation='ARI', city='Arizona', name='Coyotes', logo_url='https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png'), start_time=datetime.datetime(2023, 9, 23, 4, 5, tzinfo=tzutc()), end_time=None, game_clock='--', away_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_opportunities=0, pp_goals=0, pp_percentage='0.0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), home_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_opportunities=0, pp_goals=0, pp_percentage='0.0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), goals=[])
        game = nhl_api_client.parse_game(self.scheduled_feed_live)
        print(game)
        self.assertEqual(game, expected)

    def test_bad_goalie_name_split(self):
        expected = ""
        name = "".split(" ")[-1]
        self.assertEqual(expected, name)


if __name__ == '__main__':
    unittest.main()
