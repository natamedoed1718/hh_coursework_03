from src.utils import load_all_data
from src.db_creator import DBCreator

EMPLOYERS = [1455, 78638, 3776, 80, 3529, 2180, 15478, 1057, 39305, 2381]

if __name__ == "__main__":
    creator = DBCreator()
    creator.create_database()
    creator.create_tables()
    load_all_data(creator, EMPLOYERS)
    user_interaction()


