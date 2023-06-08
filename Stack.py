class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if not self.is_empty():
            return self.data.pop()

    def is_empty(self):
        return len(self.data) == 0

    def clear(self):
        self.data = []

    def get_values(self):
        return self.data

    def peek(self):
        if not self.is_empty():
            return self.data[-1]
