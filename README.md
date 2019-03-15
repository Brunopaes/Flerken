## Flerken - An triggered bot ##

Optmised for python 3.6.

This project is aimed on entering on the 'ingresso.com' website and verifying 
if the pre-released tickets are already available to buy.

----------------

### Project's Structure ###

- __data:__ log files:
    - __log_all:__ status code - 200
    - __log_error:__ status code != 200
    - __recipients:__ list of email address

- __doc:__ documentation & application requirements.

- __src:__ source code (scripts).

----------------

### Modules ###

- __Scraper:__ Class responsible for entering on the website and verifying if the tickets are already available to buy.
- __SendMail:__ Class responsible for sending the email to an mail-list.

----------------

### Python requirements ###

In your python environment, run the following command:

`pip install requests bs4`

or access the doc directory _(./doc)_ and run the following command:

`pip install -r requirements.txt`

----------------

### Usage Notes ###

For running the script on terminal/cmd, access the project directory _(./src)_ and run the following command:

`python scraper_movie.py`

_obs: you must be inside the scr directory._

----------------

### References ###

- [__List of HTTP status codes__](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)

----------------
