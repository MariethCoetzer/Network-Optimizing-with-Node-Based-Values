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
        dfs_title = Text("Depth-First Search with: ").to_edge(UP)
        self.play(Transform(title, dfs_title))
        self.wait(0.5)

        # ----------------------------
        # MEMORY BOX
        # ----------------------------
        memory_box = Rectangle(width=3.4, height=1.2, color=WHITE, stroke_width=2)
        memory_box.to_corner(UR, buff=0.1)
        memory_title = Text("Memory", font_size=22, color=WHITE).next_to(memory_box.get_top(), DOWN, buff=0.15)
        memory_content = VGroup()  # Will hold the path texts
        
        self.play(Create(memory_box), Write(memory_title))
        self.wait(0.3)

        # ----------------------------
        # ADJ LIST
        # ----------------------------
        adj = {node: [] for node in nodes}
        for u, v in edges:
            adj[u].append(v)

        target = "Node8"
        paths = []
        
        # Memory tracking
        node5_memorized = False
        memory_paths = []

        # ----------------------------
        # HELPER: Update Memory Display
        # ----------------------------
        def update_memory_display():
            nonlocal memory_content
            
            # Remove old content
            if len(memory_content) > 0:
                self.remove(memory_content)
            
            # Create new content
            new_content = VGroup()
            for i, path_str in enumerate(memory_paths):
                path_text = Text(path_str, font_size=16, color=WHITE)
                path_text.next_to(memory_title, DOWN, buff=0.2 + i * 0.35)
                new_content.add(path_text)
            
            # Animate addition
            self.play(FadeIn(new_content), run_time=0.4)
            memory_content = new_content

        # ----------------------------
        # DFS FUNCTION
        # ----------------------------
        def dfs(current, path):
            nonlocal node5_memorized
            
            path.append(current)

            # Check if we've reached Node5 for the second time (after memorization)
            if current == "Node5" and node5_memorized:
                # Turn Node5 blue to show the algorithm has arrived
                self.play(
                    graph.vertices[current][0].animate.set_color(BLUE),
                    run_time=0.3
                )
                self.wait(0.4)

                # Flash memory box — memory recognised!
                for _ in range(3):
                    self.play(
                        memory_box.animate.set_color(RED),
                        run_time=0.25
                    )
                    self.play(
                        memory_box.animate.set_color(WHITE),
                        run_time=0.25
                    )

                # Reset Node5 to white before returning
                self.play(
                    graph.vertices[current][0].animate.set_color(WHITE),
                    run_time=0.3
                )

                # Don't explore further - return early
                path.pop()
                return

            # Animate only the circle, not the label (keeps text visible and black)
            self.play(
                graph.vertices[current][0].animate.set_color(BLUE),
                run_time=0.3
            )

            if current == target:
                paths.append(path.copy())
                
                # If this path contains Node5, extract and store the subpath from Node5 to Node8
                if "Node5" in path:
                    node5_index = path.index("Node5")
                    subpath = path[node5_index:]  # From Node5 to Node8
                    path_str = " -> ".join([node.replace("Node", "Node ") for node in subpath])
                    
                    # Add to memory if not already there
                    if path_str not in memory_paths:
                        memory_paths.append(path_str)
                        update_memory_display()
                        
                        # Mark as memorized after we've found both paths from Node5
                        if len(memory_paths) == 2:
                            node5_memorized = True
                
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