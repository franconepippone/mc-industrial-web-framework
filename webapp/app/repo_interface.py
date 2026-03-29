from typing import List
import yaml
import github
from spec_schemas import BaseDeviceSpec, RDSRouterSpec, FootprintSpec, build_device_spec_object

class SpecFilter:
    def __init__(self):
        pass


class RepoInterface:
    REPO_NAME = "franconepippone/mc-industrial-web-framework"
    BRANCH = "master"

    def __init__(self, token: None | str = ""):
        self.design_specs: List[BaseDeviceSpec] = []
        
        if not token: token = ""

        auth = github.Auth.Token(token)
        self.g = github.Github(auth=auth)

        self.repo = self.g.get_repo(self.REPO_NAME)

    def load_design_specs(self):

        spec_paths = []
        branch = self.repo.get_branch(self.BRANCH)
        tree = self.repo.get_git_tree(branch.commit.sha, recursive=True)
        for element in tree.tree:
            path = element.path
            if path.startswith("designs/") and path.endswith("specs.yaml"):
                spec_paths.append(path)


        self.design_specs.clear() # reset designs list

        for path in spec_paths:
            content = self.repo.get_contents(path, ref=self.BRANCH)
            if isinstance(content, list):
                print(f"Warning: {path} is a directory, skipping")
                continue
            
            # handles parsing and conversion from YAML to dict
            try:
                yaml_data = yaml.safe_load(content.decoded_content)
            except yaml.YAMLError as e:
                print("YAML parsing error:")
                print(e)
                continue
            
            # construct a valid spec object from the dict, if device class is valid
            obj = build_device_spec_object(yaml_data)
            obj.repopath = path  # Set the repository path
            self.design_specs.append(obj)
        
        print(f"Loaded {len(self.design_specs)} design specs")

        for spec in self.design_specs:
            print(spec.repopath)

    def get_filtered(self, filter0: SpecFilter) -> List[BaseDeviceSpec]:
        pass



if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    repo = RepoInterface(token)
    repo.load_design_specs()