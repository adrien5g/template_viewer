import json
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path("templates")
DATA_FILE = Path("data.json")
TEMPLATE_TO_WATCH = "pendencia_adm.html"
OUTPUT_FILE = Path("output.html")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def render_template():
    print(f"🔄 Renderizando {TEMPLATE_TO_WATCH}...")
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(TEMPLATE_TO_WATCH)
    data = load_data()
    output = template.render(object_list=[data])
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"✅ Template renderizado em: {OUTPUT_FILE}")

class TemplateChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(TEMPLATE_TO_WATCH):
            try:
                render_template()
            except Exception as e:
                print(f"❌ Erro ao renderizar: {e}")

if __name__ == "__main__":
    observer = Observer()
    handler = TemplateChangeHandler()
    observer.schedule(handler, str(TEMPLATES_DIR), recursive=False)

    print(f"👀 Observando mudanças em: {TEMPLATE_TO_WATCH}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()