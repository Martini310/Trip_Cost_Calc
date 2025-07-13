# Trip Cost Calc

Python application to calculate cost of a car trip based on fuel prices in your neighbourhood.

## 🚀 New PWA Version Available!

A modern Progressive Web App (PWA) version is now available with Next.js frontend and Python backend. Check out [README_PWA.md](./README_PWA.md) for details.

**Quick Start (PWA):**
```bash
npm run install:all
npm run dev
```

## 🐳 Docker Deployment Ready!

The backend is now containerized and ready for deployment on mikr.us or any Docker-compatible platform. See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment instructions.

**Quick Deploy:**
```bash
# Build and deploy to mikr.us
./deploy.sh your-mikrus-registry latest
```

## Content of project
* [Application view](#application-view)
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Functionalities](#functionalities)
* [Inspiration & Sources](#inspiration--sources)
* [Contact](#contact)

## Application view

<img src='https://user-images.githubusercontent.com/108935246/206874249-4b3cb9af-48d4-4ef0-a5fc-e1541d4d561e.png' width='50%' height='50%'>

<img src='https://user-images.githubusercontent.com/108935246/206874251-efe84db2-b442-94ca-63aa724b3796.png' width='50%' height='50%'>

## General info

Trip Cost Calc (yeah, I know, this name is not brilliant..) was generally created to calculate cost of a car trip.
While writing it I extended it with several functionalities. So, for now it shows following data:
* **Cost** *of the trip in PLN*
* **Time**
* **Distance**
* **Fuel price**
* **Visibility**
* **Cloudiness**
* **Map** *with an overview route*

## Technologies

* Python 3.10.5
* Kivy 2.1.0
* Dotenv 0.21.0
* Requests 2.28.1
* Beautifull Soup 4.11.0
* GoogleMaps API
* OpenWeatherMap API

## Setup

#### Google API

First of all insert your **Google API KEY** in ```.env``` file.<br>

```commandline
API_KEY= YOUR_API_KEY
```

or insert it directly in variable in ```backend.py```:

```commandline
self.api_key = 'YOUR_API_KEY'
```
If you don't have an API KEY from Google or you don't know what is that, look up 
[**here**](https://developers.google.com/maps/documentation/javascript/get-api-key) 
for more details.
<br><br><br>
#### Weather API
You will also need an **[OpenWeatherMap](https://openweathermap.org/api) API**. <br>
Similarly put it in ```.env``` file:
```commandline
WEATHER_API= YOUR_API_KEY
```
Or directly in ```backend.py``` code:
```commandline
self.w_api_key = 'WEATHER_API'
```
<br><br>
To run app correctly you'll also need some extra modules.<br>
Let's install them via ```pip``` module:<br>
* For **Kivy** module run this line in your terminal:
```commandline
python -m pip install "kivy[base]" kivy_examples
```
&ensp; to install the current stable version of ```kivy``` and optionally ```kivy_examples```
from the kivy-team provided PyPi wheels. <br>
&ensp; If you want another configuration of Kivy visit
[this page](https://kivy.org/doc/stable/gettingstarted/installation.html).
<br><br>

**DOTENV**

* If you will import Api keys from ```.env``` file, install a package, if not skip this:
```commandline
pip install dotenv
```
<br>

**REQUESTS**

* Another necessarily module is ```requests```:
```commandline
pip install requests
```
<br>

**Beautigull SOUP**

* Next one, to parse a web page with fuel prices is Beautifull Soup:
```commandline
pip install beautifulsoup4
```
<br>

*Now you can run the script and everything should work properly.*
<br><br>
### Creating a package for Windows/Mac/iOS/Android

This topic is more complicated. To describe all steps for each platform, this readme would be few times longer, but 
luckily Kivy authors did all the job and 
[**here**](https://kivy.org/doc/stable/gettingstarted/packaging.html)
is all you need to deploy the app on a chosen platform.

## Functionalities
Interface of the App is as simple as possible. Only 4 steps are needed to get full information.
1. #### Start address
    - A place where you want to start your trip. Put here a city, coordinates or full address, 
   just like you do it on Google Maps.
2. #### Destination
    - Finnish of a trip
3. #### Consumption
    - An average fuel consumption on 100km of your car. Slider step is 0.1l.
4. #### Fuel price
   1. 
       - There are 5 types of fuel to choose from. An app checks the average price of a checked fuel type in user
      voivodeship based on geolocation.
      [Web page with fuel prices](https://www.autocentrum.pl/paliwa/ceny-paliw/). If there is a problem with determining
      user's location, an average price from country will be used instead.
   2. 
      - Second way is to set fuel price manually using slider. Step of the slider is 0.01 PLN.

Finally click **_Oblicz_** and wait for the results!

## Inspiration & Sources

Inspiration to do this app was a tutorial from **Kacper Sieradziński** on his YouTube channel. 
[link](https://www.youtube.com/watch?v=Yt6TrXT-ZH4)<br>
Also my family was helpful. Especially their comments about *when I will finally create something useful!* ;) 

Making this App wouldn't be possible without some help:<br>

&emsp;&emsp;The Kivy series by ```Codemy.com``` on **YouTube**<br>
&emsp;&emsp;A good documentation of a ```Kivy``` was also helpfully.


## Contact
If you have any questions or ideas for development fell free to contact me via email:<br/>
```maritn.brzezinski@wp.eu```
