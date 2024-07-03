# This is a useful file to have the same aliases/functions in bash and zsh

source "$DOTFILES_PATH/shell/aliases.sh"
source "$DOTFILES_PATH/shell/exports.sh"
source "$DOTFILES_PATH/shell/functions.sh"

# Load SDKMAN
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

# Load thefuck
eval $(thefuck --alias)
