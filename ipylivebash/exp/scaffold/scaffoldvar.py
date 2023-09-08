class ScaffoldVar:
    def __call__(self, value, output):
        self.write(value)
        output(self.write_message(value))

    def __str__(self):
        ret = self.read()
        return ret if ret is not None else ""
