local M = {}

function M.init()
    local tracks = vim.g.spotify_search_results
    print(vim.inspect(tracks))
end

return M
