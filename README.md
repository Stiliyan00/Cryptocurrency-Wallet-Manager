# Cryptocurrency-Wallet-Manager

## Brief description:
A client-server application with functionality that simulates a personal cryptocurrency wallet. The application will accept user commands, send them to the server for processing, accept its response and provide it to the user in a readable format(on the terminal, web platform or UI).

Cryptocurrencies are one of the most popular options for investing right now, and our cryptocurrency portfolio aims to make it easier for both experienced investors and amateurs.

### Functionalities
#### (For now, we will be looking at the console application option.)

- **sing-up**
  User registration with username and password; Registered users are stored in a file on the server - it serves as a database. At shutdown and
  restart, the server can load the already registered users into its memory.
        
        $ signup <username> <password>
       

- **login**:
        
        $ login <username> <password>
              
- **help**
  For the convenience of the user, a command is also provided to show him all available commands he can use at that particular moment:
        
        $ help
 
- A registered user can:
    - **deposit-money** - adds a certain amount of money to the user's wallet. Since the API that we will use in the task works with dollars, we will    
      assume that the amounts we deposit will be in dollars. For example:
        ```bash
        $ deposit-money 10000.00
        ```
    - **list-offerings** - provides information about all available cryptocurrencies from which the user can buy. The information about the available currencies 
      we get from [CoinAPI](#CoinAPI).

        ```bash
        $ clist-offerings
        ```

    - **buy** - buys a quantity of a given cryptocurrency for the specified amount of money. The amount must be available in the user's wallet.
        ```bash
        $ buy --offering=<offering_code> --money=<amount>
        ```
    - **sell** - sells concrent cryptocurrency. The amount received from the profit remains in the user's wallet.
        ```bash
        $ sell --offering=<offering_code>
        ```
    - **get-wallet-summary** - provides comprehensive information about the user's portfolio - information about all active investments at the time of command execution, about the money in his portfolio.
        ```bash
        $ get-wallet-summary
        ```
    - **get-wallet-overall-summary** - provides information on the overall profit/loss of the user's investment. The app compares the price for each cryptocurrency from the time of purchase and its current price to get the overall information.
        ```bash
        $ get-wallet-overall-summary
        ```
    ## CoinAPI 
    The cryptocurrency information the server needs is available via a public free REST API - [CoinAPI](https://www.coinapi.io/).

    Requests to the REST API require authentication with an API key, which you can get by registering [тук](https://www.coinapi.io/pricing?apikey).

    *Note*: The functionality offered by the API is quite extensive, but we will focus on the one described [here](https://docs.coinapi.io/#list-all-assets). It would be sufficient for the functionality of the project. 

    The following API endpoints would be useful:
    - **GET /v1/assets** - returns information about all accessed assets in JSON format
    - **GET /v1/assets/{asset_id}** - returns information about a specific asset in JSON format.

     - **Пример:**
    ```bash
     GET /v1/assets/BTC
    ```

    ```bash
    [
      {
        "asset_id": "BTC",
        "name": "Bitcoin",
        "type_is_crypto": 1,
        "data_start": "2010-07-17",
        "data_end": "2021-01-24",
        "data_quote_start": "2014-02-24T17:43:05.0000000Z",
        "data_quote_end": "2021-01-24T19:07:51.7954142Z",
        "data_orderbook_start": "2014-02-24T17:43:05.0000000Z",
        "data_orderbook_end": "2020-08-05T14:38:38.3413202Z",
        "data_trade_start": "2010-07-17T23:09:17.0000000Z",
        "data_trade_end": "2021-01-24T19:08:47.4460000Z",
        "data_symbols_count": 46840,
        "volume_1hrs_usd": 9160288508835.92,
        "volume_1day_usd": 197928243055426.88,
        "volume_1mth_usd": 11571260516151083.22,
        "price_usd": 31304.448721266051267349441838,
        "id_icon": "4caf2b16-a017-4e26-a348-2cea69c34cba"
      }
    ]
    ```


- Each time a user logs in, they receive notifications if their investments have gone up or down.
For example:
    ```bash
    $ login bobi bobislongpassword
    Successful login!
    No notifications to show.
    ```
    
    или
    
    ```bash
    $ login bobi bobislongpassword
    You successfully logged in!
    => Notifications: 
    ***************************
    Your investment in BTC has droped from 5345.00 to 5343.21.
   
    
- The server will be able to serve multiple clients in parallel.  
- The server will cache the information received from the API and it will only be valid for a period of 30 minutes because of the constantly changing cost of
  cryptocurrencies.
- The server stores information about users and their wallets in a way that allows it to be able to reload that information after a shutdown or reboot.
- If the program is used incorrectly, appropriate error messages are displayed to the user.
- User Login Validation.
  
  ## File Architecture:
    ```bash
           src
            └─ bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency
                ├─ client
                |     └─ CryptocurrencyWalletClient.py
                |     
                |       
                ├─ command
                |     ├─ exceptions
                |     |       └─ InvalidCryptocurrencyCommandException.py
                |     |
                |     ├─ Command.py
                |     └─ DefaultCommand.py
                |
                ├─ exceptions
                |     ├─ PasswordIsNotCorrectException.py
                |     ├─ UserAlreadyExistsException.py
                |     └─ UserDoesNotExistException.py
                |
                |
                ├─ repository
                |     └─ CryptocurrencyCoinsAPIClient.py
                |
                ├─ server
                |     └─ CryotocurrencyWalletServer.py
                |
                ├─ user
                |     ├─ exceptions
                |     |       ├─ CryptocurrencyDoesNotExistException.py
                |     |       ├─ NotEnoughMoneyError.py
                |     |       └─ UserDoesNotHaveCryptocurrencyException.py
                |     |
                |     ├─ StandardUser.py
                |     └─ User.py
                |
                ├─ CryptocurrencyWallet.py
                └─ DefaultCryptocurrencyWallet.py
           test
            └─ bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency
                ├─ user
                |    └─ test_user.py
                |
                └─ test_cryptocurrency_wallet.py
    ```
