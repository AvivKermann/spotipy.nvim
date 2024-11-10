if exists('g:loaded_neovim_spotify')
    finish
endif
let g:loaded_neovim_spotify = 1

" Ensure python3 support is available
if !has('python3')
    echohl ErrorMsg
    echom 'This plugin requires python3 support'
    echohl None
    finish
endif

" Force python3 plugin registration
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
python3 << EOF
import sys
from pathlib import Path
plugin_root = Path(vim.eval('s:plugin_root_dir')).parent
python_root = plugin_root / 'rplugin' / 'python3'
sys.path.append(str(python_root))
EOF
