import sys

import common_own as co

connection_base = "https://dappradar.com/rankings"
base_url = "https://dappradar.com/v2/api/dapps?params="
file_path = "/Users/pundix2022/Juypter Working Env"

cate_map = {
    # chains
    "rank_all": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbk52Y25ROWRYTmxjaVp2Y21SbGNqMWtaWE5qSm14cGJXbDBQVEky",
    "rank_eth": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWxkR2hsY21WMWJTWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09",
    "rank_eos": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWxiM01tYzI5eWREMTFjMlZ5Sm05eVpHVnlQV1JsYzJNbWJHbHRhWFE5TWpZPQ==",
    "rank_tron": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTBjbTl1Sm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg==",
    "rank_ont": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXZiblJ2Ykc5bmVTWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09",
    "rank_thunderCore": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTBhSFZ1WkdWeVkyOXlaU1p6YjNKMFBYVnpaWEltYjNKa1pYSTlaR1Z6WXlac2FXMXBkRDB5Tmc9PQ==",
    "rank_waves": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTNZWFpsY3laemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_wax": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTNZWGdtYzI5eWREMTFjMlZ5Sm05eVpHVnlQV1JsYzJNbWJHbHRhWFE5TWpZPQ==",
    "rank_steem": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXpkR1ZsYlNaemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_hive": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMW9hWFpsSm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg==",
    "rank_bnb": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWlhVzVoYm1ObExYTnRZWEowTFdOb1lXbHVKbk52Y25ROWRYTmxjaVp2Y21SbGNqMWtaWE5qSm14cGJXbDBQVEky",
    "rank_polygon": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXdiMng1WjI5dUpuTnZjblE5ZFhObGNpWnZjbVJsY2oxa1pYTmpKbXhwYldsMFBUSTI=",
    "rank_flow": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMW1iRzkzSm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg==",
    "rank_near": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXVaV0Z5Sm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg==",
    "rank_avalanche": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWhkbUZzWVc1amFHVW1jMjl5ZEQxMWMyVnlKbTl5WkdWeVBXUmxjMk1tYkdsdGFYUTlNalk9",
    "rank_telos": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTBaV3h2Y3laemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_tezos": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTBaWHB2Y3laemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_rsk": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXljMnNtYzI5eWREMTFjMlZ5Sm05eVpHVnlQV1JsYzJNbWJHbHRhWFE5TWpZPQ==",
    "rank_iotex": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXBiM1JsZUNaemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_vulcan": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTJkV3hqWVc1bWIzSm5aV1FtYzI5eWREMTFjMlZ5Sm05eVpHVnlQV1JsYzJNbWJHbHRhWFE5TWpZPQ==",
    "rank_harmony": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMW9ZWEp0YjI1NUpuTnZjblE5ZFhObGNpWnZjbVJsY2oxa1pYTmpKbXhwYldsMFBUSTI=",
    "rank_okc": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXZaV01tYzI5eWREMTFjMlZ5Sm05eVpHVnlQV1JsYzJNbWJHbHRhWFE5TWpZPQ==",
    "rank_solana": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXpiMnhoYm1FbWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_ronin": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXliMjVwYmlaemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_klaytn": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXJiR0Y1ZEc0bWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_everscale": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWxkbVZ5YzJOaGJHVW1jMjl5ZEQxMWMyVnlKbTl5WkdWeVBXUmxjMk1tYkdsdGFYUTlNalk9",
    "rank_heco": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMW9aV052Sm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg==",
    "rank_dep": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWtaWEFtYzI5eWREMTFjMlZ5Sm05eVpHVnlQV1JsYzJNbWJHbHRhWFE5TWpZPQ==",
    "rank_immutablex": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXBiVzExZEdGaWJHVjRKbk52Y25ROWRYTmxjaVp2Y21SbGNqMWtaWE5qSm14cGJXbDBQVEky",
    "rank_fuse": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMW1kWE5sSm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg==",
    "rank_algorand": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWhiR2R2Y21GdVpDWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09",
    "rank_telosevm": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTBaV3h2YzJWMmJTWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09",
    "rank_cronos": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWpjbTl1YjNNbWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_moonriver": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXRiMjl1Y21sMlpYSW1jMjl5ZEQxMWMyVnlKbTl5WkdWeVBXUmxjMk1tYkdsdGFYUTlNalk9",
    "rank_moonbean": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXRiMjl1WW1WaGJTWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09",
    "rank_fantom": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMW1ZVzUwYjIwbWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_oasisNetwork": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXZZWE5wY3laemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_shiden": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXphR2xrWlc0bWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_celo": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWpaV3h2Sm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg==",
    "rank_kardiaChain": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXJZWEprYVdGamFHRnBiaVp6YjNKMFBYVnpaWEltYjNKa1pYSTlaR1Z6WXlac2FXMXBkRDB5Tmc9PQ==",
    "rank_Hedera": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMW9aV1JsY21FbWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_optimism": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXZjSFJwYldsemJTWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09",
    "rank_astar": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWhjM1JoY2laemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_stacks": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXpkR0ZqYTNNbWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_zilliqa": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTZhV3hzYVhGaEpuTnZjblE5ZFhObGNpWnZjbVJsY2oxa1pYTmpKbXhwYldsMFBUSTI=",
    "rank_aurora": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWhkWEp2Y21FbWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_theta": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMTBhR1YwWVNaemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    # categories
    "rank_cate_games": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQV2RoYldWekpuTnZjblE5ZFhObGNpWnZjbVJsY2oxa1pYTmpKbXhwYldsMFBUSTI=",
    "rank_cate_defi": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQV1JsWm1rbWMyOXlkRDExYzJWeUptOXlaR1Z5UFdSbGMyTW1iR2x0YVhROU1qWT0=",
    "rank_cate_gambling": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQV2RoYldKc2FXNW5Kbk52Y25ROWRYTmxjaVp2Y21SbGNqMWtaWE5qSm14cGJXbDBQVEky",
    "rank_cate_exchanges": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQV1Y0WTJoaGJtZGxjeVp6YjNKMFBYVnpaWEltYjNKa1pYSTlaR1Z6WXlac2FXMXBkRDB5Tmc9PQ==",
    "rank_cate_collectibles": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQV052Ykd4bFkzUnBZbXhsY3laemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_cate_marketplaces": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQVzFoY210bGRIQnNZV05sY3laemIzSjBQWFZ6WlhJbWIzSmtaWEk5WkdWell5WnNhVzFwZEQweU5nPT0=",
    "rank_cate_social": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQWE52WTJsaGJDWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09",
    "rank_cate_highRisks": "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbU5oZEdWbmIzSjVQV2hwWjJndGNtbHpheVp6YjNKMFBYVnpaWEltYjNKa1pYSTlaR1Z6WXlac2FXMXBkRDB5Tmc9PQ=="}

if __name__ == '__main__':
    driver = co.common_start(connection_base)
    filelist = co.req_save_file(driver, file_path, base_url, cate_map)
    sin_file_name = ""
    for v in filelist:
        sin_file_name += v + ","
    print(sin_file_name)
    sys.exit()
