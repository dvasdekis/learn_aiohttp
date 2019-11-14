# learn_aiohttp and asyncio

Best explanation I've read so far is here: https://www.roguelynn.com/words/asyncio-we-did-it-wrong/


My take on understanding the async paradigm is:

In normal programming, we tell the computer what to do, and the order in which it should do it. ETL is the common example: we command the computer to extract some data, then transform it, then load it somewhere else. The transform step waits for the extract step, which waits for the load step.

Modern Async hinges on the concept of awaitables. The program instead starts the request (for example a network request), but instead of holding up program execution until the request has completed, we start doing something else, and only come back to the function dealing with the network request when the result of that function returns. In this sense, we 'await' the result of the network return.

Before awaitables in Python 3.5+, Async started with the concept of generators, because a generator by definition may have no end. If you inspect/slice the generator at its beginning, you're going to see a set of results produced, but there's no way you can wait for the generator to keep running before you perform the rest of your code - it will run forever. So in order to handle generators, Python developed some legacy Async concepts.

Now with awaitables, we define a coroutine with async def, 
