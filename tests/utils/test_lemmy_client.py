import random
import sys
import unittest
import uuid

import tests.test_constants as test_constants
from src.db.comments.comments_dao import CommentsDao
from src.db.daily_threads.daily_threads_dao import DailyThreadsDao
from src.db.daily_threads.daily_threads_record import DailyThreadsRecord
from src.db.db_manager import DbManager
from src.db.game_day_threads.game_day_threads_dao import GameDayThreadsDao
from src.utils import datetime_util
from src.utils.environment_util import EnvironmentUtil
from src.utils.lemmy_client import LemmyClient
import pydash

# This is a dummy post on lemmy.world that is safe to spam comments to
TEST_POST_URL = "https://lemmy.world/post/14305925"
DICT_KEY_POST = 'post'
DICT_KEY_ID = 'id'


class TestLemmyClient(unittest.TestCase):
    comment_id: int = None
    post_id: int = None
    result_daily_thread: DailyThreadsRecord = None
    lemmy_client: LemmyClient = None

    def setUp(self) -> None:
        environment_util = EnvironmentUtil()
        self.db_manager = DbManager(test_constants.TEST_DB_PATH)
        self.game_day_threads_dao = GameDayThreadsDao(self.db_manager)
        self.daily_threads_dao = DailyThreadsDao(self.db_manager)
        self.comments_dao = CommentsDao(self.db_manager)
        TestLemmyClient.lemmy_client = LemmyClient(environment_util.lemmy_instance, environment_util.bot_name,
                                        environment_util.password, environment_util.community_name,
                                        self.game_day_threads_dao, self.daily_threads_dao, self.comments_dao)

    def test_create_comment(self):
        # This test actually creates a comment on a lemmy instance.
        random.seed(str(uuid.uuid4()))
        game_id = random.randint(0, sys.maxsize)
        print(f"generated game_id: {game_id}")
        resolved_items = TestLemmyClient.lemmy_client.lemmy.resolve_object(TEST_POST_URL)
        post_id = pydash.get(resolved_items, f"{DICT_KEY_POST}.{DICT_KEY_POST}.{DICT_KEY_ID}", -1) if resolved_items else -1
        print(f"post_id: {post_id}")
        self.assertNotEqual(post_id, -1, "Failed to resolve post ID in local Lemmy instance. Is this instance federated with lemmy.world?")
        result_comment = TestLemmyClient.lemmy_client.create_comment(post_id, game_id, f"commenting from a unit test! generated game_id: {game_id}")
        self.assertIsNotNone(result_comment, "result_comment was None")
        print(f"result_comment_id: {result_comment.comment_id}")
        TestLemmyClient.comment_id = self.comments_dao.get_comment(game_id).comment_id
        print(f"comment_id: {TestLemmyClient.comment_id}")
        self.assertNotEqual(TestLemmyClient.comment_id, -1, "Failed to retrieve comment from the db")
        self.assertEqual(TestLemmyClient.comment_id, result_comment.comment_id, "Comment IDs don't match.")

    def test_create_game_day_thread(self):
        # This test actually creates a post on a lemmy instance.
        # Make sure the 'COMMUNITY_NAME' in the environment file you are running this test with is safe to spam to.
        random.seed(str(uuid.uuid4()))
        game_id = random.randint(0, sys.maxsize)
        result_post_id = TestLemmyClient.lemmy_client.create_game_day_thread("unit test title", f"unit test body. generated game_id: {game_id}", game_id)
        self.assertNotEqual(result_post_id, -1, "Failed to create game day thread")
        TestLemmyClient.post_id = self.game_day_threads_dao.get_game_day_thread(game_id).post_id
        print(f"post_id: {TestLemmyClient.post_id}")
        self.assertNotEqual(TestLemmyClient.post_id, -1, "Failed to retrieve comment from the db")
        self.assertEqual(TestLemmyClient.post_id, result_post_id, "Post IDs don't match.")

    def test_create_daily_thread(self):
        # This test actually creates a post on a lemmy instance.
        # Make sure the 'COMMUNITY_NAME' in the environment file you are running this test with is safe to spam to.
        most_recent_daily_thread = self.daily_threads_dao.get_most_recent_daily_thread()
        if most_recent_daily_thread:
            date = datetime_util.next_day(most_recent_daily_thread.date)
        else:
            date = datetime_util.today()
        TestLemmyClient.result_daily_thread = TestLemmyClient.lemmy_client.create_daily_thread(date, "daily thread unit test", f"daily thread unit test body. date: {date}")
        self.assertIsNotNone(TestLemmyClient.result_daily_thread, "result_daily_thread was None")

    @classmethod
    def tearDownClass(cls):
        if cls.comment_id:
            cls.lemmy_client.delete_comment(cls.comment_id)
        if cls.post_id:
            cls.lemmy_client.delete_post(cls.post_id)
        if cls.result_daily_thread:
            cls.lemmy_client.delete_post(cls.result_daily_thread.post_id)


if __name__ == '__main__':
    unittest.main()
