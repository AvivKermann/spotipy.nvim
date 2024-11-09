local pickers = require('telescope.pickers')
local finders = require('telescope.finders')
local actions = require('telescope.actions')
local action_state = require('telescope.actions.state')
local conf = require('telescope.config').values

local M = {}

function M.search_tracks()
    pickers.new({}, {
        prompt_title = 'Search Spotify Tracks',
        finder = finders.new_table {
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
        attach_mappings = function(prompt_bufnr, map)
            actions.select_default:replace(function()
                local input = action_state.get_current_line()
                vim.inspect("SpotifySearch " .. input)
                if input and input ~= "" then
                    vim.api.nvim_command("SpotifySearch " .. vim.fn.escape(input, " "))
                else
                    print("Search query cannot be empty")
                end
            end)
            return true
        end,
    }):find()
end

return M

