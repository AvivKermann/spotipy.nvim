local config = {}
local function setup(cfg)
    config = cfg
    vim.keymap.set('n', '<Leader>w', ':call HelloWorld World<CR>', { silent = true })
end
local function getConfig()
    return config
end
return { setup=setup, getConfig=getConfig }
