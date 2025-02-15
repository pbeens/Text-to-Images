#!/usr/bin/env python3
"""
-------------------------------------------------------------------------------
Program: Text to Images
Author: Peter Beens
Date: 2025-02-15
-------------------------------------------------------------------------------
Description:
    This Python script reads an article from 'article.txt' and converts the text
    into one or more fixed-height PNG images. Each page is sized to a specified
    height (e.g., 1200 pixels) to ensure uniform page dimensions. Paragraphs are
    preserved and wrapped, with a blank line before each paragraph except the first.
    A small page marker (e.g., "1/3") is added to the bottom-right corner of each page.

Usage:
    1. Install dependencies via pip:
         pip install -r requirements.txt
    2. Place 'article.txt' in the same directory.
    3. Run: python text_to_images.py
    4. Generated images are saved to an 'images' folder, which is created or cleared.

Notes:
    - Adjust 'max_image_height', font sizes, and line spacing as needed.
    - Paragraphs in 'article.txt' should be separated by two newlines.
    - See the project's README.md for more details on configuration and usage.
-------------------------------------------------------------------------------
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import re

# Determine the current directory (for file paths)
current_directory = os.path.dirname(os.path.realpath(__file__))

def filter_simple_unicode(text):
    """
    Normalize punctuation (e.g., curly quotes, dashes, ellipses) 
    and remove non-ASCII characters.
    """
    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "..."
    }
    for smart, ascii_equiv in replacements.items():
        text = text.replace(smart, ascii_equiv)
    # Remove any remaining non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def paginate_lines(
    all_lines,
    font,
    normal_line_spacing,
    extra_paragraph_spacing,
    max_image_height,
    padding
):
    """
    Split wrapped lines into multiple 'pages' based on max_image_height.
    Each page is a list of lines that fit within (max_image_height - 2*padding).
    Returns a list of pages, where each page is a list of text lines.
    """
    pages = []
    current_page = []
    
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)
    
    current_height = 0
    
    for line in all_lines:
        # Measure line height
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        
        # Determine vertical space needed for this line
        if line.strip() == "":
            needed_space = line_height + extra_paragraph_spacing
        else:
            needed_space = line_height + normal_line_spacing
        
        # If adding this line exceeds the page height, start a new page
        if current_height + needed_space > (max_image_height - 2 * padding) and current_page:
            pages.append(current_page)
            current_page = []
            current_height = 0
        
        # Add line to the current page
        current_page.append(line)
        current_height += needed_space
    
    # Add the last page if it has any lines
    if current_page:
        pages.append(current_page)
    
    return pages

def text_to_image(page_lines, filename, page_num, total_pages, max_image_height=1200):
    """
    Render a single page (list of lines) into an image. The image is forced to 
    a fixed height (max_image_height) for uniformity. A small page marker 
    (e.g., "1/3") is placed at the bottom-right corner.
    """
    font_path = os.path.join(current_directory, "Roboto-Regular.ttf")
    try:
        main_font = ImageFont.truetype(font_path, size=36)
        marker_font = ImageFont.truetype(font_path, size=18)
    except IOError:
        # Fallback if font is not found
        main_font = ImageFont.load_default()
        marker_font = ImageFont.load_default()
    
    # Layout constants
    padding = 20
    normal_line_spacing = 4
    extra_paragraph_spacing = 25
    
    # Measure lines to find the width needed
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)
    
    line_sizes = []
    for line in page_lines:
        bbox = draw.textbbox((0, 0), line, font=main_font)
        line_width = bbox[2] - bbox[1]
        line_height = bbox[3] - bbox[1]
        # Correction: line_width = bbox[2] - bbox[0] (typo fix)
        line_width = bbox[2] - bbox[0]
        line_sizes.append((line_width, line_height))
    
    # Calculate text block size
    max_line_width = max((lw for lw, _ in line_sizes), default=0)
    total_text_height = 0
    for (line, (lw, lh)) in zip(page_lines, line_sizes):
        if line.strip() == "":
            total_text_height += lh + extra_paragraph_spacing
        else:
            total_text_height += lh + normal_line_spacing
    
    # Final image dimensions: fixed height, dynamic width
    image_width = max_line_width + 2 * padding
    image_height = max_image_height  # Force fixed height
    
    # Create final image (light gray background)
    bg_color = (250, 250, 250)
    img = Image.new("RGB", (image_width, image_height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw text lines from the top
    y_text = padding
    for (line, (lw, lh)) in zip(page_lines, line_sizes):
        if line.strip() == "":
            y_text += lh + extra_paragraph_spacing
        else:
            draw.text((padding, y_text), line, font=main_font, fill="black")
            y_text += lh + normal_line_spacing
    
    # Page marker in bottom-right corner (e.g. "1/3")
    marker_text = f"{page_num}/{total_pages}"
    bbox_marker = draw.textbbox((0, 0), marker_text, font=marker_font)
    marker_width = bbox_marker[2] - bbox_marker[0]
    marker_height = bbox_marker[3] - bbox_marker[1]
    
    marker_x = image_width - padding - marker_width
    marker_y = image_height - padding - marker_height
    draw.text((marker_x, marker_y), marker_text, font=marker_font, fill="black")
    
    # Save the generated page
    img.save(filename)

def main():
    """
    Main entry point:
      1. Read article from 'article.txt'.
      2. Split into paragraphs and wrap lines.
      3. Paginate based on fixed max_image_height.
      4. Render each page into an image with a page marker.

    Note: If you haven't installed dependencies, run:
          pip install -r requirements.txt
    """
    # Read the article
    article_path = os.path.join(current_directory, "article.txt")
    with open(article_path, "r", encoding="utf-8") as f:
        article = f.read()
    
    # Split into paragraphs on double newlines
    paragraphs = article.split("\n\n")
    
    # Build a list of wrapped lines
    all_lines = []
    for i, paragraph in enumerate(paragraphs):
        # Insert a blank line before paragraphs except the first
        if i > 0:
            all_lines.append("")
        paragraph = filter_simple_unicode(paragraph)
        
        # Wrap each paragraph at 70 characters
        wrapped = textwrap.wrap(paragraph, width=70)
        all_lines.extend(wrapped)
    
    # Prepare a font for pagination measurement
    font_path = os.path.join(current_directory, "Roboto-Regular.ttf")
    try:
        main_font = ImageFont.truetype(font_path, size=36)
    except IOError:
        main_font = ImageFont.load_default()
    
    # Set desired page height (all pages will be this tall)
    max_image_height = 1200
    normal_line_spacing = 4
    extra_paragraph_spacing = 25
    padding = 20
    
    # Convert wrapped lines into multiple pages
    pages = paginate_lines(
        all_lines,
        font=main_font,
        normal_line_spacing=normal_line_spacing,
        extra_paragraph_spacing=extra_paragraph_spacing,
        max_image_height=max_image_height,
        padding=padding
    )
    
    # Create or clear the 'images' folder
    images_folder = os.path.join(current_directory, "images")
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    else:
        for fn in os.listdir(images_folder):
            os.remove(os.path.join(images_folder, fn))
    
    # Render each page
    total_pages = len(pages)
    for i, page_lines in enumerate(pages, start=1):
        page_filename = os.path.join(images_folder, f"{i:03}.png")
        text_to_image(
            page_lines=page_lines,
            filename=page_filename,
            page_num=i,
            total_pages=total_pages,
            max_image_height=max_image_height
        )
    
    print(f"Created {total_pages} page(s) in '{images_folder}'.")

if __name__ == "__main__":
    main()
