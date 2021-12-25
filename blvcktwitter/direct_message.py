import tweepy

# Authenticate access
auth = tweepy.OAuthHandler("cGoEPcAFLRV7yho8OFsVnzVge", "Tl9Bl3o5DyvzRbO8tgrN7GROuNeDONVLwmBYTgTeOFdyE7oGGA")
auth.set_access_token("1572023088-h4Qney3hlDyAdxkHn5FVHXRqCKKrzQoTNazP6UE", "VHdE6EQ5R50SrIrCvcFa4bnzzer0iVgi75XVcUUAjkotg")

# Create API handler
api = tweepy.API(auth)

messages = api.list_direct_messages(count=5)
for message in reversed(messages):
  # who is sending?  
  sender_id = message.message_create["sender_id"]
  # what is she saying?
  text = message.message_create["message_data"]["text"]
#Note reciepnt id is a numerical value and to get that do this
user = api.get_user("username")
recipient_id = user.id_str

api.send_direct_message(recipient_id, "Hola hola, this pvrple blvck twitter bot")
