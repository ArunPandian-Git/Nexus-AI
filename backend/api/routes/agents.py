from fastapi import APIRouter

router = APIRouter(
    prefix="/agents",
    tags=["Agentic Intelligence"]
)

AGENTS = [
    {
        "id": "supervisor",
        "name": "Supervisor Agent",
        "purpose": "Coordinates specialized AI agents"
    },
    {
        "id": "research",
        "name": "Research Agent",
        "purpose": "Research and information discovery"
    },
    {
        "id": "document",
        "name": "Document Agent",
        "purpose": "Document understanding and retrieval"
    },
    {
        "id": "analyst",
        "name": "Data Analyst Agent",
        "purpose": "Data analysis and insights"
    },
    {
        "id": "sql",
        "name": "SQL Agent",
        "purpose": "Structured database queries"
    },
    {
        "id": "report",
        "name": "Report Agent",
        "purpose": "Generate analytical reports"
    }
]


@router.get("/")
async def list_agents():

    return {
        "application": "NEXUS AI",
        "total_agents": len(AGENTS),
        "agents": AGENTS
    }


@router.get("/{agent_id}")
async def get_agent(agent_id: str):

    for agent in AGENTS:
        if agent["id"] == agent_id:
            return agent

    return {
        "status": "not_found",
        "message": "Agent does not exist."
    }
