import sys
sys.path.append("..") # Adds higher directory to python modules path.
from get_values import get_background_information

class CompanyInformation:
    def __init__(self):
        self.name = self.get_name()
        self.company_name = self.get_company_name()
        self.product_name = self.get_product_name()
        self.product_description = self.get_product_description()
        self.desire = self.get_desire()
        self.common_mistake = self.get_common_mistake()
        self.ideal_market_avatar = self.get_ideal_market_avatar()
        self.common_enemy = self.get_common_enemy()
        self.everyday_person = self.get_everyday_person()
        self.well_known_experts = self.get_well_known_experts()
        self.realistic_time_frame = self.get_realistic_time_frame()
        self.common_occurrence = self.get_common_occurrence()
        self.consequence = self.get_consequence()
        self.traditional_way = self.get_traditional_way()
        self.ideal_person = self.get_ideal_person()
        self.painful_attempt = self.get_painful_attempt()
        self.relatable_pain_point = self.get_relatable_pain_point()
        self.commonly_used_vehicles = self.get_commonly_used_vehicles()
        self.solution = self.get_solution()
        self.hack_tool_trick = self.get_hack_tool_trick()
        self.common_achievement = self.get_common_achievement()
        self.perceived_experts = self.get_perceived_experts()
        self.current_year = self.get_current_year()
        self.easy_task = self.get_easy_task()
        self.biggest_objection = self.get_biggest_objection()
        self.display_information()

    def get_name(self):
        if get_background_information(info_name='company_info')[0].strip():
            return get_background_information(info_name='company_info')[0]
        return input("What is your name? ")

    def get_company_name(self):
        if get_background_information(info_name='company_info')[1].strip():
            return get_background_information(info_name='company_info')[1]
        return input("What is the name of your company? ")

    def get_product_name(self):
        if get_background_information(info_name='company_info')[2].strip():
            return get_background_information(info_name='company_info')[2]
        return input("What is the name of your product? ")

    def get_product_description(self):
        if get_background_information(info_name='company_info')[3].strip():
            return get_background_information(info_name='company_info')[3]
        return input("What is the description of your product? ")
    
    def get_desire(self):
       if  get_background_information(info_name='company_info')[4].strip():
            return get_background_information(info_name='company_info')[4]
       return input("What is the desire of your target market? ")

    def get_common_mistake(self):
        if get_background_information(info_name='company_info')[5].strip():
            return get_background_information(info_name='company_info')[5]
        return input("What is the most common mistake made by your target market? ")

    def get_ideal_market_avatar(self):
        if get_background_information(info_name='company_info')[6].strip():
            return get_background_information(info_name='company_info')[6]
        return input("Who is your ideal market avatar? ")

    def get_common_enemy(self):
        if get_background_information(info_name='company_info')[7].strip():
            return get_background_information(info_name='company_info')[7]
        return input("What is the common enemy of your target market? ")

    def get_everyday_person(self):
        if get_background_information(info_name='company_info')[8].strip():
            return get_background_information(info_name='company_info')[8]
        return input("Who is the everyday person in your target market? ")

    def get_well_known_experts(self):
        if get_background_information(info_name='company_info')[9].strip():
            return get_background_information(info_name='company_info')[9]
        return input("Who are the well-known experts in your target market? ")

    def get_realistic_time_frame(self):
        if get_background_information(info_name='company_info')[10].strip():
            return get_background_information(info_name='company_info')[10]
        return input("What is the realistic time frame for achieving success in your target market? ")

    def get_common_occurrence(self):
        if get_background_information(info_name='company_info')[11].strip():
            return get_background_information(info_name='company_info')[11]
        return input("What is the most common occurrence in your target market? ")

    def get_consequence(self):
        if get_background_information(info_name='company_info')[12].strip():
            return get_background_information(info_name='company_info')[12]
        return input("What is the consequence of the common occurrence in your target market? ")

    def get_traditional_way(self):
        if get_background_information(info_name='company_info')[13].strip():
            return get_background_information(info_name='company_info')[13]
        return input("What is the traditional way of achieving success in your target market? ")

    def get_ideal_person(self):
        if get_background_information(info_name='company_info')[14].strip():
            return get_background_information(info_name='company_info')[14]
        return input("Who is the ideal person to achieve success in your target market? ")

    def get_painful_attempt(self):
        if get_background_information(info_name='company_info')[15].strip():
            return get_background_information(info_name='company_info')[15]
        return input("What is the most painful attempt to achieve success in your target market? ")

    def get_relatable_pain_point(self):
        if get_background_information(info_name='company_info')[16].strip():
            return get_background_information(info_name='company_info')[16]
        return input("What is the most relatable pain point in your target market? ")

    def get_commonly_used_vehicles(self):
        if get_background_information(info_name='company_info')[17].strip():
            return get_background_information(info_name='company_info')[17]
        return input("What are the commonly used vehicles to achieve success in your target market? ")

    def get_solution(self):
        if get_background_information(info_name='company_info')[18].strip():
            return get_background_information(info_name='company_info')[18]
        return input("What is the solution to the pain point in your target market? ")

    def get_hack_tool_trick(self):
        if get_background_information(info_name='company_info')[19].strip():
            return get_background_information(info_name='company_info')[19]
        return input("What is the hack, tool, or trick to achieve success in your target market? ")

    def get_common_achievement(self):
        if get_background_information(info_name='company_info')[20].strip():
            return get_background_information(info_name='company_info')[20]
        return input("What is the most common achievement in your target market? ")

    def get_perceived_experts(self):
        if get_background_information(info_name='company_info')[21].strip():
            return get_background_information(info_name='company_info')[21]
        return input("Who are the perceived experts in your target market? ")

    def get_current_year(self):
        if get_background_information(info_name='company_info')[22].strip():
            return get_background_information(info_name='company_info')[22]
        return input("What is the current year? ")

    def get_easy_task(self):
        if get_background_information(info_name='company_info')[23].strip():
            return get_background_information(info_name='company_info')[23]
        return input("What is the easiest task to achieve success in your target market? ")

    def get_biggest_objection(self):
        if get_background_information(info_name='company_info')[24].strip():
            return get_background_information(info_name='company_info')[24]
        return input("What is the biggest objection to achieving success in your target market? ")

    def display_information(self):
        print("Name:", self.name)
        print("Company Name:", self.company_name)
        print("Product Name:", self.product_name)
        print("Product Description:", self.product_description)
        print("Desire:", self.desire)
        print("Common Mistake:", self.common_mistake)
        print("Ideal Market Avatar:", self.ideal_market_avatar)
        print("Common Enemy:", self.common_enemy)
        print("Everyday Person:", self.everyday_person)
        print("Well-Known Experts:", self.well_known_experts)
        print("Realistic Time Frame:", self.realistic_time_frame)
        print("Common Occurrence:", self.common_occurrence)
        print("Consequence:", self.consequence)
        print("Traditional Way:", self.traditional_way)
        print("Ideal Person:", self.ideal_person)
        print("Painful Attempt:", self.painful_attempt)
        print("Relatable Pain Point:", self.relatable_pain_point)
        print("Commonly Used Vehicles:", self.commonly_used_vehicles)
        print("Solution:", self.solution)
        print("Hack/Tool/Trick:", self.hack_tool_trick)
        print("Common Achievement:", self.common_achievement)
        print("Perceived Experts:", self.perceived_experts)
        print("Current Year:", self.current_year)
        print("Easy Task:", self.easy_task)
        print("Biggest Objection:", self.biggest_objection)
        
        
        
        