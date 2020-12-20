# CmdSearch #

__Note:__ CmdSearch is a bacon utility.

## Setup ##

CmdSearch is a superficial wrapper for The Silver Searcher.  You will need this installed in order for CmdSearch to work.

Mac OS X:

```
brew install the_silver_searcher
```

Once The Silver Searcher is installed, you can clone the CmdSearch repo into your bacon-bits folder.

CmdSearch uses the alias `srch` to run.  Be sure to add this to your bacon's .bashrc file:

```
alias srch="python ~/Documents/bacon-bits/CmdSearch/actions.py"
```

## Usage ##

To search the directory that you are currently in, do:

```
srch - name:someFile.txt
```

Note that CmdSearch uses the "-" character as the search's action command.  The "name" parameter is just as it sounds; it searches files by name.  If you would like to search contents instead, do:

```
srch - contains:someString
```

If you would like to search a different directory than the one that you're in, do:

```
srch - contains:someString dir:~/
```

Finally, if you would like to include hidden files in the search, do:

```
srch - contains:someString dir:~/ hidden:true
```

You can also do "h" for short:

```
srch - contains:someString dir:~/ h:true
```

## Arguments ##

- __name:__ = string to search (as file name)
- __contains:__ = search contents
- __dir:__ = specify the root directory to start searching
- __hidden:__ = 'true', include hidden files
- __h:__ = shortened version of "hidden"
- __kind:__ = filter by selected file kind (Options: `srch kind`)




