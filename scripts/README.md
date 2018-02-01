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