from RPLCD import CharLCD

class LCD():

    def __init__(self, cols, rows, pin_rs, pin_e, pins_data):
        self.cols = cols
        self.rows = rows
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_data = pins_data
        self.display = CharLCD(cols, rows, pin_rs, pin_e, pins_data)

    def print_complete_status(self, temp_message, humidity_message):
        positions = [(0, 0), (1, 0)]
        for pos, message in zip(positions, [temp_message, humidity_message]:
            self.display.cursor_pos = positions[0]
            self.display.write_string(message)

    def clear_screen(self):
        self.display.clear()
