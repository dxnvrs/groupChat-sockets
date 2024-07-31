# groupChat-sockets
*its not finished yet. need to work on [WinError 10057] that appears in serverChat.py and others minor errors.*

- This repository contains my project for the computers' networks class.
- It consists in two .py archives (client.py and serverChat.py).

  This project was made using sockets and threads to make an application that resambles a chat app that have following fuctions:
  * Login - all users have to sign up to use the chat;
  * Private chats - users can send private mensages to any other user that has already signed up in the chat;
  * Groupchats - users can also send mensages to groups that they are in;
  * Create groups - users can create groupchats, add other users and also remove them;
  * Users' profiles - users can see others users' profiles and it contains the name, email and ip address of said user;
  * Send media archives - users can send videos, photos and audios in private chats and groupchats.
 
  An graphic interface was also implemanted using the PySimpleGUI library. In total, these are all the libraries that were used in the project: socket, threading, time, os and PySimpleGUI (only PySimpleGUI isn't native to Python).
