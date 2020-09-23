import pulsar


class BytesSerDe(pulsar.SerDe):
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

class ReadInput(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        # return input[::-1]
        logger = context.get_logger()

        try:
            logger.warn("this doesn't break")
            return input
        except AttributeError as e:
            logger.warn("Context: {}".format(context.__dict__))
            logger.warn("type(input): {}".format(type(input)))
            logger.warn("This is error 2: {}".format(e))
            return "This is error 2: {}".format(e)

