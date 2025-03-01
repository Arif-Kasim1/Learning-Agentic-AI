#   UV Commands

1.  uv init --package HelloLiteLLM
2.  uv add litellm   
3.  uv venv 
4.  .venv\Scripts\activate

#   .gitignore

1.  Install gitignore (CodeZombie)
2.  View -> Command Palette - > Add Gitignore -> Python -> It will create .gitignore file (for Python project) in your project.

#   .env
1.  Manually create .env file in src folder enter GEMINI_API_KEY=KEY

#   pyproject.toml
1.  In [project.scripts] add custom command (Project:file) (Project...folder:file)
    *   show = "hellolitellm:main"
    *   check = "hellolitellm:TestLiteLLM"


