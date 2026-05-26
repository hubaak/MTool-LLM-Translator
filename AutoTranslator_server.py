import argparse
import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
import uvicorn

from src.translator import Translator

# =========================
# Global
# =========================
request_queue = asyncio.Queue()
translator = None
worker_task = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)



class TranslationTask:
    def __init__(self, text, source_lang, target_lang):
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang

        self.future = asyncio.get_running_loop().create_future()


# =========================
# worker
# =========================

async def translation_worker():
    global translator
    logger.info("Translation worker started")

    while True:
        task = await request_queue.get()

        try:
            logger.info(
                f"Translating from={task.source_lang} "
                f"to={task.target_lang} "
                f"text={task.text[:30]}"
            )
            result = translator.translate(
                task.text,
                task.source_lang,
                task.target_lang
            )

            task.future.set_result(result)

        except Exception as e:
            task.future.set_exception(e)

        finally:
            request_queue.task_done()


# =========================
# life long
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    global translator
    global worker_task

    logger.info("Loading translator...")
    translator = Translator()
    logger.info("Translator loaded")
    worker_task = asyncio.create_task(
        translation_worker()
    )
    logger.info("Server started")

    yield

    logger.info("Shutting down...")
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        logger.info("Worker cancelled")


# =========================
# API
# =========================
app = FastAPI(lifespan=lifespan)

@app.get("/translate")
async def translate_api(
    from_: str = Query(alias="from"),
    to: str = Query(),
    text: str = Query()
):
    task = TranslationTask(text, from_, to)
    await request_queue.put(task)
    result = await task.future
    return PlainTextResponse(result)



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host ip of service")
    parser.add_argument("--port", type=int, default=80, help="Port of the api, default is 80")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    
    uvicorn.run(
        "AutoTranslator_server:app",
        host=args.host,
        port=args.port,
        workers=1
    )