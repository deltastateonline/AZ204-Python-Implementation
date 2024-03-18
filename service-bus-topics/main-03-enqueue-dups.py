import json
import os
import csv
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage, ServiceBusSender
from dotenv import load_dotenv
from datetime import datetime , timedelta


async def read_csv(fname , sender : ServiceBusSender):
    suffix = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    with open(fname, newline='') as csvfile:
        employees = csv.DictReader(csvfile)
        for employee in employees:
            #print(employee)
            json.dumps(employee)
            message1 = ServiceBusMessage(json.dumps(employee), content_type="application/json")
            message1.application_properties = {'sentby':'cli', 'language':'python310', 'data-type': 'dictionary' , 
                                               'employeeGroup': employee.get('Group'),
                                               'terminatedDate': employee.get('Termination Date')}
            message1.time_to_live = timedelta(seconds=60)
            message1.message_id = employee.get('Employee')
            await sender.send_messages(message1)


async def run():
    #await s
    load_dotenv()

    



    # create a Service Bus client using the connection string
    async with ServiceBusClient.from_connection_string(
        conn_str=os.getenv('NAMESPACE_CONNECTION_STR'),
        logging_enable=True) as servicebus_client:
        # Get a Queue Sender object to send messages to the queue
        sender : ServiceBusSender = servicebus_client.get_topic_sender(topic_name=os.getenv('TOPIC_NAME'))
        async with sender:
            # Send one message            
            await read_csv("../data/Employees.csv", sender)
   


#async def main():
print("Start Processing ")
asyncio.run(run())
print("Done sending messages")
print("-----------------------")

#if __name__ == "__main__":
    #main()