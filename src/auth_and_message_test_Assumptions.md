
# Assumptions


## Assumptions for auth tests

* All functions called in tests are assumed to be working.
* Assume that registering a user also automatically log them in.
* Assume that 1122 is an invalid email address.
* Assume that you can not logout a user twice.
* Assume that you can have a same password, first name and last name as other users.

## Assumptions for message tests

* All functions called in tests are assumed to be working.
* User who create the channel automatically join the channel.
* Assume that after remove a message, the old message id become invalid.
* Assume that the message_edit function simply replace the old message with the new message.
