from pydantic import (
    BaseModel,
    ValidationError
)
import json

class TicketClassification(BaseModel):
    category:str
    priority:str
    team:str


def build_ticket_prompt(text):
    f"""
Classify this support ticket.

Return JSON only.

Ticket:

{text}
"""
    
def validate_ticket_response(response: str):

    try:

        # Convert JSON string -> dict
        result = json.loads(response)

        # Validate schema
        ticket = TicketClassification(
            **result
        )

        return ticket

    except json.JSONDecodeError:

        print(
            "Invalid JSON returned by model"
        )

        return None

    except ValidationError as error:

        print(
            "Schema validation failed"
        )

        print(error)

        return None