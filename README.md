A GUI for viewing intermediate steps and results when processing leave images.

### Running

To run the program `python >= 3.5` is needed. The python package `virtualenv` is needed to create an isolated python environment for further packages to be installed in.

```
> git clone https://github.com/ttoe/leaves-ui
> cd leaves-ui
> virtualenv .
> source bin/activate
```

Make sure a python executable of version 3.5 or newer was copied into the local environment.

Then install the needed packages in the activated virtual environment.

```
> pip install -r leaves-ui/packages.txt
```

Run `Main.py` form within the activated virtual environment, e.g. `leaves-ui/src/Main.py`.
