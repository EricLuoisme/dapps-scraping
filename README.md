# DApps-Scraping

The main objective of this project is to study and analyze the quality of the decentralised applications available in some public repositories. This project scrapes the DApps websites and repositories such as State of the DApps and DAppRadar.

The extracted datasets are available in Zenodo: https://zenodo.org/record/3382127. 
A long-term observation dataset is tracked here: https://github.com/serviceprototypinglab/dapps-dataset

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
To acquire the required DApps metrics from websites, we have used the package Selenium which along with a custom driver and a corresponding web browser will have to be set up correctly.

```bash
pip install -r requirements.txt
```
The used python package Selenium requires a chrome driver to be downloaded. Please downloaded following the below URL.

(https://chromedriver.chromium.org/downloads)

For Linux and Mac OS users, run the following script to download the chrome driver:

```bash
./download.sh 
```
#### Please make sure that the version of you chrome is 76, otherwise update your chrome or install the chrome driver for your version.

For Mac users, please make sure you have wget installed in your system, use the following command to install it:

```bash
brew install wget 
```

Once the driver is downloaded, please check the path of the chrome driver to both scripts (DappRadar.py, stateDapps.py).
if you have downloaded the chrome driver manually, please change the path specified in the codes to your own path. You don't have to change the path if you have used the script to download your driver.

Note: Google Chrome must also be present in the corresponding version. See the text file downloadchrome.doc for details.
Use Chrome for debugging as well - in case the web pages change structure, type Ctrl+Shift+I and use the pointer tool with Ctrl+Shift+C to find out the new XPath expressions.

## Usage

There is one Python script per DApps website.
 - DappRadar.py: for dappradar.com
 - stateDapps.py: for www.stateofthedapps.com
 - dappcom.py: for dapp.com

To run the script (shown with the example of DappRadar), use the following command:

```bash
python DappRadar.py
```
For testing purposes you can specify the number of pages you want to scrape. The command below crawls only three pages.

```bash
python DappRadar.py 3 
```

You may specify fractional pages; i.e., as there are typically 50 entries per page, specifying 0.1 will fetch metrics on 5 DApps.

The scraping time depends on the number of the pages, and it may take 1 to 2 hours to fully run the script.
Once the extractions are done, the scripts will generate plots from the extracted data and automatically save them in a folder with the website name and date of the run.

You can customise the scraping by adding additional parameters: 'nosocial', 'noplot'
This is again primarily of interest for testing.

## Disclaimer
Be aware that web scraping is considered a bad practice. Please be advised that this was created for research and education purposes only.
Ask us to share our crawling data rather than crawling on your own without strong reason.
