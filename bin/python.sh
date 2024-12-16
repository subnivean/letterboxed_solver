if [[ ! -v VIRTUAL_ENV ]]; then
  echo "You must be in an active Python virtual environment!"
else
  source $VIRTUAL_ENV/../config/env_defaults.sh
  if [ -f $VIRTUAL_ENV/../config/env_local.sh ]; then
    source $VIRTUAL_ENV/../config/env_local.sh
  fi
  python "$@"
fi
