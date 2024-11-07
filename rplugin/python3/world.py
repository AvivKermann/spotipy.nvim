import pynvim

@pynvim.plugin
class HelloWorld(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.cfg = nvim.exec_lua("require('HelloWorld').getConfig()")

    @pynvim.command("World", nargs=0)
    def world(self):
        self.nvim.out_write("Hello, World!\n")

