<h1> Assumptions (T18A-WELV)</h1>

<h4> Channel Test Assumptions</h4>

* All functions called in tests are assumed to be working
* Assumes that registering a user does not log them in 
* All variables with "_id" suffix: 0 is an invalid id (For testing purposes)
* If a member creates a new channel (Using channel_create) then they are automatically added as an owner
* List "messages" from channel_messages contains all the messages in the channel
* Channels can have a name ""
* Assumes that if you're not a member of a channel, you're not an admin

<h4> Assumptions for auth tests</h4>

* All functions called in tests are assumed to be working.
* Assume that registering a user also automatically log them in.
* Assume that 1122 is an invalid email address.
* Assume that you can not logout a user twice.
* Assume that you can have a same password, first name and last name as other users.

<h4> Assumptions for message tests </h4>

* All functions called in tests are assumed to be working.
* User who create the channel automatically join the channel.
* Assume that after remove a message, the old message id become invalid.
* Assume that the message_edit function simply replace the old message with the new message.

<h4>  Assumptions for user tests </h4>
* assume valid users are the ones having an existing user_id
* 
