import os
import logging
import asyncio
import aiofiles
import aiohttp

class FileHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)

    async def read_file(self) -> str:
        """Reads a file and returns its contents"""
        if not os.path.exists(self.file_path):
            self.logger.error("Error reading file: File does not exist")
            raise FileNotFoundError

        async with aiofiles.open(self.file_path, "r", encoding="utf-8") as file:
            file_size = os.stat(self.file_path).st_size
            content = await file.read(file_size)
        return content

    async def write_file(self, content: str):
        """Writes content to a file"""
        async with aiofiles.open(self.file_path, "w", encoding="utf-8") as file:
            await file.write(content)

    async def read_write_file(self, content: str):
        """Reads and writes content to a file"""
        read_file_task = asyncio.create_task(self.read_file())
        write_file_task = asyncio.create_task(self.write_file(content))
        await asyncio.gather(read_file_task, write_file_task)

if __name__ == '__main__':
    file_handler = FileHandler('test.txt')
    asyncio.run(file_handler.read_write_file('Test content'))
