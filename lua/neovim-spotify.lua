local pickers = require "telescope.pickers"
local finders = require "telescope.finders"
local actions = require "telescope.actions"
local actions_state = require "telescope.actions.state"
local entry_display = require "telescope.pickers.entry_display"
local conf = require("telescope.config").values

local function finder_fn()
    return function(_)
        local res = vim.g.spotify_results
        local results = {}

        for _, v in pairs(res) do
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
            { entry.title, "TelescopeResultsNumber" },
            { entry.artist, "TelescopeResultsComment" },
        }
    end

    return function(entry)
        return {
            artist = entry.artist,
            title = entry.title,
            uri = entry.uri,
            display = make_display,
            ordinal = entry.title .. " " .. entry.artist,
        }
    end
end

local spotify = function (opts)
    opts = opts or {}
    local query = vim.g.spotify_query
    pickers.new(opts, {
        prompt_title = "Showing Spotify results for: " .. query,
        finder = finders.new_dynamic({
            entry_maker = entry_fn(opts),
            fn = finder_fn()
        }),
        sorter = conf.generic_sorter(opts),
        initial_mode = "normal",
        attach_mappings = function (prompt_bufnr, map)
            actions.select_default:replace(function()
                actions.close(prompt_bufnr)
                local selection = actions_state.get_selected_entry()
                local cmd = ":silent SpotifyPlay " .. selection.uri
                vim.api.nvim_command(cmd)
            end)
            -- This maps control to add to queue instead of playing immediately.
            map('n', '<C-c>', function()
                actions.close(prompt_bufnr)
                local selection = actions_state.get_selected_entry()
                local cmd = ":silent SpotifyAdd " .. selection.uri
               vim.api.nvim_command(cmd)
            end)
            map('i', '<C-c>', function()
                actions.close(prompt_bufnr)
                local selection = actions_state.get_selected_entry()
                local cmd = ":silent SpotifyAdd " .. selection.uri
               vim.api.nvim_command(cmd)
            end)
            return true
        end
    }):find()
end

local list_devices = function (opts)
    opts = opts or {}
    pickers.new(opts, {
        prompt_title = "Select a Spotify device to connect to",
        finder = finders.new_dynamic({
            entry_maker = function(entry)
                return {
                    name = entry.name,
                    id = entry.id,
                    display = entry.name,
                    ordinal = entry.name
                }
            end,
            fn = function()
                local res = vim.g.spotify_devices
                local results = {}
                for _, v in pairs(res) do
                    table.insert(results,{name = v.name, id = v.id})
                end
                return results
            end
        }),
        sorter = conf.generic_sorter(opts),
        initial_mode = "normal",
        attach_mappings = function(prompt_bufnr, _)
            actions.select_default:replace(function()
                actions.close(prompt_bufnr)
                local selection = actions_state.get_selected_entry()
                vim.g.spotify_device = selection
            end)
            return true
        end
    }):find()
end


local M = {
    opts = {
        status = {
            update_interval = 10000,
        }
    },
    status = {},
    _status_line = ""
}

M.namespace = "Spotipy.nvim"

function M.setup(opts)

    M.opts = vim.tbl_deep_extend("force", M.opts, opts or {})
    vim.api.nvim_set_keymap("n", "<leader>mt", ":SpotifyToggle<CR>", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>ml", ":SpotifyPlaylist<CR>", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>mn", ":SpotifyPlayback -n<CR>", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>mp", ":SpotifyPlayback -p<CR>", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>md", ":SpotifyDevices<CR>", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>ms", ":lua require('neovim-spotify').search()<CR>", { noremap = true, silent = true })

end

function M.init()
    local opts = require'telescope.themes'.get_dropdown{}
    spotify(opts)
end

function M.show_devices()
    local opts = require'telescope.themes'.get_dropdown{}
    list_devices(opts)
end

function M.search()
    local query = vim.fn.input("Search Spotify: ")
    vim.cmd("SpotifySearch " .. vim.fn.shellescape(query))
end

function M.status:start()
    local timer = vim.loop.new_timer()
    timer:start(1000, M.opts.status.update_interval, vim.schedule_wrap(function()
        vim.api.nvim_call_function("SpotifyLine", {})
        local status = vim.g.spotify_line or nil
        self:on_event(status)
    end))
end

function M.status:on_event(data)
    if data then
        M._status_line = data
    end
end
function M.status:listen()
    return M._status_line
end

return M
