local pickers = require('telescope.pickers')
local actions = require('telescope.actions')
local action_state = require('telescope.actions.state')
local conf = require('telescope.config').values

local M = {}

function M.search_tracks()
    pickers.new({}, {
        prompt_title = 'Search Spotify',
        finder = require('telescope.finders').new_table {
            results = {},
            entry_maker = function(entry)
                return {
                    value = entry,
                    display = entry,
                    ordinal = entry,
                }
            end,
        },
        sorter = conf.generic_sorter({}),
        previewer = false,
        layout_strategy = "center",
        layout_config = {
            width = 0.3,
            height = 0.05,
            anchor = "CENTER",
            prompt_position = "top"
        },
        results_title = false,
        borderchars = {
            prompt = {"─", "│", "─", "│", "╭", "╮", "╯", "╰"},
        },
        window = {
            results_width = 0,
            winblend = 0 ,
            results = {
                winblend = 0
            }
        },
        attach_mappings = function(prompt_bufnr, map)
            actions.select_default:replace(function()
                local input = action_state.get_current_line()
                actions.close(prompt_bufnr)
                if input and input ~= "" then
                    local tracks = vim.cmd("SpotifySearch " .. vim.fn.escape(input, " "))
                    vim.inspect(vim.g.spotify_search_results)
                else
                    vim.notify("Search query cannot be empty", vim.log.levels.ERROR)
                end
            end)
            return true
        end,
    }):find()
end
return M
