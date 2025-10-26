from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from controller.app_controller import AppController
import uvicorn

from devices.base_device import DeviceInfo

app = FastAPI(title="SmartApp IoT System")

templates = Jinja2Templates(directory="web/templates")

app.mount("/static", StaticFiles(directory="web/static"), name="static")

controller = AppController()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    status = controller.get_all_statuses()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "devices": status}
    )


@app.post("/toggle_speaker")
async def toggle_speaker():
    controller.toggle_speaker()
    return RedirectResponse(url="/", status_code=303)


@app.post("/set_volume")
async def set_volume(volume: int = Form(...)):
    controller.set_speaker_volume(volume)
    return RedirectResponse(url="/", status_code=303)


@app.post("/set_track")
async def set_track(track: str = Form(...)):
    controller.set_speaker_track(track)
    return RedirectResponse(url="/", status_code=303)


@app.post("/toggle_light")
async def toggle_light():
    controller.toggle_light()
    return RedirectResponse(url="/", status_code=303)


@app.post("/set_brightness")
async def set_brightness(brightness: int = Form(...)):
    controller.set_light_brightness(brightness)
    return RedirectResponse(url="/", status_code=303)


@app.post("/set_rgb")
async def set_rgb(r: int = Form(...), g: int = Form(...), b: int = Form(...)):
    controller.set_light_rgb(r, g, b)
    return RedirectResponse(url="/", status_code=303)


@app.post("/toggle_curtain")
async def toggle_curtain():
    controller.toggle_curtain()
    return RedirectResponse(url="/", status_code=303)


@app.post("/set_position")
async def set_position(position: int = Form(...)):
    controller.set_curtain_position(position)
    return RedirectResponse(url="/", status_code=303)


@app.post("/api/device/register")
async def register_device(device_info: DeviceInfo):
    controller.register_device(device_info)
    return {"status": "registered"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
