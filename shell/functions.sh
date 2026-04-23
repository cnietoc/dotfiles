function cdd() {
	cd "$(ls -d -- */ | fzf)" || echo "Invalid directory"
}

function j() {
	z "$@"
}

function recent_dirs() {
	# This script depends on pushd. It works better with autopush enabled in ZSH
	escaped_home=$(echo $HOME | sed 's/\//\\\//g')
	selected=$(dirs -p | sort -u | fzf)

	cd "$(echo "$selected" | sed "s/\~/$escaped_home/")" || echo "Invalid directory"
}

function bwu() {
    BW_STATUS=$(bw status | jq -r .status)
    case "$BW_STATUS" in
    "unauthenticated")
        echo "Logging into BitWarden"
        export BW_SESSION=$(bw login --raw)
        ;;
    "locked")
        echo "Unlocking Vault"
        export BW_SESSION=$(bw unlock --raw)
        ;;
    "unlocked")
        echo "Vault is unlocked"
        ;;
    *)
        echo "Unknown Login Status: $BW_STATUS"
        return 1
        ;;
    esac
    bw sync
}

function load_secrets() {
    [[ -z "$BW_SESSION" ]] && bwu
    for scope in "$@"; do
        case "$scope" in
            spotify)
                export SPOTIFY_CLIENT_ID=$(bw get username spotify-api --session "$BW_SESSION")
                export SPOTIFY_CLIENT_SECRET=$(bw get password spotify-api --session "$BW_SESSION")
                ;;
            telegram)
                export TL_TELEGRAM_TOKEN=$(bw get password telegram-tl-bot --session "$BW_SESSION")
                export TL_TELEGRAM_CHAT_ID=$(bw get notes telegram-tl-bot --session "$BW_SESSION")
                ;;
            steam)
                export STEAM_API_KEY=$(bw get password steam-api --session "$BW_SESSION")
                export STEAM_VANITY_URL=$(bw get username steam-api --session "$BW_SESSION")
                ;;
            notion)
                export NOTION_TOKEN=$(bw get password notion-api --session "$BW_SESSION")
                export NOTION_DHCP_DATASOURCE=$(bw get notes notion-api --session "$BW_SESSION")
                ;;
            router)
                export ROUTER_IP=$(bw get uris router-home --session "$BW_SESSION")
                export ROUTER_USER=$(bw get username router-home --session "$BW_SESSION")
                export ROUTER_PASS=$(bw get password router-home --session "$BW_SESSION")
                ;;
            atuin)
                export ATUIN_USERNAME=$(bw get username "hub.atuin.sh" --session "$BW_SESSION")
                export ATUIN_PASSWORD=$(bw get password "hub.atuin.sh" --session "$BW_SESSION")
                ;;
            *) echo "load_secrets: unknown scope '$scope'" >&2; return 1 ;;
        esac
    done
}

bitrate () {
    echo `basename "$1"`: `file "$1" | sed 's/.*, \(.*\)kbps.*/\1/' | tr -d " " ` kbps
}
