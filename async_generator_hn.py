import asyncio
# from https://medium.com/velotio-perspectives/an-introduction-to-asynchronous-programming-in-python-af0189a88bbb
# This is an example of a coroutine running with a generator.
# We send it stuff using the send method on the function object we create at the bottom.
# Only when the string sent contains the word 'Dear' will the except statement be executed.


def print_name(prefix):
    print("Searching prefix:{}".format(prefix))
    try:
        while True:
            # yeild used to create coroutine
            name = (yield)
            if prefix in name:
                print(name)
    except GeneratorExit:
        print("Closing coroutine!!")


corou = print_name("Dear")
corou.__next__()
corou.send("James")
corou.send("Dear James")
corou.close()