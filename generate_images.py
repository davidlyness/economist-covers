# coding=utf-8
"""generate_images"""

import io
import os

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import database


def generate_images():
    """
    Generate a tiled view of Economist covers.
    """
    if not os.path.exists("output"):
        os.makedirs("output")
    db = database.Database("db.sqlite3")
    covers_by_year = {}
    for cover, issue_date in db.get_covers():
        year = issue_date[:4]
        if year not in covers_by_year:
            covers_by_year[year] = []
        covers_by_year[year].append(cover)
    for current_year in covers_by_year:
        new_image = PIL.Image.new("RGB", (3840, 2160))
        horizontal_position = 0
        vertical_position = 0
        for cover in covers_by_year[current_year][:50]:
            cover_image = PIL.Image.open(io.BytesIO(cover))
            cover_image = cover_image.crop((8, 126, 392, 526))
            new_image.paste(im=cover_image, box=(384 * horizontal_position, 80 + 400 * vertical_position))
            horizontal_position += 1
            if horizontal_position % 10 == 0:
                horizontal_position = 0
                vertical_position += 1

        draw = PIL.ImageDraw.Draw(new_image, "RGBA")
        font = PIL.ImageFont.truetype("~/Library/Fonts/SFCompactDisplay-Light.otf", 48)  # Change to your desired font
        draw.text((3885, 2103), current_year, (255, 255, 255, 0), font=font)
        new_image = new_image.resize((1920, 1080), PIL.Image.ANTIALIAS)  # Remove this line to retain 4K resolution
        new_image.save('output/{year}.png'.format(year=current_year), quality=85, optimize=True)


if __name__ == "__main__":
    generate_images()
