# GeoGuessr-Bot (w/ Discord Integration!)

A bot that allows users to create GeoGuessr game links automatically.

This bot can be run though CLI or can be run as a discord bot!

## Requirements
<ul>
<li>Python 3.5+</li>
<li>Selenium</li>
<li>Discord.py</li>
<li>A browser, preferably Google Chrome. (To use other browsers, change the selenium initializations respectively</li>
<li> <a href="https://sites.google.com/a/chromium.org/chromedriver/downloads">Latest version of chromedriver</a> (only if you are using Google Chrome with Selenium)</li>
<li> <strong><em>GeoGuessr Pro Account</em></strong> </li>
<li> Heroku (or your own hosting service) for hosting the discord bot. Skip this requirement if you want to run the bot on your location machine. </li>
</ul>



## Installation for Heroku
<strong>
To make the bot work as a discord bot, you need to make a discord bot and get your own token. Please visit the Discord Developers site for more information.</strong>

<p> </p>

This bot was updated to run on a hosting service like Heroku. Below are the steps to set up the bot on Heroku. To host on your own hosting service, please make sure to use environment variables for keys and tokens.

1. Create an account on Heroku.
2. Create a new app from the Heroku Dashboard.
3. Choose your app name.
4. Choose your deployment method and deploy this code. Using the Heroku CLI is recommended.
5. In Settings, configure `CHROMEDRIVER_PATH`, `GOOGLE_CHROME_PATH`, `PASSWORD`, `USERNAME`, and `TOKEN`. ![image](https://user-images.githubusercontent.com/51961095/123005787-b0c86900-d384-11eb-8da8-5dbcc7da8cd2.png)
6. In Settings, configure the following heroku buildpacks
  ```
  heroku/python
  https://github.com/heroku/heroku-buildpack-chromedriver
  https://github.com/heroku/heroku-buildpack-google-chrome
  ```
7. Check the log and see if your build is successful.
8. Go to Deploy and manually deploy the app.


## Installation for Location Machine (Discord Version)
<strong>
To make the bot work as a discord bot, you need to make a discord bot and get your own token. Please visit the Discord Developers site for more information.</strong>
<p> </p>

1. Install Python 3.5 or higher. Verify your python version with `py --version`
2. Install the `requirements.txt` with pip. Use this command: `pip install -r requirements.txt`. Make sure your command prompt is open where the requirement.txt file is located.
3. Install the <a href="https://sites.google.com/a/chromium.org/chromedriver/downloads">latest version of chromedriver</a>.
4. Go to secret.py and edit the file to include the path of the chrome driver, GeoGuessr username, and GeoGeussr password.
    ```
    PATH = "put chrome driver path here"
    username = "put GeoGuesser username here"
    password = "put GeoGuesser password here"
    token = "put token here"
    ```
 5. Go to `geoguessr.py` and add the import `from secret.py import *`
 6. Go to the `def login()` function in  `geoguessr.py` and change `emailField` values and `passKey' values.` ![image](https://user-images.githubusercontent.com/51961095/123002031-6bee0380-d37f-11eb-8cbe-dd5c858d6490.png)
 7.  Go to the bottom of `geoguessrdiscordbot.py` and change the `client.run` value to to `token`. ![image](https://user-images.githubusercontent.com/51961095/123004861-38ad7380-d383-11eb-9b42-b92c962a2c20.png)
 8.   Go to `geoguessrdiscordbot.py` and add the import `from secret import *`


## Installation for Location Machine (CLI Version)
1. Install Python 3.5 or higher. Verify your python version with `py --version`
2. Install the `requirements.txt` with pip. Use this command: `pip install -r requirements.txt`. Make sure your command prompt is open where the requirement.txt file is located.
3. Install the  <a href="https://sites.google.com/a/chromium.org/chromedriver/downloads">latest version of chromedriver</a>.
4.  Go to secret.py and edit the file to include the path of the chrome driver, GeoGuessr username, and GeoGeussr password.
```
PATH = "put chrome driver path here"
username = "put GeoGuesser username here"
password = "put GeoGuesser password here"
token = "put token here"
```
2. Go to `geoguessr.py` and add the import `from secret import *`
3. Go to the `def login()` function in  `geoguessr.py` and change `emailField` values and `passKey' values.` ![image](https://user-images.githubusercontent.com/51961095/123002031-6bee0380-d37f-11eb-8cbe-dd5c858d6490.png)


## Using the Bot
### Discord Version
After installing the Discord version of this bot, using the discord version is very simple. Make sure the Discord bot you created through the Discord Developers portal is invited to the server you want to use this bot on. Also make sure everything is installed and ready to go. Note: running the discord bot script on local machine will require you to install the bot differently than using the bot through a hosting service. Please refer to the installation guides above for details.

#### Bot Commands
To play a game of Geoguessr:
```
  -geo [map] [rule]
  -g [map] [rule]
  -game [map] [rule] 
```

To get a list of maps:
`-maps`

To get a list of options(rules):
`-options`

For more information regarding commands:
`-help`

For author information:
`-author`

### Notes:
* The help command is very usefull and will help users figure out how to use the bot efficiently.
* Maps are all hardcoded in `inputs.py`. You can add onto the `maps{}` section with any type of map you can find. See more below.
* Custom Maps can be used. However, you will need to manually add an if statement to the `inputs.py` so the bot understands to read the custom map. Add custom maps in the `maps{}` section.
 
    ```
    #custom map aliases
    "urban-world-nobrr",
    "diverse-world",
    ```
    Then add an if-statement to the `checkCustom()` function to bind the hash value of the custom map with your own alias. (Do not use spaces)
    
    ```
    def checkCustom(map):
        if map == "urban-world-nobrr":
            map = "5e818e96b3ec17842c0bcce8"
            return map
        if map == "diverse-world":
            map = "59a1514f17631e74145b6f47"
            return map
        else:
            return map
    ```


### CLI Version 
<strong> Note: Version 0.2-alpha integrated the Discord API, therefore some funcitionality of the CLI version was changed. A future update will make the installation and usage process smoother. </strong>

1. Open a new command prompt window or terminal window. Make sure you have python installed.
2. Check the inputs.py to see all the maps and rules that you can use.
3. Run the script in command prompt or terminal. To run the script, use the following syntax:
```
python geoguessr.py [map] [rule]
```
3. Enjoy the game! You can `Press X to close program` after you grabbed the game link from the command line. Below is a sample output of the program.

```
Output:
Bot Initialized
GeoGuessr login successful.
Enter the Map you want and rule: usa nm
Game link generated:
https://www.geoguessr.com/challenge/wYjPeOmTi2oDmZ7K

```

### Notes:
* Maps are all hardcoded in `inputs.py`. You can add onto the `maps{}` section with any type of map you can find. See more below.
* The script needs two arguments to run. `[maps]` is the name of the map you would like to play. `[rule]` is the rule you want to set for the GeoGuessr game. You can find each rule below:
  #### Game Rules
  ```
  default = default
  no move = nm
  no zoom = nz
  no move, no zoom = nmnz
  no move, no pan, no zoom = nmnpnz
  
  ```
  Example of using the bot:
  ```python geoguessr.py usa nm```
 * Custom Maps can be used. However, you will need to manually add an if statement to the `inputs.py` so the bot understands to read the custom map. Add custom maps in the `maps{}` section.
 
    ```
    #custom map aliases
    "urban-world-nobrr",
    "diverse-world",
    ```
    Then add an if-statement to the `checkCustom()` function to bind the hash value of the custom map with your own alias. (Do not use spaces)
    
    ```
    def checkCustom(map):
        if map == "urban-world-nobrr":
            map = "5e818e96b3ec17842c0bcce8"
            return map
        if map == "diverse-world":
            map = "59a1514f17631e74145b6f47"
            return map
        else:
            return map
    ```
    
  
### Final Comments
This bot is still very much in development. If you have any suggestions or bug reports, please let me know!
_______________________________________________________________________________

## Update 5/17/2022
This bot is severely broken, however I have been working on this project from time to time. Looking up update the GeoGuessr link generation code, but I am probably discontinuing the discord integration as I do not intend to make a separate GeoGuessr bot at this time.

## Release Version 0.2-alpha
Version 0.2-alpha features the integration of the Discord API! This GeoGuessr bot can now be run as a discord bot!

### Features:
+ New Discord integration!
+ Beautiful Discord commands.
+ Better error checking.
+ New official maps!
+ Heroku support.

### Fixes
* Fixed an error where the bot would crash after generating links for a certain period of time.
* Fixed an error that would not generate the correct links based on user input since the game rule settings was displayed.

### Feature Release Plans:
* Add time game rule for GeoGuessr game link generation.
* Add the ability to link game maps and create game links.
* Add more Discord features.
_______________________________________________________________________________
## Release Version 0.1-alpha

### Features
* Create GeoGuessr game links with most official maps!
* Customize GeoGuessr games with the default settings or with game rules. (Except time)

### Future Release Plans:
* Discord API Integration
* Add time game rule for GeoGuessr game link generation.
* More user customization features such as adding new maps. 
* Better error checking.
