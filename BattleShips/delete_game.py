import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'autogen', 'python-client'))

import swagger_client

api = swagger_client.api.DefaultApi()

gameid = sys.argv[1]

api.games_game_id_delete(gameid)

