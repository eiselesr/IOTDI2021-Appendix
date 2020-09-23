from pulsar import Function, SerDe


# class MyObject(object):
#     def __init__(self):
#         self.a = 0
#         self.b = 0


class CustomSerDe(SerDe):
    def __init__(self):
        pass

    def serialize(self, input_bytes):
        return input_bytes
        # return ("%d,%d" % (object.a, object.b)).encode('utf-8')

    def deserialize(self, input_bytes):
        return input_bytes
        # split = str(input_bytes.decode()).split(',')
        # retval = MyObject()
        # retval.a = int(split[0])
        # retval.b = int(split[1])
        # return retval


# Function that deals with custom objects
class CustomObjectFunction(Function):
    def __init__(self):
        pass

    def process(self, input, context):
        logger = context.get_logger()
        return type(input)
        # retval = MyObject()
        # retval.a = input.a + 11
        # retval.b = input.b + 24
        # return retval