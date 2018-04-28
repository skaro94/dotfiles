machine_type = {
        'p': 'personal',
        's': 'server'
}
default_type = 'p'

tasks = {
    # SHELLS
    '~/.bashrc' : 'bashrc',
    '~/.screenrc' : 'screenrc',

    # VIM
    '~/.vimrc' : 'vim/vimrc',
    '~/.vim' : 'vim',
    '~/.vim/autoload/plug.vim' : 'vim/bundle/vim-plug/plug.vim',

    # NeoVIM
    '~/.config/nvim' : 'nvim',

    # GIT
    '~/.gitconfig' : 'git/gitconfig',
    '~/.gitignore' : 'git/gitignore',

    # ZSH
    '~/.zgen'     : 'zsh/zgen',
    '~/.zsh'      : 'zsh',
    '~/.zlogin'   : 'zsh/zlogin',
    '~/.zlogout'  : 'zsh/zlogout',
    '~/.zpreztorc': 'zsh/zpreztorc',
    '~/.zprofile' : 'zsh/zprofile',
    '~/.zshenv'   : 'zsh/zshenv',
    '~/.zshrc'    : 'zsh/zshrc',

    # Bins
    '~/.local/bin/dotfiles' : 'bin/dotfiles',
    '~/.local/bin/fasd' : 'zsh/fasd/fasd',
    '~/.local/bin/is_mosh' : 'zsh/is_mosh/is_mosh',
    '~/.local/bin/imgcat' : 'bin/imgcat',
    '~/.local/bin/imgls' : 'bin/imgls',
    '~/.local/bin/fzf' : '~/.fzf/bin/fzf', # fzf is at $HOME/.fzf

    # X
    '~/.Xmodmap' : 'Xmodmap',

    # GTK
    '~/.gtkrc-2.0' : 'gtkrc-2.0',

    # tmux
    '~/.tmux'     : 'tmux',
    '~/.tmux.conf' : 'tmux/tmux.conf',

    # .config
    '~/.config/terminator' : 'config/terminator',
    '~/.config/pudb/pudb.cfg' : 'config/pudb/pudb.cfg',

    # pip and python
    #'~/.pip/pip.conf' : 'pip/pip.conf',
    '~/.pythonrc.py' : 'python/pythonrc.py',
    '~/.pylintrc' : 'python/pylintrc',
    '~/.condarc' : 'python/condarc',
    '~/.config/pycodestyle' : 'python/pycodestyle',
}

post_actions = [
    # zgen installation
    '''# Update zgen modules and cache (the init file)
    zsh -c "
        source ${HOME}/.zshrc                   # source zplug and list plugins
        zgen reset
        zgen update
    "
    '''

    # validate neovim package installation
    '''# neovim package needs to be installed
    if which nvim 2>/dev/null; then
        /usr/local/bin/python3 -c 'import neovim' || /usr/bin/python3 -c 'import neovim'
        rc=$?; if [[ $rc != 0 ]]; then
        echo -e '\033[0;33mNeovim requires 'neovim' package on the system python3. Please try:'
            echo -e '   /usr/local/bin/pip3 install neovim'
            echo -e '\033[0m'
        fi
    fi
    ''',

    # Run vim-plug installation
    {'install' : 'vim +PlugInstall +qall',
     'update'  : 'vim +PlugUpdate +qall',
     'none'    : ''}[args.vim_plug],

    # Install tmux plugins via tpm
    '~/.tmux/plugins/tpm/bin/install_plugins',

    # Change default shell if possible
    r'''# Change default shell to zsh
    if [[ ! "$SHELL" = *zsh ]]; then
        echo -e '\033[0;33mPlease type your password if you wish to change the default shell to ZSH\e[m'
        chsh -s /bin/zsh && echo -e 'Successfully changed the default shell, please re-login'
    fi
    ''',

    # Create ~/.gitconfig.secret file and check user configuration
    r'''# Create ~/.gitconfig.secret and user configuration
    if [ ! -f ~/.gitconfig.secret ]; then
        cat > ~/.gitconfig.secret <<EOL
# vim: set ft=gitconfig:
EOL
    fi
    if ! git config --file ~/.gitconfig.secret user.name 2>&1 > /dev/null; then echo -ne '
    \033[1;33m[!] Please configure git user name and email:
        git config --file ~/.gitconfig.secret user.name "(YOUR NAME)"
        git config --file ~/.gitconfig.secret user.email "(YOUR EMAIL)"
\033[0m'
    fi
    ''',
]
