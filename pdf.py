import asyncio
import hashlib
import logging
import os
import pickle
import re
import threading

import numpy as np
import pandas as pd
import PyPDF2
from txtai.pipeline import Summary, Tokenizer


class PDFSummarizer:
    def __init__(self):
        self.cached_summaries = {}

    def open_pdf_file(self, pdf_file):
        """
        Opens a pdf file.
        """
        try:
            logging.info("Opening pdf file: %s", pdf_file)
            pdf_file = open(pdf_file, "rb")
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
        except Exception as e:
            logging.error("Error opening pdf file: %s", e)
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
        return read_pdf

    def extract_text_from_pdf(self, read_pdf):
        """
        Extracts text from a pdf file and returns a dictionary with keys: page_number, page_content.
        """
        try:
            number_of_pages = read_pdf.getNumPages()
            # get all pages
            pages = {
                page_number: read_pdf.getPage(page_number).extractText()
                for page_number in range(number_of_pages)
            }
        except Exception as e:
            logging.error("Error extracting text from pdf file: %s", e)
        return pages

    def format_pages(self, pages):
        """
        Formats pages by replacing newline characters and multiple spaces with a single space in the page contents.
        """
        try:
            pages = {
                page_number: re.sub(r"\n", " ", page_content)
                for page_number, page_content in pages.items()
            }
            pages = {
                page_number: re.sub(r"\s+", " ", page_content)
                for page_number, page_content in pages.items()
            }
        except Exception as e:
            logging.error("Error formatting pages: %s", e)
        return pages

    def cache_summaries(self, page_content):
        """
        Caches the summaries.
        """
        try:
            cache_key = hashlib.md5(page_content.encode("utf-8")).hexdigest()
            if cache_key in self.cached_summaries:
                return self.cached_summaries[cache_key]
        except Exception as e:
            logging.error("Error caching summaries: %s", e)

    async def tokenize_and_summarize_page(self, page_content):
        """
        Tokenizes and summarizes the page.
        """
        try:
            page_content = re.sub(r"[^\w\s]", "", page_content)
            tokenizer = Tokenizer()
            tokenized_content = tokenizer(str(page_content))
            tokenized_content = [
                token for token in tokenized_content if not re.fullmatch(r"\s+", token)
            ]
            summary_content = pipeline(str(page_content)).strip()

            if summary_content:
                cache_key = hashlib.md5(page_content.encode("utf-8")).hexdigest()
                self.cached_summaries[cache_key] = summary_content

            return summary_content
        except Exception as e:
            logging.error("Error tokenizing and summarizing page: %s", e)

    def create_threads(self, pages):
        """
        Creates threads for each page in the pages dictionary.
        """
        try:
            threads = []
            for page_number, page_content in pages.items():
                thread_obj = threading.Thread(
                    target=self.tokenize_and_summarize_page, args=(page_content,)
                )
                threads.append(thread_obj)
                thread_obj.start()
            for thread in threads:
                thread.join()
        except Exception as e:
            logging.error("Error creating threads: %s", e)

    async def create_async_tasks(self, pages):
        """
        Creates async tasks for each page in
        the pages dictionary.
        """
        try:
            tasks = []
            for page_number, page_content in pages.items():
                task = asyncio.create_task(
                    self.tokenize_and_summarize_page(page_content)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)
        except Exception as e:
            logging.error("Error creating async tasks: %s", e)

    def summarize_pdf(self, pdf_file):
        """
        Summarizes a pdf file.
        """
        try:
            read_pdf = self.open_pdf_file(pdf_file)
            pages = self.extract_text_from_pdf(read_pdf)
            formatted_pages = self.format_pages(pages)

            # Use threads to summarize pages
            self.create_threads(formatted_pages)
            # Use async tasks to summarize pages
            asyncio.run(self.create_async_tasks(formatted_pages))

            # return the cached summaries
            return self.cached_summaries

        except Exception as e:
            logging.error("Error summarizing pdf: %s", e)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )
    logging.info("Starting program")
    if os.path.exists("files/model.pickle"):
        try:
            pipeline = pickle.load(open("model.pickle", "rb"))
        except Exception as e:
            logging.error("Error loading model: %s", e)
            pipeline = Summary("sshleifer/distilbart-cnn-12-6")
    else:
        # create the model
        pipeline = Summary("sshleifer/distilbart-cnn-12-6")
        # save the model to disk
        # filename = "model.pickle"
        # pickle.dump(pipeline, open(filename, "wb"))
    pdf = PDFSummarizer().open_pdf_file(
        "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/auto_coder/files/pdf/comp-pr2022-219.pdf"
    )

    pages = PDFSummarizer().extract_text_from_pdf(pdf)
    formatted_pages = PDFSummarizer().format_pages(pages)
    # Use asyncio to summarize pages
    asyncio.run(PDFSummarizer().create_async_tasks(formatted_pages))

    summaries = PDFSummarizer().cached_summaries
    print(summaries)


# import hashlib
# import logging
# import os
# import pickle
# import re
# import threading
# import logging

# import numpy as np
# import pandas as pd
# import PyPDF2
# from txtai.pipeline import Summary, Tokenizer


# class PDFSummarizer:
#     def __init__(self):
#         self.cached_summaries = {}

#     def open_pdf_file(self, pdf_file):
#         """
#         Opens a pdf file.
#         """
#         try:
#             logging.info("Opening pdf file: %s", pdf_file)
#             pdf_file = open(pdf_file, "rb")
#             read_pdf = PyPDF2.PdfFileReader(pdf_file)
#         except Exception as e:
#             logging.error("Error opening pdf file: %s", e)
#         return read_pdf

#     def extract_text_from_pdf(self, read_pdf):
#         """
#         Extracts text from a pdf file and returns a list of the pages.
#         """
#         try:
#             number_of_pages = read_pdf.getNumPages()
#             # get all pages
#             page_content = np.array([])
#             for page_number in range(number_of_pages):
#                 page = read_pdf.getPage(page_number)
#                 page_content = np.append(page_content, page.extractText())
#         except Exception as e:
#             logging.error("Error extracting text from pdf file: %s", e)
#         return page_content

#     def create_page_dict(self, pdf):
#         """
#         Creates a dictionary with keys: page_number, page_content
#         """
#         try:
#             page_dict = {
#                 page_number: pdf[page_number] for page_number in range(len(pdf))
#             }
#         except Exception as e:
#             logging.error("Error creating page dictionary: %s", e)
#         return page_dict

#     def format_pdf(self, page_dict):
#         """
#         Formats a pdf into a dictionary with keys: page_number, page_content
#         """
#         try:
#             page_dict = {
#                 page_number: re.sub(r"\n", " ", page_content)
#                 for page_number, page_content in page_dict.items()
#             }
#             page_dict = {
#                 page_number: re.sub(r"\s+", " ", page_content)
#                 for page_number, page_content in page_dict.items()
#             }
#         except Exception as e:
#             logging.error("Error formatting pdf: %s", e)
#         return page_dict

#     def cache_summaries(self, page_content):
#         """
#         Caches the summaries.
#         """
#         try:
#             cache_key = hashlib.md5(page_content.encode("utf-8")).hexdigest()
#             if cache_key in self.cached_summaries:
#                 return self.cached_summaries[cache_key]
#         except Exception as e:
#             logging.error("Error caching summaries: %s", e)

#     def tokenize_and_summarize_page(self, page_content):
#         """
#         Tokenizes and summarizes the page.
#         """
#         try:
#             page_content = re.sub(r"[^\w\s]", "", page_content)
#             tokenizer = Tokenizer()
#             tokenized_content = tokenizer(str(page_content))
#             tokenized_content = [
#                 token for token in tokenized_content if not re.fullmatch(r"\s+", token)
#             ]
#             summary_content = pipeline(str(page_content))
#             print(summary_content)

#             if summary_content:
#                 self.cached_summaries[cache_key] = summary_content

#             return summary_content
#         except Exception as e:
#             logging.error("Error tokenizing and summarizing page: %s", e)

#     def create_threads(self, page_dict):
#         """
#         Creates threads.
#         """
#         try:
#             threads = []
#             for page_content in page_dict.values():
#                 thread_obj = threading.Thread(
#                     target=self.summarize_page, args=(str(page_content),)
#                 )
#                 threads.append(thread_obj)
#                 thread_obj.start()
#         except Exception as e:
#             logging.error("Error creating threads: %s", e)
#         return threads

#     def join_threads(self, threads):
#         """
#         Joins threads.
#         """
#         try:
#             for thread_obj in threads:
#                 thread_obj.join()
#             logging.info("Summaries generated")
#         except Exception as e:
#             logging.error("Error joining threads: %s", e)

#     def summarize_page(self, page_content):
#         """
#         Summarizes a page.
#         """
#         try:
#             logging.info("Summarizing page")
#             self.cache_summaries(page_content)
#             return self.tokenize_and_summarize_page(page_content)
#         except Exception as e:
#             logging.error("Error summarizing page: %s", e)

#     def summarize_each_page(self, page_dict):
#         """
#         Summarizes each page.
#         """
#         try:
#             logging.info("Summarizing each page")
#             page_dict = self.format_pdf(page_dict)
#             threads = self.create_threads(page_dict)
#             self.join_threads(threads)
#         except Exception as e:
#             logging.error("Error summarizing each page: %s", e)
#         print(page_dict)
#         return {
#             page_number: self.summarize_page(str(page_content))
#             for page_number, page_content in page_dict.items()
#         }


# if __name__ == "__main__":
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
#     )
#     logging.info("Starting program")
#     if os.path.exists("model.pickle"):
#         pipeline = pickle.load(open("model.pickle", "rb"))
#     else:
#         # create the model
#         pipeline = Summary("sshleifer/distilbart-cnn-12-6")
#         # save the model to disk
#         # filename = "model.pickle"
#         # pickle.dump(pipeline, open(filename, "wb"))
#     pdf = PDFSummarizer().open_pdf_file("comp-pr2022-219.pdf")
#     page_content = PDFSummarizer().extract_text_from_pdf(pdf)
#     page_dict = PDFSummarizer().create_page_dict(page_content)
#     PDFSummarizer().summarize_each_page(page_dict)
