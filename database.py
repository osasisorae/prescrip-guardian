import chromadb
import os


class Vectorizer:
    def __init__(self, user_id, data_type) -> None:
        self.working_dir = os.getcwd()
        self.unique_username = f"first_admin"
        self.client = chromadb.PersistentClient(path=f"{self.working_dir}/{data_type}/{self.unique_username}")
        self.user_id = user_id

    def save_first_admin(self, data: tuple) -> None:
        """
        Simple method to save the first admin to local.
        Data is vectorized and stored. 
        """
        first_name, last_name, username, date_ = data
        collection = self.client.get_or_create_collection(name=self.unique_username)
        
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
        collection = self.client.get_or_create_collection(name=self.unique_username)
        results = collection.query(
            query_texts=['This is the first admin'],
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