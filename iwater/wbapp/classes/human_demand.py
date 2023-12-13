from wbapp.models.census import CensusDatum


class HumanDemand:

    CONSUMPTION_FACTOR = 27.375/10000

    def __init__(self, male, female):
        self.male = male
        self.female = female
    
    def json(self, CONSUMPTION_FACTOR = 27.375/10000):
        return {
            "male": self.male,
            "female" : self.female,
            "consumption" : (self.male + self.female) * CONSUMPTION_FACTOR
        }

    def total_population(self, village_id):
        census = CensusDatum.get_by_village(village_id=village_id)
        self.male = census['male_population']
        self.female = census['female_population']
        return self.male + self.female
    
