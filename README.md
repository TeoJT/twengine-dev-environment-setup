# TWEngine Development Environment Installer

A tool used to automatically set up your entire work environment for developing [Timeway](https://github.com/TeoJT/Timeway), [SketchIO](https://github.com/TeoJT/Sketchio), and any other project that uses TWEngine.

## How to use

Super easy!

First, clone/download this repository (duh)

Then, [install Python](https://www.python.org/downloads/) on your machine if not installed already. If you're using Windows, you can use either native Windows Python or Python in Windows Subsystem for Linux.

Then, run `python3 setup.py`.

The installer will run you through the rest.

## What it does

1. Download and extract the Processing IDE
2. Patches the Processing core
3. Installs icons and themes.
4. Installs libraries. These libraries are stored in your Documents/Processing folder and if you already have an instance of Processing installed, there may be conflicts. TODO: Rename libraries to avoid conflicts.
