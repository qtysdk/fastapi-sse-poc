'''
Get status as an event generator
'''
import asyncio
import datetime
import logging

logger = logging.getLogger('sse')

status_stream_delay = 5  # second
status_stream_retry_timeout = 30000  # milisecond


async def status_event_generator(request):
    while True:
        if await request.is_disconnected():
            logger.debug('Request disconnected')
            break

        yield {"event": "update", "data": datetime.datetime.isoformat(datetime.datetime.now())}

        await asyncio.sleep(status_stream_delay)
