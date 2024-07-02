if (( ${+ZIM_HOME} )) zimfw() { source "${HOME}/.dotfiles/shell/zsh/.zim/zimfw.zsh" "${@}" }
fpath=("${HOME}/.dotfiles/shell/zsh/.zim/modules/git-info/functions" "${HOME}/.dotfiles/shell/zsh/.zim/modules/zsh-completions/src" ${fpath})
autoload -Uz -- coalesce git-action git-info
source "${HOME}/.dotfiles/shell/zsh/.zim/modules/environment/init.zsh"
source "${HOME}/.dotfiles/shell/zsh/.zim/modules/input/init.zsh"
source "${HOME}/.dotfiles/shell/zsh/.zim/modules/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
source "${HOME}/.dotfiles/shell/zsh/.zim/modules/zsh-autosuggestions/zsh-autosuggestions.zsh"
source "${HOME}/.dotfiles/shell/zsh/.zim/modules/completion/init.zsh"
