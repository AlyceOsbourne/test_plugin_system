import tkinter as tk

import ttkbootstrap as ttk

from tools.plugin_tools import PluginMixin
from tools.state_tools import State


class StateViewer(ttk.ScrolledText, PluginMixin):
    states = ("window_notebook", )
    requirements = ("WindowNotebook",)

    def __init__(self, *args, **kwargs):
        super().__init__(self.window_notebook, *args, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.window_notebook.add(self, text="State Viewer")

    def update(self):
        self.delete(1.0, tk.END)
        self.insert(tk.END, str("\n".join([f"{k}: {v}" for k, v in State.states().items()])))
