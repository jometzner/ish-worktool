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
