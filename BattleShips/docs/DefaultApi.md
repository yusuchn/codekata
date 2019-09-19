# swagger_client.DefaultApi

All URIs are relative to *http://10.44.37.98:9000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**games_game_id_delete**](DefaultApi.md#games_game_id_delete) | **DELETE** /games/{gameId}/ | Delete the given game
[**games_game_id_get**](DefaultApi.md#games_game_id_get) | **GET** /games/{gameId}/ | Get the current status of a game
[**games_game_id_grid_ref_put**](DefaultApi.md#games_game_id_grid_ref_put) | **PUT** /games/{gameId}/{gridRef}/ | Make a move
[**games_get**](DefaultApi.md#games_get) | **GET** /games/ | Get an index of all known games
[**games_post**](DefaultApi.md#games_post) | **POST** /games/ | Start a new game
[**players_get**](DefaultApi.md#players_get) | **GET** /players/ | Get the list of all known players
[**players_name_get**](DefaultApi.md#players_name_get) | **GET** /players/{name}/ | Get information about a specific player


# **games_game_id_delete**
> games_game_id_delete(game_id)

Delete the given game

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
game_id = 'game_id_example' # str | The ID of the game to return

try:
    # Delete the given game
    api_instance.games_game_id_delete(game_id)
except ApiException as e:
    print("Exception when calling DefaultApi->games_game_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **game_id** | **str**| The ID of the game to return | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **games_game_id_get**
> GetGame games_game_id_get(game_id)

Get the current status of a game

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
game_id = 'game_id_example' # str | The ID of the game to return

try:
    # Get the current status of a game
    api_response = api_instance.games_game_id_get(game_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->games_game_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **game_id** | **str**| The ID of the game to return | 

### Return type

[**GetGame**](GetGame.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **games_game_id_grid_ref_put**
> MoveResponse games_game_id_grid_ref_put(game_id, grid_ref, body=body)

Make a move

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
game_id = 'game_id_example' # str | The ID of the game
grid_ref = 'grid_ref_example' # str | The location at which to make a move
body = swagger_client.Move() # Move | Information about the move (optional)

try:
    # Make a move
    api_response = api_instance.games_game_id_grid_ref_put(game_id, grid_ref, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->games_game_id_grid_ref_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **game_id** | **str**| The ID of the game | 
 **grid_ref** | **str**| The location at which to make a move | 
 **body** | [**Move**](Move.md)| Information about the move | [optional] 

### Return type

[**MoveResponse**](MoveResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **games_get**
> GetGamesIndexResponse games_get()

Get an index of all known games

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    # Get an index of all known games
    api_response = api_instance.games_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->games_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetGamesIndexResponse**](GetGamesIndexResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **games_post**
> StartGameResponse games_post(body)

Start a new game

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.StartGame() # StartGame | Definition of game to start

try:
    # Start a new game
    api_response = api_instance.games_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->games_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StartGame**](StartGame.md)| Definition of game to start | 

### Return type

[**StartGameResponse**](StartGameResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **players_get**
> GetPlayersIndexResponse players_get()

Get the list of all known players

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    # Get the list of all known players
    api_response = api_instance.players_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->players_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GetPlayersIndexResponse**](GetPlayersIndexResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **players_name_get**
> GetPlayer players_name_get(name)

Get information about a specific player

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
name = 'name_example' # str | The name of the player to retrieve

try:
    # Get information about a specific player
    api_response = api_instance.players_name_get(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->players_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the player to retrieve | 

### Return type

[**GetPlayer**](GetPlayer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

