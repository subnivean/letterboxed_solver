*Save this next line for your project's `README.md`:*
This project was created from the template at https://github.com/subnivean/python_venv_app_template.

This is a template for setting up an app in a Python virtualenv.

After cloning, add your python venv to the `./venv` directory, e.g.:

```bash
python3.12 -m venv --prompt . venv312 --upgrade-deps
```

For standardardization, link your particular venv directory to one named `venv`:

```bash
ln -sf venv312 venv
```

Then, activate it with:

```bash
source ./venv/bin/activate
```

and then run (after giving `requirements.pip` a look):

```bash
./bin/python.sh -m pip install --upgrade pip
./bin/python.sh -m pip install -r requirements.pip
```

When using this framework, always run python via `python.sh` in the
`./bin` directory - this will set the proper environment variables
for IPython use and for importing packages from `./app-packages`.

You can override environment variables set in `./config/env_defaults.sh`
by creating a `./config/env_local.sh` file - this file will not be
tracked by Git.

Best practice for running IPython Qtconsole is thusly:
```
./bin/python.sh -m jupyter qtconsole &
```

You can also get easier access to programs in `./bin` by running:
```
source ./config/env_defaults.sh
```
which will prepend `./bin` to the PATH environment variable.

Finally, you might want to clone the `msk-python` repo into `./app-packages`:
```
git clone pihole2:gitrepos/msk-python.git $VIRTUAL_ENV/../app-packages/msk
```

