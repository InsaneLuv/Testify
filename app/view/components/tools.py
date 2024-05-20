from PyQt5.QtCore import QTime, QTimer

def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

class TimerManager:
    def __init__(self, total_time_minutes, update_callback, on_end_callback=None):
        self.total_time_seconds = total_time_minutes * 60
        self.elapsed_time_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.update_callback = update_callback
        self.on_end_callback = on_end_callback

    def start_timer(self):
        self.update_timer()  # Update immediately
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        self.elapsed_time_seconds += 1
        remaining_time = self.calculate_remaining_time()
        self.update_callback(remaining_time)

        if remaining_time == QTime(0, 0):
            self.timer.stop()
            if self.on_end_callback is not None:
                self.on_end_callback()

    def calculate_remaining_time(self):
        remaining_time_seconds = max(0, int(self.total_time_seconds) - self.elapsed_time_seconds)
        remaining_time = QTime(0, 0).addSecs(remaining_time_seconds)
        return remaining_time
