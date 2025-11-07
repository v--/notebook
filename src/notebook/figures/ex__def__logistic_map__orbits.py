import math
import pathlib
import shutil
import subprocess
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

max_iterations = 1750
min_iterations = 1000

max_threads = 20
pixels_per_thread = a_resolution // max_threads
pixels = np.full((x_resolution, a_resolution), dtype=np.uint8, fill_value=np.iinfo(np.uint8).max)


def fill_column(j: int) -> None:
    a = a_min + ((a_max - a_min) * j / a_resolution)
    x = x_0

    for it in range(max_iterations):
        x = a * x * (1 - x)

        if it >= min_iterations:
            i = x_resolution - math.floor(x * x_resolution)

            if 0 <= i < x_resolution:
                pixels[i, j] = 0


def fill_columns(thread_index: int) -> None:
    for j in range(thread_index * pixels_per_thread, (thread_index + 1) * pixels_per_thread):
        fill_column(j)


with ThreadPoolExecutor() as executor:
    list(executor.map(fill_columns, list(range(max_threads))))


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
              p=fontsize(7),
              axis=Bottom,
              ticks=Ticks(pTick=pens.thin, Step=0.5, step=0.1)
            );

            yaxis(
              Label('$\\Phi_{{a,t}}(x_0)$'),
              p=fontsize(7),
              autorotate=false,
              axis=Left,
              ticks=Ticks(pTick=pens.thin, Step=0.2, step=0.1)
            );
            '''
        )
    )

try:
    subprocess.run(f'asy -dir={ROOT_PATH} -outname={output_path} {code_path}', shell=True, check=True)  # noqa: S602
except subprocess.CalledProcessError as err:
    raise SystemExit(1) from err
finally:
    shutil.rmtree(tmp_path)
