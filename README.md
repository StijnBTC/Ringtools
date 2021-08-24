# Ringtools
Ringtools is a tool to keep an eye on the by you provided channels, like to monitor a Ring of Fire.

--------------------

## Installation
1. Open your SSH client and login your node
2. Update pip to be sure `pip3 install --upgrade pip`
3. Clone this Github `git clone https://github.com/StijnBTC/Ringtools`
4. Navigate to the right folder `cd Ringtools`
5. Install the requirements `pip3 install -r requirements.txt`
6. Edit the channel file `sudo nano channels.txt`
7. Replace all channels with the channels from your ring and save (Ctrl+X following Y (Yes))
8. Run Ringtools `python3 ringtools.py --lnddir /home/umbrel/umbrel/lnd/ -f -l status` (When you're ready hit Ctrl+C)
