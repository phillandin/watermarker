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
<p></p>
<h3>Updating the watermark text</h3>
<p></p>
<h3>Displaying the file name</h3>
<p></p>