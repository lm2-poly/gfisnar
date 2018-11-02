This code is designed to transform a .gcode file obtained from a FDM 3D printer slicer to the format required by Fisnar.
The code can also support multimaterial 3D-printing using a Fisnar dispenser with a custom 3D printed head for the fisnar. Please note that this code cannot support more than 3 materials.

# Ubuntu users

Before downloading the code and installing the necessary libraries, we will first need to install some dependencies you will need:
`sudo apt-get install python-dev python-pip`

Now, go to an empty folder you'd like to use for this repository.
Open a terminal (`Ctrl` + `T`):

1. Download the code: `git clone git@github.com:lm2-poly/gfisnar.git`
2. Install the necessary python dependencies: `pip install requirements.txt`

You can now use the gfisnar code.

We would recommend you to use a Python Virtual Environment before step 2.

# Basic Usage

1. Edit `input.yaml` and set your parameters

2. execute 'main.py' in order to try the code: `python main.py`

3. The code will produce an `output.csv` file that you can open with Excel

### Input

The file `input.yaml.example` provides an example of input file.

The parameters in the file:
* `InputFile / Path` : Path of the .gcode input file

* `Minimal print distance / D` : Smallest acceptable distance between two points for the fisnar machine

# Current limitation

The code is limited to 3 materials for multimaterial printing.

