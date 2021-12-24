# MazePuzzle
I made a maze that my algorithm isn't able to solve. I put it at the bottom of my script.  
My best guess is that by the time the computer reaches the wall of 1's, every adjacent node to a removable wall has been most efficiently reached by skipping a wall.  
Because of this, all the wall nodes retain a distance of 1000, so all unvisited nodes connected retain a distance of 1000 as well.
