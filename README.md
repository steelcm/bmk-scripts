## Dependencies
It's expected your system already has Python and PIP installed, the following is a list of python module dependencies:

```
pip install beautifulsoup4
pip install Pillow 
```

## Borough Market Scraper

This script will scrape trader information from the borough market website ([http://boroughmarket.org.uk]()), and assign a unique identifier to each trader. This will output the data in JSON format to the file `scrape.json`.

``` python boroughmarket-scaper.py ```

## Avatar Scraper

Iterates through the borough market traders and extracts the social media name from the URL, it then uses this name to download the avatar from [https://www.avatars.io/]() and rename using the unique identifier of the trader.

``` python avatar-scraper.py ```
