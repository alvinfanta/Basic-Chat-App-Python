
# Basic Chat App Python

Project to learn basic networking (Server and Client) and network handling.
## Installation

### Server side

    1. Install server.py
    2. Run server.py
    3. Server's on! (Currently port is set to 23901)

### Client side

    1. Install Client.py
    2. Run Client.py
    3. Enter server's IP
    4. Enter server's port
    5. Enter your username
    6. Enjoy chatting!
    
## FAQ

#### How does this work?

The server is set to listen to multiple connections. When there are new connections, the server will create a new thread. Every message that's sent to server will be broadcasted to every client that's not the author.

#### Can I use this with people outside of my network?

Yes. While it is possible to connect to the server from outside of it's network, there are still extra steps to it. If possible, you can try forwarding the server's port. But if it's not possible, the workaround is you run ngrok or other tunneling agent that gives you a public ip that can access your server.

### Are there any chatlog in this program?

For now, no. I might add this in the future if I decided to keep working on this project.
## Authors

- [@alvinfanta](https://www.github.com/alvinfanta)

