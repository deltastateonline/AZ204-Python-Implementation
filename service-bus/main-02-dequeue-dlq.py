import os
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusReceivedMessage , ServiceBusReceiveMode , ServiceBusReceiver
from dotenv import load_dotenv


async def peek_message(sbClient : ServiceBusReceiver):

    messages : list[ServiceBusReceivedMessage]  = await sbClient.receive_messages(max_message_count=10)
  
    for message in messages :
        print(f"{message} : Properties : {message.application_properties} , Content-Type: {message.content_type}")



async def run():

    load_dotenv()

    # create a Service Bus client using the connection string
    async with ServiceBusClient.from_connection_string(
        conn_str=os.getenv('NAMESPACE_CONNECTION_STR'),
        logging_enable=True) as servicebus_client:
        # Get a Queue receiver object to receiver messages to the queue       
        sbClient = servicebus_client.get_queue_receiver(queue_name=f"{os.getenv('QUEUE_NAME')}/$DeadLetterQueue", receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE)
        print(sbClient.fully_qualified_namespace)
        print(sbClient.entity_path)
        
        async with sbClient:
            # dequeue messages
            await peek_message(sbClient)




if __name__ == "__main__":
    print("Start Processing ")
    asyncio.run(run())
    print("Done processing messages")
    print("-----------------------")