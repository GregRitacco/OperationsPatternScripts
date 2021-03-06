## JMRI Operations - Pattern Scripts (pre-release)
This is a jython plugin for JMRI Operations Pro that creates track patterns for any single location.  
Track patterns are lists of rolling stock in tracks, essentially an inventory report.  
The user can then directly move selected cars and engines from one track to another within a single location, without building and terminating trains.   
Moving cars around a yard, the yard pattern, generally involves working with JMRI 'Yards.'  
Moving cars around a location, Intra-Plant swtiching, generally involves JMRI 'Classification/Interchange' tracks, and 'Spurs.'  
This is the current version, 2.0, and is under development. Consider it pre-release.  

## Yard Patterns
Yard patterns are track patterns for a yard. They are a useful tool for a yardmaster to use to help manage his/her yard.  
A yardmaster would use a yard pattern to:  
* Check track capacity and verify inventory.  
* Group cars by destination or train.  
* Create switch lists to assign work to crews.  
* Repurpose a yard tracks use throughout an operating session.  

## Intra-Plant Switching
Track patterns can also be used for intra-plant switching, which are switching movements confined to a single location, often done by a private railroad or plant equipment.  
Examples of this would include:  
* Moving cars to and from an Off Spot alternate track.  
* A steel mill operator moving slag cars to and from a furnace.  
* A mine operator loading hoppers from a pool of empties.  
* An inter-modal operator selecting certain types of well cars to load.  
* A grain exchange selling loaded hoppers to brokers.  

## JMRI Schedules
Moving cars TO a spur by using this plugin will apply the spur's schedule if enabled, setting the appropriate load and destination.  
If there is no schedule the plugin will attempt to apply the car's RWE or RWL parameters.
If no RWE or RWL, the plugin will then try to load the car with the custom designation for 'Empty' or 'Load' for that cars' load type.  
If none of the above, a car moved from a spur will toggle default load/empty designation.  

## Use with TrainPlayer software
This plugin also contains a subroutine so that JMRI can be used as the Ops engine for TrainPlayer's Advanced Ops module. The TrainPlayer side scripts can be found [here](https://github.com/GregRitacco/QuickKeys).  

## How To Use This Plugin
The following are YouTube videos covering the use of this plugin:  

How to add this plugin to JMRI  
[How to use this plugin](https://youtu.be/GjPtXk3oKmc)  
[Plugin demonstration at a yard](https://youtu.be/IdXvxyo-E3Y)  
[Plugin demonstration at industry](https://youtu.be/2Tv6sUMDD_Y)  
[How to modify this plugin](https://youtu.be/DK6O9AQmqXo)  
[Use this plugin with TrainPlayer??](https://youtu.be/rlUfoSesnQo)  

Disclaimer:
There are many people on YouTube who are good at making demo videos. I am not one of them.  

## Testing
This plugin has been tested with:
* JMRI 4.25.4 with Java 8u301, JMRI 4.26 with Java 8u311, Windows 10 Pro and Home  

## License
The scripts included in this plugin are ?? 2021 Greg Ritacco.  
Other then that, there are no restrictions on use.


![GitHub repo file count](https://img.shields.io/github/directory-file-count/GregRitacco/JMRI-Operations---Pattern-Scripts?style=flat-square)
