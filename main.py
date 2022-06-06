import sys
from math import ceil
from PySide6 import QtCore, QtWidgets, QtGui
from PIL import Image, ImageFont, ImageDraw


class StartScreen(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()


class Editor(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.start_image = None
        self.edited_image = None
        self.edit_timer = None
        self.wm_pos = "bottom_rt"
        self.font_factor = 7

        self.setWindowTitle('WaterMarker')
        self.setStyleSheet(u"QDialog {\n"
            "background-color: rgba(237, 230, 219, 255);\n"
            "font: Microsoft Sans Serif;\n"
            "color: rgb(70, 70, 70);"               
        "}")

        self.layout = QtWidgets.QGridLayout(self)

        # image section
        self.image_widget = QtWidgets.QWidget()
        self.layout.addWidget(self.image_widget, 1, 1, 4, 6)

        self.image_widget_layout = QtWidgets.QGridLayout(self.image_widget)
        # self.image_widget_layout.setContentsMargins(10, 10, 0, 0)

        self.preview = QtWidgets.QLabel()
        self.preview.setMaximumHeight(420)
        self.preview.setMaximumWidth(600)
        self.image_widget_layout.addWidget(self.preview)
        pix_map = QtGui.QPixmap("./placeholder.jpg")
        self.preview.setPixmap(pix_map.scaledToWidth(600))

        # right panel (selecting file and downloading watermarked file)
        self.ul_dl_widget = QtWidgets.QWidget()
        self.ul_dl_widget.setStyleSheet("font: 10pt")
        self.ul_dl_widget.setMaximumWidth(150)
        self.ul_dl_widget.setMinimumWidth(150)
        self.layout.addWidget(self.ul_dl_widget, 0, 8, 5, 1)

        self.ul_dl_layout = QtWidgets.QVBoxLayout(self.ul_dl_widget)
        self.ul_dl_layout.setContentsMargins(20, 50, 20, 50)

        self.ul_dl_spacer1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.ul_dl_layout.addItem(self.ul_dl_spacer1)

        self.ul_button = QtWidgets.QPushButton("Select Image")
        self.ul_button.setObjectName("ul_button")
        self.ul_button.setStyleSheet(u"#ul_button {\n"
                                     "background-color: rgb(65, 125, 122);\n"
                                     "font: 10pt;\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-style: outset;\n"
                                     "border-width: 1px;\n"
                                     "border-radius: 5px;\n"
                                     "border-color: rgb(70, 70, 70);\n"
                                     "padding: 4px;\n"
                                     "}\n"
                                     "#ul_button:hover {\n"
                                     "background-color: rgb(102,151,148)\n"
                                     "}\n")
        self.ul_button.clicked.connect(self.select_file)
        self.ul_dl_layout.addWidget(self.ul_button)

        self.ul_text = QtWidgets.QLabel(u"\nChoose an image")
        self.ul_dl_layout.addWidget(self.ul_text)
        self.ul_text.setAlignment(QtCore.Qt.AlignTop)
        self.dl_button = QtWidgets.QPushButton("Save Image")
        self.dl_button.setObjectName("dl_button")
        self.dl_button.setStyleSheet(u"#dl_button {\n"
                                     "background-color: rgb(65, 125, 122);\n"
                                     "font: 10pt;\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border-style: outset;\n"
                                     "border-width: 1px;\n"
                                     "border-radius: 5px;\n"
                                     "border-color: rgb(70, 70, 70);\n"
                                     "padding: 4px;\n"
                                     "}\n"
                                     "#dl_button:hover {\n"
                                     "background-color: rgb(102,151,148);\n"
                                     "}")
        self.dl_button.clicked.connect(self.save_file)
        self.ul_dl_layout.addWidget(self.dl_button)

        self.ul_dl_spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Preferred,
                                                   QtWidgets.QSizePolicy.Preferred)
        self.ul_dl_layout.addItem(self.ul_dl_spacer2)

        # bottom panel (editing watermark)
        self.edit_widget = QtWidgets.QWidget()
        self.layout.addWidget(self.edit_widget, 7, 0, 3, 9)
        self.edit_widget_layout = QtWidgets.QGridLayout(self.edit_widget)
        self.edit_widget_layout.setContentsMargins(20, 20, 20, 20)

        # watermark position section
        self.wm_pos_label = QtWidgets.QLabel("POSITION")
        self.wm_pos_label.setStyleSheet("font: 10pt High Tower Text")
        self.edit_widget_layout.addWidget(self.wm_pos_label, 0, 0)
        self.pos_button_group = QtWidgets.QButtonGroup(self)

        self.bot_right_pos_button = QtWidgets.QRadioButton("Bottom Right")
        self.bot_right_pos_button.setChecked(True)
        self.bot_right_pos_button.toggled.connect(self.bottom_rt)
        self.pos_button_group.addButton(self.bot_right_pos_button)
        self.edit_widget_layout.addWidget(self.bot_right_pos_button, 2, 1)

        self.bot_left_pos_button = QtWidgets.QRadioButton("Bottom Left")
        self.bot_left_pos_button.toggled.connect(self.bottom_lf)
        self.pos_button_group.addButton(self.bot_left_pos_button)
        self.edit_widget_layout.addWidget(self.bot_left_pos_button, 2, 0)

        self.top_right_pos_button = QtWidgets.QRadioButton("Top Right")
        self.top_right_pos_button.toggled.connect(self.top_rt)
        self.pos_button_group.addButton(self.top_right_pos_button)
        self.edit_widget_layout.addWidget(self.top_right_pos_button, 1, 1)

        self.top_left_pos_button = QtWidgets.QRadioButton("Top Left")
        self.top_left_pos_button.toggled.connect(self.top_lf)
        self.pos_button_group.addButton(self.top_left_pos_button)
        self.edit_widget_layout.addWidget(self.top_left_pos_button, 1, 0)

        self.center_pos_button = QtWidgets.QRadioButton("Center")
        self.center_pos_button.toggled.connect(self.center)
        self.pos_button_group.addButton(self.center_pos_button)
        self.edit_widget_layout.addWidget(self.center_pos_button, 3, 0)

        # divider
        self.divider_1 = QtWidgets.QFrame()
        self.divider_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.divider_1.setStyleSheet("color: rgba(161,182,180,150)")
        self.edit_widget_layout.addWidget(self.divider_1, 1, 2, 4, 1, QtCore.Qt.AlignHCenter)

        # watermark font size section
        self.font_size_label = QtWidgets.QLabel("SIZE")
        self.font_size_label.setStyleSheet("font: 10pt High Tower Text")
        self.edit_widget_layout.addWidget(self.font_size_label, 0, 3)

        self.font_button_group = QtWidgets.QButtonGroup(self)

        self.font_xsmall_button = QtWidgets.QRadioButton("Extra Small")
        self.font_xsmall_button.toggled.connect(self.font_xsmall)
        self.edit_widget_layout.addWidget(self.font_xsmall_button, 1, 3)

        self.font_small_button = QtWidgets.QRadioButton("Small")
        self.font_small_button.toggled.connect(self.font_small)
        self.edit_widget_layout.addWidget(self.font_small_button, 2, 3)

        self.font_med_button = QtWidgets.QRadioButton("Medium")
        self.font_med_button.setChecked(True)
        self.font_med_button.toggled.connect(self.font_med)
        self.edit_widget_layout.addWidget(self.font_med_button, 3, 3)

        self.font_large_button = QtWidgets.QRadioButton("Large")
        self.font_large_button.toggled.connect(self.font_large)
        self.edit_widget_layout.addWidget(self.font_large_button, 4, 3)

        # divider
        self.divider_2 = QtWidgets.QFrame()
        self.divider_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.divider_2.setStyleSheet("color: rgba(161,182,180,255)")
        self.edit_widget_layout.addWidget(self.divider_2, 1, 4, 4, 1, QtCore.Qt.AlignHCenter)

        # watermark text section
        self.wm_text_label = QtWidgets.QLabel("TEXT")
        self.wm_text_label.setStyleSheet("font: 10pt High Tower Text")
        self.edit_widget_layout.addWidget(self.wm_text_label, 0, 5)

        self.wm_text_field = QtWidgets.QLineEdit("watermark")
        self.wm_text_field.setMaximumWidth(200)
        self.edit_widget_layout.addWidget(self.wm_text_field, 1, 5)
        self.wm_text_field.textChanged.connect(self.timed_edit)

    def edit_image(self):
        try:
            with Image.open(self.start_image).convert("RGBA") as base:
                x, y = base.size
                # creates a new white Image with the same dimensions as the user-selected image file to later
                # superimpose onto the image file
                txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

                # makes the size of the font proportional to the size of the image, with the font_factor adjusting
                # according to the font size selected
                font_size = round((.6 * y) / self.font_factor * x / y)
                font = ImageFont.truetype("./Imperator.ttf", font_size)
                text = self.wm_text_field.text()
                font_width, font_height = font.getsize(text)
                if self.wm_pos == "bottom_rt":
                    new_x = .95 * x - font_width
                    new_y = .95 * y - font_height
                elif self.wm_pos == "bottom_lf":
                    new_x = .05 * x
                    new_y = .95 * y - font_height
                elif self.wm_pos == "top_rt":
                    new_x = .95 * x - font_width
                    new_y = .05 * y
                elif self.wm_pos == "top_lf":
                    new_x = .05 * x
                    new_y = .05 * y
                else:
                    new_x = .5 * x - .5 * font_width
                    new_y = .5 * y - .5 * font_height

                # creates a watermark by writing the text 5 time: 4 times with black and medium opacity (each time
                # offset slightly in a different direction) and once in white with less opacity
                d = ImageDraw.Draw(txt)
                d.text((new_x - 2, new_y), text, font=font, fill=(0, 0, 0, 100))
                d.text((new_x + 2, new_y), text, font=font, fill=(0, 0, 0, 100))
                d.text((new_x, new_y - 2), text, font=font, fill=(0, 0, 0, 100))
                d.text((new_x, new_y + 2), text, font=font, fill=(0, 0, 0, 100))
                d.text((new_x, new_y), text, font=font, fill=(255, 255, 255, 75))

                # superimposes the blank Image with the watermark onto the user-selected image file, saving it both as
                # a PIL Image object (self.edited_image) and as a converted jpg file. The latter is necessary for the
                # QtGui.QPixmap object, which displays the watermarked image file.
                wm_image = Image.alpha_composite(base, txt)
                self.edited_image = wm_image
                wm_jpg = wm_image.convert("RGB")
                wm_jpg.save("watermarked_im.jpg")
                pix_map = QtGui.QPixmap("watermarked_im.jpg")

                # limits size of pixmap by widest dimension
                if pix_map.width() > pix_map.height():
                    self.preview.setPixmap(pix_map.scaledToWidth(600))
                else:
                    self.preview.setPixmap(pix_map.scaledToHeight(400))
                self.preview.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        except AttributeError:
            pass

    def select_file(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "c:\\", "Image files (*.jpg *.png *.webp)")
        if file_name[0] != "":
            self.start_image = file_name[0]
            # ensure that the image file name isn't too long for the space available, which comfortably displays lines
            # 15 characters in length
            name = self.start_image.split("/")[-1]
            if len(name) > 15:
                num_lines = ceil(len(name) / 15)
                # print 15 characters in each line with the remainder on its own line
                print_name_lines = [f"{name[(15 * (i - 1)):(15 * i)]}\n" for i in range(num_lines + 1)]
                name = "".join(print_name_lines)
            self.ul_text.setText(f"\nYou're editing:\n\n{name}")
            self.edit_image()

    def save_file(self):
        if self.start_image is not None:  # ensures that there is actually an image to save
            file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file',
                                                              "watermarked-image", "JPEG")
            wm_jpg = self.edited_image.convert("RGB")
            wm_jpg.save(f"{file_name[0]}.jpg")

    # watermark-position radio button functions
    def bottom_rt(self, selected):
        if selected:
            self.wm_pos = "bottom_rt"
            self.edit_image()

    def bottom_lf(self, selected):
        if selected:
            self.wm_pos = "bottom_lf"
            self.edit_image()

    def top_rt(self, selected):
        if selected:
            self.wm_pos = "top_rt"
            self.edit_image()

    def top_lf(self, selected):
        if selected:
            self.wm_pos = "top_lf"
            self.edit_image()

    def center(self, selected):
        if selected:
            self.wm_pos = "center"
            self.edit_image()

    # font size radio button functions
    def font_xsmall(self, selected):
        if selected:
            self.font_factor = 11.5
            self.edit_image()

    def font_small(self, selected):
        if selected:
            self.font_factor = 9
            self.edit_image()

    def font_med(self, selected):
        if selected:
            self.font_factor = 7
            self.edit_image()

    def font_large(self, selected):
        if selected:
            self.font_factor = 5
            self.edit_image()

    def update_text(self):
        widget.edit_image()
        self.edit_timer = None

    # automatically update watermark text to match wm_text_field 2 seconds after first edit
    def timed_edit(self):
        if not self.edit_timer:  # checks for a timer that has already been started due to a change to the wm_text_field
            self.edit_timer = QtCore.QTimer()
            self.edit_timer.timeout.connect(widget.update_text)
            self.edit_timer.start(2000)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Editor()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
