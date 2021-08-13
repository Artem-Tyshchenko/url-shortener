Project shorten long URL to short

The service display a page with a text field and a button in the browser. The user enters a link in the text field, the address of which he wants to shorten. When you click on the button, a shortened version of the link appears. When using a shortened version of the link, the service redirects the browser to the original page.

GET /display/<url>
Show your shorted url

GET /<shorted_url>
Redirect you to original URL with given short URL. 
If link not exist return "Url doesn`t exist"

Use flask run for run the app

For run project please provide the .env file with DATABASE_URL