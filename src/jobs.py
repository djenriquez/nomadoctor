import requests
import json
import os
import logging
import base64

class Jobs:
    JOBS_URI = '/v1/jobs'

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._headers = { 'X-Nomad-Token': token } if token is not None else {}

    # Call /v1/jobs to fetch all jobs
    def __list_jobs(self):
        request_url = f'{self._endpoint}{self.JOBS_URI}'
        r = requests.Response()
        jobs = []
        try:
            r = requests.get(request_url, headers=self._headers)
            r.raise_for_status()
            jobs = json.loads(r.text)
        except:
            logging.critical("Failed to list nomad jobs")
            raise

        return jobs

    def __extract_job_names(self, jobs):
        job_names = [ job['Name'] for job in jobs ]
        return job_names

    def __fetch_job_definitions(self, job_names):
        job_definitions = []
        for job_name in job_names:
            request_url = f'{self._endpoint}/v1/job/{job_name}'
            r = requests.Response()
            try:
                r = requests.get(request_url, headers=self._headers)
                r.raise_for_status()
                job_def = base64.b64encode(bytes(r.text, 'utf-8')).decode('utf-8')
                job_definitions.append(job_def)
            except:
                logging.critical(f'Failed to fetch job definition for {job_name}', exc_info=True)
        return job_definitions


    def __output_jobs(self, job_definitions):
        for job_def in job_definitions:
            print(job_def)

    def backup_jobs(self):
        # fetch all jobs
        jobs = self.__list_jobs()
        # extract job names
        job_names = self.__extract_job_names(jobs)
        # fetch job definitions
        job_definitions = self.__fetch_job_definitions(job_names)
        # print out jobs
        self.__output_jobs(job_definitions)

    def restore_jobs(self, jobs_file):
        with open(f'/restore/{jobs_file}', 'r') as job_definitions:
            for job in job_definitions:
                self.__deploy_job(job)
        job_definitions.close()
    
    def __deploy_job(self, job):
        r = requests.Response()
        job_def = base64.b64decode(job).decode('utf-8')
         
        job_name = json.loads(job_def)['Name']

        data = json.loads(job_def)
        job_def = { 'Job': data }
        

        request_url = f'{self._endpoint}{self.JOBS_URI}'
        try:
            r = requests.post(request_url, data=json.dumps(job_def), headers=self._headers)
            r.raise_for_status()
            logging.info(f'Deploying {job_name}: {r.text}')
        except:
            logging.critical(f'Failed to deploy {job_name}', exc_info=True)
    