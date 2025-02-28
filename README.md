# PlasmaNet 
PlasmaNet is a simple and barebones information system modelled closely to the Tim Berners-Lee 1989 World Wide Web.<br>

PlasmaNet uses `pttp` (Plasma Text Transfer Protocol), as the method to transmit data across the PlasmaNet. `pttp` remains ambigous in regards to its label as a "New Protocol", so do take these labels with a pinch of salt.<br>

<b>Please keep in mind, PlasmaNet is a fun toy project, meant purely for curiousity and enjoyement. I do not assume PlasmaNet is anything more then that, I made this for entertainment</b><br>
With that over, lets actually delve into PlasmaNet.
# Features
PlasmaNet features its own protocol of sorts, it also doesn't use HTML, CSS or JavaScript and cannot be rendered in any browser other then the custom built `Ion` browser, which I will explain in detail. Here is a more in depth overview:

## Plasma Text Transfer Protocol (pttp)
As mentioned earlier, this protocol is unique, not using https. This carries with it a risk, due to the lack of encryption using a standard https module would provide.<br>
pttp works identical to https, infact, less so as it only features one request type: `GET`. This is specifically hardcoded for getting pages and websites and is stuctured tightly around the Ion browser.<br>

The host computer features two things, `server.py` and the `pages/` directory, thats all it needs.<br>
The client, or user, surfing the PlasmaNet needs only `client.py` and `browser.py`.<br>

When the client enters a url into `browser.py`, for example "pttp://main.com/main.pst", the browser invokes `client.py` and passes the domain and page.<br>
```
Browser -> "pttp://main.com/main.pst" -> Domain: "main.com" Page: "main.pst"
```
After this, `client.py` attempts to connect to the host computers IP and Port.<br>
<i>(`client.py` needs to have the host IP to connect. I will explain how to set this up later)<br></i>

Once the client successfully connects a socket to the port and IP, `pttp` comes into use. The client will send the request across the socket to the Host.<br>

The host computer should be running `server.py` throughout this process. This server will listen continously on the given port for information.<br>
In our example, `server.py` will be given this request: `GET main.com/main.pst`, following this request, the server will go to the `pages/` directory, which should be in the same location as the server, if its in a different location, just change the hardcode in the file.<br>
`server.py` does this in our example:
```
SEARCH pages/ FOR main.com/
IF FOUND
  SEARCH main.com/ FOR main.pst
```
This is just an abstracted outline of what it does, in essence, it just looks into the directories to check the existence for both the domain(website) and the page.<br>
If it finds both the website and page specified, it gets the content of the file, and sends it back to `client.py`, which during this whole time has been listening on the port for the content.<br>
The response sent back to `client.py` is sent to the browser, which then parses and renders the .pst format, which will be explained in the <b>Plasma Structure Text</b> section aswell as the <b>Ion</b> section.

## Plasma Structure Text

## Ion

## Domain System
