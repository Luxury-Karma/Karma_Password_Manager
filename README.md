# Karma Little Password Manager 
    
    - What is this for : 
        This is for someone who can host a password manager on his network for him and other people.
    
    - Why does this exist : 
        I personally belive that we should control our own data and stop using big corporation to keep it safe
    
    - How does this work : 
        By creating a password manager webserver (backend python with a SQL db). 
        The server will generate a webpage (Duh) where user can connect.
        Once connected the user can see all the website he added to his db and can ask to receive the for any of them
        The server will not send anything related to the password without the direct demand of the client.


# Security feature
    the Application will do all the decryption and encryption on the client side.
    This way the onlything moving betweenn the server and the client are allready encrypted data. 
    It might protect against a man in the middle attack.
    
    The Server owner does not keep the master password nor any particullar data to be able to easily get the 
    user password. The server keep a hashmap for the loggin 


# How To Setup
    TBD