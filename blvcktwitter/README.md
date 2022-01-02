# Well ,the simplest way to go about this would be to do it like this...

### This app is going to

> Create a tweet

>check timeline

>get username ,details

>follow a user

> like most recent tweet
> see blocked contacts

> search for a tweet

### First you would need to install twitterAPI using pip(windows)
> pip install twitterAPI
### then import it as well as json
> from TwitterAPI import TwitterAPI
import json
> Now we need to assign our keys inorder to access the api and be able to send messages and whatnot
> But first we need to create a twitter app,where we get our api's
> I wont go into too much detail,but if you go to your twitter settings>scroll down to developers>
> It takes you to a developer plaform,where you create a twitter app which automatically create consumer key/secret
> Below that,you will see a button to generate access token,copy all that and save them somewhere safe.
### Remember to always keep these private and i find the best way to do this is by creating a separate file
> .env . and importing these into your main file is as simple as e.g(access_token=os.getenv('name_of_the_string'))
> And of course we have to (import os) first
> From here on,everything is simple


```api = TwitterAPI(<consumer key>,
                 <consumer secret>,
                 <access token key>,
                 <access token secret>)

user_id = <user id of the recipient>
message_text = <the DM text>

event = {https://developer.twitter.com/en/portal/dashboard
    "event": {
        "type": "message_create",
        "message_create": {
            "target": {
                "recipient_id": user_id
            },
            "message_data": {
                "text": message_text
            }
        }
    }
}

r = api.request('direct_messages/events/new', json.dumps(event))
print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text) 
```



# Now, in this project i am going to use tweepy to familiarize myself with it
                   
### And as always the first is to apply for a twitter dev account at  (https://developer.twitter.com/en/portal/)

