# Synack_mission
This is a fork of Mad-robot mission bot.

Mission Bot updated to include the paus for 30 seconds after each attempt to claim a mission.

open imacro and click on record Then record macro.

Then click on stop and save as.

After saving the macro, highlight the macro you just created and click manage then Edit Macro

copy the code above and paster over the code in the macro you just created and click save.

Then when you are ready to run, click on Play.

For max set the number to 100 (that's most allowed in free mode). Then click Play Loop.



# Mission.py
is my own script and attempt at creating a bot. Could use some cleaning up. The authorization baerer needs to be put into the command line. I don't believe you 
can run this while being logged into the Synack and looking for vulns. The Auth cookie gets refreshed after awhile and may cause issues.

Using selenium and requests. Using requests to send all the api calls and claim the missions. Using selenium to click ok when it asks if you want to stay logged in. There is probably away to do this in requests but i'm not sure how to keep the session alive.
