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
        
    # Trigger the omx multi-agent team mode
    omx_command = f'cd workspace && omx team 3:executor "{clean_prompt}"'
    subprocess.Popen(omx_command, shell=True, env=os.environ)
    
    return {"type": "message", "text": "Agents deployed to the develop branch of silver-pancake. I'll open a PR when finished."}
