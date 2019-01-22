# phrag.py

A simple python script that can be used to generate config files from phragments.

## How it works

Let's say, for the sake of example, that you use [i3wm](https://i3wm.org/). You have your config file in a git repo, and you share it across machines, for the ultimate uniform experience.

But sometimes, the ultimate uniform experience may not be what you are looking for.

You may want to have a certain set of theme colors in a computer (say, your personal ThinkPad x220) and a completely different one in another.

So, how can phrag help?

The i3wm `config` file is, by default (at least on ubuntu, which I use), on `~/.config/i3/config`.

Create a folder inside that folder called `phrag` (so, `~/.config/i3/phrag`).

Inside that folder, create a folder called `config` (note, same name as the file we will end up creating).

And inside that one, create 3 files:
  * `config.template`
  * `colors`
  * `colors.default`
  
Fill the file `config.template` with the settings that will be common to all versions of the `config` file. Bindings, startup programs, etc...

Now, in the place where you would fill the colors, with something like this:

```
client.focused           #222AD9 #222AD9 #FFFFFF #2E9EF4 #285577 
client.focused_inactive  #5F676A #5F676A #FFFFFF #484E50 #5F676A 
client.urgent            #FF003F #FF003F #FFFFFF #FF003F #FF003F 
client.unfocused         #333333 #333333 #888888 #292D2E #222222 
client.placeholder       #0C0C0C #0C0C0C #FFFFFF #000000 #0C0C0C 
client.background        #FFFFFF
```
instead put only this:

```
{{colors}}
```
Put the color information in the `colors` file you created earlier instead. The `colors.default` file will be used instead, if found, if the `colors` file is not found.

If a file with the same name as a matching string is not found, the tag is ignored. This may cause errors, so it is advisable to have defaults files for each tag.

Now run `phrag`, like so:

`python3 phrag.py --workingDir ~/.config/i3`

And voilá, a new version of the `~/.config/i3/config` file will have been generated, that has the phragments defined in `~/.config/i3/phrag/config` that have matching tags.

This allows one to only have to check into VCS the `.template`  and `.default` files, leaving you free to override them at will in individual machines.
