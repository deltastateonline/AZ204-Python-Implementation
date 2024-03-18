import base64
import sys
import os
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage, BinaryBase64DecodePolicy, BinaryBase64EncodePolicy
from dotenv import load_dotenv
from azure.core.exceptions import AzureError


load_dotenv()

connectionString = os.getenv('CONNECTION_STRING')
#logging.basicConfig(level=logging.INFO)

queue_name='queue01'

def main():
    print("Start Processing ")
    try:
        account_url = "https://staiwclientapp003.queue.core.windows.net"
        queue_client = QueueClient.from_connection_string(connectionString, queue_name=queue_name)


        

        while True:
            peeked_messages = queue_client.receive_messages(max_messages=5)
            for peeked_message in peeked_messages:
            # Display the message
                message = base64.b64decode(peeked_message.content)
                print("Message: " + message.decode("utf-8")) 
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