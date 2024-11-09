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
            results = {}, -- No initial results; this is for input.
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
            local execute_search = function()
                local input = action_state.get_current_line()
                actions.close(prompt_bufnr)
                if input and input ~= "" then
                    vim.cmd("SpotifySearch " .. vim.fn.escape(input, " "))
                else
                    print("Search query cannot be empty")
                end
            end

            -- Map <CR> in Normal mode
            map('n', '<CR>', execute_search)

            -- Map <CR> in Insert mode
            map('i', '<CR>', execute_search)

            return true
        end,
    }):find()
end

return M

