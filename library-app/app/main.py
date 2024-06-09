from starlette.applications import Starlette
from starlette.routing import Mount

from app.views.v1 import app as v1_app

app = Starlette(
    routes=[
        Mount("/api/v1", v1_app),
    ]
)
