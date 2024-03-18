import os
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage, BinaryBase64DecodePolicy, BinaryBase64EncodePolicy
from dotenv import load_dotenv
from azure.core.exceptions import AzureError
from datetime import datetime
import base64


load_dotenv()


#logging.basicConfig(level=logging.INFO)
connectionString = os.getenv('CONNECTION_STRING')

queue_name='queue01'
fname = 'data/product.txt'

def main():
    print("Start Processing ")
    
    try:
        account_url = "https://staiwclientapp003.queue.core.windows.net"
        queue_client = QueueClient.from_connection_string(connectionString, queue_name=queue_name)
        #queue_client.from_connection_string

        with open(fname,"r") as jf:
             for txt in jf:        
                suffix1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
                print(txt.strip())
                data = {}
                data["message"] = txt.strip()
                data["created"] = suffix1
                encoded_dict = str(data).encode("utf-8")
                encoded_string = base64.b64encode(encoded_dict).decode()
                print(encoded_string)

                queue_client.send_message(encoded_string,time_to_live=180)        

    except AzureError as ex:
            error_message = f"Error creating container:\n{str(ex)}"
            logging.critical(error_message)

    print("Done.")

def createQueue(queue_client: QueueClient):
     logging.info("Creating Queue")
     queue_client.create_queue()
     

if __name__ == "__main__":
    main()