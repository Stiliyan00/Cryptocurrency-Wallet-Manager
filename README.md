# Cryptocurrency-Wallet-Manager

## Кратко описание:
Клиент-сървър приложение с функционалност, което симулира личен портфейл за криптовалути. Приложението ще приема потребителски команди, изпраща ги за обработка на сървъра, приема отговора му и го предоставя на потребителя в четим формат(на терминала, уеб платформата или UI-a).

Криптовалутите са един от най-популярните варианти за инвестиране в момента,а нашият криптовалутният портфейл цели улесняване както на опитни инвеститори, така и на любителите.

### Функционалности
#### (Засега ще разглеждаме варианта за конзолно приложение.)

- **sing-up**
  Регистрация на потребител с username и password; Регистрираните потребители се пазят във файл при сървъра - той служи като база от данни. При спиране и
  повторно пускане, сървърът може да зареди в паметта си вече регистрираните потребители.
        
        $ signup <username> <password>
       

- **login**:
        
        $ login <username> <password>
              
- **help**
  За удобството на потребителя е предоставена и команда, която да му показва всички налични команди, който може да използва в конкретния момент:
        
        $ help
 
- Регистриран потребител може да:
    - **deposit-money** - добавя определена сума пари към портфейла на потребителя. Тъй като API-то, което ще използваме в задачата, работи с долари, ще    
      приемем, че сумите, които депозираме, ще са в долари. Например:
        ```bash
        $ deposit-money 10000.00
        ```
    - **list-offerings** - предоставя информацията за всички налични криптовалути, от които потребителят може да купува. Информацията за наличните валути 
      взимаме от [CoinAPI-то](#CoinAPI)-то.

        ```bash
        $ clist-offerings
        ```

    - **buy** - купува количество от дадена криптовалута за определената сума пари. Сумата трябва да е налична в портфейла на потребителя.
        ```bash
        $ buy --offering=<offering_code> --money=<amount>
        ```
    - **sell** - продава конкрента криптовалута. Сумата, получена от печалбата, остава в портфейла на потребителя.
        ```bash
        $ sell --offering=<offering_code>
        ```
    - **get-wallet-summary** - предоставя цялостна информацията за портфейла на потребителя - информация за всички активни инвестиции към момента на изпълнение на командата, за парите в портфейла му.
        ```bash
        $ get-wallet-summary
        ```
    - **get-wallet-overall-summary** - предоставя информацията за цялостната печалба/загуба от инвестициите на потребителя. Приложението сравнява цената за всяка криптовалута от момента на купуване и текущата ѝ цена, за да получи цялостната информация.
        ```bash
        $ get-wallet-overall-summary
        ```
    ## CoinAPI 
    Информацията за криптовалутите, от която сървърът има нужда, е достъпна чрез публично безплатно REST API - [CoinAPI](https://www.coinapi.io/).

    Заявките към REST API-то изискват автентикация с API key, какъвто може да получите като се регистрирате [тук](https://www.coinapi.io/pricing?apikey).

    *Note*: Функционалността, която предлага  API-то, е доста обширна, но ние ще се фокусираме на описаната [тук](https://docs.coinapi.io/#list-all-assets). Тя би била достатъчна за функционалността на проекта. 

    Следните endpoints от API-то биха ви били полезни:
    - **GET /v1/assets** - връща инфомрация за всички достъпи asset-и в JSON формат
    - **GET /v1/assets/{asset_id}** - връща инфромация за конкретен asset в JSON формат.

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


- При всяко влизане на потребителя в системата, той получава известия, ако неговите инвестиции са покачили или понижили.
Например:
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
   
    
- Сървърът ще може да обслужва множество клиенти паралелно.  
- Сървърът ще кешира получената от API-то информация като тя ще е валидна само за период от 30 минути, заради постоянно променящата се цена на
  криптовалутите.
- Сървърът пази информацията за потребителите и техните портфейли по начин, който му позволява след спиране или рестартиране да може да зареди тази информация отново.
- При неправилно използване на програмата, на потребителя да се извеждат подходящи съобщения за грешка.
- Валидацията на потребителския вход.
  
  ## Файлова артектура:
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
