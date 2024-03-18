import os
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage, BinaryBase64DecodePolicy, BinaryBase64EncodePolicy
from dotenv import load_dotenv
from azure.core.exceptions import AzureError
from datetime import datetime


load_dotenv()


#logging.basicConfig(level=logging.INFO)

queue_name='queue01'
fname = 'data/product.txt'



def main():
    print("Start Processing ")
    
    try:
        account_url = "https://staiwclientapp002.queue.core.windows.net"
        clientCreds : DefaultAzureCredential = DefaultAzureCredential()
        queue_client = QueueClient(account_url, queue_name=queue_name ,credential=clientCreds)

        with open(fname,"r") as jf:
             for txt in jf:        
                suffix1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
                print(txt.strip())
                data = {}
                data["message"] = txt.strip()
                data["created"] = suffix1
                queue_client.send_message(data,time_to_live=180)        

    except AzureError as ex:
            error_message = f"Error creating container:\n{str(ex)}"
            logging.critical(error_message)

    print("Done.")

def createQueue(queue_client: QueueClient):
     logging.info("Creating Queue")
     queue_client.create_queue()
     

if __name__ == "__main__":
    main()