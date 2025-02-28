# PlasmaNet 
PlasmaNet is a simple and barebones information system modelled closely to the Tim Berners-Lee 1989 World Wide Web.<br>

PlasmaNet uses `pttp` (Plasma Text Transfer Protocol), as the method to transmit data across the PlasmaNet. `pttp` remains ambiguous in regards to its label as a "New Protocol", so do take this, aswell as other similar labels with a pinch of salt.<br>

<b>Please keep in mind, PlasmaNet is a fun toy project, meant purely for curiousity and enjoyement. I do not assume PlasmaNet is anything more then that, I made this for entertainment</b><br>
With that over, lets actually delve into PlasmaNet.
<br>

# Features
PlasmaNet features its own protocol of sorts, it also doesn't use HTML, CSS or JavaScript and cannot be rendered in any browser other then the custom built `Ion` browser, which I will explain in detail. Here is a more in depth overview:<br>
<br>

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
The response sent back to `client.py` is sent to the browser, which then parses and renders the .pst format, which will be explained in the <b>Plasma Structure Text</b> section aswell as the <b>Ion</b> section.<br>
<br>

## Plasma Structure Text
Plasma Structure Text (pst) is the static markup language made for the Plasma ecosystem. Yes, I could've used HTML, but, as mentioned this project was a fun toy side project, and the purpose was to make everything from scratch.<br>

***Hopefully that warning will excuse the poor markup abillities, sorry about that, I plan to expand it in the future!*** <br>

Before delving into syntax, It is imperitive that I explain the purpose of the heirarchy under the `pages/` directory on the host machine<br>
A website is defined by a folder, for example, to create a website called `hello.com`, you would create a folder called `hello.com` under `pages/`, this is how a website is registered on the psuedo-dns type database.<br>
`pages/hello.com/` is where you would then place the `.pst` files that make up your website.<br>

Each website should have a file called `index.pst`, your website does not need this, but it is incredibly important for this reason:<br>
If the user enters `hello.com` or `pttp://hello.com/` into the browser without specifying the page, `pttp` sends a request for all the pages under `hello.com` and then searches for `index.pst`, the default home page. If you dont have this, entering just the domain will return a 404 error.<br>

### How to use index.pst
You can have index.pst be the default page and have it display your content directly, or, you can have it automatically redirect to a page. To do this, use `@`, for example if `hello.com` has the index file and another file called `hello.pst` in it:
```
pages\
  hello.com\
    index.pst
    hello.pst
```
Your `index.pst` file would look like this:
```
@hello.pst
```
This would mean your website redirects automatically to `hello.pst` if the user types just the domain into the search bar. You could also have `index.pst` be your home default page. I reccomend using it to redirect however, just for clean code.

### Plasma Structure Syntax
pst is incredibly simplistic and barebones, which has the dual effect of giving simplicity but also limiting user control and creativity, I apologise for this, I will update pst very soon.<br>

Below is a cheatsheet-type list of the Plasma Structure Text syntax:<br>

### <ins>**Displaying Text**</ins>

•**`text><`** - This displays a line of text, contained between the `>` and `<` arrow brackets, with no newline at the end.<br>
•**`line><`** - This displays a line of text identically to the `text><` parameter, but adds a newline, can also be used between `text><` to act as a newline.<br>
•**`link<><`** - This allows you to create a hyperlink, acts analogous to the `text><` parameter, not having a newline, however, includes an argument to pass between the `<>` brackets, this being the source of the hyperlink and the text between `><` is displayed as the surface text.<br>

<ins>**Example**</ins>
```
line>Heading!<
text>Hello, <
text>World! You should <
link<example.com/switch.pst>Click Me!<
```
This page would look something like this:<br>
<hr>
Heading!<br>
Hello, World! You should <ins>Click Me!</ins> <br>

However, with only these, pst would be pitiful at best, thats where the format tags come in.<br>
### <ins>**Formatting Tags**</ins>
•**`[b=]` and `[/b]`** - These are used to set a specific font weight and to then reset it. The opening tag could look something like `[b=1000]` to set the following text to be bold.<br>
•**`[i]` and `[/i]`** - `[i]` initalises the following text to be italic, `[/i]` defines the point where text is no longer italic.<br>
•**`[u]` and `[/u]`** - `[u]` and `[/u]` are used to define underlined text.<br>
•**`[s=]`** - Used to set the pt font size, which is 16 by default, there is no closing tag technically but `[s=16]` will reset the font size to the default, which essentially acts as a closing tag.<br>
•**`[left]`, `[center]` and `[right]`** - These tags will set the alignment of the succeeding text, by default, `pst` pages are aligned to the center of the page.<br>
•**`[font=]`** - Allows you to change the font family, of which, the following are possible: <br>
<ul>
  <li>Arial </li>
  <li>Verdana </li>
  <li>Tahoma </li>
  <li>Trebuchet MS </li>
  <li>Times New Roman </li> 
  <li>Georgia </li>
  <li>Garamond </li>
  <li>Courier New </li>
  <li>Brush Script MT</li>
</ul>
Here is an example utilising all the formatting tags, note how when formatting tags are called, they must be on a new line not occupied by a display tag, the formatting tags will affect all the text under them.<br>
<br>

<ins>**Example**</ins>

```
[b=1000][u][left][s=35]
line>Awesome Page Heading<
[/b][/u][s=16]
line><
text>You should totally <
link<example.com/click.pst>click this<
[i]
text> awesome<
[/i]
line> link.<
[center][s=20]
line>Diary Entry:<
[font=Brush Script MT][left][s=16]
line>28th Febuary 2025<
[center][font=Brush Script MT]
line>I found this github repo about something called PlasmaNet?<
line>I mean, its alright- like...<
```
This example, when rendered and displayed by the Ion browser looks like this:<br>
![image](https://github.com/user-attachments/assets/367b6b4f-46d2-4475-8a7c-bda4aaa915a8)
<br>

## Ion
Ion is the browser that allows you to surf the Plasma Network, It is the only browser (as of now) that can do so, but do feel free to make a fork and create your own, any contribution is 110% welcome and appreciated.<br>
The Ion browser is rudimentry and barebones, just like the Plasma ecosystem as a whole. On entry, you will be defaulted to `pttp://main.com/main.pst`, given you just cloned the repo, if you expand on the Domain System and the pages, make sure you either remove this default redirect, or change it to one of your liking.<br>
<br>

### Loading pages
For example, if my host is running the `server.py` file with this Domain System:
```
pages\
  main.com\
    index.pst
    main.pst
```
and my default redirect is to `pttp://main.com/main.pst`, Ion will by default load the page `main.pst`, the URL bar will look like this:
![image](https://github.com/user-attachments/assets/429d538d-62cf-41e2-963e-c40f636184af) <br>
If the user types this into the URL feild:
![image](https://github.com/user-attachments/assets/42eaf6fc-bea7-4d3c-a75c-0e8e3c51f15c) <br>
Ion will load the same page, as with most browsers, the pttp:// aspect is optional when querying.<br>
Earlier, I mentioned `index.pst`, in this case, lets say our `index.pst` file looks like this:
```
@main.pst
```
If the user were to type this into the URL field:
![image](https://github.com/user-attachments/assets/f4686675-0dda-426f-8e26-070610322a9a) <br>
Ion will load `index.pst` which will immediately redirect to `main.pst`. If our `index.pst` file did not exist, typing the above would return this:
![image](https://github.com/user-attachments/assets/07bec1d9-90bd-4b41-ad8e-a7ebbd4cf926) <br>
And, like I said earlier, a Plasma website will load withou `index.pst`, given the user knows the exact page they want, which is unlikely in wide use cases, hence why adding `index.pst` to your website is highly reccomended.<br>
You can make your `index.pst` file act like any other, if the first line doesn't start with `@`, Ion will treat the file like any other, so you could just make `index.pst` your default home page, its up to you!<br>

# How to create A PlasmaNet
## Step 1:
Download the repo onto the host system and create a directory for `server.py` and `pages/` to sit in. This is what you need to run a host server.<br>
In `server.py`, you can change the port and other settings to your liking, but remember these for the next step.

## Step 2:
Still on the host system, open `client.py`, you should see these two lines at the top:<br>
```python
import socket

HOST, PORT = "Host IPv4", 8888  # IPv4 address of the computer hosting the server.py file goes in HOST
```
Now, open the command line and type in your OS ipconfig command, for example on windows, type `ipconfig` <br>
At the bottom, you should see something like this:
```
Wireless LAN adapter WiFi:

   Connection-specific DNS Suffix  . : x
   IPv6 Address. . . . . . . . . . . : x
   Temporary IPv6 Address. . . . . . : x
   Link-local IPv6 Address . . . . . : x
   IPv4 Address. . . . . . . . . . . : y
   Subnet Mask . . . . . . . . . . . : x
   Default Gateway . . . . . . . . . : x
                                       x
```
*(Actual values will be in places of the x and y on your machine, obviously I have nixed mine from the example)*
From this line: `IPv4 Address. . . . . . . . . . . : ` copy the IP beside it.
## Step 3:
Go back to your `client.py` file and replace "Host IPv4" with the copied IPv4 address, for example:
```python
import socket

HOST, PORT = "192.x.x.x", 8888  # IPv4 address of the computer hosting the server.py file goes in HOST
```
Now you have configured the client so that pttp is routed to the host system always, this means you can access your PlasmaNet from any device that has the `client.py` and `browser.py` file.

## Step 4:
From here, if you wish to surf your PlasmaNet from a computer, it must have `client.py` and `browser.py` in the same directory. The host only needs `server.py` and `pages/` in the same directory, just for example, this is how that could look<br>
<br>
***HOST COMPUTER:***
```
MyPlasmaNet\
  server.py
  pages\
    main.com\
      index.pst
      main.pst
```
***ANY CLIENT COMPUTER:***
```
SurfPlasma\
  client.py
  browser.py
```
## Step 5: Getting Online
On your Host computer, run this command:<br>
`\MyPlasmaNet> py server.py` <br>

Once `server.py` has been run on your host PC, run this command on any client:<br>
`\SurfPlasma> py browser.py`<br>

It is as simple as that! You are now surfing the PlasmaNet, given you have structured your `pages\` directory correctly, everything should work.<br>
<br>
***NOTE:*** <br>
If you git clone this repo and do the steps without changing anything under `pages\`, it will work fine, but if you clone this repo and change the website(s) under `pages\` without updating the `browser.py` file, you will run into a few errors.<br>
As mentioned, Ion redirects to `pages\main.com\main.pst`, so if you rename anything here, or delete anything, make sure you either remove this redirect feature, or update it accordingly.<br>

