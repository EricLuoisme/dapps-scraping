import sys

import common_own as co

connection_base = "https://dappradar.com/rankings"
base_url = "https://dappradar.com/v2/api/dapps?params="
file_path = "/Users/pundix2022/Juypter Working Env"

cate_map = {}
cate_map[
    "rank_top_all"] = "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbk52Y25ROWRYTmxjaVp2Y21SbGNqMWtaWE5qSm14cGJXbDBQVEky"
cate_map[
    "rank_eth_all"] = "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWxkR2hsY21WMWJTWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09"
cate_map[
    "rank_polygon_games"] = "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMXdiMng1WjI5dUptTmhkR1ZuYjNKNVBXZGhiV1Z6Sm5OdmNuUTlkWE5sY2ladmNtUmxjajFrWlhOakpteHBiV2wwUFRJMg"

if __name__ == '__main__':
    driver = co.common_start(connection_base)
    filelist = co.req_save_file(driver, file_path, base_url, cate_map)
    sin_file_name = ""
    for v in filelist:
        sin_file_name += v + ","
    print(sin_file_name)
    sys.exit()
