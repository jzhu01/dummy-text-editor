from tkinter import *
import copy

DOWN = "Down"
UP = "Up"
LEFT = "Left"
RIGHT = "Right"
direction_dict = {UP: [0, -10], DOWN: [0, 10], LEFT: [-10, 0], RIGHT: [10, 0]}
DELTA = 5

class TextEditor(Canvas):
    def __init__(self, canvas_height=600, canvas_width=600, bkgd_color="white", cursor_color="black"):
        super().__init__(
            width=canvas_width,
            height=canvas_height,
            background=bkgd_color
        )
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.cursor = self.create_cursor(cursor_color)

        self.char_matrix = None
        self.set_empty_matrix()
        self.bind_all("<Key>", self.on_press)
        self.pack()

    def create_cursor(self, cursor_color):
        return self.create_rectangle(10, 10, 20, 20, outline=cursor_color, fill=cursor_color)

    def set_empty_matrix(self):
        self.char_matrix = [[None for i in range(self.canvas_height)] for j in range(self.canvas_width)]

    def on_press(self, event):
        if event.char is not None:
            print('{0} pressed'.format(event.char))
        self.process_keypress(event)

    def process_keypress(self, event):
        key = event.keysym
        if key in [DOWN, UP, LEFT, RIGHT]:                  # if it is a directional key, we move the cursor
            x, y = direction_dict.get(key)
            self.trigger_cursor_move(x, y)
        elif key == 'Escape':                               # if esc is hit, we exit
            root.destroy()
            exit()
        elif key == 'Clear':                                # clear the entire screen
            self.set_empty_matrix()
        elif key == 'Shift':                                # ignore shift as it is a complementary keypress
            return
        elif key == 'Enter':
            x, y = direction_dict.get(DOWN)                 # treat enter as a new line
            self.trigger_cursor_move(x, y)
        elif key == 'BackSpace':
            self.delete_char()
        else:                                               # otherwise, display the text
            self.write(event)

    def trigger_cursor_move(self, x, y):
        self.move(self.cursor, x, y)

    def write(self, event, catch=Exception):
        # get the current x and y position of cursor
        x1, y1, x2, y2 = self.coords(self.cursor)
        # want to add text in the center
        x = int(x1 + DELTA)  # todo: make this more flexible
        y = int(y1 + DELTA)
        # write to canvas
        # check if text object exists
        if self.char_matrix[x][y] is not None:
            text_obj = self.char_matrix[x][y]
            original_txt = self.itemcget(text_obj, 'text')
            if original_txt != event.char:  # shift everything to the right
                curr_row = self.char_matrix[y]
                updated_row = copy.deepcopy(curr_row)
                updated_row[x] = text_obj

                # update the matrix with the shifted value
                for i in range(x+DELTA, self.canvas_height, DELTA):
                    updated_row[i] = curr_row[i-DELTA]
                self.char_matrix[x] = updated_row

                # update the screen with the shifted value
                for i in range(x, self.canvas_height, DELTA):
                    try:
                        txt = self.itemcget(self.char_matrix[x][y], 'text')
                        self.itemconfigure(self.char_matrix[x][y], text=txt)
                    except TclError:
                        print("Unable to process")

        print(f'{event.char} at X:{x} and Y:{y}')
        text_obj = self.create_text(x, y, text=event.char)
        self.char_matrix[x][y] = text_obj
        # move the cursor to reflect the text added
        x, y = direction_dict.get(RIGHT)
        self.trigger_cursor_move(x, y)

    def delete_char(self):
        x1, y1, x2, y2 = self.coords(self.cursor)
        x = int(x1 + DELTA)
        y = int(y1 + DELTA)

        if self.char_matrix[x][y] is not None:
            text_obj = self.char_matrix[x][y]
            self.delete(text_obj)
            self.char_matrix[x][y] = None

        x, y = direction_dict.get(LEFT)
        self.trigger_cursor_move(x, y)


if __name__ == "__main__":
    root = Tk()
    root.title("TextEditor")
    root.resizable(False, False)
    window = TextEditor()
    root.mainloop()
