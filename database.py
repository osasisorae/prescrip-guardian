import chromadb
import os


class Vectorizer:
    def __init__(self, user_id: str, folder: str) -> None:
        self.working_dir = os.getcwd()
        self.user_id = user_id
        self.folder = folder

    def save_first_admin(self, data: tuple) -> None:
        """
        Simple method to save the first admin to local.
        Data is vectorized and stored. 
        """
        client = chromadb.PersistentClient(path=f"{self.working_dir}/{self.folder}")
        
        first_name, last_name, username, date_ = data
        collection = client.get_or_create_collection(name="first_admin")
        
        collection.add(
            documents=["This is the first admin",],
            metadatas=[
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "date": date_
                 },
            ],
            ids=[str(self.user_id),]
        )
        print('success!!')
        return 0

    def get_first_admin(self):
        """
        This method checks for the first admin
        """
        client = chromadb.PersistentClient(path=f"{self.working_dir}/{self.folder}")
        
        collection = client.get_or_create_collection(name="first_admin")
        results = collection.query(
            query_texts=['This is the first admin'],
            n_results=1
            )
        empty = {'ids': [[]], 'distances': [[]], 'metadatas': [[]], 'embeddings': None, 'documents': [[]]}
        # print(results)
        if results == empty:
            print('No admin found, proceed to store first admin')
            return 0, "None"
        else:
            print('Admin already exists')
            return 2, results['ids'][0][0] # Return the first admin
        
    def save_admins(self, date_):
        """
        Simple method to save the consequent admins to local.
        Data is vectorized and stored. 
        """
        client = chromadb.PersistentClient(path=f"{self.working_dir}/{self.folder}")
        
        collection = client.get_or_create_collection(name="admins")
        
        collection.add(
            documents=[f"Veirfified admin {self.user_id}.",],
            metadatas=[
                {
                    "date": date_
                 },
            ],
            ids=[str(self.user_id),]
        )
        print('success!!')
        return 0
    
    def save_doctor(self, date_):
        """
        Simple method to save the consequent doctors to local.
        Data is vectorized and stored. 
        """
        client = chromadb.PersistentClient(path=f"{self.working_dir}/{self.folder}")
        
        collection = client.get_or_create_collection(name="doctors")
        
        collection.add(
            documents=[f"Veirfified Doctor {self.user_id}.",],
            metadatas=[
                {
                    "date": date_
                 },
            ],
            ids=[str(self.user_id),]
        )
        print('success!!')
        return 0
    
    def get_admin(self):
        
        client = chromadb.PersistentClient(path=f"{self.working_dir}/{self.folder}")
        
        collection = client.get_or_create_collection(name="admins")
        results = collection.query(
            query_texts=[f"Veirfified admin {self.user_id}."],
            n_results=1
            )
        empty = {'ids': [[]], 'distances': [[]], 'metadatas': [[]], 'embeddings': None, 'documents': [[]]}
        print(results)
        if results == empty:
            print('No admin found, proceed to store first admin')
            return 0, "None"
        else:
            print('Admin already exists')
            return 2, results['ids'][0][0] # Return the first admin
        
    def get_admins(self):
        client = chromadb.PersistentClient(path=f"{self.working_dir}/{self.folder}")
        collection = client.get_or_create_collection(name="admins")
        results = collection.query(
            query_texts=[f"Veirfified admin {self.user_id}."],
            n_results=5
            )
        print(results)
        
    def is_user_admin(self):
        client = chromadb.PersistentClient(path=f"{self.working_dir}/{self.folder}")
        collection = client.get_or_create_collection(name="admins")
        results = collection.get(
            ids=[str(self.user_id),]
            )
        empty = {'ids': [[]], 'distances': [[]], 'metadatas': [[]], 'embeddings': None, 'documents': [[]]}
        
        if results != empty:
            return 1
        else:
            return 0