import os
from tableau_api_lib import TableauServerConnection

def main():
    tableau_config = {
        'tableau_prod': {
            'server': os.environ['TABLEAU_SERVER'],  # e.g., 'https://prod-apsoutheast-b.online.tableau.com'
            'api_version': '3.26',  # Use your Tableau server's REST API version
            'personal_access_token_name': os.environ['TABLEAU_PAT_NAME'],
            'personal_access_token_secret': os.environ['TABLEAU_PAT_SECRET'],
            'site_name': os.environ['TABLEAU_SITE'],  # e.g., 'bhargavdanda99-da6fdff91b'
            'site_url': os.environ['TABLEAU_SITE'],   # Usually same as site_name or '' for default site
        }
    }

    # Base artifact folder in agent pipeline
    base_dir = os.environ.get('SYSTEM_DEFAULTWORKINGDIRECTORY')
    if not base_dir:
        raise Exception("SYSTEM_DEFAULTWORKINGDIRECTORY environment variable not found.")

    # Adjust folder path based on your artifact download location
    artifact_dir = os.path.join(base_dir, '_My_project-CI (3)', 'Job1')

    if not os.path.exists(artifact_dir):
        raise Exception(f"Artifact directory does not exist: {artifact_dir}")

    print(f"Changing working directory to artifact directory: {artifact_dir}")
    os.chdir(artifact_dir)

    connection = TableauServerConnection(config_json=tableau_config, env='tableau_prod')
    connection.sign_in()

    try:
        response = connection.query_projects()
        response_json = response.json()
        print("DEBUG: Full query_projects() response:", response_json)

        projects = response_json.get('projects', {}).get('project', [])
        if not projects:
            raise Exception("No projects found in Tableau Cloud site.")

        project_name = os.environ.get('PROJECT_NAME')
        if not project_name:
            raise Exception("PROJECT_NAME environment variable is not set.")

        project_id = None
        for p in projects:
            if p.get('name') == project_name:
                project_id = p.get('id')
                break

        if not project_id:
            raise Exception(f"Project '{project_name}' not found in Tableau Cloud site.")

        workbook_files = [f for f in os.listdir('.') if f.endswith('.twb') or f.endswith('.twbx')]
        if not workbook_files:
            print("No workbook files found in the artifact directory.")
        else:
            print(f"Workbook files found to publish: {workbook_files}")

        for filename in workbook_files:
            workbook_name = os.path.splitext(filename)[0]
            print(f"Publishing workbook file {filename} as workbook name \"{workbook_name}\"")
            response = connection.publish_workbook(
                workbook_file_path=filename,
                workbook_name=workbook_name,
                project_id=project_id
            )
            print(f"Publish response for {filename}: {response.json()}")

    except Exception as e:
        print(f"Error during Tableau interaction: {e}")
        raise
    finally:
        connection.sign_out()

if __name__ == "__main__":
    main()
