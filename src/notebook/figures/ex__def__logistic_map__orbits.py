import math
import os
import pathlib
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from textwrap import dedent

import numpy as np
import PIL.Image

from ..paths import AUX_PATH, ROOT_PATH


output_path = AUX_PATH / pathlib.Path(__file__).with_suffix('').name
tmp_path = pathlib.Path(tempfile.mkdtemp())
raster_path = tmp_path / 'intermediate.eps'  # Asymptote requires EPS, which does not support transparency
code_path = tmp_path / 'diagram.asy'


x_resolution = 1500
x_0 = 0.5

a_resolution = 3000
a_min = 2
a_max = 4

iterations = 600
min_iterations = 100


def fill_pixels(j: int) -> np.ndarray:
    a = a_min + (a_max - a_min) * j / a_resolution
    x = x_0
    column = np.full(x_resolution, dtype=np.uint8, fill_value=255)

    for it in range(iterations):
        x = a * x * (1 - x)

        if it >= min_iterations:
            i = x_resolution - math.floor(x * x_resolution)

            if 0 <= i < x_resolution:
                column[i] = 0

    return column


with ThreadPoolExecutor() as executor:
    columns = list(executor.map(fill_pixels, list(range(a_resolution))))


# We concatenate along axis 1 and not 0 because Pillow expects a transposed matrix
pixels = np.stack(columns, axis=1)
img = PIL.Image.fromarray(pixels, 'L')
img.save(raster_path)


with open(code_path, 'w') as code_file:
    code_file.write(
        dedent(f'''\
            unitsize(6.5cm);

            import graph;

            from notebook access pens;

            limits(min=(2, 0), max=(4, 1));
            label(graphic('{raster_path}', 'width=13cm, height=6.5cm'), (3, 0.5));

            xaxis(
              Label('$a$'),
              axis=Bottom,
              ticks=Ticks(pTick=pens.thin, Step=0.5, step=0.1)
            );

            yaxis(
              Label('$x$'),
              axis=Left,
              ticks=Ticks(pTick=pens.thin, Step=0.2, step=0.1)
            );
            '''
        )
    )

os.system(f'asy -dir={ROOT_PATH} -outname={output_path} {code_path}')  # noqa: S605
shutil.rmtree(tmp_path)
