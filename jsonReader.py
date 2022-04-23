


import os ,json




 
class  configHandler():
    def __init__(self):
        self.current_dir = os.path.abspath(os.path.dirname(__file__)) 
        self.accounts_file_name = os.path.join(self.current_dir,'accounts.json' ) 
        self.data = self.readHeadlineFile(self.accounts_file_name)['accounts']
    
    def readHeadlineFile(self,file_name): 
        with open (file_name)as file:  
            return json.load(file)
      
     
      
    def updateDataFile(self, new_data):
        with open(self.old_listing_file_name, 'w') as f:
            json.dump({"old_listing":new_data}, f, ensure_ascii=True, indent=4)

    def getUserPassDict(self):
        container  = {}
        for x in self.data:
            container[x['username']] = x['password']
        
     
        return container
        
    def getUserId(self,username):
        for x in self.data:
            if x['username'] == username:
                return x['user_id']



 
if __name__ == '__main__':
    config = configHandler() 
    difference = config.getUserPassDict() 
    print((difference))
    # print(config.getFilters())
    
    pass