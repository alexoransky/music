def screen_size(app):
    rec = app.desktop().screenGeometry()
    return rec.width(), rec.height()


def window_size(app):
    return app.width(), app.height()
