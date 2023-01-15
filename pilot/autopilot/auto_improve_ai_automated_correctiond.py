import aiohttp
import aiofiles
import argparse
import asyncio
import logging
import os
import unittest

import openai

def get_openai_api_key() -> str:
    """Returns the OpenAI API key"""
    return os.getenv("OPENAI_API_KEY")

class CodeImprover:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.file_contents: str = self._read_file('weather.txt')
        self.file_types: dict = {
            "py": "python script to run poetry install",
            "js": "javascript script",
            "rb": "ruby script",
            "php": "php script",
            "txt": "Instructions List on how to build a lego house",
            "c++": "c++ script to find the area of a triangle",
            # "txt": "free verse poem",
            
        }
        self.file_type: str = self.get_file_type()
        self.selected_suggestions: str = None
        self.engine: str = os.getenv('OPENAI_ENGINE')
        self.logger = logging.getLogger(__name__)

    async def _read_file(self, file_path: str) -> str:
        """Reads a file and returns its contents"""
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
                content: str = await file.read()
        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            raise e
        return content

    async def _write_file(self, file_path: str, content: str):
        """Writes content to a file"""
        try:
            async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
                await file.write(content)
        except Exception as e:
            self.logger.error(f"Error writing file: {e}")
            raise e

    def get_file_type(self) -> str:
        """Gets the file type of the code file"""
        return self.file_types.get(self.file_path.split(".")[-1], "unknown")
    
    async def _get_file_content(self) -> str:
        """Gets the content of the code file"""
        return await self._read_file(os.path.basename(self.file_path))

    async def _get_suggestions(self, prompt: str, engine: str='text-davinci-003', temperature: float=0.7, max_tokens: int=3000, top_p: float=1, frequency_penalty: float=0, presence_penalty: float=0) -> str:
        """Makes an API call to the OpenAI API and returns the suggestions for improvement"""
        try:
            openai.api_key = get_openai_api_key()
            async with aiohttp.ClientSession() as session:
                async with session.post(f'https://api.openai.com/v1/engines/{engine}/completions',headers={'Authorization': f'Bearer {openai.api_key}'},
                                        json={'prompt': prompt,
                                              'temperature': temperature,
                                              'max_tokens': max_tokens,
                                              'top_p': top_p,
                                              'frequency_penalty': frequency_penalty,
                                              'presence_penalty': presence_penalty,
                                              'stop': ['\n\n### Suggestions', '\n\n### New']}) as resp:
                    response = await resp.json()
                    # self.logger.info("Response from OpenAI API: %s", response)
                    # response = openai.Completion.create(engine=engine, prompt=prompt, temperature=temperature, max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stop=['\n\n### Suggestions', '\n\n### New'])
                    return response['choices'][0]['text']
                    # return response.choices[0].text
        except Exception as e:
            self.logger.error(f"Error getting suggestions from OpenAI API: {e}")
            raise e

    async def get_possible_improvement_categories(self) -> str:
        """Gets the possible categories for improvement based on file type and contents"""
        instruction = f"#### List how to improve this {self.file_type}\n\n### Old {self.file_type}\n{await self._get_file_content()}\n\n\nHow could I improve this {self.file_type}?\n"
        return await self._get_suggestions(instruction, self.engine)

    async def apply_improvements(self, suggestions: str, old_code: str) -> str:
        """Apply the selected suggestions to the code"""
        instruction = f'''#### Improve the following {self.file_type} using the instructions below\n\n### Old {self.file_type}\n"""\n{old_code}\n"""\n\n### Suggestions\n"""\n{suggestions}\n"""\n\n### New {self.file_type}\n"""\n'''
        self.logger.info("apply improvement instruction: %s", instruction)
        try:
            improved_code = await self._get_suggestions(instruction, engine='text-davinci-003')
            # improved_code = await self._get_suggestions(instruction, engine='code-davinci-002')
            await self._write_file(self.file_path, improved_code)
            return improved_code
        except Exception as e:
            self.logger.error(f"Error applying suggestions: {e}")
            raise e

    async def main(self):
        logging.basicConfig(level=logging.INFO)
        args = parse_args()
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)
        self.engine = args.engine
        possible_improvement_categories = await self.get_possible_improvement_categories()
        await self.apply_improvements(
            possible_improvement_categories, await self._get_file_content()
        )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="code_improvement")
    parser.add_argument("file_path")
    parser.add_argument("--engine", default='text-davinci-003')
    parser.add_argument("--verbose", action="store_true")

    return parser.parse_args()

async def main() -> None:
    code_improvement = CodeImprover(parse_args().file_path)
    await code_improvement.main()

if __name__ == "__main__":
    while True:
        asyncio.run(main())











# '''
# import argparse
# import asyncio
# import logging
# import os
# import unittest

# import aiofiles
# import aiohttp
# import openai


# def get_openai_api_key() -> str:
#     """Returns the OpenAI API key"""
#     return openai.get_openai_api_key()

# class CodeImprover:
#     def __init__(self, file_path: str) -> None:
#         self.file_path: str = file_path
#         self.file_contents: str = self._read_file('test.py')
#         self.file_types: dict = {
#             "py": "python script",
#             "js": "javascript script",
#             "rb": "ruby script",
#             "php": "php script",
#         }
#         self.file_type: str = self.get_file_type()
#         self.selected_suggestions: str = None
#         self.engine: str = os.getenv('OPENAI_ENGINE')
#         self.logger = logging.getLogger(__name__)

#     async def _read_file(self, file_path: str) -> str:
#         """Reads a file and returns its contents"""
#         try:
#             async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
#                 content: str = await file.read()
#         except Exception as e:
#             self.logger.error(f"Error reading file: {e}")
#             raise e
#         return content

#     async def _write_file(self, file_path: str, content: str) -> None:
#         """Writes content to a file"""
#         try:
#             async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
#                 await file.write(content)
#         except Exception as e:
#             self.logger.error(f"Error writing file: {e}")
#             raise e

#     def get_file_type(self) -> str:
#         """Gets the file type of the code file"""
#         return self.file_types.get(self.file_path.split(".")[-1], "unknown")
    
#     async def _get_file_content(self) -> str:
#         """Gets the content of the code file"""
#         return await self._read_file(os.path.basename(self.file_path))

#     async def _get_suggestions(self, prompt: str, engine: str='text-davinci-003', temperature: float=0.7, max_tokens: int=2000, top_p: float=1, frequency_penalty: float=0, presence_penalty: float=0) -> str:
#         """Makes an API call to the OpenAI API and returns the suggestions for improvement"""
#         try:
#             openai.api_key = get_openai_api_key()
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(f'https://api.openai.com/v1/engines/{engine}/completions',headers={'Authorization': f'Bearer {openai.api_key}'},
#                                         json={'prompt': prompt,
#                                               'temperature': temperature,
#                                               'max_tokens': max_tokens,
#                                               'top_p': top_p,
#                                               'frequency_penalty': frequency_penalty,
#                                               'presence_penalty': presence_penalty,
#                                               'stop': ['\n\n### Suggestions', '\n\n### New']}) as resp:
#                     response = await resp.json()

                    
#                     # self.logger.info("Response from OpenAI API: %s", response_text)
#                     # response = openai.Completion.create(engine=engine, prompt=prompt, temperature=temperature, max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stop=['\n\n### Suggestions', '\n\n### New'])
#                     return response.choices[0].text
#         except Exception as e:
#             self.logger.error(f"Error getting suggestions from OpenAI API: {e}")
#             raise e

#     async def get_possible_improvement_categories(self) -> str:
#         """Gets the possible categories for improvement based on file type and contents"""
#         instruction = f"#### List how to improve this {self.file_type}\n\n### Old {self.file_type}\n{await self._get_file_content()}\n\n\nHow could I improve this {self.file_type}?\n"
#         return await self._get_suggestions(instruction, self.engine)

#     async def apply_improvements(self, suggestions: str, old_code: str) -> str:
#         """Apply the selected suggestions to the code"""
#         instruction = f'''#### Implement the following suggestions in {self.file_type}\n\n### Old {self.file_type}\n"""\n{old_code}\n"""\n\n### Suggestions\n"""\n{suggestions}\n"""\n\n### New {self.file_type}\n"""\n'''
#         self.logger.info("apply improvement instruction: %s", instruction)
#         try:
#             improved_code = await self._get_suggestions(instruction, self.engine)
#             improved_code = await self._add_type_hints_and_annotations(improved_code)
#             improved_code = await self._extract_common_functionality(improved_code)
#             improved_code = await self._add_logging_statements(improved_code)
#             improved_code = await self._add_comments(improved_code)
#             improved_code = await self._refactor_long_complex_functions(improved_code)
#             improved_code = await self._use_descriptive_variable_names(improved_code)
#             improved_code = await self._add_unit_tests(improved_code)
#             improved_code = await self._add_command_line_arguments(improved_code)
#             improved_code = await self._add_error_handling(improved_code)
#             improved_code = await self._reformat_code(improved_code)
#             await self._write_file(self.file_path, improved_code)
#             return improved_code
#         except Exception as e:
#             self.logger.error(f"Error applying suggestions: {e}")
#             raise e
    
#     async def _add_type_hints_and_annotations(self, code: str) -> str:
#         """Adds type hints and annotations to the code to make it more readable and self-documenting."""
#         instruction = f'''#### Add type hints and annotations to the code to make it more readable and self-documenting.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _extract_common_functionality(self, code: str) -> str:
#         """Extracts common functionality into separate methods to reduce code duplication and increase code readability."""
#         instruction = f'''#### Extract common functionality into separate methods to reduce code duplication and increase code readability.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _add_logging_statements(self, code: str) -> str:
#         """Adds logging statements to track errors, performance issues, and other important events."""
#         instruction = f'''#### Add logging statements to track errors, performance issues, and other important events.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)
    
#     async def _add_comments(self, code: str) -> str:
#         """Adds comments to the code to make it easier to understand."""
#         instruction = f'''#### Add comments to the code to make it easier to understand.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _refactor_long_complex_functions(self, code: str) -> str:
#         """Refactors long and complex functions into smaller functions to make them easier to understand."""
#         instruction = f'''#### Refactor long and complex functions into smaller functions to make them easier to understand.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _use_descriptive_variable_names(self, code: str) -> str:
#         """Uses descriptive variable names to make the code easier to understand."""
#         instruction = f'''#### Use descriptive variable names to make the code easier to understand.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _add_unit_tests(self, code: str) -> str:
#         """Adds unit tests to ensure the code works as expected."""
#         instruction = f'''#### Add unit tests to ensure the code works as expected.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _add_command_line_arguments(self, code: str) -> str:
#         """Adds command line arguments to make the code more flexible."""
#         instruction = f'''#### Add command line arguments to make the code more flexible.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _add_error_handling(self, code: str) -> str:
#         """Adds error handling to make the code more robust."""
#         instruction = f'''#### Add error handling to make the code more robust.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _reformat_code(self, code: str) -> str:
#         """Reformats the code to make it more readable."""
#         instruction = f'''#### Reformat the code to make it more readable.\n\n### Old {self.file_type}\n"""\n{code}\n"""\n\n### New {self.file_type}\n"""\n'''
#         return await self._get_suggestions(instruction, self.engine)

#     async def _get_suggestions(self, instruction: str, engine: str) -> str:
#         """Gets suggestions from the engine."""
#         self.logger.info("getting suggestions from %s", engine)
#         if engine == "code2seq":
#             return await self._get_suggestions_from_code2seq(instruction)
#         elif engine == "code2vec":
#             return await self._get_suggestions_from_code2vec(instruction)
#         else:
#             raise ValueError(f"invalid engine: {engine}")

#     async def _get_suggestions_from_code2seq(self, instruction: str) -> str:
#         """Gets suggestions from code2seq."""
#         self.logger.info("getting suggestions from code2seq")
#         try:
#             # write the instruction to a file
#             instruction_file_path = os.path.join(self.temp_dir, "instruction.txt")
#             await self._write_file(instruction_file_path, instruction)
#             # run code2seq
#             code2seq_command = f"python3 {self.code2seq_path} --load {self.code2seq_model_path} --predict {instruction_file_path} --max_contexts 1000 --max_path_length 8 --max_path_width 2 --max_target_width 0 --num_threads 1 --batch_size 1 --beam_size 1 --print_paths"
#             self.logger.info("running code2seq command: %s", code2seq_command)
#             code2seq_output = await self._run_command(code2seq_command)
#             # parse the output
#             code2seq_output = code2seq_output.split(" | ")[1]
#             code2seq_output = code2seq_output.replace(" ", "")
#             code2seq_output = code2seq_output.replace("", "")
        
#             self.logger.error(f"Error applying suggestions: {e}")
#             raise e
#         except Exception as e:
#             self.logger.error(f"Error applying suggestions: {e}")
#             raise e

#     async def _get_suggestions_from_code2vec(self, instruction: str) -> str:
#         """Gets suggestions from code2vec."""
#         self.logger.info("getting suggestions from code2vec")
#         try:
#             # write the instruction to a file
#             instruction_file_path = os.path.join(self.temp_dir, "instruction.txt")
#             await self._write_file(instruction_file_path, instruction)
#         except Exception as e:
#             self.logger.error(f"Error applying suggestions: {e}")
#             raise e

#     async def _get_file_content(self) -> str:
#         """Gets the content of the file."""
#         self.logger.info("getting file content")
#         try:
#             async with aiofiles.open(self.file_path, "r") as f:
#                 return await f.read()
#         except Exception as e:
#             self.logger.error(f"Error getting file content: {e}")
#             raise e

#     async def _write_file(self, file_path: str, content: str) -> None:
#         """Writes content to a file."""
#         self.logger.info("writing file")
#         try:
#             async with aiofiles.open(file_path, "w") as f:
#                 await f.write(content)
#         except Exception as e:
#             self.logger.error(f"Error writing file: {e}")
#             raise e

#     async def _run_command(self, command: str) -> str:
#         """Runs a command."""
#         self.logger.info("running command")
#         try:
#             process = await asyncio.create_subprocess_shell(
#                 command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
#             )
#             stdout, stderr = await process.communicate()
#             if process.returncode != 0:
#                 raise Exception(f"command failed with return code {process.returncode}")
#             return stdout.decode().strip()
#         except Exception as e:
#             self.logger.error(f"Error running command: {e}")
#             raise e

#     async def _get_possible_improvement_categories(self) -> List[str]:
#         """Gets possible improvement categories."""
#         self.logger.info("getting possible improvement categories")
#         try:
#             possible_improvement_categories = []
#             if self.file_type == "python":
#                 possible_improvement_categories = [
#                     "add_error_handling",
#                     "reformat_code",
#                 ]
#             elif self.file_type == "java":
#                 possible_improvement_categories = [
#                     "add_error_handling",
#                     "reformat_code",
#                 ]
#             else:
#                 raise ValueError(f"invalid file type: {self.file_type}")
#             return possible_improvement_categories
#         except Exception as e:
#             self.logger.error(f"Error getting possible improvement categories: {e}")
#             raise e

#     async def _apply_improvements(
#         self, possible_improvement_categories: List[str], file_content: str
#     ) -> str:
#         """Applies improvements to the file."""
#         self.logger.info("applying improvements")
#         try:
#             for possible_improvement_category in possible_improvement_categories:
#                 if possible_improvement_category == "add_error_handling":
#                     file_content = await self._apply_add_error_handling(file_content)
#                 elif possible_improvement_category == "reformat_code":
#                     file_content = await self._apply_reformat_code(file_content)
#                 else:
#                     raise ValueError(
#                         f"invalid possible improvement category: {possible_improvement_category}"
#                     )
#             return file_content
#         except Exception as e:
#             self.logger.error(f"Error applying improvements: {e}")
#             raise e
                                    

#     async def main(self):
#         logging.basicConfig(level=logging.INFO)
#         args = parse_args()
#         if args.verbose:
#             logging.basicConfig(level=logging.DEBUG)
#         self.engine = args.engine
#         possible_improvement_categories = await self.get_possible_improvement_categories()
#         await self.apply_improvements(
#             possible_improvement_categories, await self._get_file_content()
#         )

# def parse_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(prog="code_improvement")
#     parser.add_argument("file_path")
#     parser.add_argument("--engine", default='text-davinci-003')
#     parser.add_argument("--verbose", action="store_true")

#     return parser.parse_args()

# async def main() -> None:
#     code_improvement = CodeImprover(parse_args().file_path)
#     await code_improvement.main()

# if __name__ == "__main__":
#     asyncio.run(main())





            
# ''''