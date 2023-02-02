import sys
sys.path.append("..") # Adds higher directory to python modules path.
from get_values import get_background_information

class CustomerInformation:
    def __init__(self):
        self.desires = self.get_desires()
        self.target_audience = self.get_target_audience()
        self.pains = self.get_pains()
        self.target_demographic = self.get_target_demographic()
        self.display_information()

    def get_desires(self):
        if get_background_information(info_name='target_audience')[0]:
            return get_background_information(info_name='target_audience')[0].strip()
        return input("What are the desires of your target audience? ")

    def get_target_audience(self):
        if get_background_information(info_name='target_audience')[1]:
            return get_background_information(info_name='target_audience')[1].strip()
        return input("What is the target audience of your product? ")

    def get_pains(self):
        if get_background_information(info_name='target_audience')[2]:
            return get_background_information(info_name='target_audience')[2].strip()
        return input("What are the pains of your target audience? ")

    def get_target_demographic(self):
        if get_background_information(info_name='target_audience')[3]:
            return get_background_information(info_name='target_audience')[3].strip()
        return input("What is the target demographic of your target audience? ")

    def display_information(self):
        print("Desires:", self.desires)
        print("Target Audience:", self.target_audience)
        print("Pains:", self.pains)
        print("Target Demographic:", self.target_demographic)