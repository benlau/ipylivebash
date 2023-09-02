class ScaffoldVar:
    def __call__(self, value, output):
        self.write(value)
        output(self.write_message(value))

    def __str__(self):
        return self.read()
