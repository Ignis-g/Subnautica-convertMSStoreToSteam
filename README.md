# Subnautica: converting MS Store save files To Steam

This little script tries to convert windows store saves (in the wgs folder) to the Steam format for Subnautica and Subnautica: Below Zero.
Not tested for anything else, but it might work too.

![image](https://user-images.githubusercontent.com/105871593/169332129-a714adac-5fff-4bea-82e3-64ba2b954b01.png)

The script generates a folder using a timestamp where it writes the extracted data. What you have to do is to follow the structure above: create the windowsStoreSave folder in the same directory as the script, place the wgs folder inside and launch it. 

Once you have the timestamp folder, copy all its content inside `Steam\SteamApps\common\Subnautica[Zero]\SNAppData\SavedGames`. 
