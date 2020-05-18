from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()


# TODO: Add Testing as Column and fetch the corresponding data
class Country(Base):
    __tablename__ = 'country'

    country = Column(String, primary_key=True)
    total_cases = Column(Integer)
    new_cases = Column(Integer)
    total_deaths = Column(Integer)
    new_deaths = Column(Integer)
    population = Column(Integer)

    def __repr__(self):
        return f"<Country(country='{self.country}', total_cases='{self.total_cases}', new_cases='{self.new_cases}', total_deaths='{self.total_deaths}', new_deaths='{self.new_deaths}', population='{self.population}')>"
