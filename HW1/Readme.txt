To execute the file, please follow the next steps:

1- Open a terminal
2- cd to the current "search.py" location
	2.1- Be sure to have the maze.txt and maze_cost.txt in the same folder as search.py
3- Copy and paste the following line in your terminal "python ./search.py -h" to see the different options available
	3.1- The program let you choose between a standard search and a custom search, the standard search have the following 
		 start, goal, and color options set by default:
		 *start = (0 , 1)
		 *goal  = (28, 29)
		 *explored nodes color = Blue
		 *final path color = Yellow
	3.2- If you want another start or goal, or if you want to change the colors displayed, you may choose the custom search,
		 otherwise, the standard search is the one to choose.
	3.3- Finally you have to specify the search algorithm: dfs, bfs or ucs
	3.4- For example, for a bfs search:
		 standard bfs search: python ./search.py -c standard -s bfs 
		 custom bfs search:	  python ./search.py -c custom -s bfs -r 0,1 -g 5,5 -f 8 -p 5
4- Enjoy!

Our team work is formed by
* Andrés Mejía
* Jhonatan Navas
