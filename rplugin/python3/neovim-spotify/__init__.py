import pynvim

@pynvim.plugin
class ExamplePlugin:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("Spotify", sync=True)
    def hello_world(self):
        self.nvim.out_write("Hello, World!\n")
