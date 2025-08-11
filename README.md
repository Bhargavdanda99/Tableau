# Tableau
when developer add the workbook to repo pipeline will trigger and it will upload to Tableau cloud
Create Repository.
And create pipeline with repository and add powershell and piblish artifact tasks.
In publish task add this in file or directory path.($(Build.ArtifactStagingDirectory)
And create release pipeline in that add to command line script task and python script task.
In command line script task add this command:pip install tableau-api-lib.
And in pytohon script add the script whicj is present in above repo.(python script to upload workbook to Tableau cloud)

<img width="753" height="436" alt="image" src="https://github.com/user-attachments/assets/332bf1df-3230-4bc8-9200-bcba61a2fadd" />

