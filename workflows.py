from temporalio import workflow
from datetime import timedelta
from temporalio import activity
from dataclasses import dataclass

@dataclass
class EchoWorkflowParams:
    name: str

@workflow.defn(name="EchoWorkflow")
class EchoWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        if not name or not isinstance(name, str):
            raise ValueError("Name parameter must be a non-empty string")
            
        try:
            return await workflow.execute_activity(
                echo_activity,
                EchoWorkflowParams(name),
                start_to_close_timeout=timedelta(seconds=10),
            )
        except workflow.ActivityError as e:
            workflow.logger.error(f"Activity execution failed: {str(e)}")
            raise
        except Exception as e:
            workflow.logger.error(f"Unexpected error in workflow: {str(e)}")
            raise

@activity.defn(name="echo_activity")
async def echo_activity(input: EchoWorkflowParams) -> str: 
    try:
        if not input or not input.name:
            raise ValueError("Invalid input: name cannot be empty")
        return f"===> {input.name} <==="
    except Exception as e:
        activity.logger.error(f"Error in echo_activity: {str(e)}")
        raise activity.ApplicationError(f"Echo activity failed: {str(e)}")
