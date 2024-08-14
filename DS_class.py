from typing import List, TypedDict, Optional 

class UserStory(TypedDict):
    title: str
    description: str
    file_name: str

class HighSupervisorState(TypedDict):
    user_stories: List[UserStory]
    assigned_files: List[str]
    
class DocumentationSearcherState(TypedDict):
    user_story: UserStory
    guidelines: Optional[str]
    templates: Optional[str]

class CodeGeneratorState(TypedDict):
    guidelines: str
    templates: str
    generated_code: Optional[str]

class CodeTesterState(TypedDict):
    generated_code: str
    test_results: Optional[str]
    is_syntax_correct: Optional[bool]
    
class TeamState(TypedDict):
    documentation_state: DocumentationSearcherState
    code_generation_state: CodeGeneratorState
    testing_state: CodeTesterState
    
class MultiAgentSystemState(TypedDict):
    high_supervisor_state: HighSupervisorState
    frontend_team_state: TeamState
    backend_team_state: TeamState
    database_team_state: TeamState