from subdomainradar import SubdomainRadarAPI

if __name__ == "__main__":
    your_api_key = "your_api_key_here" # https://subdomainradar.io/profile
    
    api = SubdomainRadarAPI(base_url="https://api.subdomainradar.io", api_key=your_api_key)
    domains = ["tesla.com", "google.com"]

    try:
        print('Enumerators:', api.list_enumerators())
        print('Enumerator Groups:', api.list_enumerator_groups())
        print('User Profile:', api.get_profile())
        print('Enumerate Domains with Results:', api.enumerate_domains_with_results(domains=domains, group="Fast"))
        print('Reverse Search:', api.reverse_search(subdomain_part="admin", domain_part="car", tld_part="com", exclude_generic_hosting_domains=True, exclude_gov_ed_domains=True))
        print('Excludes:', api.get_excludes())
        tasks = api.list_tasks()
        print('Tasks:', tasks)
        if tasks:
            task_id = tasks[0]['task_id']
            print('Task Status:', api.get_task(task_id))
    except ValueError as ve:
        print('Value Error:', ve)
    except PermissionError as pe:
        print('Permission Error:', pe)
    except Exception as e:
        print('Error:', e)
