# watermarker
Application for adding a watermark to images, made using PIL and PyQt.

<h1>How it works</h1>
<p>When the user clicks "Select File," they choose an image file from their computer in the file browser. The image
appears in the preview window with the text, size, and position of the watermark set according to the options selected. 
As the user changes the watermark options, the preview updates to reflect their selection. Clicking "Save
Image" summons a file browser to choose the file name and save location.</p>
<p>The application is housed in a QtWidgets.QDialog window. The layout of the window is managed by a
QtWidgets.QGridLayout, which contains three widgets (each with its own layout manager): one containing the image
preview, one containing the "Select File" and "Save File" buttons, and one containing the watermark editing options.</p>
<h1>Some challenges</h1>
<h3>Making the watermark</h3>
<p>The watermark effect is achieved by writing the user-chosen text five times: four times in black with medium opacity
and once in white with slightly less opacity. The four black writings of the text serve as an outline and are
offset slightly from the placement of the main text, each in a different direction. The white writing serves as the
actual text.</p>
<p>To determine the placement of the watermark, an ImageFont.truetype object is created using the Imperator font, and
the size of the user-input text (in x, y format) is received from a font.getsize(text) function. The width and height of
the image is received from the Image object created from the chosen file. The text's width and height is subtracted from
the total width and height of the chosen image (with a 5% margin allowed between the text and image edge), and the text
is written at the resulting coordinates.</p>
<h3>Updating the watermark text</h3>
<p>Originally the watermark was updated whenever there was a change in the watermark text field. This resulted in severe
lag as the watermark-writing process was happening constantly as the user edited the watermark text. To resolve this, a
QtCore.QTimer object is created upon any change to the watermark text field and assigned to a previously NoneType
instance attribute. (If there is already a timer assigned to the attribute, no timer is created.) This timer is set for
two seconds, at which point the image is edited to match the new watermark text.
<h3>Displaying the file name</h3>
<p>Once the user selects the image to watermark, the file name appears below the "Select Image" button. Since there is
limited space, it was necessary to break the file name string into multiple lines for longer file names. To do this, the
length of the string is divided by 15 (the number of characters that fit comfortably on each line) and rounded up to
determine how many lines are needed. Then each number in a range of the number of lines is used to slice the string into
each consecutive series of 15 characters, and each line is then printed with a new line at its end.</p>