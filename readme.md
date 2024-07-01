Finds the best word for Discord's spellcast.

Does not take into account anything to do with crystals, such as swaps or shuffles.

# Example Usage

py spellcast.py A B C D E F G H I J K L M N O P Q R S T U V W X Y -x 00 -d 10 -t 43

Arguments:  
The board layout, left to right, top to bottom. 25 letters exactly. Uppercase or lowercase  

Optional arguments:  
The position of the bonuses, row by column, with the top left corner being 00 and the bottom right being 44.  
-x: Location of 2x bonus  
-d: Location of double letter bonus  
-t: Location of triple letter bonus  