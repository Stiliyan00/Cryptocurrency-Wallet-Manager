def list_offerings(self) -> Dict[str, float]:
    json_str = CryptocurrencyCoinsAPIClient.get_list_of_all_assets().json()
    result = dict()
    for i in json_str:
        # not optimal at all
        if i['type_is_crypto'] == 1:
            price_usd = \
                CryptocurrencyCoinsAPIClient.get_specific_rate_of_currency(i['asset_id'], 'USD').json()['rate']
            result[i['asset_id']] = price_usd
    return result