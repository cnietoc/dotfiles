# aliases
nvm_cmds=("nvm" "npm" "node" "npx" "yarn")
function lazy_nvm {
  local value;
  for value in "${nvm_cmds[@]}"; do
    unset -f "${value}";
  done

  if [ -d "${HOME}/.nvm" ]; then
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" # linux
    [ -s "$(brew --prefix nvm)/nvm.sh" ] && source "$(brew --prefix nvm)/nvm.sh" # osx
  fi
}

# aliases
for value in "${nvm_cmds[@]}"; do
   eval "
    ${value}() {
      lazy_nvm
      ${value} \"\$@\"
    }"
done

unset value;
