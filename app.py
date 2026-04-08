from fastapi import FastAPI, Request
import subprocess
import os

app = FastAPI()

@app.post("/teams-trigger")
async def handle_teams_message(request: Request):
    data = await request.json()
    user_prompt = data.get("text", "")
    clean_prompt = user_prompt.replace("@PipelineTeam", "").strip()
    
    # Authenticate via PAT so the agents can push PRs
    repo_url = f"https://oauth2:{os.environ.get('GITHUB_TOKEN')}@github.com/kushal-sharma-24/silver-pancake.git"
    
    # Clone the repo, strictly checkout the develop branch, or pull latest if it exists
    if not os.path.exists("workspace"):
        subprocess.run(f"git clone {repo_url} workspace", shell=True)
        subprocess.run("cd workspace && git checkout develop", shell=True)
    else:
        subprocess.run("cd workspace && git checkout develop && git pull", shell=True)
        
    # Trigger the agents and FORCE the server to wait for them to finish
    omx_command = f'cd workspace && omx team 3:executor "{clean_prompt}"'
    result = subprocess.run(omx_command, shell=True, env=os.environ, capture_output=True, text=True)
    
    # Return the actual live output from the agents instead of a static message
    return {
        "type": "message", 
        "text": f"Execution Complete!\n\nAgent Output:\n{result.stdout}\n\nCheck GitHub for your PR."
    }
