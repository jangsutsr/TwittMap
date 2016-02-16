# TwittMap
The goal of this assignment is to provide you experience in developing and deploying a web application using AWS Cloud services. Your web application would collect Twitts and do some processing and represent the Twitts on GoogleMaps. Following are the required steps:  

* Use Twitter Streaming API to fetch tweets from the twitter hose in real-time.
* Use ElasticSearch or AWS CloudSearch to store the tweets on the backend
* Create a web UI that allows users to search for a few keywords (via a dropdown). The keywords (up to 10) can be of your choosing.
* Use Google Maps API(or any other mapping library) to render these filtered tweets in the map in whatever manner you want.
* Deploy your application on AWS Elastic Beanstalk in an auto-scaling environment.
* **Bonus**: Use ElasticSearch’s or CloudSearch’s geospatial feature that shows tweets that are within a certain distance from the point the user clicks on the map. 

You can choose whichever backend data services if you need any. Also feel free to choose any Web Application Framework. We've provided you with a comprehensive list of frameworks and tutorials on this page. 

Here's an example of plotting tweets on a map :  [https://worldmap.harvard.edu/tweetmap/](https://worldmap.harvard.edu/tweetmap/)
