import os
from app import create_app

app = create_app()


@app.shell_context_processor
def make_shell_contest():
    # return dict(context objects, when they'll be added)
    pass
