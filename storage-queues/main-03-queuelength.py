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

        properties = queue_client.get_queue_properties()
        print(f"{properties.name} queue has {properties.approximate_message_count} messages")    

    except AzureError as ex:
            error_message = f"Error creating container:\n{str(ex)}"
            logging.critical(error_message)


     

if __name__ == "__main__":
    main()