from selenium import webdriver
import proxy
import header_modifier

selenium_proxy = webdriver.Proxy()
browser_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def run_test():
    # add to proxy
    from selenium.webdriver import DesiredCapabilities
    capabilities = DesiredCapabilities.CHROME
    selenium_proxy.add_to_capabilities(capabilities)

    # prepare request
    options = webdriver.ChromeOptions()
    options.binary_location = browser_path
    options.add_argument('headless')
    options.add_argument('window-size=1200x900')

    driver_path = "/Users/pundix2022/Juypter Working Env" + '/chromedriver'
    d_driver = webdriver.Chrome(driver_path, chrome_options=options)

    base_req_url = "https://dappradar.com/v2/api/dapps?params="
    special_code = "UkdGd2NGSmhaR0Z5Y0dGblpUMHhKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptWmxZWFIxY21Wa1BURW1jbUZ1WjJVOVpHRjVKbk52Y25ROWRYTmxjaVp2Y21SbGNqMWtaWE5qSm14cGJXbDBQVEky"

    d_driver.get(base_req_url + special_code)
    print(d_driver.find_element_by_xpath("/html/body").text)
    d_driver.quit()


if __name__ == '__main__':
    from proxy.common import utils

    proxy_port = utils.get_available_port()
    with proxy.start(
            ['--host', '127.0.0.1',
             '--port', str(proxy_port),
             '--ca-cert-file', '/test/mitm/wec-ca.pem',
             '--ca-key-file', '/test/mitm/wec-ca.key',
             '--ca-signing-key-file', '/test/mitm/wec-signing.key'],
            plugins=
            [b'header_modifier.BasicAuthorizationPlugin',
             header_modifier.BasicAuthorizationPlugin]):
        from selenium.webdriver.common.proxy import ProxyType

        selenium_proxy.proxyType = ProxyType.MANUAL
        selenium_proxy.httpProxy = '127.0.0.1:' + str(proxy_port)
        selenium_proxy.sslProxy = '127.0.0.1:' + str(proxy_port)
        print('Proxy address: ' + selenium_proxy.httpProxy)
        run_test()
