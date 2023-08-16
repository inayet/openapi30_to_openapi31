import os
import re
import asyncio
import aiofiles
import logging
import json

logging.basicConfig(level=logging.INFO)

DEFAULT_IGNORE_PATTERNS = [r"\./__pycache__", r".*\.git.*", r".*\.env.*", r"README\.md"]
CONCURRENT_TASKS_LIMIT = 4
sem = asyncio.Semaphore(CONCURRENT_TASKS_LIMIT)

def compile_patterns(patterns):
    """Compile regex patterns."""
    return [re.compile(pattern) for pattern in patterns]

async def should_ignore(item, compiled_patterns):
    """Check if the item should be ignored based on patterns."""
    for pattern in compiled_patterns:
        if pattern.search(item):
            logging.info(f"Ignoring item due to pattern {pattern.pattern}: {item}")
            return True
    logging.info(f"Item not ignored: {item}")
    return False

added_content = set()

async def generate_md_files(directory, ignore_patterns):
    """Generate markdown files for a directory."""
    logging.info(f"Processing directory: {directory}")
    async with sem:
        content_filepath = os.path.join(directory, "content.md")
        readme_filepath = os.path.join(directory, "README.md")

        user_content = ""
        # Commented out code related to README.md
        '''
        if os.path.exists(readme_filepath):
            async with aiofiles.open(readme_filepath, 'r') as f:
                content = await f.read()
            user_content_match = re.search('###BEGIN_USER_GENERATED###.*###END_USER_GENERATED###', content, re.DOTALL)
            if user_content_match:
                user_content = user_content_match.group(0)
        '''

        toc_content = "## Table of Contents\n"
        file_content_list = []
        toc_set = set()

        for entry in os.scandir(directory):
            if entry.is_file() and not await should_ignore(entry.path, ignore_patterns):
                if entry.name.endswith(".json"):
                    try:
                        json_content = json.loads(file_content)
                        formatted_json = json.dumps(json_content, indent=4)
                        file_content_list.append(f"\n### {entry.name}\n```json\n{formatted_json}\n```\n")
                    except json.JSONDecodeError:
                        file_content_list.append(f"\n### {entry.name}\n**[ERROR reading {entry.name} as JSON.]**\n")
                else:
                    if entry.name not in toc_set:
                        toc_content += f"- [{entry.name}](#{entry.name.replace('.', '-')})\n"
                        toc_set.add(entry.name)
                    try:
                        async with aiofiles.open(entry.path, 'r', encoding='utf-8') as f:
                            file_content = await f.read()
                            if file_content not in added_content:
                                if entry.name not in ["content.md", "README.md"]:
                                    file_content_list.append(f"\n### {entry.name}\n```\n{file_content}\n```\n")
                                    added_content.add(file_content)
                    except UnicodeDecodeError:
                        file_content_list.append(f"\n### {entry.name}\n**[ERROR reading {entry.name} as text. Might be a binary file or use a different encoding.]**\n")

        new_content = toc_content + "\n" + ''.join(file_content_list)

        async with aiofiles.open(content_filepath, 'w') as f:
            await f.write(new_content)

async def process_directory(directory):
    """Recursively process directories."""
    logging.info(f"Checking directory: {directory}")

    ignore_file_path = os.path.join(directory, "display_project_files.ignore")
    if os.path.exists(ignore_file_path):
        async with aiofiles.open(ignore_file_path, 'r') as f:
            ignore_patterns = compile_patterns([line.strip() for line in await f.readlines()])
        logging.info(f"Loaded ignore patterns for {directory}: {ignore_patterns}")
    else:
        ignore_patterns = compile_patterns(DEFAULT_IGNORE_PATTERNS)

    await generate_md_files(directory, ignore_patterns)

    for entry in os.scandir(directory):
        if entry.is_dir():
            await process_directory(entry.path)

if __name__ == "__main__":
    asyncio.run(process_directory("."))
