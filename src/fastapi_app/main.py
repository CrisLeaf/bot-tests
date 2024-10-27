import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.wsgi import WSGIMiddleware

import sys
sys.path.append('../dash_app/')

from start_plot import create_start_dash_app
from dashboards.plot1 import create_plot1_dash_app


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

start_plot = create_start_dash_app(requests_pathname_prefix="/start_plot/")
app.mount("/start_plot", WSGIMiddleware(start_plot.server))

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('start.html', {'request': request})


plot1 = create_plot1_dash_app(requests_pathname_prefix="/plot1/")
app.mount("/plot1", WSGIMiddleware(plot1.server))

@app.get('/home')
async def root(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


if __name__ == '__main__':    
    uvicorn.run(app, port=8000)
    