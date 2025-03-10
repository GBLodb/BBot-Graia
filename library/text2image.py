import sys
import asyncio

from io import BytesIO
from pathlib import Path
from loguru import logger
from PIL import Image, ImageFont, ImageDraw

from .strings import get_cut_str

font_file = (
    Path(__file__)
    .parent.parent.joinpath("data")
    .joinpath("font")
    .joinpath("sarasa-mono-sc-semibold.ttf")
)
if font_file.exists():
    font = ImageFont.truetype(str(font_file), size=20)
else:
    logger.error(
        f"未找到字体文件：{font_file}，请前往 https://github.com/djkcyl/ABot-Resource/releases/tag/Font 进行下载后解压至 BBot 根目录"
    )
    sys.exit(1)


async def text2image(text: str, cut=64) -> bytes:
    return await asyncio.to_thread(_create_image, text, cut)


def _create_image(text: str, cut: int) -> bytes:
    cut_str = "\n".join(get_cut_str(text, cut))
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 40, texty + 40), (235, 235, 235))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    imageio = BytesIO()
    image.save(
        imageio,
        format="JPEG",
        quality=90,
        subsampling=2,
        qtables="web_high",
    )
    return imageio.getvalue()
