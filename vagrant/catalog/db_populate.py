from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, CatalogItem

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Populate categories
soccer = Category(category='Soccer')
session.add(soccer)
session.commit()

baseball = Category(category='Baseball')
session.add(baseball)
session.commit()

basketball = Category(category='Basketball')
session.add(basketball)
session.commit()

jiu_jitsu = Category(category='Jiu Jitsu')
session.add(jiu_jitsu)
session.commit()

# Populate items
session.add(CatalogItem(item_name='Soccer Ball', description='', category=soccer))
session.commit()

session.add(CatalogItem(item_name='Bat', description='', category=baseball))
session.commit()

session.add(CatalogItem(item_name='Glove', description='', category=baseball))
session.commit()

session.add(CatalogItem(item_name='Gi', description='', category=jiu_jitsu))
session.commit()