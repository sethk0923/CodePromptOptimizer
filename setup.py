from setuptools import setup

setup(
    name="code_prompt_optimizer",
    version="1.0.0",
    description="A GUI tool that optimizes prompts and code files for AI tools",
    author="Your Name",
    packages=["code_prompt_optimizer"],
    install_requires=[
        "tiktoken==0.7.0",
        "nltk==3.8.1",
        "pyinstaller==6.3.0"
    ],
    entry_points={
        'console_scripts': [
            'code_prompt_optimizer=code_prompt_optimizer.token_script_v2:main',
        ],
    },
) 