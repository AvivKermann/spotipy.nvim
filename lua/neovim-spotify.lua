local pickers = require "telescope.pickers"
local finders = require "telescope.finders"
local actions = require "telescope.actions"
local actions_state = require "telescope.actions.state"
local entry_display = require "telescope.pickers.entry_display"
local conf = require("telescope.config").values

local function finder_fn()
    return function(_)
        local res = vim.g.spotify_search
        local results = {}

        for _, v in pairs(res) do
            table.insert(results, { v[1], v[2], v[3] })
        end

        return results
    end
end

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
        if vim.g.spotify_type == 'Artists' or vim.g.spotify_type == 'Playlists' then
            return displayer {
                { entry.track, "TelescopeResultsNumber" },
            }
        end

        return displayer {
            { entry.track, "TelescopeResultsNumber" },
            { entry.artist, "TelescopeResultsComment" },
        }
    end

    return function(entry)
        print(vim.inspect(entry))
        return {
            artist = entry[2],
            track = entry[1],
            uri = entry[3],
            display = make_display,
            ordinal = entry[1] .. entry[2],
        }
    end
end

local spotify = function (opts)
    opts = opts or {}
    pickers.new(opts, {
        prompt_title = "Spotify (" .. vim.g.spotify_type .. ": " .. vim.g.spotify_title .. ")",
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

local M = {}
M.namespace = "Spotify"
function M.init()
    spotify(require("telescope.themes").get_dropdown{})
end

