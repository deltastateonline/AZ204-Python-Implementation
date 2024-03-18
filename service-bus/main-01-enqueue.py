import os
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from dotenv import load_dotenv
from datetime import datetime , timedelta




async def send_single_message(sender):
    suffix = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # Create a Service Bus message and send it to the queue
    message = ServiceBusMessage("Single Message",application_properties={'sentby':'cli', 'language':'python310', 'created': suffix}, subject="Az204")
    #message.application_properties({'sentby':'cli', 'language':'python310'})

    message.time_to_live = timedelta(seconds=10)
    
    await sender.send_messages(message)

    person : dict = {
        "name": "Mike West",
        "age": 30,
        "married" : True,
        "created": suffix
    }
    

    message1 = ServiceBusMessage(str(person), content_type="application/json")
    message1.application_properties = {'sentby':'cli', 'language':'python310', 'data-type': 'dictionary'}
    await sender.send_messages(message1)

    print("Sent a single message")


async def send_a_list_of_messages(sender):
    # Create a list of messages and send it to the queue
    messages = [ServiceBusMessage("Message in list") for _ in range(5)]
    await sender.send_messages(messages)
    print("Sent a list of 5 messages")


async def send_batch_message(sender):
    # Create a batch of messages
    async with sender:
        batch_message = await sender.create_message_batch()
        for _ in range(10):
            try:
                # Add a message to the batch
                batch_message.add_message(ServiceBusMessage("Message inside a ServiceBusMessageBatch"))
            except ValueError:
                # ServiceBusMessageBatch object reaches max_size.
                # New ServiceBusMessageBatch object can be created here to send more data.
                break
        # Send the batch of messages to the queue
        await sender.send_messages(batch_message)
    print("Sent a batch of 10 messages")

async def run():
    #await s
    load_dotenv()

    # create a Service Bus client using the connection string
    async with ServiceBusClient.from_connection_string(
        conn_str=os.getenv('NAMESPACE_CONNECTION_STR'),
        logging_enable=True) as servicebus_client:
        # Get a Queue Sender object to send messages to the queue
        sender = servicebus_client.get_queue_sender(queue_name=os.getenv('QUEUE_NAME'))
        async with sender:
            # Send one message
            await send_single_message(sender)
            # Send a list of messages
            #await send_a_list_of_messages(sender)
            # Send a batch of messages
            #await send_batch_message(sender)


#async def main():
print("Start Processing ")
asyncio.run(run())
print("Done sending messages")
print("-----------------------")

#if __name__ == "__main__":
    #main()