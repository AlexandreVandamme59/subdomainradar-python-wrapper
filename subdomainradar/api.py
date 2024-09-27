import requests
import time
from typing import List, Optional

class SubdomainRadarAPI:
    ENUMERATORS_ENDPOINT = '/enumerators'
    GROUPS_ENDPOINT = '/enumerators/groups'
    PROFILE_ENDPOINT = '/profile'
    TASKS_ENDPOINT = '/tasks'
    ENUMERATE_ENDPOINT = '/enumerate'
    REVERSE_SEARCH_ENDPOINT = '/reverse_search'
    EXCLUDES_ENDPOINT = '/excludes'

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "SubdomainRadarAPI-Python"
        }

    def handle_response(self, response):
        if response.status_code >= 400:
            try:
                error_detail = response.json().get('detail', response.text)
            except ValueError:
                error_detail = response.text

            if response.status_code == 400:
                raise ValueError(f"Bad Request: {error_detail}")
            elif response.status_code == 401:
                raise PermissionError(f"Unauthorized: {error_detail}")
            elif response.status_code == 402:
                raise PermissionError(f"Payment Required: {error_detail}")
            elif response.status_code == 404:
                raise ValueError(f"Not Found: {error_detail}")
            elif response.status_code == 422:
                raise ValueError(f"Validation Error: {error_detail}")
            elif response.status_code == 429:
                raise PermissionError(f"Rate Limit Exceeded: {error_detail}")
            else:
                raise Exception(f"Error {response.status_code}: {error_detail}")
        return response.json()

    def request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data, params=params)
        return self.handle_response(response)

    def list_enumerators(self) -> List[dict]:
        return self.request('GET', self.ENUMERATORS_ENDPOINT)

    def list_enumerator_groups(self) -> List[dict]:
        return self.request('GET', self.GROUPS_ENDPOINT)

    def get_profile(self) -> dict:
        return self.request('GET', self.PROFILE_ENDPOINT)

    def get_task(self, task_id: str) -> dict:
        return self.request('GET', f"{self.TASKS_ENDPOINT}/{task_id}")

    def list_tasks(self) -> List[dict]:
        return self.request('GET', self.TASKS_ENDPOINT)

    def reverse_search(
        self,
        subdomain_part: Optional[str] = None,
        domain_part: Optional[str] = None,
        tld_part: Optional[str] = None,
        exclude_generic_hosting_domains: bool = False,
        exclude_gov_ed_domains: bool = False
    ) -> dict:
        params = {
            "subdomain_part": subdomain_part,
            "domain_part": domain_part,
            "tld_part": tld_part,
            "exclude_generic_hosting_domains": str(exclude_generic_hosting_domains).lower(),
            "exclude_gov_ed_domains": str(exclude_gov_ed_domains).lower(),
        }
        params = {k: v for k, v in params.items() if v not in [None, '', 'false']}
        return self.request('GET', self.REVERSE_SEARCH_ENDPOINT, params=params)

    def enumerate_domains(
        self,
        domains: List[str],
        enumerators: Optional[List[str]] = None,
        group: Optional[str] = None
    ) -> dict:
        if not enumerators and not group:
            raise ValueError("You must provide either enumerators or a group")

        if group:
            groups = self.list_enumerator_groups()
            group_data = next((g for g in groups if g["name"] == group), None)
            if not group_data:
                raise ValueError(f"Group {group} not found")
            enumerators = [enum["display_name"] for enum in group_data["enumerators"]]

        payload = {
            "domains": domains,
            "enumerators": enumerators,
        }
        return self.request('POST', self.ENUMERATE_ENDPOINT, data=payload)

    def enumerate_domains_with_results(
        self,
        domains: List[str],
        enumerators: Optional[List[str]] = None,
        group: Optional[str] = None
    ) -> dict:
        response = self.enumerate_domains(domains, enumerators, group)
        task_ids = response["tasks"]

        results = {}
        for domain, task_id in task_ids.items():
            results[domain] = self._wait_for_task(task_id)
        return results

    def _wait_for_task(self, task_id: str) -> dict:
        while True:
            task = self.get_task(task_id)
            if task["status"] == "completed":
                return task
            elif task["status"] == "failed":
                raise ValueError(f"Task failed: {task.get('error', 'Unknown error')}")
            time.sleep(5)

    # New method for Excludes
    def get_excludes(self) -> dict:
        return self.request('GET', self.EXCLUDES_ENDPOINT)