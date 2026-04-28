from manim import *

class ParetoLogicSearch(Scene):
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
        # FIXED POSITIONS (left ~60% of screen)
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
        finding_title = Text("Finding Paths").to_edge(UP)
        self.play(Transform(title, finding_title))
        self.wait(0.3)

        # Reset start/end color to white for DFS
        self.play(
            start[0].animate.set_color(WHITE),
            end[0].animate.set_color(WHITE),
        )

        # ----------------------------
        # PARETO LOGIC BOX (top-right, Slide 20 style)
        # Taller box to fit both paths + comparison
        # ----------------------------
        memory_box = Rectangle(width=4.4, height=3.8, color=WHITE, stroke_width=2)
        memory_box.to_edge(RIGHT, buff=0.2)
        memory_title = Text("Pareto Logic", font_size=24, color=WHITE, weight=BOLD)
        memory_title.next_to(memory_box.get_top(), DOWN, buff=0.2)

        self.play(Create(memory_box), Write(memory_title))
        self.wait(0.3)

        # Persistent references so we can update without flicker
        path1_block = VGroup()   # stays on screen the whole time
        path2_block = VGroup()   # added later, then replaced

        def show_path1_plain():
            """Slide 21: Path 1 recorded, plain white text."""
            nonlocal path1_block

            p1_label  = Text("Path 1",     font_size=22, color=WHITE, weight=BOLD)
            p1_time   = Text("Time = 2",   font_size=22, color=WHITE)
            p1_profit = Text("Profit = 5", font_size=22, color=WHITE)

            path1_block = VGroup(p1_label, p1_time, p1_profit).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            path1_block.next_to(memory_title, DOWN, buff=0.2)
            path1_block.align_to(memory_box.get_left() + RIGHT * 0.25, LEFT)

            self.play(FadeIn(path1_block), run_time=0.4)

        def show_path2_halfway():
            """Slide 22: Fade in Path 2 (Halfway) below the existing Path 1 block."""
            nonlocal path2_block

            p2_label  = Text("Path 2 (Halfway)", font_size=22, color=WHITE, weight=BOLD)
            p2_time   = Text("Time = 3",          font_size=22, color=WHITE)
            p2_profit = Text("Profit = 2",         font_size=22, color=WHITE)

            path2_block = VGroup(p2_label, p2_time, p2_profit).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            path2_block.next_to(path1_block, DOWN, buff=0.4)
            path2_block.align_to(memory_box.get_left() + RIGHT * 0.25, LEFT)

            self.play(FadeIn(path2_block), run_time=0.8)

        def show_comparison():
            """Slide 23: Replace both blocks with colored comparison versions."""
            nonlocal path1_block, path2_block

            # --- Build new Path 1 block (colored values) ---
            p1_label = Text("Path 1", font_size=22, color=WHITE, weight=BOLD)

            p1_time_prefix = Text("Time = ",   font_size=22, color=WHITE)
            p1_time_val    = Text("2",          font_size=22, color=RED)
            p1_time_line   = VGroup(p1_time_prefix, p1_time_val).arrange(RIGHT, buff=0.02)

            p1_profit_prefix = Text("Profit = ", font_size=22, color=WHITE)
            p1_profit_val    = Text("5",          font_size=22, color=GREEN)
            p1_profit_line   = VGroup(p1_profit_prefix, p1_profit_val).arrange(RIGHT, buff=0.02)

            new_p1_block = VGroup(p1_label, p1_time_line, p1_profit_line).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            new_p1_block.next_to(memory_title, DOWN, buff=0.35)
            new_p1_block.align_to(memory_box.get_left() + RIGHT * 0.25, LEFT)

            # --- Build new Path 2 block (comparison with colored refs) ---
            p2_label = Text("Path 2 (Halfway)", font_size=22, color=WHITE, weight=BOLD)

            p2_time_prefix = Text("Time = 3 > ",   font_size=22, color=WHITE)
            p2_time_ref    = Text("2",               font_size=22, color=RED)
            p2_time_line   = VGroup(p2_time_prefix, p2_time_ref).arrange(RIGHT, buff=0.02)

            p2_profit_prefix = Text("Profit = 2 < ", font_size=22, color=WHITE)
            p2_profit_ref    = Text("5",              font_size=22, color=GREEN)
            p2_profit_line   = VGroup(p2_profit_prefix, p2_profit_ref).arrange(RIGHT, buff=0.02)

            new_p2_block = VGroup(p2_label, p2_time_line, p2_profit_line).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            new_p2_block.next_to(new_p1_block, DOWN, buff=0.4)
            new_p2_block.align_to(memory_box.get_left() + RIGHT * 0.25, LEFT)

            # Swap out old blocks, fade in new ones simultaneously
            self.play(
                FadeOut(path1_block),
                FadeOut(path2_block),
                run_time=0.4
            )
            path1_block = new_p1_block
            path2_block = new_p2_block
            self.play(
                FadeIn(path1_block),
                FadeIn(path2_block),
                run_time=0.5
            )

        # ----------------------------
        # MANUAL DFS — Path 1 first
        # ----------------------------

        # Step 1: Visit Node1 (blue)
        self.play(graph.vertices["Node1"][0].animate.set_color(BLUE), run_time=0.3)

        # Step 2: Traverse edge Node1→Node2, visit Node2
        e12 = graph.edges[("Node1", "Node2")]
        self.play(e12.animate.set_color(BLUE), run_time=0.4)
        self.play(graph.vertices["Node2"][0].animate.set_color(BLUE), run_time=0.3)

        # Step 3: Traverse edge Node2→Node5, visit Node5 (target)
        e25 = graph.edges[("Node2", "Node5")]
        self.play(e25.animate.set_color(BLUE), run_time=0.4)
        self.play(graph.vertices["Node5"][0].animate.set_color(BLUE), run_time=0.3)

        # Record Path 1 in the box (Slide 21)
        show_path1_plain()
        self.wait(0.6)

        # Step 4: Backtrack — reset Node5, edge Node2→Node5, Node2
        self.play(graph.vertices["Node5"][0].animate.set_color(WHITE), run_time=0.4)
        self.play(e25.animate.set_color(WHITE), run_time=0.4)
        self.play(graph.vertices["Node2"][0].animate.set_color(WHITE), run_time=0.4)
        self.play(e12.animate.set_color(WHITE), run_time=0.4)

        # ----------------------------
        # Path 2 — Node1 stays blue, go down to Node3
        # ----------------------------

        # Step 5: Traverse edge Node1→Node3, visit Node3
        e13 = graph.edges[("Node1", "Node3")]
        self.play(e13.animate.set_color(BLUE), run_time=0.4)
        self.play(graph.vertices["Node3"][0].animate.set_color(BLUE), run_time=0.3)

        # Show Path 2 (Halfway) in the box (Slide 22)
        show_path2_halfway()
        self.wait(0.6)

        # Show colored comparison (Slide 23) — Pareto check fires
        show_comparison()
        self.wait(0.8)

        # ----------------------------
        # Slide 24+25: "Path 1 Dominates" and "Stop Search" below the memory box
        # ----------------------------
        dominates_text = Text("Path 1 Dominates Path 2", font_size=24, color=BLUE_C)
        dominates_text.next_to(memory_box, DOWN, buff=0.25)
        self.play(Write(dominates_text), run_time=0.5)
        self.wait(0.6)

        stop_text = Text("Stop Search", font_size=24, color=BLUE_C)
        stop_text.next_to(dominates_text, DOWN, buff=0.15)
        self.play(Write(stop_text), run_time=0.5)
        self.wait(0.8)

        # ----------------------------
        # Slide 26: Reset all nodes to white, fade out traversal
        # ----------------------------
        self.play(
            graph.vertices["Node1"][0].animate.set_color(WHITE),
            graph.vertices["Node3"][0].animate.set_color(WHITE),
            e13.animate.set_color(WHITE),
            run_time=0.6
        )
        self.wait(2)