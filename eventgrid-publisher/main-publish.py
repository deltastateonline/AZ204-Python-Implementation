import os
import asyncio
import csv
from dotenv import load_dotenv
from datetime import datetime , timedelta
from azure.eventgrid import EventGridEvent
from azure.eventgrid.aio import EventGridPublisherClient
from azure.core.credentials import AzureKeyCredential


async def read_csv(fname , client : EventGridPublisherClient):
    suffix = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(fname, newline='') as csvfile:
        employees = csv.DictReader(csvfile)
        for employee in employees:
            message1 = EventGridEvent(
                event_type= 'app.neworder',
                data= employee,
                subject= f"cli/publisher/{employee.get('Group')}",
                data_version="2.0"
            )

            await client.send([message1])
   




async def main():
    #await s
    load_dotenv()

    key = os.getenv('KEY')
    endpoint = os.getenv('TOPIC_CONNECTION_STR')
    
    #credential = AzureSasCredential(sas)
    credential = AzureKeyCredential(key)
    client = EventGridPublisherClient(endpoint, credential)

    async with client :
        await read_csv("../data/Employees.csv", client)

    print("main")




print("Start Processing ")
asyncio.run(main())
print("Done sending messages")
print("-----------------------")
