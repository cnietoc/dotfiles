#!/usr/bin/env zsh
# Uncomment for debuf with `zprof`
# zmodload zsh/zprof

source "$DOTLY_PATH/shell/zsh/bindings/dot.zsh"
source "$DOTLY_PATH/shell/zsh/bindings/reverse_search.zsh"
source "$DOTFILES_PATH/shell/zsh/key-bindings.zsh"
source "$DOTFILES_PATH/shell/zsh/lazy-functions.zsh"
source "$DOTFILES_PATH/shell/init.sh"

# ZSH Ops
# History
export HISTSIZE=200000                 # en memoria
export SAVEHIST=200000                 # en disco

# Escritura/lectura entre varias terminales
setopt APPEND_HISTORY                  # nunca sobrescribe, siempre añade
setopt INC_APPEND_HISTORY_TIME         # escribe al terminar cada comando (con duración)
setopt SHARE_HISTORY                   # comparte historial en tiempo real entre sesiones
setopt HIST_FCNTL_LOCK                 # lock seguro del archivo (importante con varias sesiones)

# Limpieza de historial
setopt HIST_IGNORE_ALL_DUPS            # elimina duplicados antiguos al guardar uno nuevo
setopt HIST_SAVE_NO_DUPS               # no duplica al volcar a fichero
setopt HIST_IGNORE_SPACE               # no guarda comandos con espacio inicial
setopt HIST_REDUCE_BLANKS              # normaliza espacios
setopt HIST_FIND_NO_DUPS               # búsquedas más limpias
setopt EXTENDED_HISTORY                # timestamp + duración

setopt nomatch
setopt autopushd

ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets)
# Async mode for autocompletion
ZSH_AUTOSUGGEST_USE_ASYNC=true
ZSH_HIGHLIGHT_MAXLENGTH=300

# Compile ZIM init if needed
if [[ ! -f "$ZIM_HOME/init.zsh.zwc" || "$ZIM_HOME/init.zsh" -nt "$ZIM_HOME/init.zsh.zwc" ]]; then
  zcompile "$ZIM_HOME/init.zsh"
fi

# Start Zim
source "$ZIM_HOME/init.zsh"

# ZSH style
if [[ -z $TMUX ]]; then
  zstyle ':completion:*:descriptions' format '[%d]'
  zstyle ':fzf-tab:*' switch-group ',' '.'
  zstyle ':fzf-tab:*' fzf-flags --height=40% --layout=reverse --border
  zstyle ':fzf-tab:*' use-fzf-default-opts yes
  zstyle ':fzf-tab:complete:*' fzf-preview '${DOTFILES_PATH}/shell/zsh/preview.sh $realpath'
else
  zstyle ':fzf-tab:*' fzf-command ftb-tmux-popup
fi;

${DOTFILES_PATH}/shell/fastfetch/run.sh

eval "$(starship init zsh)"

if command -v mise &> /dev/null; then
  eval "$(mise activate zsh)"
fi

# Added by ToolHive UI - do not modify this block
export PATH="$HOME/.toolhive/bin:$PATH"
# End ToolHive UI

eval "$(zoxide init zsh)"
source <(fzf --zsh)
eval "$(atuin init zsh)"
