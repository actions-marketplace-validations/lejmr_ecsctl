
# Helper function making reading external override easier
def parse_value_override(arg):
    i = arg.index("=")
    key = arg[:i].strip()
    val = arg[i+1:].strip()
    return {key:val}