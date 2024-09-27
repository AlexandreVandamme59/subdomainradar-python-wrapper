# SubdomainRadar Python API Wrapper

This repository contains Python wrapper for the SubdomainRadar API, allowing you to interact with the SubdomainRadar service for enumerating subdomains, managing tasks, performing reverse searches.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Python](#python)
- [API Methods](#api-methods)
  - [Python Methods](#python-methods)
- [Contribution](#contribution)
- [License](#license)

## Features

- List enumerators
- List enumerator groups
- Retrieve user profile
- Manage tasks
- Perform reverse search
- Enumerate domains
- Retrieve excluded domains and TLDs

## Installation

### Python

1. Clone the repository:

    ```sh
    pip install subdomainradar
    ```

## Usage

### Python 3.9+

1. Import the `SubdomainRadarAPI` class:

    ```python
    from subdomainradar import SubdomainRadarAPI
    ```

2. Create an instance of the `SubdomainRadarAPI` class:

    ```python
    api = SubdomainRadarAPI(base_url="https://api.subdomainradar.io", api_key="YOUR_API_KEY")
    ```

3. Call the available methods:

    ```python
    # Enumerate domains
    domains = ["tesla.com", "google.com"]
    results = api.enumerate_domains_with_results(domains=domains, group="Fast")
    print(results)
    ```

## API Methods

### Python Methods

- **Enumerators**
  - `list_enumerators()`
  - `list_enumerator_groups()`
  
- **Profile**
  - `get_profile()`
  
- **Tasks**
  - `get_task(task_id)`
  - `list_tasks()`
  - `enumerate_domains(domains, enumerators=None, group=None)`
  - `enumerate_domains_with_results(domains, enumerators=None, group=None)`
  
- **Reverse Search**
  - `reverse_search(subdomain_part=None, domain_part=None, tld_part=None, exclude_generic_hosting_domains=False, exclude_gov_ed_domains=False)`
  
- **Excludes**
  - `get_excludes()`

## Contribution

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
