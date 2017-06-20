A GUI for viewing intermediate steps and results when processing leave images.

### Running

This application was tested with `python==3.6.1`. The python package `virtualenv` is needed to create an isolated python environment for further packages to be installed in.

Clone the repository, `cd` into it and run `run.sh` or follow these steps:

```
git clone https://github.com/ttoe/leaves-ui

cd leaves-ui

virtualenv .

source bin/activate
```

Make sure a python executable of at least version 3.6 was copied into the local environment.

Then install the needed packages in the activated virtual environment.

```
pip install -r packages.txt
```

Run `Main.py` from within the activated virtual environment, i.e. `src/Main.py` after making it executable or run `python src/Main.py` instead.

Choose a directory containing images, e.g. the `img/` directory from this repository.

After quitting the program run `deactivate` to deactivate the virtual environment.

### Using a custom image processing pipe

The entrance point Main.py uses the returned data of a function called `processing_pipe` from `pipe.py`. This function takes as input an image file that must be readable by skimage's `imread` function.

The base app needs the `processing_pipe` function to return a dictionary of the following key-value pairs:

```python
{
  "original_img": <ndarray> # dimensions: MxNx3; returned by skimage.data.imread()
  "greyscale_img": <ndarray> # dimensions: MxNx1
  "segmented_ubyte_img_bw": <ndarray of uint8> # dimensions: MxNx1; returned by skimage.util.img_as_ubyte()
  "labelled_image": <ndarray of dtype int> # dimensions: MxNx1; returned by skimage.measure.label() 
  "labelled_ubyte_img_rbg": <ndarray of uint8> # dimensions: MxNx3; applying skimage.util.img_as_ubyte() to the combination of labelled_image with the original image using skimage.color.label2rgb() 
  "regions_properties": <pandas.Dataframe> # containing arbitrary data calculated and aggregated during image processing
}
```

Other modifications would most likely make it necessary, to modify utility functions and the `BaseApp` class.