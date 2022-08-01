**Python Discord Summer Code Jam 2022** submission from the team **KinglyKelpies**
# *for level_id in range(14)*
A simple multiplayer puzzle game, 
in which you aim is to reach the goal by pressing buttons, standing on plates, moving boxes.
Together with a friend!

# Table of contents
1. [Installation](https://github.com/Kingly-elpies/KinglyKelpies/blob/read-me-update/README.md#installation)
2. [How to Run](https://github.com/Kingly-elpies/KinglyKelpies/blob/read-me-update/README.md#how-to-run)
3. [How to join a game](https://github.com/Kingly-elpies/KinglyKelpies/blob/read-me-update/README.md#how-to-join-a-game)
4. [How to play](https://github.com/Kingly-elpies/KinglyKelpies/blob/read-me-update/README.md#how-to-play)
   - [Movement](https://github.com/Kingly-elpies/KinglyKelpies/blob/read-me-update/README.md#1-movement)
   - [Interaction](https://github.com/Kingly-elpies/KinglyKelpies/blob/read-me-update/README.md#2-interaction)


# Installation
### 0. Requirements:
   - access *python 3.10* on you system

### 1. Download:
   Run this command in the directory you want to download it to.
   ```shell
   $ git clone https://github.com/Kingly-elpies/KinglyKelpies
   ```
 
### 2. Create a venv
  with python as python as python 3.10 create a virtual environment in the folder `.venv`.
  ```shell
  $ python -m venv .venv
  ```

  #### Enter the environment
  It will change based on your operating system and shell.
  ```shell
  # Linux, Bash
  $ source .venv/bin/activate
  # Linux, Fish
  $ source .venv/bin/activate.fish
  # Linux, Csh
  $ source .venv/bin/activate.csh
  # Linux, PowerShell Core
  $ .venv/bin/Activate.ps1
  # Windows, cmd.exe
  > .venv\Scripts\activate.bat
  # Windows, PowerShell
  > .venv\Scripts\Activate.ps1
  ```

  #### Exiting the environment 
  Run this after you played our game.
  ```shell
  $ deactivate
  ```

### 3. Install the dependencies
  In the `/KinglyKelpies` directory run:
  ```shell
  $ pip insall -r dev-requirements.txt
  ```
  This installs all modules you need to run the game

#### Now you are setup to run the game!
  
# How to Run
  - First follow or instructions for [Installation](https://github.com/Kingly-elpies/KinglyKelpies/edit/read-me-update/README.md#installation)
  - Then run in the venv:
  ```shell
  $ python main.py
  ```  
  - you will be greeted by our main menu
  
# How To join a game:
From the Main menu
- press on `Host`, if you want to host a game. After that enter the port you want to host the game and press the arrow to the right.
- press on `Client`, if you want to join a game. After that enter the ip of the host and the port to connect to `ip:host`.

# How to play:
## Basics
   - `w` for up   
   - `a` for left
   - `s` for down  
   - `d` for right
   - `e` to press buttons
   - `q` to pick up boxes and put them down
