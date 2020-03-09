<h1> Assumptions (T18A-WELV)</h1>

* All functions called in tests are assumed to be working
* Assumes that registering a user does not log them in 
* All variables with "_id" suffix: 0 is an invalid id (For testing purposes)
* If a member creates a new channel (Using channel_create) then they are automatically added as an owner
* List "messages" from channel_messages contains all the messages in the channel
* Channels can have a name ""
* Assumes that if you're not a member of a channel, you're not an admin