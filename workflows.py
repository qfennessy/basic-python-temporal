from temporalio import workflow
from datetime import timedelta
from temporalio import activity
from dataclasses import dataclass

import logging

# Configure the logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
workflow_logger = logging.getLogger("workflow_logger")
activity_logger = logging.getLogger("activity_logger")

@dataclass
class EchoWorkflowParams:
    name: str

@workflow.defn(name="EchoWorkflow")
class EchoWorkflow:
    @workflow.run
    async def run(self, name: str = None) -> str:
        workflow_logger.info(f"Starting EchoWorkflow with name: {name}")

        if not name:
            workflow.logger.error("Name parameter is required but not provided.")
            raise ValueError("Name parameter must be a non-empty string")
            
        try:
            return await workflow.execute_activity(
                echo_activity,
                EchoWorkflowParams(name),
                start_to_close_timeout=timedelta(seconds=10),
            )
        except Exception as e:
            workflow_logger.error(f"Error in workflow execution: {e}", exc_info=True)
            raise

@activity.defn(name="echo_activity")
async def echo_activity(input: EchoWorkflowParams) -> str: 
    try:
        activity_logger.info(f"Starting echo_activity with input: {input}")

        if not input.name:
            raise ValueError("Invalid input: name cannot be empty")
        result = f"===> {input.name} <==="
        activity_logger.info(f"Activity completed successfully with result: {result}")
        return result
    except Exception as e:
        activity_logger.error(f"Error in echo_activity: {e}", exc_info=True)
        raise
