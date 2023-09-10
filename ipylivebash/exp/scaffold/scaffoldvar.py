class ScaffoldVar:
    def __call__(self, value, append):
        self.write(value)
        append(self.write_message(value))

    def __str__(self):
        ret = self.read()
        return ret if ret is not None else ""
