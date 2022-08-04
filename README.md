**Python Discord Summer Code Jam 2022** submission from the team **KinglyKelpies**.
Using the technology Websockets and the theme *Its not a bug its a feature*

# *for level_id in range(14)*
<p align="center">
    <img src="https://user-images.githubusercontent.com/62175543/182180722-6496cbdc-d033-41fd-ae5c-936ad99b635b.gif">
</p>

## What is this?
    
A simple multiplayer puzzle game, 
in which your aim is to reach the goal by pressing buttons, standing on plates and moving boxes.
    
Together with a friend!

*But some say that a few bugs snuck in...*

# Table of contents
1. [Quick instructions](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#quick-instructions)
2. [Video description](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#video-description)
3. [Installation](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#installation)
4. [How to run](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#how-to-run)
5. [How to join a game](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#how-to-join-a-game)
6. [How to play](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#how-to-play)
7. [Help i softlocked myself\!](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#help-i-softlocked-myself)
8. [Credits](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#credits)
9. [Previews](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#previews)
10. [Spoilers](https://github.com/Kingly-elpies/KinglyKelpies/blob/main/README.md#spoilers)

# Quick instructions
1. [Get a friend!](https://www.wikihow.com/Have-Friends)
2. Have [python 3.10](https://www.python.org/downloads/release/python-3100/) installed.
3. You both install the game by running:
    ```shell
    $ git clone https://github.com/Kingly-elpies/KinglyKelpies
    $ cd KinglyKelpies/
    $ pip install -r dev-requirements.txt
    ```
4. Run the game:
    ```shell
    $ python main.py
    ```
5. One player hosts on a port, the other joins as client on ip:port
6. use `w`,`a`,`s`,`d` to move 
8. reach the blue arrow to win!
<img height=48 width=48 align="top" src = "https://user-images.githubusercontent.com/62175543/182195574-53a3c7ea-7551-457a-81cf-539b1fbcec96.png"></img>
    
# Video description

Disclaimer: The video contains Spoilers

<details>
    <summary>Click here to expand</summary>
    https://www.youtube.com/watch?v=-VQ_ijuo-Mg
</details>

# Installation

### 0. Requirements:
   - [python 3.10](https://www.python.org/downloads/release/python-3100/)

### 1. Download:
   Run this command in the directory you want to download it to.
   ```shell
   $ git clone https://github.com/Kingly-elpies/KinglyKelpies
   ```
    
### 2. Install the dependencies:
  In the `/KinglyKelpies` directory run:
  ```shell
  $ pip install -r dev-requirements.txt
  ```
  This installs all modules you need to run the game

#### Now you are setup to run the game!
  
# How to run
  - First follow or instructions in [Installation](https://github.com/Kingly-elpies/KinglyKelpies/edit/read-me-update/README.md#installation)
  - Then run in `/KinglyKelpies` (with the python version 3.10)
  ```shell
  $ python main.py
  ```  
  - You will be greeted by our main menu
  
# How to join a game:
From the Main menu
<p align= "center">
    <img src="https://user-images.githubusercontent.com/62175543/182196702-51a61a48-89b7-48a3-a36f-a566749bae11.png">
</p>

- press on `Host`, if you want to host a game. After that enter the port you want to host the game on.
- press on `Client`, if you want to join a game. After that enter the ip of the host and the port to connect to `ip:host`.

To confirm press the arrow to the right. 

### Notes:
   - As a host you have to make sure that a client can connect to your port, this may include port forwarding.
   - If you want to connect to localhost don't use the ip `127.0.0.1` use `localhost` instead.

# How to play:
### Controls
   - `w` for up   
   - `a` for left
   - `s` for down  
   - `d` for right
   - `e` to press buttons
   - `q` to pick up and drop boxes
   - `esc` to open the pause menu
      - the host can acces the level menu from here
      - by hitting reload you can r̵͎̀e̷̪̤̟̠͓̥͑͋̓́͊̀̚ḻ̸̰̯̏̑͛̂̎̄̽͘ơ̶̮̼̯͋̅͛å̴͇͍̩̲̍̈́͘d̶͇̰͐̓͑͒̕ the level
    
### Objects
<!-- Button-->
<p align="left">
    <img height=48 width=48 align="top" src = "https://user-images.githubusercontent.com/62175543/182188591-da67cfd8-0e70-4a2c-824e-f682fe93278f.gif">
    <t> A button can be toggled on or off, used to open and close doors</t>
</p>

<!-- Plate-->
<p align="left">
    <img height=48 width=48 align="top" src = "https://user-images.githubusercontent.com/62175543/182190339-8801967b-7d60-4260-92c6-eddc30f956b4.gif">
    <t> A plate is toggled on or off if a player walks or a box is placed on it, used to open and close doors</t>
</p>

<!-- Door-->
<p align="left">
    <img height=48 width=48 align="top" src = "https://user-images.githubusercontent.com/62175543/182191249-53668d2d-0eb8-493f-aa8f-8e5399d44468.gif">
    <t> A door can be opend by plates and buttons. Sometimes more than one of each!</t>
</p>

<!-- Hole-->
<p align="left">
    <img height=48 width=48 align="top" src = "https://user-images.githubusercontent.com/62175543/182194195-fe95896c-a610-4a24-b806-030beb6a6e52.gif">
    <t> A hole can't be walked over unless you fill it with a box. Be carefull you are not getting the box out of there!</t>
</p>

<!-- Box-->
<p align="left">
    <img height=48 width=48 align="top" src = "https://user-images.githubusercontent.com/62175543/182194668-cf9ec242-c51b-4512-a1bf-88e4d80ec139.png">
    <t> A box can be picked up and placed on plates to keep them active, put them next to a hole and they fall in</t>
</p>

<!-- Goal-->
<p align="left">
    <img height=48 width=48 align="top" src = "https://user-images.githubusercontent.com/62175543/182195574-53a3c7ea-7551-457a-81cf-539b1fbcec96.png">
    <t> If both players have walked over a goal the next level will start! </t>
</p>

# Help i softlocked myself!

This contains *some* Spoilers
<details>
    <summary>Click here to expand
    </summary>
<br />
You have probably noticed that the reload level function doesn't work. 
    
This is because it contains our bug!
    
To actually reload a level:
- open the level select
- enter the number of your current level (starting at 0)
- press go
    
</details>

# Credits
This project was created by: 
  | [Falkan#4044](https://github.com/falkanson) | [Vinyzu#1470](https://github.com/Vinyzu) | [Redriel#3335](https://github.com/Redriel57) | 
  |---------------------------------------------|------------------------------------------|----------------------------------------------|
  |  Art, game and websocket communication      | Menus, sound and game                    | Level design                                 |
  
### Outside Sources
Music:

> Tobu - Infectious http://youtube.com/tobuofficial: Provided by http://spoti.fi/NCS
    
Keyboard Key Sprites:

> Dream Mix - Pixel Keyboard Keys - for UI: https://dreammix.itch.io/keyboard-keys-for-ui

# Previews

<p align="center">
    <img src="https://user-images.githubusercontent.com/62175543/182314896-cb0c655d-efcb-4202-bbfd-4259e67852ba.png">
    <img src="https://user-images.githubusercontent.com/62175543/182314902-1849938a-24bb-4d0f-a8dc-3507686dbce3.png">
    <img src="https://user-images.githubusercontent.com/62175543/182314871-0e00d42c-89db-45ab-a2eb-ee72204812a4.png">
    <img src="https://user-images.githubusercontent.com/62175543/182314884-ec0ea6e4-e8d3-4ed1-94cb-872529452278.png">
</p>

# Spoilers
This section contains **full** Spoilers for the game's twist and explanation of the bug
<details>
    <summary>Click here to expand</summary>

## The Bug - Phantom Boxes

We call the Bug **Phantom Boxes** 

It is caused by the reload feature which does not work correctly. (Or does it 🤔)

### To reproduce it follow these steps:

- Move one box you want to create a phantom version of
- Reload the game using the button in the pause menu
    
### The effect:

- There will now be two iterations of the box, one at the original starting position and one at the position you moved the box to
- The other player will only see the box that was **last** placed by you, if he moves the duplicated box the phantom boxes will disapear on your end
- Phantom boxes can activate plates and fill holes but only on your end!
- But be careful, reloading turns off activated buttons without updating the door
    
    
### Explanation 
    
This happens because if you reload the other instance of the game won't be notified. 
    
Additionally all old existing boxes won't be deleted if they are not updated from the other instance.

This results in the existence of multiple iterations of the same box.
    
</details>
