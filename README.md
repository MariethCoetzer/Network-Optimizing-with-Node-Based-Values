# Network Path Optimizer

**Disclaimer:** This README and all the code in this repository were written by Claude, with the GitHub author overseeing the process.

An interactive dashboard for visualizing and optimizing paths through a directed acyclic graph (DAG) where the optimization is based on node values rather than edge costs. This tool finds all possible paths from Node 1 to Node 8 using depth-first search with memoization, identifies Pareto-optimal paths based on *Power* and *Time* metrics, and provides an interactive slider to explore different path preferences.

[**Link to deployed website**(https://mariethcoetzer.github.io/Network-Optimizing-with-Node-Based-Values/)]

For detailed explanations of the path-finding algorithm and Pareto optimization approach, see the corresponding blog posts:
- [Network Optimizing with Node-Based Values – Memoization](Placeholder for link)
- [Network Optimizing with Node-Based Values – Pareto Optimization](Placeholder for link)

## Features

- **Memoized Path Finding**: Uses depth-first search (DFS) with memoization to efficiently find all valid paths through the network
- **Pareto Optimization**: Identifies Pareto-optimal paths that maximize *Power* while minimizing *Time*
- **Interactive Visualization**: 
  - Network diagram showing nodes and their connections
  - Pareto frontier chart displaying all paths, with Pareto-optimal paths highlighted
  - Slider to adjust preference between maximum *Power* and minimum *Time*
- **Dynamic Path Highlighting**: Selected paths are highlighted in both visualizations with bolder colors

## Live Demo

You can interact with the dashboard to:
1. View all 4 possible paths from Node 1 to Node 8
2. See which 3 paths are Pareto-optimal (paths where no other path offers both more *Power* AND less *Time*)
3. Use the slider to select paths based on your preference for *Power* vs. *Time*
4. Watch the network diagram update to show the selected path highlighted

## Technical Details

### Network Structure

The network consists of 8 nodes with the following properties:
- **Node 1** 🍄: *Time*: 5, *Power*: 5 (Start)
- **Node 2** 🐫: *Time*: 7, *Power*: 5
- **Node 3** ☁️: *Time*: 8, *Power*: 4
- **Node 4** 👨: *Time*: 4, *Power*: 6
- **Node 5** 🌲: *Time*: 6, *Power*: 8
- **Node 6** 🌸: *Time*: 8, *Power*: 6
- **Node 7** 🐟: *Time*: 7, *Power*: 6
- **Node 8** 🚧: *Time*: 10, *Power*: 2 (End)

### Algorithm and Optimization

1. **Path Finding with Memoization**: DFS algorithm finds all valid paths from Node 1 to Node 8. Memoization stores previously computed subpaths to avoid redundant calculations, improving efficiency from exponential to $O(N+E)$ complexity for the graph traversal.
2. **Metric Calculation**: Each path's total *Time* and *Power* are calculated by summing the node values along the path.
3. **Pareto Optimization**: A path is Pareto-optimal if no other path has both higher *Power* AND lower *Time*. In other words, a path is on the Pareto frontier if it is not dominated by any other path.
4. **Path Selection**: The slider uses a weighted score to select the best Pareto-optimal path based on user preference between *Power* and *Time*.

## Videos Used in Blog Posts

The code to replicate the videos used in the blog posts is saved in the `Videos` folder. 
The videos were created using the Python package Manim. 

## License

Free to use and modify for any purpose. Please cite this GitHub repository.
