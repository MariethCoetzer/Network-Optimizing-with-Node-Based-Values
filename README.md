# Network Path Optimizer

An interactive dashboard for visualizing and optimizing paths through a directed acyclic graph (DAG). This tool finds all possible paths from Node 1 to Node 8, identifies Pareto-optimal paths based on power and time metrics, and provides an interactive slider to explore different path preferences.

## Features

- **Path Finding**: Uses depth-first search (DFS) to find all valid paths through the network
- **Pareto Optimization**: Identifies Pareto-optimal paths that maximize power and minimize time
- **Interactive Visualization**: 
  - Network diagram showing nodes and connections
  - Pareto chart displaying all paths with optimal paths highlighted
  - Slider to adjust preference between maximum power and minimum time
- **Dynamic Path Highlighting**: Selected paths are highlighted in both visualizations with darker colors

## Live Demo

Once deployed, you can interact with the dashboard to:
1. View all 21 possible paths from Node 1 to Node 8
2. See which 6 paths are Pareto-optimal
3. Use the slider to select paths based on your preference for power vs. time
4. Watch the network diagram update to show the selected path in bold

## Deployment Instructions

### Deploy to Netlify (Easiest)

1. **Drag & Drop Method**:
   - Go to [Netlify](https://app.netlify.com/)
   - Sign up or log in
   - Drag and drop the `network-optimizer.html` file (rename it to `index.html` first)
   - Your site will be live instantly!

2. **GitHub + Netlify Method**:
   - Create a new repository on GitHub
   - Upload this project
   - Connect your GitHub repo to Netlify
   - Netlify will auto-deploy on every push

### Deploy via GitHub Pages

1. Create a new repository on GitHub
2. Upload `network-optimizer.html` and rename it to `index.html`
3. Go to Settings → Pages
4. Select your branch and click Save
5. Your site will be available at `https://yourusername.github.io/repo-name/`

## Technical Details

### Network Structure

The network consists of 8 nodes with the following properties:
- **Node 1** 🍄: Time: 5, Power: 5 (Start)
- **Node 2** 🐫: Time: 7, Power: 5
- **Node 3** ☁️: Time: 8, Power: 4
- **Node 4** 👨: Time: 4, Power: 6
- **Node 5** 🌲: Time: 6, Power: 8
- **Node 6** 🌸: Time: 8, Power: 6
- **Node 7** 🐟: Time: 7, Power: 6
- **Node 8** 🚧: Time: 10, Power: 2 (End)

### Algorithm

1. **Path Finding**: DFS algorithm finds all valid paths from Node 1 to Node 8
2. **Metric Calculation**: Each path's total time and power are calculated by summing node values
3. **Pareto Optimization**: A path is Pareto-optimal if no other path has both higher power AND lower time
4. **Path Selection**: The slider uses a weighted score to select the best Pareto path based on user preference

### Files

- `network-optimizer.html` - Single-file application (rename to `index.html` for deployment)
- `README.md` - This file

## Customization

You can easily customize the network by editing the JavaScript in the HTML file:

- **Nodes**: Modify the `nodes` array to change properties, icons, or colors
- **Edges**: Update the `edges` array to change connections
- **Colors**: Change the color scheme in the CSS section
- **Metrics**: Adjust how power and time are calculated in the `calculatePathMetrics` function

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## License

Free to use and modify for any purpose.
