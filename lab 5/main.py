from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from controller.app_controller import AppController
import uvicorn
import os

app = FastAPI(title="SmartApp IoT System")

# Ensure correct paths when running from project root
templates = Jinja2Templates(directory=os.path.join("web", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join("web", "static")), name="static")

controller = AppController()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

@app.post("/toggle_speaker")
async def toggle_speaker(request: Request):
    speaker_status = controller.toggle_speaker()
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status, "updated_device": speaker_status})

@app.post("/toggle_light")
async def toggle_light(request: Request):
    light_status = controller.toggle_light()
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status, "updated_device": light_status})

@app.post("/set_volume")
async def set_volume(request: Request, volume: int = Form(...)):
    controller.set_speaker_volume(volume)
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

@app.post("/set_brightness")
async def set_brightness(request: Request, brightness: int = Form(...)):
    controller.set_light_brightness(brightness)
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

# Extra: set curtains position and toggle curtains
@app.post("/toggle_curtains")
async def toggle_curtains(request: Request):
    # controller doesn't include explicit toggle for curtains in README, add via facade
    status_before = controller.get_all_status()
    # try to toggle by checking status via facade
    curtains_status = controller.facade.get_device_status("curtains_001")
    if curtains_status:
        current_open = curtains_status.get("is_open", False)
        action = "close" if current_open else "open"
        controller.facade.perform_device_action("curtains_001", "power", state=action)
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

@app.post("/set_curtains_position")
async def set_curtains_position(request: Request, position: int = Form(...)):
    # clamp position 0..100
    pos = max(0, min(100, position))
    controller.facade.perform_device_action("curtains_001", "position", value=pos)
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)