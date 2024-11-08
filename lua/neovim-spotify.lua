local pickers = require("telescope.pickers")
local finders = require("telescope.finders")
local conf = require("telescope.config").values
local actions = require("telescope.actions")
local action_state = require("telescope.actions.state")
local entry_display = require("telescope.pickers.entry_display")

local M = {}

M.spotify_live_search = function()
  -- Create a displayer to format the entries
  local displayer = entry_display.create({
    separator = " by ",
    items = {
      { width = 40 },  -- Track name width
      { remaining = true }  -- Artist name takes the rest of the space
    },
  })

  -- Function to generate the display format for each entry
  local function make_display(entry)
    return displayer({ entry.track_name, entry.artist_name })
  end

  local opts = {
    prompt_title = "Spotify Live Search",
    finder = finders.new_dynamic({
      fn = function(input)
        -- If the input is empty, return an empty table
        if not input or input == "" then
          return {}
        end
        -- Call the `spotify.search` function in Neovim and get the results
        local search_results = vim.fn.rpcrequest(0, "nvim_exec_lua", "return require('spotify').search('" .. input .. "')", {})
        -- If no results are found, return an empty table
        if not search_results or #search_results == 0 then
          return {}
        end

        -- Create the entries to display in Telescope
        local entries = {}
        for _, result in ipairs(search_results) do
          -- Add each result entry with necessary fields for display and sorting
          table.insert(entries, {
            value = result.uri,  -- Unique identifier (URI of the track)
            track_name = result.track_name,  -- Track name
            artist_name = result.artist_name,  -- Artist name
            display = make_display,  -- Display formatting function
            ordinal = result.track_name .. " " .. result.artist_name  -- Used for sorting
          })
        end
        return entries
      end
    }),
    sorter = conf.generic_sorter({}),  -- Default sorting for entries
    attach_mappings = function(prompt_bufnr, map)
      -- Define the default action when an entry is selected (Enter key)
      actions.select_default:replace(function()
        local selection = action_state.get_selected_entry()
        if selection then
          actions.close(prompt_bufnr)
          -- Play the selected track by its URI
          vim.fn.rpcnotify(0, "nvim_exec_lua", "require('spotify').play_track('" .. selection.value .. "')", {})
        end
      end)

      return true
    end,
  }

  -- Start the picker with the given options
  pickers.new({}, opts):find()
end

return M

