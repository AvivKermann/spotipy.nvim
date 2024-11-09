local pickers = require "telescope.pickers"
local finders = require "telescope.finders"
local actions = require "telescope.actions"
local actions_state = require "telescope.actions.state"
local entry_display = require "telescope.pickers.entry_display"
local conf = require("telescope.config").values

-- local tracks = {
--   { artist = "Metallica", title = "Nothing Else Matters", uri = "spotify:track:0nLiqZ6A27jJri2VCalIUs" },
--   { artist = "Metallica", title = "Nothing Else Matters - Remastered 2021", uri = "spotify:track:6QAsrXPnMSXIbV0yEJHlEX" },
--   { artist = "Metallica", title = "Nothing Else Matters - Live", uri = "spotify:track:4nvFgshg9sO9YVnlKgQysN" },
--   { artist = "Metallica", title = "Nothing Else Matters - Live", uri = "spotify:track:5jEfQZmmwwKymr9cfmgfsd" },
--   { artist = "Miley Cyrus", title = "Nothing Else Matters", uri = "spotify:track:2mC33mxgLJN3IT65MGN3B0" },
--   { artist = "Hardwell", title = "Nothing Else Matters vs F*CKING SOCIETY - Hardwell Mashup", uri = "spotify:track:107nvz0Fjnsq9O9g61myZ5" },
--   { artist = "Naughty Boy", title = "Runnin' (Lose It All)", uri = "spotify:track:5yZvaUVyuXfSVUaMumFi6l" },
--   { artist = "newvoicesbg", title = "Nothing Else Metters", uri = "spotify:track:5YEqUrOkj1Pvw3mCXVALyQ" },
--   { artist = "Roni Alter", title = "I Follow Rivers", uri = "spotify:track:4a2MIdV2CBdA9mUOgi0RWR" },
--   { artist = "Yoni Rechter", title = "שוב היא כאן", uri = "spotify:track:0G8ooolx3x5DNkKkcZ19zp" }
-- }

-- Finder function for tracks
local function finder_fn()
    return function(_)
        local res = vim.g.spotify_search_results
        vim.notify(vim.inspect(res))
        local results = {}

        for _, v in pairs(res) do
            print("Track found:", v.artist, v.title)  -- Debugging line
            table.insert(results, { artist = v.artist, title = v.title, uri = v.uri })
        end

        return results
    end
end

-- Entry maker function for handling track entries in Telescope
local function entry_fn(opts)
    opts = opts or {}

    local display_items = {
        { width = 40 },
        { width = 25 },
    }

    local displayer = entry_display.create {
        separator = " by ",
        items = display_items
    }

    local make_display = function (entry)
        return displayer {
            { entry.track, "TelescopeResultsNumber" },
            { entry.artist, "TelescopeResultsComment" },
        }
    end

    return function(entry)
        return {
            artist = entry.artist,
            track = entry.title,
            uri = entry.uri,
            display = make_display,
            ordinal = entry.title .. " " .. entry.artist,  -- using title and artist for sorting
        }
    end
end

-- Main function for showing tracks using Telescope
local spotify = function (opts)
    opts = opts or {}
    pickers.new(opts, {
        prompt_title = "Spotify Search Results",
        finder = finders.new_dynamic({
            entry_maker = entry_fn(opts),
            fn = finder_fn()
        }),
        sorter = conf.generic_sorter(opts),
        attach_mappings = function (prompt_bufnr, _)
            actions.select_default:replace(function()
                actions.close(prompt_bufnr)
                local selection = actions_state.get_selected_entry()
                local cmd = ":call SpotifyPlay('" .. selection.uri .. "')"
                vim.api.nvim_command(cmd)
            end)
            return true
        end
    }):find()
end

-- Function to list available Spotify devices
local list_devices = function (opts)
    opts = opts or {}
    pickers.new(opts, {
        prompt_title = "Connect to a Device",
        finder = finders.new_dynamic({
            entry_maker = function (entry)
                return {
                    value = entry,
                    display = entry[1],
                    ordinal = entry[1]
                }
            end,
            fn =  function(_)
                local res = vim.g.spotify_devices
                local results = {}

                for _, v in pairs(res) do
                    table.insert(results, { v[1] })
                end

                return results
            end
        }),
        sorter = conf.generic_sorter(opts),
        attach_mappings = function (prompt_bufnr, _)
            actions.select_default:replace(function()
                actions.close(prompt_bufnr)
                local selection = actions_state.get_selected_entry()
                vim.g.spotify_device = selection.value
            end)
            return true
        end
    }):find()
end

local M = {
    opts = {
        status = {
            update_interval = 10000,
            format = '%s %t by %a'
        }
    },
    status = {},
    _status_line = ""
}

M.namespace = 'Spotify'

-- Setup function to configure mappings
function M.setup(opts)
    M.opts = vim.tbl_deep_extend("force", M.opts, opts)

    vim.api.nvim_set_keymap("n", "<Plug>(SpotifySkip)", ":call SpotifyPlayback('next')<CR>", { silent = true })
    vim.api.nvim_set_keymap("n", "<Plug>(SpotifyPause)", ":call SpotifyPlayback('pause')<CR>", { silent = true })
    vim.api.nvim_set_keymap("n", "<Plug>(SpotifySave)", ":call SpotifySave()<CR>", { silent = true })
    vim.api.nvim_set_keymap("n", "<Plug>(SpotifyPrev)", ":call SpotifyPlayback('prev')<CR>", { silent = true })
    vim.api.nvim_set_keymap("n", "<Plug>(SpotifyShuffle)", ":call SpotifyPlayback('shuffle')<CR>", { silent = true })
end

function M.init()
    local opts = require'telescope.themes'.get_dropdown{}
    spotify(opts)
end

function M.devices()
    list_devices(require'telescope.themes'.get_dropdown{})
end

-- Status management for Spotify
function M.status:start()
    local timer = vim.loop.new_timer()
    timer:start(1000, M.opts.status.update_interval, vim.schedule_wrap(function ()
        local cmd = "spt playback --status --format '" .. M.opts.status.format .. "'"
        vim.fn.jobstart(cmd, { on_stdout = self.on_event, stdout_buffered = true })
    end))
end

function M.status:on_event(data)
    if data then
        M._status_line = data[1]
    end
end

function M.status:listen()
    return M._status_line
end

return M

