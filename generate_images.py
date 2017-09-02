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
    covers = {}
    for cover, issue_date in db.get_covers():
        year = issue_date[:4]
        if year not in covers:
            covers[year] = []
        covers[year].append(cover)
    valid_years = dict((k, v) for k, v in covers.items() if len(v) >= 40)
    for current_year in valid_years:
        new_image = PIL.Image.new("RGB", (3840, 2160))
        horizontal_position = 0
        vertical_position = 0
        for cover in valid_years[current_year][:40]:
            cover_image = PIL.Image.open(io.BytesIO(cover))
            new_image.paste(im=cover_image, box=(-80 + 400 * horizontal_position, 526 * vertical_position))
            horizontal_position += 1
            if horizontal_position % 10 == 0:
                horizontal_position = 0
                vertical_position += 1

        draw = PIL.ImageDraw.Draw(new_image, "RGBA")
        font = PIL.ImageFont.truetype("~/Library/Fonts/SFCompactDisplay-Light.otf", 48)  # Change to your desired font
        draw.text((3725, 2103), current_year, (255, 255, 255, 0), font=font)
        new_image = new_image.resize((1920, 1080), PIL.Image.ANTIALIAS)
        new_image.save('output/{year}.png'.format(year=current_year), quality=85, optimize=True)


if __name__ == "__main__":
    generate_images()
