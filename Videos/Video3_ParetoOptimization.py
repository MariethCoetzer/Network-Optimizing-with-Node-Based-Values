from manim import *

class ParetoLogic(Scene):
    def construct(self):
        # ----------------------------
        # Nodes (5-node diamond DAG)
        # Node1 = Start (left)
        # Node2 = Top (Time:2, Profit:5)
        # Node3 = Bottom-left (Time:3, Profit:2)
        # Node4 = Bottom-right (Time:2, Profit:1)
        # Node5 = End (right)
        # ----------------------------
        nodes = [f"Node{i}" for i in range(1, 6)]

        edges = [
            ("Node1", "Node2"),
            ("Node1", "Node3"),
            ("Node2", "Node5"),
            ("Node3", "Node4"),
            ("Node4", "Node5"),
        ]

        # ----------------------------
        # FIXED POSITIONS (matching Slide 15 layout)
        # ----------------------------
        positions = {
            "Node1": [-5.5, 0, 0],    # Start (left)
            "Node2": [-3.2, 1.6, 0],  # Top
            "Node3": [-3.2, -1.6, 0], # Bottom-left
            "Node4": [-0.9, -1.6, 0], # Bottom-right
            "Node5": [1.4, 0, 0],     # End (right)
        }

        # ----------------------------
        # Graph
        # ----------------------------
        graph = DiGraph(
            nodes,
            edges,
            layout=positions,
            vertex_config={
                "radius": 0.5,
                "fill_opacity": 1
            },
        )

        self.play(Create(graph))
        self.wait(0.5)

        # ----------------------------
        # NODE LABELS (Time / Profit on intermediate nodes)
        # ----------------------------
        label_node2 = VGroup(
            Text("Time: 2",   font_size=22, color=WHITE),
            Text("Profit: 5", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.05)
        label_node2.next_to(graph.vertices["Node2"], DOWN, buff=0.15)

        label_node3 = VGroup(
            Text("Time: 3",   font_size=22, color=WHITE),
            Text("Profit: 2", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.05)
        label_node3.next_to(graph.vertices["Node3"], DOWN, buff=0.15)

        label_node4 = VGroup(
            Text("Time: 2",   font_size=22, color=WHITE),
            Text("Profit: 1", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.05)
        label_node4.next_to(graph.vertices["Node4"], DOWN, buff=0.15)

        self.play(
            FadeIn(label_node2),
            FadeIn(label_node3),
            FadeIn(label_node4),
        )
        self.wait(0.5)

        # ----------------------------
        # INTRO TITLE
        # ----------------------------
        title = Text("Finding Optimized Path from Node 1 to Node 5").to_edge(UP)
        self.play(Write(title))

        start = graph.vertices["Node1"]
        end   = graph.vertices["Node5"]

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
        pareto_title = Text("Finding Paths").to_edge(UP)
        self.play(Transform(title, pareto_title))
        self.wait(0.3)

        # Reset start/end color to white for DFS
        self.play(
            start[0].animate.set_color(WHITE),
            end[0].animate.set_color(WHITE),
        )

        # ----------------------------
        # MEMORY BOX (top-right)
        # ----------------------------
        memory_box = Rectangle(width=4.2, height=3.2, color=WHITE, stroke_width=2)
        memory_box.to_corner(UR, buff=0.2).shift(DOWN * 1.0)
        memory_title = Text("Paths Found", font_size=26, color=WHITE).next_to(memory_box.get_top(), DOWN, buff=0.2)
        memory_content = VGroup()

        self.play(Create(memory_box), Write(memory_title))
        self.wait(0.3)

        # ----------------------------
        # ADJ LIST
        # ----------------------------
        adj = {node: [] for node in nodes}
        for u, v in edges:
            adj[u].append(v)

        target     = "Node5"
        paths      = []
        memory_paths = []  # list of (label_str, time_str, profit_str)

        # ----------------------------
        # HELPER: Update Memory Display
        # ----------------------------
        def update_memory_display():
            nonlocal memory_content
            if len(memory_content) > 0:
                self.remove(memory_content)

            new_content = VGroup()
            y_offset = 0.35
            for i, entry in enumerate(memory_paths):
                label_text, time_text, profit_text = entry
                path_label  = Text(label_text,  font_size=22, color=WHITE, weight=BOLD)
                path_time   = Text(time_text,   font_size=22, color=WHITE)
                path_profit = Text(profit_text, font_size=22, color=WHITE)

                block = VGroup(path_label, path_time, path_profit).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
                block.next_to(memory_title, DOWN, buff=y_offset)
                block.align_to(memory_box.get_left() + RIGHT * 0.25, LEFT)
                new_content.add(block)
                # Add extra gap before Path 2 (paragraph break)
                y_offset += 1.0 if i == 0 else 0.85

            self.play(FadeIn(new_content), run_time=0.4)
            memory_content = new_content

        # ----------------------------
        # DFS FUNCTION
        # ----------------------------
        def dfs(current, path):
            path.append(current)

            self.play(
                graph.vertices[current][0].animate.set_color(BLUE),
                run_time=0.3
            )

            if current == target:
                paths.append(path.copy())

                # Compute cumulative time and profit for the full path
                time_vals   = {"Node2": 2, "Node3": 3, "Node4": 2}
                profit_vals = {"Node2": 5, "Node3": 2, "Node4": 1}

                total_time   = sum(time_vals.get(n, 0)   for n in path)
                total_profit = sum(profit_vals.get(n, 0) for n in path)

                path_num = len(paths)

                if path_num == 1:
                    # Path 1: just top node contributes
                    time_str   = f"Time = {total_time}"
                    profit_str = f"Profit = {total_profit}"
                else:
                    # Path 2: show addition
                    time_str   = f"Time = 3 + 2 = {total_time}"
                    profit_str = f"Profit = 2 + 1 = {total_profit}"

                memory_paths.append((f"Path {path_num}", time_str, profit_str))
                update_memory_display()
                self.wait(0.6)

            else:
                for neighbor in adj[current]:
                    if neighbor not in path:
                        edge = graph.edges[(current, neighbor)]
                        self.play(edge.animate.set_color(BLUE), run_time=0.4)
                        dfs(neighbor, path)
                        self.play(edge.animate.set_color(WHITE), run_time=0.4)

            path.pop()
            self.play(
                graph.vertices[current][0].animate.set_color(WHITE),
                run_time=0.4
            )

        # ----------------------------
        # RUN DFS
        # ----------------------------
        

        dfs("Node1", [])
        self.wait(1.0)

        # ----------------------------
        # TRANSITION: Pareto Comparison Table (Slide 18)
        # ----------------------------
        self.play(
            FadeOut(graph),
            FadeOut(label_node2),
            FadeOut(label_node3),
            FadeOut(label_node4),
            FadeOut(memory_box),
            FadeOut(memory_title),
            FadeOut(memory_content),
            FadeOut(title),
            run_time=0.8
        )
        self.wait(0.3)

        # ----------------------------
        # Title above the box
        # ----------------------------
        table_title = Text("Pareto Logic", font_size=32, color=WHITE, weight=BOLD)
        table_title.move_to(ORIGIN + UP * 2.8)

        # Comparison table box — centered on screen
        table_box = Rectangle(width=6.5, height=2.8, color=WHITE, stroke_width=2)
        table_box.move_to(ORIGIN + UP * 0.6)

        # Use the box center and padding to place content evenly
        cx  = table_box.get_center()[0]   # horizontal center
        pad = 1.8                          # column offset from center
        lx  = cx - pad                    # Path 1 column x
        rx  = cx + pad                    # Path 2 column x
        ox  = cx                          # operator column x
        row_lx = table_box.get_left()[0] + 0.55  # row-label x

        box_top    = table_box.get_top()[1]
        box_bottom = table_box.get_bottom()[1]
        box_h      = box_top - box_bottom

        # Distribute 3 rows (header, time, profit) evenly with equal top/bottom padding
        header_y = box_top  - box_h * 0.22
        time_y   = box_top  - box_h * 0.52
        profit_y = box_top  - box_h * 0.72

        # Header row
        col_path1 = Text("Path 1", font_size=24, color=WHITE, weight=BOLD).move_to([lx, header_y, 0])
        col_path2 = Text("Path 2", font_size=24, color=WHITE, weight=BOLD).move_to([rx, header_y, 0])

        # Time row
        row_label_time = Text("Time",   font_size=24, color=WHITE).move_to([row_lx, time_y, 0])
        val_time1      = Text("2",      font_size=24, color=WHITE).move_to([lx, time_y, 0])
        val_time_op    = Text("<",      font_size=24, color=WHITE).move_to([ox, time_y, 0])
        val_time2      = Text("5",      font_size=24, color=WHITE).move_to([rx, time_y, 0])

        # Profit row
        row_label_profit = Text("Profit", font_size=24, color=WHITE).move_to([row_lx, profit_y, 0])
        val_profit1      = Text("5",      font_size=24, color=WHITE).move_to([lx, profit_y, 0])
        val_profit_op    = Text(">",      font_size=24, color=WHITE).move_to([ox, profit_y, 0])
        val_profit2      = Text("3",      font_size=24, color=WHITE).move_to([rx, profit_y, 0])

        self.play(Write(table_title), run_time=0.5)
        self.play(Create(table_box), run_time=0.5)
        self.play(
            FadeIn(col_path1), FadeIn(col_path2),
            run_time=0.4
        )
        self.play(
            FadeIn(row_label_time),
            FadeIn(val_time1), FadeIn(val_time_op), FadeIn(val_time2),
            run_time=0.5
        )
        self.play(
            FadeIn(row_label_profit),
            FadeIn(val_profit1), FadeIn(val_profit_op), FadeIn(val_profit2),
            run_time=0.5
        )
        self.wait(0.8)

        # Conclusion text
        conclusion = Text("Path 1 Dominates Path 2", font_size=28, color=WHITE)
        conclusion.next_to(table_box, DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)