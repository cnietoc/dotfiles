# Enable aliases to be sudo’ed
alias sudo='sudo '

alias ..="cd .."
alias ...="cd ../.."
alias ll="ls -l"
alias la="ls -la"
alias ~="cd ~"
alias dotfiles='cd $DOTFILES_PATH'

# Git
alias gaa="git add -A"
alias gc='$DOTLY_PATH/bin/dot git commit'
alias gca="git add --all && git commit --amend --no-edit"
alias gco="git checkout"
alias gd='$DOTLY_PATH/bin/dot git pretty-diff'
alias gs="git status -sb"
alias gf="git fetch --all -p"
alias gps="git push"
alias gpsf="git push --force"
alias gpl="git pull --rebase --autostash"
alias gb="git branch"
alias gl='$DOTLY_PATH/bin/dot git pretty-log'

# Utils
alias k='kill -9'
alias i.='(idea $PWD &>/dev/null &)'
alias c.='(code $PWD &>/dev/null &)'
alias o.='open .'
alias up='dot package improved_update_all'

# Python
alias python="python3"

# Telefonica
alias devtools='if [[ ":$PATH:" != *":$DEVTOOLS_PATH/bin:"* ]]; then export PATH="$DEVTOOLS_PATH/bin:$PATH"; echo "Enabled devtools"; else export PATH=$(echo "$PATH" | tr ":" "\n" | grep -v "$DEVTOOLS_PATH/bin" | tr "\n" ":"); PATH=${PATH%:}; echo "Disabled devtools"; fi'
