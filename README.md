# git-backupper

![tests](https://github.com/vladpunko/git-backupper/actions/workflows/tests.yml/badge.svg)

Simplest way to back up and restore git repositories.

![usage-example](https://raw.githubusercontent.com/vladpunko/git-backupper/master/git-backupper.gif)

## Installation

You are to have [git](https://git-scm.com) installed on your machine.

Use the package manager [pip](https://pip.pypa.io/en/stable) to install `git-backupper` with the command-line interface:

```bash
python3 -m pip install --user git-backupper
```

## Basic usage

Using this program allows you to mirror your git repositories to a backup location.

> **Warning:**
> Before you begin, it is important to make sure that you have configured git properly and have access to the repositories you want to back up.
> This will ensure that the backup process goes smoothly and your valuable data is protected.

You are to create a configuration file `.git_backupper.json` in your home directory with the following content:

```json
{
  "backup_path": "/tmp/backup_repositories",
  "repositories": [
    "https://github.com/vladpunko/git-backupper.git"
  ]
}
```

This configuration file specifies the directory where backups will be stored, and the git repositories that will be backed up.
By default, the backups will be stored in a hidden directory called `.backup_repositories` in your home directory.
You can customize the backup directory path by changing the value of the **backup_path** field.
If you want to include additional repositories in the backup list, just append their urls to the **repositories** array.

You can back up and restore your repository with the following commands:

```bash
# Step -- 1.
git-backupper  # back up all repositories from the configuration file

# Step -- 2.
cd /tmp/backup_repositories/git-backupper.git

# Step -- 3.
git push --mirror 'https://github.com/vladpunko/git-backupper.git'
```

## Contributing

Pull requests are welcome.
Please open an issue first to discuss what should be changed.

Please make sure to update tests as appropriate.

```bash
# Step -- 1.
python3 -m venv .venv && source ./.venv/bin/activate && pip install pre-commit tox

# Step -- 2.
pre-commit install --config .githooks.yml

# Step -- 3.
tox && tox -e lint
```

## License

[MIT](https://choosealicense.com/licenses/mit)
