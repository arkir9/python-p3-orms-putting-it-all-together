import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self,name, breed) :
        self.name = name
        self.breed = breed
        self.id = None
    pass

    @classmethod
    def create_table(self):
        sql = """
                CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY ,
                name TEXT,
                breed TEXT
                )"""
        CURSOR.execute(sql)

    @classmethod
    def drop_table(self):
        sql = """
                DROP TABLE IF EXISTS dogs"""
        CURSOR.execute(sql)

  
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed) VALUES(?,?)"""
       
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()

    @classmethod 
    def create(cls, name, breed ):
        dog = cls(name, breed)
        dog.save()
        db_dog = CURSOR.execute(
            "SELECT * FROM dogs WHERE name=? AND breed=?",
            (dog.name, dog.breed)
        ).fetchone()
        dog.id = db_dog[0]
        return dog

    @classmethod
    def new_from_db(cls, row):
       
            if len(row) >= 3:  # Ensure that row has at least 3 elements
                dog = cls(row[1], row[2])
                dog.id = row[0]
                return dog
    
   
    @classmethod 
    def get_all(cls):
        sql = """SELECT * FROM dogs"""
        all_records = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in all_records]

    @classmethod 
    def find_by_name(cls,name):
        sql = """SELECT * FROM dogs WHERE name = ?"""
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod 
    def find_by_id(cls,id):
        sql = """SELECT * FROM dogs WHERE id = ?"""
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod 
    def find_or_create_by(cls, name, breed):
        # First, try to find a dog with the given name and breed
        existing_dog = cls.find_by_name(name, breed)
        if existing_dog:
            return existing_dog
        else:
            # If no matching dog found, create a new one
            new_dog = cls(name, breed)
            new_dog.save()
            return new_dog
