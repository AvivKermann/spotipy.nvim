local pickers = require "telescope.pickers"
local finders = require "telescope.finders"
local actions = require "telescope.actions"
local actions_state = require "telescope.actions.state"
local entry_display = require "telescope.pickers.entry_display"
local conf = require("telescope.config").values

local function finder_fn()
    return function(_)
        local res = vim.g.spotify_search_results
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

local function spotify_search_input()
    vim.ui.input({ prompt = "Search Spotify Tracks: " }, function(input)
        -- no need to check input, python does this for us
        spotify_search(input)
    end)
end

local function spotify_search(query)
    query = query or ""
    local cmd = ":call SpotifySearch('" ..query.. "')"
    vim.api.nvim_command(cmd)
end

local M = {}

M.namespace = 'Spotify'

function M.setup(_)
    -- M.opts = vim.tbl_deep_extend("force", M.opts, opts)
    vim.api.nvim_set_keymap("n", "<Leader>ms", ":lua spotify_search_input()<CR>", { noremap = true, silent = true })
end

function M.init()
    local opts = require'telescope.themes'.get_dropdown{}
    spotify(opts)
end
return M

