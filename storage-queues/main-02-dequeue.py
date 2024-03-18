import sys
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage, BinaryBase64DecodePolicy, BinaryBase64EncodePolicy
from dotenv import load_dotenv
from azure.core.exceptions import AzureError


load_dotenv()


#logging.basicConfig(level=logging.INFO)

queue_name='queue01'

def main():
    print("Start Processing ")
    try:
        account_url = "https://staiwclientapp002.queue.core.windows.net"
        clientCreds : DefaultAzureCredential = DefaultAzureCredential()
        queue_client = QueueClient(account_url, queue_name=queue_name ,credential=clientCreds)


        

        while True:
            peeked_messages = queue_client.receive_messages(max_messages=5)
            for peeked_message in peeked_messages:
            # Display the message
                print("Message: " + peeked_message.content) 
                queue_client.delete_message(peeked_message)

            x = input('Press enter to continue or s to stop processing')
            if x == "s":
                 sys.exit(0)



             

        

    # Create the queue
        

    except AzureError as ex:
            error_message = f"Error creating container:\n{str(ex)}"
            logging.critical(error_message)


     

if __name__ == "__main__":
    main()