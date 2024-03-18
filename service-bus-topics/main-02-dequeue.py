import os
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusReceivedMessage , ServiceBusReceiveMode , ServiceBusReceiver
from dotenv import load_dotenv


async def peek_message(sbClient : ServiceBusReceiver):

    while True:
        messages : list[ServiceBusReceivedMessage]  = await sbClient.receive_messages(max_message_count=10 )
    
        for message in messages :
            print(f"{message} : Properties : {message.application_properties} , Content-Type: {message.content_type}") 

        
    return "Test"


async def run():

    load_dotenv()

    # create a Service Bus client using the connection string
    async with ServiceBusClient.from_connection_string(
        conn_str=os.getenv('NAMESPACE_CONNECTION_STR'),
        logging_enable=True) as servicebus_client:
        # Get a Queue Sender object to send messages to the queue
        #sbClient = servicebus_client.get_queue_receiver(queue_name=os.getenv('QUEUE_NAME'), receive_mode=ServiceBusReceiveMode.PEEK_LOCK)
        sbClient = servicebus_client.get_subscription_receiver(topic_name=os.getenv('TOPIC_NAME'), subscription_name='sub1', receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE)


        async with sbClient:
            # Send one message
            await peek_message(sbClient)




if __name__ == "__main__":
    print("Start Processing ")
    asyncio.run(run())
    print("Done processing messages")
    print("-----------------------")