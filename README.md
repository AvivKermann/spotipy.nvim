# 🎵spotipy.nvim

For productivity addicts who enjoy coding while listening to Spotify, and cannot lose their focus switching to the app to control their music.

`spotipy.nvim` requires [pynvim](https://github.com/neovim/pynvim)

## Features
-   Display/Filter the search results with Telescope  

-   Currently playing statusline.  

-   Currently playing notification.

-   Toggle track status

-   Skip a track  

-   Add a track to queue

-   Select which device to play on  

-   Search by tracks


## Requirements
> `spotipy.nvim` is a python based plugin, using the [spotipy](https://github.com/spotipy-dev/spotipy) library to interact with the Spotify API.

-   [pynvim](https://github.com/neovim/pynvim)
-   [spotipy](https://github.com/spotipy-dev/spotipy)
-   [Telescope](https://github.com/nvim-telescope/telescope.nvim)


## Installation

### [packer](https://github.com/wbthomason/packer.nvim)
```lua
-- Lua
use {
    "AvivKehrmann/spotipy.nvim",
    requires = 'nvim-telescope/telescope.nvim',
    config = function()
    local spotipy = require("spotipy.nvim")
    spotipy.setup({
        status = {
            update_interval = 10000}
        })
    end
}
```
### [lazy.nvim](https://github.com/folke/lazy.nvim)
```lua
return {
    {
        "AvivKehrmann/spotipy.nvim",
        requires = "nvim-telescope/telescope.nvim",
        config = function()
            local spotipy = require("spotipy.nvim")
            spotipy.setup({
                status = {
                    update_interval = 10000}
            })
        end
    }
}
```

#### Notes
Decreasing the `update_interval` value means more API calls in a shorter period. Because of the Spotify API rate limiter, setting this too low can block future requests.
Besides that, keep in mind these updates are api calls, they will slow your computer down. 

## Usage
`spotipy.nvim` has several commands:

### Adding a Track to the Queue
Add a song to the queue (plays it next) by specifying a track URI.
```bash
:SpotifyAdd <track_uri>
```

### Connecting to a Device
Open a menu of the devices connected to your Spotify account and select which one to play on.
```bash
:SpotifyDevices
```

### Playing a Song
Play a song by providing its URI.
```bash
:SpotifyPlay <track_uri>
```

### Controlling Playback
Control the playback with options to skip or go back a song.
```bash
:SpotifyPlayback -n/next      # Skip to the next song
:SpotifyPlayback -p/prev      # Go back to the previous song
```

### Displaying the Playlist
Show the next 20 songs in the queue.
```bash
:SpotifyPlaylist
```

### Searching for a Song
Search for a song by providing its name and display the top 20 results.
```bash
:SpotifySearch <song_name>
```

### Checking Current Status
Uses the `vim.notify` API to display the current Spotify status, including song name, album name, artist name, and duration. If no song is playing, an appropriate message will be shown.
Also supports [nvim.notify](https://github.com/rcarriga/nvim-notify) plugin.
```bash
:SpotifyStatus
```

### Toggling Playback
Toggle the current playback on or off based on the current state.
```bash
:SpotifyToggle
```

### Default keymaps
The following keymaps are set by default:
| mode | key | Description |
|---|---|---|
| normal | Esc | Close
| normal | q | Close
| normal| <leader>ms | search for songs
| normal | <leader>mt | toggle playback
| normal | <leader>ml | show Playlist
| normal | <leader>mn | skip song
| normal | <leader>mp | go back to the previous song
| normal | <leader>md | show devices
| normal | <leader>mm | show current status

### Override keymaps
The default keymaps are set during the spotipy.nvim setup function.
Make sure to call the setup function before setting your own keymaps.
You can override the default keymaps by settings your own in the following way:
```lua
vim.api.nvim_set_keymap("n", "<leader>mt", ":SpotifyToggle<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("n", "<leader>ml", ":SpotifyPlaylist<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("n", "<leader>mn", ":SpotifyPlayback -n<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("n", "<leader>mp", ":SpotifyPlayback -p<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("n", "<leader>mm", ":SpotifyStatus<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("n", "<leader>md", ":SpotifyDevices<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("n", "<leader>ms", ":lua require('neovim-spotify').search()<CR>", { noremap = true, silent = true })
```

### Statusline
You can display what's currently playing on your statusline. The example below shows how to show it on [lualine](https://github.com/nvim-lualine/lualine.nvim),
although the configuration should be quite similar on other statusline plugins:
```lua
local status = require"spotipy.nvim".status

status:start()

require('lualine').setup {
    sections = {
        lualine_x = {
            status.listen
        }
    }
}
```

### Notifications
You can display the current status and many other notifications using the [nvim.notify](https://github.com/rcarriga/nvim-notify) plugin.
```lua

