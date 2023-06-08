# Deciphering Cloud Optimized GeoTIFFs

Here is the code to reproduce the analysis in [this blog post](https://www.kitware.com/deciphering-cloud-optimized-geotiffs/)

Also hosted [here](https://data.kitware.com/#folder/6267337e4acac99f42fa5844)

## Steps

### 1. Install dependencies

Install `rangehttpserver` to be able to launch a local web server that supports HTTP range requests so that we can simulate a "real" webserver.

```bash
pip install rangehttpserver memory_profiler GDAL
```

### 2. Download the data

Download the two raster datasets from [here](https://data.kitware.com/#folder/6267337e4acac99f42fa5844).
One is a valid COG (labeled with the `_COG` suffix) and the other is invalid.

Place these files in a dedicated directory from which to launch the web server

### 3. Launch web server

Run the following to launch a webserver where you save the above data files

```bash
python -m RangeHTTPServer
```

### 4. Run the test script

Run the test script for the valid and invalid files individually and count the the amount of GET requests on the web server to see the difference in efficiencies.

```py
python test_cog.py
```
