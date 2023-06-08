from urllib.parse import urlencode, urlparse

from memory_profiler import profile
from osgeo import gdal

kwargs = dict(
    xRes=611.49622628141,
    yRes=611.49622628141,
    outputBounds=[
        -9079495.967826376,
        3443946.7464169012,
        -8922952.933898335,
        3600489.780344942,
    ],
    srcSRS="+proj=utm +zone=17 +datum=WGS84 +units=m +no_defs",
    dstSRS="epsg:3857",
)


def make_vsi(url: str, **options):
    if str(url).startswith("s3://"):
        s3_path = url.replace("s3://", "")
        vsi = f"/vsis3/{s3_path}"
    else:
        gdal_options = {
            "url": str(url),
            "use_head": "no",
            "list_dir": "no",
        }
        gdal_options.update(options)
        vsi = f"/vsicurl?{urlencode(gdal_options)}"
    return vsi


@profile
def get_tile(path):
    # Open from remote server that supports HTTP range requests
    source = gdal.Open(path)
    # Extract tile 8/70/105
    ds = gdal.Warp("", source, format="VRT", **kwargs)
    # Perform operation and fetch data
    return ds.ReadAsArray()


# Web hosted data files
# valid = "/vsicurl?url=https%3A%2F%2Fdata.kitware.com%2Fapi%2Fv1%2Ffile%2F62d70e66bddec9d0c478d85c%2Fdownload&use_head=no&list_dir=no"
# invalid = "/vsicurl?url=https%3A%2F%2Fdata.kitware.com%2Fapi%2Fv1%2Ffile%2F626733ce4acac99f42fa5894%2Fdownload&use_head=no&list_dir=no"


# Or run locally with rangehttpserver
valid = make_vsi(
    "http://localhost:8000/LC08_L1TP_016039_20170829_20170914_01_T1_B7_COG.TIF"
)
invalid = make_vsi(
    "http://localhost:8000/LC08_L1TP_016039_20170829_20170914_01_T1_B7.TIF"
)


# Valid COG
get_tile(valid)
# uses ~25Mb
# 13.8 ms ± 1.54 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# Non-COG
get_tile(invalid)
# Uses ~160 Mb
# 17.2 s ± 1.74 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
