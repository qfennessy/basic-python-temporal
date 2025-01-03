import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("temporalio.worker._workflow_instance").setLevel(logging.ERROR)

# Other worker setup code
from temporalio.worker import Worker
from temporalio.client import Client
from workflows import EchoWorkflow, echo_activity

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="echo-task-queue",
        workflows=[EchoWorkflow],
        activities=[echo_activity],
    )

    print("Worker started. Listening for tasks...")
    await worker.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
