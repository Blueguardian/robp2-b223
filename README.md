# robp2-b223 Semester project

This is the semester project for group B223 in Robotics. The project contains a simulation for an industrial mamipulator.
The project as is will only introduce a simulation of 90 iterations of the full process of both combining covers and engraving them or
the short process of only combining covers. This can also be any combination of the two. 

The simulation contains:
- 1 Fanuc LR Mate 200iC
- 1 Linear movement FESTO base
- 1 Pallette carrier
- 1 Bottom cover in black (Can be recoloured)
- 1 Custom designed storage container
- 1 Custom designed Cage
- 1 Standard table
- 1 Box
- 1 Custom designed engraving environment with laser engraver
- 10 Black flat covers 
- 10 Black curved edges covers
- 10 Black curved covers
- 10 White flat covers
- 10 White curved edges covers
- 10 White curved covers
- 10 Blue flat covers
- 10 Blue curved edges covers
- 10 Blue curved covers

## Simulation walkthrough
The simulation is based on calculations in RoboDK, which cannot is NOT entirely transferable to the real world, as there are alot more variables to consider.
The simulation can do a couple of thins that will be introduced and documented here:

### Simulation scripts
**The script called 'main':**
The main script of the simulation opens a GUI where you can select what colour top- and bottom cover you would like to have produced along with options for
curvature of the cover. The GUI also includes options for engraving, one asking the user if theu would like the phone engraved and an option for uploading your
own .scg image for engraving.

When you are done selecting the options you would like for your phone, clcik the button marked "Order" in the bottom of the GUI. The process of creating the phone
will then begin, to speed up the process you can change perspective to the engraving environment (the small black box) as rendering this from afar is quite slow). 
When the process is finished it will depending on your settings prompt with a "script successfully run" window. This concludes the main script.

**NOTE: The time used in the simulation is not considered equal to the real time used as this is highly dependant on your GPU and Processor**

**The script called 'restock':**
The restock script MUST only be used on a hard reset of the simulation as this resets the sim stock, without changing the amount of covers left in the storage container. The reasoning behind not creating a script adding alle the covers again is that after each object added to RoboDK the simulation has to wait 60 seconds
before another action can be performed (Stated in the API code) The would add up to 90 minutes to include all covers again.

**The script called 'call_stat':**
The call stat or call statistics script is for showing the amount of different covers created along with how many of these that have been engraved. This is the 
data that is simulated for integrating Industry 4.0 intro the project, as this alloweds data to be collected of how many covers of each type is created.

### Running scripts
Each script can be run by either double-clicking the sciprt in the content tree in RoboDK, or by right-clicking and selecting 'run python script'.
The scripts can also be run external from RoboDK either in a command prompt/terminal, in an API or any other way possible for running python scripts, the only
requirement is that the station is open in RoboDK.

### Changing the simulation
It is possible to move objects in the simulation, as it would still work, the only thing to mention here is that there is no garantee that each script will complete succesfully, as some items in RoboDK would not be reachable for the robot. The current positions are set as default, as these positions allow for the scripts to run withour errors.

### Out of stock
When the storage container is empty, or your would like to refill the storage container regardless of emptyness or not, you will have to close the station without 
saving it, and reopening it, this can be done by right-clicking the station folder in the and selecting 'close'.
Reopening it can either be done by selecting 'file' in the top menu and selecting the 'open' option and browsing for it again, or pressing Ctrl+1 on your keyboard.

