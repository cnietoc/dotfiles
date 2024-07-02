#!/usr/bin/env zsh
# Uncomment for debuf with `zprof`
# zmodload zsh/zprof

# ZSH Ops
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FCNTL_LOCK
setopt +o nomatch
# setopt autopushd

ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets)

# Start Zim
source "$ZIM_HOME/init.zsh"

# Async mode for autocompletion
ZSH_AUTOSUGGEST_USE_ASYNC=true
ZSH_HIGHLIGHT_MAXLENGTH=300

source "$DOTFILES_PATH/shell/init.sh"

fpath=("$DOTFILES_PATH/shell/zsh/themes" "$DOTFILES_PATH/shell/zsh/completions" "$DOTLY_PATH/shell/zsh/themes" "$DOTLY_PATH/shell/zsh/completions" $fpath)

FPATH="$(brew --prefix)/share/zsh/site-functions:${FPATH}"

autoload -Uz promptinit && promptinit
prompt ${DOTLY_THEME:-codely}

source "$DOTLY_PATH/shell/zsh/bindings/dot.zsh"
source "$DOTLY_PATH/shell/zsh/bindings/reverse_search.zsh"
source "$DOTFILES_PATH/shell/zsh/key-bindings.zsh"

# Jenv
# export PATH="$HOME/.jenv/bin:$PATH"
# eval "$(jenv init -)"

eval $(thefuck --alias)

# Brew zsh-autosuggestions
# source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# Created by `pipx` on 2023-11-27 10:55:37
export PATH="$PATH:/Users/cx02243/.local/bin"

export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion

export DOCKER_SOCK_FILE=/var/run/docker.sock

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
