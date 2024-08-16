# ------------------------------------------------------------------------------
# Codely theme config
# ------------------------------------------------------------------------------
export CODELY_THEME_MODE="dark"
export CODELY_THEME_PWD_MODE="home_relative"    # full, short, home_relative
export CODELY_THEME_STATUS_ICON_OK="➤"  #  ﭧ ﯓ ﬦ          
export CODELY_THEME_STATUS_ICON_KO="✖"  # ﮊ
export CODELY_THEME_PROMPT_IN_NEW_LINE=true

if [[ $__CFBundleIdentifier == "com.jetbrains."* ]]; then
  export CODELY_THEME_MINIMAL=false
fi

if [[ $__CFBundleIdentifier == "com.microsoft."* ]]; then
  export CODELY_THEME_MINIMAL=true
  export CODELY_THEME_MODE=light
fi

# ------------------------------------------------------------------------------
# Languages
# ------------------------------------------------------------------------------
export GEM_HOME="$HOME/.gem"
export GOPATH="$HOME/.go"
export SDKMAN_DIR="$HOME/.sdkman"

# ------------------------------------------------------------------------------
# Apps
# ------------------------------------------------------------------------------
if [ "$CODELY_THEME_MODE" = "dark" ]; then
  fzf_colors="pointer:#ebdbb2,bg+:#3c3836,fg:#ebdbb2,fg+:#fbf1c7,hl:#8ec07c,info:#928374,header:#fb4934"
else
  fzf_colors="pointer:#db0f35,bg+:#d6d6d6,fg:#808080,fg+:#363636,hl:#8ec07c,info:#928374,header:#fffee3"
fi

export FZF_DEFAULT_OPTS="--color=$fzf_colors --reverse"

export DOCKER_SOCK_FILE=/var/run/docker.sock

# Homebrew
export HOMEBREW_AUTO_UPDATE_SECS=604800 # 1 week
if [ -f "/opt/homebrew/bin/brew" ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Default lang
export LANG="es_ES.UTF-8"

# ------------------------------------------------------------------------------
# OneDrive
# ------------------------------------------------------------------------------
export ONE_DRIVE_TELEFONICA="$HOME/Library/CloudStorage/OneDrive-Telefonica"
export ONE_DRIVE_PERSONAL="$HOME/Library/CloudStorage/OneDrive-Personal"

# ------------------------------------------------------------------------------
# Telefonica tooling
# ------------------------------------------------------------------------------
export DEVTOOLS_PATH="$HOME/Projects/Telefonica/devtools"
export TELEFONICA_CONFIG_PATH="$ONE_DRIVE_TELEFONICA/config"

# ------------------------------------------------------------------------------
# Scripts environment variables
# ------------------------------------------------------------------------------
export AZURE_CONTEXTS="$TELEFONICA_CONFIG_PATH/azure-k8s-contexts"

# ------------------------------------------------------------------------------
# Path - The higher it is, the more priority it has
# ------------------------------------------------------------------------------
path=(
	"$HOME/bin"
	"$DOTLY_PATH/bin"
	"$DOTFILES_PATH/bin"
	"$JAVA_HOME/bin"
	"$GEM_HOME/bin"
	"$GOPATH/bin"
	"$HOME/Library/Application Support/JetBrains/Toolbox/scripts"
	"$HOME/.local/bin"
	"$HOME/.cargo/bin"
	"/usr/local/opt/ruby/bin"
	"/usr/local/opt/python/libexec/bin"
	"/opt/homebrew/bin"
	"/usr/local/bin"
	"/usr/local/sbin"
	"/bin"
	"/usr/bin"
	"/usr/sbin"
	"/sbin"
	$path
)

export path
