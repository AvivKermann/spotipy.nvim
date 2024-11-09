local pickers = require('telescope.pickers')
local finders = require('telescope.finders')
local actions = require('telescope.actions')
local action_state = require('telescope.actions.state')
local conf = require('telescope.config').values

local M = {}

function M.search_tracks()
    pickers.new({}, {
        prompt_title = 'Search Spotify',
        finder = finders.new_table {
            results = {}, -- No initial results, just an input prompt.
            entry_maker = function(entry)
                return {
                    value = entry,
                    display = entry,
                    ordinal = entry,
                }
            end,
        },
        sorter = conf.generic_sorter({}),
        layout_config = {
            width = 0.5, -- Adjust width of the picker window (50% of the screen width)
            height = 0.1, -- Adjust height of the picker window (10% of the screen height)
            preview_width = 0.4, -- Optional: Set the preview window width, you can remove this if not needed
        },
        previewer = false,
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

