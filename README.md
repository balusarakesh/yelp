This web scraping project helps to collect data from Yelp(http://www.yelp.com/) website and store it in your database. 

How to use:
 - setup your DB in the yelp/settings.py, if not set then a default DB will be used locally.
 - run the command "./manage.py runserver".
 - goto the url "http://localhost/collector" and start collecting data.
 - Example: 
   - if places = "restaurants, coffee" and locations = "san jose, san francisco"
   - for the above places and locations this app can collect all the restaurants and coffee places in San Jose and San Francisco.
 **WARNINGS
  - Yelp doesn't show more than 1000 results and this app can only collect what's hosted on yelp.com.
  - This may also collect data from surrounding cities too.

Any feedback is appreciated.
Please post any issues you have in the tickets or you can email me - rakesh8015@gmail.com

