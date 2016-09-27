import vim


# NOTE:
# vim.options['encoding'] returns bytes but vim.eval('&encoding') returns str
ENCODING = vim.eval('&encoding')


def bind(cls, component_cls, attr):
    if hasattr(cls, attr) or not hasattr(component_cls, attr):
        return
    original = getattr(component_cls, attr)

    def method(self, *args, **kwargs):
        return original(self.component, *args, **kwargs)

    setattr(cls, attr, method)


class Decorator:
    def __init__(self, component):
        self.component = component
        self.__class__ = type('Decorator', (self.__class__,), {})
        for attr in component.__class__.__dict__.keys():
            bind(self.__class__, component.__class__, attr)

    def __getattr__(self, name):
        value = getattr(self.component, name)
        return self.__class__.decorate(value)

    @classmethod
    def decorate(cls, component):
        if component in (vim.buffers, vim.windows, vim.tabpages, vim.current):
            return Decorator(component)
        elif isinstance(component, (vim.Buffer, vim.Window, vim.TabPage)):
            return Decorator(component)
        elif isinstance(component, (vim.List, vim.Dictionary, vim.Options)):
            return ContainerDecorator(component)
        return component


class ContainerDecorator(Decorator):
    def __getitem__(self, key):
        value = self.component[key]
        if isinstance(value, bytes):
            value = value.decode(ENCODING)
        return value

    def __setitem__(self, key, value):
        if isinstance(value, str):
            value = value.encode(ENCODING)
        self.component[key] = value


class Nvim(Decorator):
    def call(self, name, *args):
        result = self.Function(name)(*args)
        if isinstance(result, bytes):
            if result.startswith(b"\x80"):
                result = "\udc80" + result[1:].decode(ENCODING)
            else:
                result = result.decode(ENCODING)
        return result
