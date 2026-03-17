access settings;

settings.autoimport = 'asymptote/init';

// OpenGL-backed rendering (render > 0) in asymptote is flaky and breaks every now and then,
// so I resort to well-supported 2D projections (render = 0).
settings.render = 0;
settings.outformat = 'pdf';
