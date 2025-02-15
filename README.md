# Text to Images

A Python utility that reads an article from `article.txt` and converts it into one or more **fixed-height** PNG images. Each page is wrapped at a specified width, preserving paragraphs and spacing, with a minimal page marker in the bottom-right corner.

---

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration and Modification](#configuration-and-modification)
6. [Fonts and Licensing](#fonts-and-licensing)
7. [Project Structure](#project-structure)
8. [License](#license)
9. [Acknowledgments](#acknowledgments)

---

## Features
- **Paragraph Preservation**: Automatically splits paragraphs based on blank lines, inserts a blank line before each paragraph (except the first), and wraps text to a specified width.  
- **Fixed-Height Pages**: Each page is forced to a uniform height, so the final images have consistent dimensions.  
- **Automatic Pagination**: The script measures the text and starts a new page when it exceeds the allowed space.  
- **Minimal Page Marker**: Each page displays a marker (e.g., “1/4”) in the bottom-right corner.  
- **Unicode Filtering**: Curly quotes, dashes, ellipses, and other non-ASCII characters are converted to simpler ASCII equivalents for compatibility.  
- **Light Gray Background**: The generated images have a subtle gray background (`(250, 250, 250)`), though this can be changed.

---

## Requirements
- **Python 3.x** (tested on 3.8+)
- **Pillow** (Python Imaging Library), version pinned in `requirements.txt`

Sample `requirements.txt`:
```text
Pillow==9.4.0
```

---

## Installation

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/pbeens/Text-to-Images.git
   cd Text-to-Images
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This ensures you have the exact Pillow version (`9.4.0`) for consistent results.

3. **Included Font**:
   - The **Roboto-Regular.ttf** font is bundled in this repository for convenience.
   - See [Fonts and Licensing](#fonts-and-licensing) for more details.

---

## Usage

1. **Place Your Article**:  
   Put your text content in a file named `article.txt`. Separate paragraphs by **two** newlines (`\n\n`).

2. **Run the Script**:
   ```bash
   python text_to_images.py
   ```
   - The script will read `article.txt`, generate one or more page images, and place them in an `images` folder.  
   - Any existing images in that folder will be cleared first.

3. **Check the Output**:  
   You’ll see files like `001.png`, `002.png`, etc., each representing a page of your article.

---

## Configuration and Modification

The **`text_to_images.py`** script contains several variables and functions you can tweak:

1. **`max_image_height`**  
   - Default: `1200` pixels  
   - This forces each page to have the same height. Increase or decrease to suit your design (e.g., 800 for smaller images, 1600 for taller).

2. **Wrap Width**  
   - In the code, `textwrap.wrap(paragraph, width=70)` controls how many characters appear on a line before wrapping.  
   - If your text is too wide, reduce the width; if it’s too narrow, increase it.

3. **Line Spacing**  
   - `normal_line_spacing = 4` and `extra_paragraph_spacing = 25` define how much vertical space is added after each line or paragraph break.  
   - Increase these values for a looser layout, or decrease for a more compact layout.

4. **Fonts**  
   - By default, the code looks for `Roboto-Regular.ttf` at size `36` for main text and `18` for page markers.  
   - If the Roboto font isn’t found, the script uses a default system font.
   - To change the font or size, edit these lines in `text_to_image()`:
     ```python
     main_font = ImageFont.truetype(font_path, size=36)
     marker_font = ImageFont.truetype(font_path, size=18)
     ```

5. **Page Marker**  
   - The function `text_to_image()` places the page marker with `marker_text = f"{page_num}/{total_pages}"`.  
   - Modify this if you want a different style, e.g. `"/1"` or `"Page 1 of 5"`.

6. **Background Color**  
   - Set by `bg_color = (250, 250, 250)` in `text_to_image()`.  
   - Change this tuple to any `(R, G, B)` color, e.g. `(255, 255, 255)` for white or `(245, 245, 245)` for a slightly different shade.

7. **Paragraph Preservation**  
   - The code inserts a blank line (`""`) before each paragraph except the first, ensuring separation.  
   - If you want paragraphs to run continuously, remove the `if i > 0: all_lines.append("")` logic in `main()`.

8. **Advanced Pagination**  
   - Currently, the script will start a new page when adding another line would exceed `(max_image_height - 2 * padding)`.  
   - If you want more refined pagination (e.g., never splitting a paragraph across pages), you’d need to modify the `paginate_lines()` function to handle paragraphs as blocks.

---

## Fonts and Licensing

- **Roboto-Regular.ttf** is included in this repository under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).  
- See [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) for the full text of the Apache 2.0 license and details about bundling Roboto.

---

## Project Structure

```
Text-to-Images/
├── article.txt
├── requirements.txt
├── text_to_images.py
├── Roboto-Regular.ttf
├── THIRD_PARTY_LICENSES.md
├── images/           # Generated output images go here
└── README.md         # This file
```

- **`article.txt`**: Your article’s text.  
- **`requirements.txt`**: Lists the dependencies for pip installation.  
- **`text_to_images.py`**: Main script that converts text to images.  
- **`Roboto-Regular.ttf`**: Bundled font (Apache 2.0).  
- **`THIRD_PARTY_LICENSES.md`**: License details for Roboto.  
- **`images`**: Auto-created folder for output images.  
- **`README.md`**: Documentation for the project (this file).

---

## License

Copyright (c) 2025 Peter Beens
> This project is licensed under the [MIT License](LICENSE). Feel free to modify and distribute, but please retain the original credit.

---

## Acknowledgments
- **[Pillow](https://pillow.readthedocs.io/)** for image processing in Python.  
- **[Roboto Font](https://fonts.google.com/specimen/Roboto)** by Google, bundled under the Apache 2.0 License (see [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md)).

