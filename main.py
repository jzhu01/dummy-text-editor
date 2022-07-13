from tkinter import *

DOWN = "Down"
UP = "Up"
LEFT = "Left"
RIGHT = "Right"
direction_dict = {UP: [0, -10], DOWN: [0, 10], LEFT: [-10, 0], RIGHT: [10, 0]}


class TextEditor(Canvas):
    def __init__(self, canvas_height=600, canvas_width=600, bkgd_color="white", cursor_color="black"):
        super().__init__(
            width=canvas_width,
            height=canvas_height,
            background=bkgd_color
        )
        self.cursor = self.create_cursor(cursor_color)
        self.location_text_dict = {}
        self.bind_all("<Key>", self.on_press)
        self.pack()

    def create_cursor(self, cursor_color):
        return self.create_rectangle(10, 10, 20, 20, outline=cursor_color, fill=cursor_color)

    def on_press(self, event):
        if event.char is not None:
            print('{0} pressed'.format(event.char))
        self.process_keypress(event)

    def process_keypress(self, event):
        key = event.keysym
        if key in [DOWN, UP, LEFT, RIGHT]:  # if it is a directional key, we move the cursor
            x, y = direction_dict.get(key)
            self.trigger_cursor_move(x, y)
        elif key == 'Escape':  # if esc is hit, we exit
            root.destroy()
            exit()
        elif key == 'Clear':  # clear the entire screen
            self.location_text_dict.clear()
        elif key == 'Shift':  # ignore shift as it is a complementary keypress
            return
        elif key == 'Enter':
            x, y = direction_dict.get(DOWN)  # treat enter as a new line
            self.trigger_cursor_move(x, y)
        elif key == 'BackSpace':
            self.delete_char()
        else:  # otherwise, display the text
            self.write(event)

    def trigger_cursor_move(self, x, y):
        self.move(self.cursor, x, y)

    def write(self, event):
        # get the current x and y position of cursor
        x1, y1, x2, y2 = self.coords(self.cursor)
        # want to add text in the center
        x = x1 + 5  # todo: make this more flexible
        y = y1 + 5
        # write to canvas
        # check if text object exists
        if (x, y) in self.location_text_dict:
            text_obj = self.location_text_dict.get((x, y))
            # todo: check left and right text values
            original_txt = self.itemcget(text_obj, 'text')
            # if original_txt == event.char: # do nothing

            self.itemconfigure(text_obj, text=event.char)
        else:
            text_obj = self.create_text(x, y, text=event.char)
            self.location_text_dict[(x, y)] = text_obj
        # move the cursor to reflect the text added
        x, y = direction_dict.get(RIGHT)
        self.trigger_cursor_move(x, y)

    def delete_char(self):
        x1, y1, x2, y2 = self.coords(self.cursor)
        x = x1 + 5
        y = y1 + 5

        if (x, y) in self.location_text_dict:
            text_obj = self.location_text_dict.get((x, y))
            self.delete(text_obj)
            self.location_text_dict.pop((x, y))

        x, y = direction_dict.get(LEFT)
        self.trigger_cursor_move(x, y)


if __name__ == "__main__":
    root = Tk()
    root.title("TextEditor")
    root.resizable(False, False)  # todo: support resizing window
    window = TextEditor()
    root.mainloop()

# todo: support insert in the middle of an existing text
