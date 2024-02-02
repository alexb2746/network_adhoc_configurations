# network_adhoc_configurations

This is a simple repo/pipeline for implementing set commands on all reachable Juniper devices from Netbox. This will do a commit check and diff on all devices, once passed will release a manual deploy job that will commit the config to the devices.

## Workflow

For a network engineer this is the workflow you will want to follow:
  1. Create a new branched named after your ticket i.e "Jira-XXXX"
  2. You will edit the file "configuration_set_commands.set" and replace the data with delete or set commands like you would on a Juniper device.
  3. You will edit ONLY ONE LINE on the "commit_config.py" file and that is the "commit_comment = 'Previous writing will be here'" <- you will edit the quotes with whatever comment you want on your config i.e commit_comment = '####-XXXX | changing some bgp things'
  4. Publish your branch
  5. Check the pipelines, you should see one for your branch
  6. There will be one job called "test" you will want to look at that job and see each diff for each device and a commit check as well. Typically you will see connect or timeout errors from devices that are unreachable.
  7. Review the test job throughly and if all looks good create a "merge request" this will re-kick off the test job
  8. Have another engineer review the merge request and have them approve once good
  9. This will kick off the main pipeline that will run the test job and then give you a "manual" deploy job, click run on the "deploy" job to commit the configurations to the devics...DONT FORGET YOUR WIA BEFORE THIS!!!
  10. Watch the job and check for errors.  
