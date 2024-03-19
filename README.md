# Karma's little Password manager
 Karma's little password manager The objectif of this password manager is an easy way to keep your password safe and back up.

# HOW TO SET UP THE GOOGLE CLOUD 
    1 : go to this website and use your own google account : https://console.cloud.google.com/
    
    2 : Create a new project (name does not mather)
    
    3 : Go at APIs & Services and in OAuth consent screen
    
    4 : If like me you're poor and do not work at google use the External app and press create
    
    5 : fill the with the requested information
    
    6 : go in credentials click on CREATE CREDENTIALS and create a new API key
    
    7 : edit the API key. Restrict the API key to Google Drive API.
    
    8 : Go back and click CREATE CREDENTIALS and Oauth Client ID
    
    9 : name the OAuth client ID as you like and give the type Web Application and redirect the URL to the URL the website will
    be on. For exemple : https://127.0.0.1:5000/authorize. This will tell google where to bring the client once the login is done
    
    10 : Download the secret as a JSON format. (IN NO CIRCUMSTANCE YOU SHOULD SHARE IT ON THE WEB KEEP IT SAFE.)
    
    11 : click on CREATE CREDENTIALS and on Service Account. This account will be use to make the backup automated. 
    
    12 : name it as you like. Give it access to the project you are working on and I would argument to grant access to yourself.

Now the google part is all set up for the app to work. The next part is to make it more secure. In this state I am unsure of the security of this app on the open web.
I would recommend doing the next step to make it more secure. But in theory the app work from this point. 

# How to set up the VPN access
TBD
# How to set up the DOCKER
TBD