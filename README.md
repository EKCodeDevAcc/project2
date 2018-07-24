# Project 2

This is Edward Kang's Project 2.

This is a chat application allows users to login, logout, create, remove channels and send message to other users in same chat.

README.md
- Include a short writeup describing the project, what's contained in each file.

application.py
- Get username, channelname, chats.
- Store those information (Store 100 most recent messages per each channel).
- Check login status, joined channel status and send it back to a page when users request those.
- Select chats belong to selected channel and select chats meet the condition and send it back to the page.
- Update, delete channel items.
- Check duplication of username and channelname.
- Remember display name and previous channel name and bring users back to their page.
- All features get updated asynchronously.
- I assumed this app is used while the app itself does not get closed, so disabled certain features like deleting usernames when users logged out, or remove session when app is closed.

index.html
- Users can login and see their username, they can also logout.
- Once users login, they can create new channel (if input channel name is duplicate, alert to the user).
- After channel list get updated asynchronously, user can select any channel.
- If a channel got selected, users can see chats of the channel.
- Chats display timestamp, username, and messages.
- All users in the same channel can see the new message without reloading the page.

Personal Touch
- After user input username, channelname, or messages, they can just hit enter key to submit instead of click buttons with mouse.
- Depends on login status, display login box only, or display logout box, lists of channels and chats.
- Display currently selected channel name.

style.css
- It is css file for basic design of this website.

Milestone 1
- Users should be prompted to type in a display name. :fa-check-square:
- When users returns to your app later, the display name should still be remembered. :fa-check-square:
- Any user should be able to create a new channel, so long as its name doesn’t conflict with the name of an existing channel. :fa-check-square:
- Users should be able to see a list of all current channels. :fa-check-square:
- selecting one should allow the user to view the channel. :fa-check-square:

Milestone 2
- The user should see any messages that have already been sent in that channel, up to a maximum of 100 messages. :fa-check-square:
- Your app should only store the 100 most recent messages per channel in server-side memory. :fa-check-square:
- Once in a channel, users should be able to send text messages to others the channel. :fa-check-square:
- When a user sends a message, their display name and the timestamp of the message should be associated with the message. :fa-check-square:
- All users in the channel should then see the new message appear on their channel page. :fa-check-square:
- Sending and receiving messages should NOT require reloading the page. :fa-check-square:

Milestone 3
- Your application should remember what channel the user was on previously and take the user back to that channel. :fa-check-square:
