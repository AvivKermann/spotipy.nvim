local builtins = require("telescope.builtin")

local M = {}

function M.search_tracks()
    builtins.input({
        prompt = "Search Tracks",
        default_text = "",
        on_submit = function(query)
            if query and query ~= "" then
                vim.cmd("SpotifySearch " .. vim.fn.escape(query, " "))
            else
                print("Search query cannot be empty")
            end
        end,
    })
end

return M
