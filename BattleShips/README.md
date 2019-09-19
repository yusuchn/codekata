# swagger-client
The API for Battleships

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 1.0.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import swagger_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import swagger_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))
game_id = 'game_id_example' # str | The ID of the game to return

try:
    # Delete the given game
    api_instance.games_game_id_delete(game_id)
except ApiException as e:
    print("Exception when calling DefaultApi->games_game_id_delete: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://10.44.37.98:9000*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DefaultApi* | [**games_game_id_delete**](docs/DefaultApi.md#games_game_id_delete) | **DELETE** /games/{gameId}/ | Delete the given game
*DefaultApi* | [**games_game_id_get**](docs/DefaultApi.md#games_game_id_get) | **GET** /games/{gameId}/ | Get the current status of a game
*DefaultApi* | [**games_game_id_grid_ref_put**](docs/DefaultApi.md#games_game_id_grid_ref_put) | **PUT** /games/{gameId}/{gridRef}/ | Make a move
*DefaultApi* | [**games_get**](docs/DefaultApi.md#games_get) | **GET** /games/ | Get an index of all known games
*DefaultApi* | [**games_post**](docs/DefaultApi.md#games_post) | **POST** /games/ | Start a new game
*DefaultApi* | [**players_get**](docs/DefaultApi.md#players_get) | **GET** /players/ | Get the list of all known players
*DefaultApi* | [**players_name_get**](docs/DefaultApi.md#players_name_get) | **GET** /players/{name}/ | Get information about a specific player


## Documentation For Models

 - [GetGame](docs/GetGame.md)
 - [GetGamesIndexResponse](docs/GetGamesIndexResponse.md)
 - [GetPlayer](docs/GetPlayer.md)
 - [GetPlayersIndexResponse](docs/GetPlayersIndexResponse.md)
 - [Knowledge](docs/Knowledge.md)
 - [Move](docs/Move.md)
 - [MoveResponse](docs/MoveResponse.md)
 - [Player](docs/Player.md)
 - [Ship](docs/Ship.md)
 - [StartGame](docs/StartGame.md)
 - [StartGameResponse](docs/StartGameResponse.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author


