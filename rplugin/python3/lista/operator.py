try:
    import vim

    encoding = vim.eval('&encoding') or 'utf-8'

    def call(vim, name, *args):
        result = vim.Function(name)(*args)
        if isinstance(result, bytes):
            if result.startswith(b"\x80"):
                result = "\udc80" + result[1:].decode(encoding)
            else:
                result = result.decode(encoding)
        return result

except ImportError:

    def call(nvim, *args):
        return nvim.call(*args)
