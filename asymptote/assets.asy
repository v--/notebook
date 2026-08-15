import graph;

path blob1 = (-0.2, -0.4) .. (-0.2, -0.2) .. (-0.1, 0.4) .. (0.1, 0.2) .. (0.5, 0.1) .. (0.1, -0.1) .. cycle;

path get_cross(real extent, real thickness) {
  return (-extent, -thickness) -- (-thickness, -thickness) -- (-thickness, -extent) -- (thickness, -extent) -- (thickness, -thickness) -- (extent, -thickness) -- (extent, thickness) -- (extent, thickness) -- (thickness, thickness) -- (thickness, extent) -- (-thickness, extent) -- (-thickness, thickness) -- (-extent, thickness) -- cycle;
}
