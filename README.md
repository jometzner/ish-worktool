# My dotfiles project
This is project contains intershop development specific settings that can be
cloned and distributed into developer machine setups. Usually it goes like
this:
- You have a new (empty) environment. Either because you have a new physical
  machine or a new OS user or a VM you want to equip with tooling
- Clone this git repository into `~/work/.dotfiles`
- Go to directory `~/work/.dotfiles/scripts` and execute `./install.sh`
- Start with setting up a new ICM development environment. You can use the
  `Work Tools` for that. Just type `wt setup_icm <version>`

# Work Tools - the swiss knife for ICM development

## System requirements

-   Python 3 or higher is necessary
-   pip - package manager for Python packages, see [PyPA](https://www.pypa.io/en/latest/)
-   git executable must be present in `PATH` system variable

## Installation

On Linux you can simply execute `./install.sh`.\
On Windows systems you need to execute `pip3 install --user easyargs && python3 setup.py install --user` **(not tested yet!)**

## Usage

`wt -h` lists every supported sub command (e.g all supported usecases)\
`wt <sub-command> -h` opens the help for the given sub-command

## Supported usecases

-   Creating folders for ICM development (scaffolding for later use cases)
-   Listing of existing ICM development environment(s)
-   Checking out assemblies or component sets from git and propagate their version to the other existing component sets
-   Updating checked out multi-projects and update incoming (and outgoing) dependencies of that project
-   Building and publish the artifact of a given multi-project
-   Build and publish all

## Known Issues

-   f_b2b and f_solrcloud are not supported yet
-   Deploying a server is not possible yet
