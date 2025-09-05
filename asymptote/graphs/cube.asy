access 'asymptote/graphs/grdraw.asy' as grdraw;

struct CubeGraph {
  pair[][][] vertices;
  int segments;

  void operator init(int segments = 1, real dist = 1, real y_factor = 1 / 2) {
    this.segments = segments;
    this.vertices = new pair[segments + 1][segments + 1][segments + 1];

    // Axis scale factor
    // sf + sf ** 3 = 1
    real sf = cbrt(1 / 2 + sqrt(31 / 108)) + cbrt(1 / 2 - sqrt(31 / 108));

    for (int x = 0; x <= segments; ++x) {
      for (int y = 0; y <= segments; ++y) {
        for (int z = 0; z <= segments; ++z) {
          this.vertices[x][y][z] = dist * (x * (sf, 0) + y * (0, sf) + z * sf ** 3 * (1, y_factor));
        }
      }
    }
  }

  void draw_vertices() {
    for (int x = 0; x <= segments; ++x) {
      for (int y = 0; y <= segments; ++y) {
        for (int z = 0; z <= segments; ++z) {
          grdraw.vert(this.vertices[x][y][z]);
        }
      }
    }
  }

  void draw_edge(bool oriented = false) {
    for (int x = 0; x <= segments; ++x) {
      for (int y = 0; y <= segments; ++y) {
        for (int z = 1; z <= segments; ++z) {
          grdraw.edge(this.vertices[x][y][z - 1], this.vertices[x][y][z], dash=x < segments && y < segments, is_arc=oriented);
        }
      }
    }

    for (int x = 0; x <= segments; ++x) {
      for (int y = 1; y <= segments; ++y) {
        for (int z = 0; z <= segments; ++z) {
          grdraw.edge(this.vertices[x][y - 1][z], this.vertices[x][y][z], dash=x < segments && z > 0, is_arc=oriented);
        }
      }
    }

    for (int x = 1; x <= segments; ++x) {
      for (int y = 0; y <= segments; ++y) {
        for (int z = 0; z <= segments; ++z) {
          grdraw.edge(this.vertices[x - 1][y][z], this.vertices[x][y][z], dash=y < segments && z > 0, is_arc=oriented);
        }
      }
    }
  }
}
