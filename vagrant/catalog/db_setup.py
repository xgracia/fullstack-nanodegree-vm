from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String(75), nullable=False)

    # print out cateogry name as a str
    def __str__(self):
        return self.category

    # used for JSON serialization
    @property
    def serialize(self):
        return {
            'id': self.id,
            'category': self.category
        }


class CatalogItem(Base):
    __tablename__ = 'catalog_items'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(75), nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)

    # print out cateogry name as a str
    def __str__(self):
        return self.item_name

    # used for JSON serialization
    @property
    def serialize(self):
        return {
            'id': self.id,
            'item_name': self.item_name,
            'description': self.description,
            'category_id': self.category_id,
            'category': self.category.category
        }

engine = create_engine('postgresql:///catalog')
Base.metadata.create_all(engine)
