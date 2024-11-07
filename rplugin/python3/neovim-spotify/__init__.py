import pynvim

@pynvim.plugin
class ExamplePlugin:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('HelloWorld', sync=True)
    def hello_world(self):
        self.nvim.out_write("Hello, World!\n")

