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

local spotify = function (opts)
    opts = opts or {}
    local query = vim.g.spotify_search_query
    pickers.new(opts, {
        prompt_title = "Showing Spotify results for: " .. query,
        finder = finders.new_dynamic({
            entry_maker = entry_fn(opts),
            fn = finder_fn()
        }),
        sorter = conf.generic_sorter(opts),
        attach_mappings = function (prompt_bufnr, _)
            actions.select_default:replace(function()
                actions.close(prompt_bufnr)
                local selection = actions_state.get_selected_entry()
                print(vim.inspect(selection.uri))
                local cmd = ":SpotifyPlay " .. selection.uri
                print(vim.inspect(cmd))
                vim.api.nvim_command(cmd)
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

function M.setup(opts)

    M.opts = vim.tbl_deep_extend("force", M.opts, opts)
    vim.api.nvim_set_keymap("n", "<leader>mt", "SpotifyToggle", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>mn", "SpotifyPlayback -n", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>mp", "SpotifyPlayback -p", { noremap = true, silent = true })
    vim.api.nvim_set_keymap("n", "<leader>ms", "lua require('neovim-spotify').search()", { noremap = true, silent = true })

end

function M.init()
    local opts = require'telescope.themes'.get_dropdown{}
    spotify(opts)
end

function M.search()
    local query = vim.fn.input("Search Spotify: ")
    vim.cmd("SpotifySearch " .. vim.fn.shellescape(query))
end
