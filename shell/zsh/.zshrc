#!/usr/bin/env zsh
# Uncomment for debuf with `zprof`
# zmodload zsh/zprof

# ZSH Ops
# History
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_SAVE_NO_DUPS
setopt HIST_REDUCE_BLANKS
setopt INC_APPEND_HISTORY_TIME
setopt EXTENDED_HISTORY
setopt HIST_FCNTL_LOCK

setopt +o nomatch
# setopt autopushd

# ZSH style
if [[ -z $TMUX ]]; then
  zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza -1 --color=always $realpath'
else
  zstyle ':fzf-tab:*' fzf-command ftb-tmux-popup
fi;

ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets)

fpath=(
    "$DOTFILES_PATH/shell/zsh/themes"
    "$DOTFILES_PATH/shell/zsh/completions"
    "$DOTLY_PATH/shell/zsh/themes"
    "$DOTLY_PATH/shell/zsh/completions"
    "$HOMEBREW_PREFIX/share/zsh/site-functions"
    $fpath)

# Async mode for autocompletion
ZSH_AUTOSUGGEST_USE_ASYNC=true
ZSH_HIGHLIGHT_MAXLENGTH=300

source "$DOTFILES_PATH/shell/init.sh"

# Start Zim
source "$ZIM_HOME/init.zsh"

# Compile ZIM init if needed
if [[ ! -f "$ZIM_HOME/init.zsh.zwc" || "$ZIM_HOME/init.zsh" -nt "$ZIM_HOME/init.zsh.zwc" ]]; then
  zcompile "$ZIM_HOME/init.zsh"
fi

# Kubectl completions
source <(kubectl completion zsh)

source "$DOTLY_PATH/shell/zsh/bindings/dot.zsh"
source "$DOTLY_PATH/shell/zsh/bindings/reverse_search.zsh"
source "$DOTFILES_PATH/shell/zsh/key-bindings.zsh"
# source "$DOTFILES_PATH/shell/zsh/lazy-functions.zsh" # Only for node tools, let Mise handle it

# if Mise is installed, activate it
if command -v mise &> /dev/null; then
  eval "$(mise activate zsh)"
fi

autoload -Uz promptinit && promptinit
prompt ${DOTLY_THEME:-codely}
