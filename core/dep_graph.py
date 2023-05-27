from framework import PluginMixin, State
import tkinter as tk

from tools.plugin_tools import plugin


def draw_dependency_tree():
    try:
        import graphviz

        graph = graphviz.Digraph(
        )
        graph.attr(
            "node",
            shape="box",
            style="rounded",
            fontname="Arial",
            fontsize="10",
            fixedsize="true",
            width="1.5",
            height="0.5",
            fontcolor="white",
            fillcolor="black",
            color="white",
        )
        graph.attr(
            "edge", fontname="Arial", fontsize="10", penwidth="1.5",
            color="white",

        )
        graph.attr(
            "graph",
            splines="ortho",
            rankdir="LR",
            pad="0.5",
            rank="same",
            concentrate="true",
            color="white",
            bgcolor="black",
            fontcolor="white",
            fillcolor="black",
        )
        for plugin in PluginMixin.plugins():
            graph.node(plugin.plugin_id)
            for requirement in plugin.requirements:
                graph.edge(requirement, plugin.plugin_id)
        graph.attr("graph", size="22, 8", ratio="fill")
        # we want a dak themed graph

        return graph.pipe(format="png")
    except ImportError:
        return "Graphviz not installed"

@plugin
class RenderDepGraph(tk.Frame):
    states = ("window_notebook",)
    requirements = ("WindowNotebook",)
    plugin_id = "DepGraph"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_notebook.add(self, text="Dependency Graph")
        self.button = tk.Button(
            self,
            text="Render Dependency Graph",
            command=self.render_dep_graph,
            height=2,
        )
        self.button.pack(fill=tk.X, expand=False)
        self.display = tk.Label(
            self, text="Click the button to render the dependency graph"
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        getattr(self, "check")

    def render_dep_graph(self):
        if hasattr(self, "display"):
            self.display.destroy()
        self.graph = draw_dependency_tree()
        if isinstance(self.graph, str):
            self.display = tk.Label(self, text=self.graph)
            self.display.pack(fill=tk.BOTH, expand=True)
            return

        self.image = tk.PhotoImage(data=self.graph)
        self.display = tk.Label(
            self, image=self.image, bg="white", relief=tk.RAISED, borderwidth=1
        )
        self.display.pack(fill=tk.BOTH, expand=True)

    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def move_stop(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
