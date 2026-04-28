from manim import *

class FindAllPathsAnimation(Scene):
    def construct(self):
        # ----------------------------
        # Nodes (8-node DAG)
        # ----------------------------
        nodes = [f"Node{i}" for i in range(1, 9)]

       # Updated to match the arrows in the image
        edges = [
            ("Node1", "Node2"),
            ("Node2", "Node3"), ("Node2", "Node4"),
            ("Node3", "Node5"), ("Node4", "Node5"),
            ("Node5", "Node7"), ("Node5", "Node6"),
            ("Node7", "Node8"), ("Node6", "Node8"),
        ]

        # ----------------------------
        # FIXED POSITIONS (Matching the image layout)
        # ----------------------------
        # Using a coordinate system where [x, y, z] 
        # shifts nodes to create the diamond shapes.
        positions = {
            "Node1": [-6.0, 0, 0],   # Mushroom (Left)
            "Node2": [-3.5, 0, 0],   # Camel
            "Node3": [-1.0, 2.0, 0],  # Cloud (Top)
            "Node4": [-1.0, -2.0, 0], # Snowman (Bottom)
            "Node5": [1.5, 0, 0],    # Tree (Center)
            "Node7": [4.0, 2.0, 0],   # Fish (Top)
            "Node6": [4.0, -2.0, 0],  # Flower (Bottom)
            "Node8": [6.5, 0, 0],    # Volcano (Right-most)
        }
        # ----------------------------
        # Graph (BIG nodes + labels)
        # ----------------------------
        graph = DiGraph(
            nodes,
            edges,
            layout=positions,
            vertex_config={
                "radius": 0.5,   # BIGGER NODES
                "fill_opacity": 1
            },
            labels={f"Node{i}": Text(f"Node {i}", font_size=16, color=BLACK) for i in range(1, 9)}
        )

        self.play(Create(graph))
        self.wait(1)

        # ----------------------------
        # INTRO TITLE
        # ----------------------------
        title = Text("Finding Paths from Node 1 to Node 8").to_edge(UP)
        self.play(Write(title))

        start = graph.vertices["Node1"]
        end = graph.vertices["Node8"]

        # Flash start and end nodes in red
        for _ in range(2):
            self.play(
                start[0].animate.set_color(RED),
                end[0].animate.set_color(RED),
                run_time=0.4
            )
            self.play(
                start[0].animate.set_color(WHITE),
                end[0].animate.set_color(WHITE),
                run_time=0.4
            )

        self.play(
            start[0].animate.set_color(RED),
            end[0].animate.set_color(RED),
        )

        self.wait(0.5)

        # ----------------------------
        # DFS TITLE
        # ----------------------------
        dfs_title = Text("Depth-First Search").to_edge(UP)
        self.play(Transform(title, dfs_title))
        self.wait(0.5)

        # ----------------------------
        # ADJ LIST
        # ----------------------------
        adj = {node: [] for node in nodes}
        for u, v in edges:
            adj[u].append(v)

        target = "Node8"
        paths = []

        # ----------------------------
        # DFS FUNCTION
        # ----------------------------
        def dfs(current, path):
            path.append(current)

            # Animate only the circle, not the label (keeps text visible and black)
            self.play(
                graph.vertices[current][0].animate.set_color(BLUE),
                run_time=0.3
            )

            if current == target:
                paths.append(path.copy())
                self.wait(0.4)
            else:
                for neighbor in adj[current]:
                    if neighbor not in path:
                        edge = graph.edges[(current, neighbor)]
                        self.play(edge.animate.set_color(BLUE), run_time=0.4)
                        dfs(neighbor, path)
                        self.play(edge.animate.set_color(WHITE), run_time=0.4)

            path.pop()
            # Animate only the circle, not the label (keeps text visible and black)
            self.play(
                graph.vertices[current][0].animate.set_color(WHITE),
                run_time=0.4
            )

        dfs("Node1", [])
        self.wait(2)
