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
        layout_config = {
            width = 0.5,
            height = 0.1,
            results_height = 0,
        },
        attach_mappings = function(prompt_bufnr, map)
            actions.select_default:replace(function()
                local input = action_state.get_current_line()
                actions.close(prompt_bufnr)
                if input and input ~= "" then
                    -- Execute the SpotifySearch command with the user input
                    vim.cmd("SpotifySearch " .. vim.fn.escape(input, " "))
                else
                    vim.notify("Search query cannot be empty", vim.log.levels.ERROR)
                end
            end)
            return true
        end,
    }):find()
end

return M

