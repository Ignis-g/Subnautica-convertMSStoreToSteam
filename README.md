# Subnautica: converting MS Store save files To Steam

Python3 required. 

This little script tries to convert windows store saves (in the wgs folder) to the Steam format for Subnautica and Subnautica: Below Zero.
Not tested for anything else, but it might work too.

![image](https://github.com/user-attachments/assets/dcb9ee21-1f2e-4783-979a-9d696eadcfc7)

The script generates a folder using a timestamp where it writes the extracted data. What you have to do is to follow the structure above: create the windows_store_save folder in the same directory as the script, place the wgs folder inside and launch it. 

Once you have the timestamp folder, copy all its content inside `Steam\SteamApps\common\Subnautica[Zero]\SNAppData\SavedGames`. 
