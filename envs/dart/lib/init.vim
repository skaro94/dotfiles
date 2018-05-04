" hot reload
autocmd BufWritePost * execute 'silent !tmux send-keys -t :2.2 r'
autocmd BufWritePost * execute 'silent !tmux send-keys -t :2.3 r'
