import pandas as pd
import json
def readData(fileName):
    df = pd.read_table(fileName)
    return df

#Table 1: product ID, string of tag ID
#Table 2: user id ,prodcut id, rating

class TriGraph():
    def __init__(self, df_tag=None, df_pref=None, dict=None, userNum=None, userCount=None, 
                prefCount=None, prodUCount=None, prodDCount=None, tagUCount=None, tagDCount=None, NodeList=None):
        if df_tag != None and df_pref != None: 
            self.dict = {}
            self.userNum = 0
            self.userCount = -1
            self.prefCount = -1
            self.prodUCount = -1
            self.prodDCount = -1
            self.tagUCount = -1
            self.tagDCount = -1
        
            self.users = {}
            self.prefs = {}
            self.products_U = {}
            self.products_D = {}
            self.tags_U = {}
            self.tags_D = {}
            self.NodeList = {}
            self.buildGraghFromProduct(df_tag)
            self.buildGraghFromUser(df_pref)
        else:
            self.dict = None
            self.userNum = userNum
            self.userCount = userCount
            self.prefCount = prefCount
            self.prodUCount = prodUCount
            self.prodDCount = prodDCount
            self.tagUCount = tagUCount
            self.tagDCount = tagDCount
        
            self.users = None
            self.prefs = None
            self.products_U = None
            self.products_D = None
            self.tags_U = None
            self.tags_D = None
            self.NodeList = NodeList
    
    def buildGraghFromUser(self, df):
        prev = ""
        prev_id = -1
        products = []
        count = 0
        for _, row in df.iterrows():
            rating = row['rating']
            product = row['product']
            if count == 0: 
                prev = row['user']
                prev_id = self.hashID('user', row['user'])
            count+=1
            #print(row['user'])
            #print('P', prev)
            if row['user'] != prev:
                #construct the graph by prev user
                #print(prev)
                products.sort(key = lambda x: x[1], reverse=True)
                self.dict[prev_id] = []
                if products[0] != products[-1]: 
                    for i in range(len(products)-1):
                        for j in range(i+1, len(products)):
                            a = products[i][0]
                            b = products[j][0]
                            if products[i][1] > products[j][1]: 
                                pref = self.compare(a,b)
                                self.dict[prev_id].append(pref)
                                if pref not in self.dict:
                                    self.dict[pref] = [prev_id]
                                else: self.dict[pref].append(prev_id)
                    
                #Start new user
                prev = row['user']
                prev_id = self.hashID('user', row['user'])
                products = [(product, rating)]
            else: 
                products.append((product, rating))
        
        products.sort(key = lambda x: x[1], reverse=True)
        self.dict[prev_id] = []
        if products[0] != products[-1]:
            for i in range(len(products)-1):
                for j in range(i+1, len(products)):
                    a = products[i][0]
                    b = products[j][0]
                    if a > b:
                        pref = self.compare(a,b)
                        self.dict[prev_id].append(pref)
                        if pref not in self.dict:
                            self.dict[pref] = [prev_id]
                        else: self.dict[pref].append(prev_id)
    
    def buildGraghFromProduct(self, df):
        products = []
        for _, row in df.iterrows():
            product = row['product']
            products.append(product)
            product_id_d = self.hashID('product', product, 'D')
            product_id_u = self.hashID('product', product, 'U')
            self.dict[product_id_d] = []
            self.dict[product_id_u] = []
            tags = row['tag'].split(',')
            tagsD = [self.hashID('tag', tag, 'D') for tag in tags]
            tagsU = [self.hashID('tag', tag, 'U') for tag in tags]
            
            for tag_id in tagsD:
                self.dict[product_id_d].append(tag_id)
                if tag_id in self.dict:
                    self.dict[tag_id].append(product_id_d)
                else:
                    self.dict[tag_id] = [product_id_d] 
                
            for tag_id in tagsU:
                self.dict[product_id_u].append(tag_id)
                if tag_id in self.dict:
                    self.dict[tag_id].append(product_id_u)
                else:
                    self.dict[tag_id] = [product_id_u] 
                
        for i in range(len(products)-1):
            for j in range(i+1, len(products)):
                a = products[i]
                b = products[j]
                pref = self.compare(a,b)
                product_id_d = self.hashID('product', a, 'D')
                product_id_u = self.hashID('product', b, 'U')
                self.dict[product_id_d].append(pref)
                self.dict[product_id_u].append(pref)
                self.dict[pref] = [product_id_d, product_id_u]

                pref = self.compare(b,a)
                product_id_d = self.hashID('product', b, 'D')
                product_id_u = self.hashID('product', a, 'U')
                self.dict[product_id_d].append(pref)
                self.dict[product_id_u].append(pref)
                self.dict[pref] = [product_id_d, product_id_u]
                              
    def hashID(self, type, id, desire = None):

        if type == 'user':
            if id not in self.users:
                self.userCount+=1
                self.users[id] = 'user_' + str(self.userCount)
            return self.users[id]
        
        if type == 'product':
            if desire == 'D':
                if id not in self.products_D:
                    self.prodDCount+=1
                    self.products_D[id] = 'product_D_' + str(self.prodDCount)
                return self.products_D[id]
            if desire == 'U':
                if id not in self.products_U:
                    self.prodUCount+=1
                    self.products_U[id] = 'product_U_' + str(self.prodUCount)
                return self.products_U[id]
        
        if type == 'tag':
            if desire == 'D':
                if id not in self.tags_D:
                    self.tagDCount+=1
                    self.tags_D[id] = 'tags_D_' + str(self.tagDCount)
                return self.tags_D[id]
            if desire == 'U':
                if id not in self.tags_U:
                    self.tagUCount+=1
                    self.tags_U[id] = 'tags_U_' + str(self.tagUCount)
                return self.tags_U[id]
        
        return    
        
    def compare(self, a, b):
        id = str(a)+'_'+str(b)
        if id not in self.prefs:
            self.prefCount+=1
            self.prefs[str(a)+'_'+str(b)] = 'pref_'+ str(a) + '_' + str(b) + '_' + str(self.prefCount)
        return self.prefs[id]

    def buildMapping(self):
        df = pd.DataFrame(columns=['orginal id', 'new id'])
        self.appendTodf(df, self.users)
        self.appendTodf(df, self.prefs)
        self.appendTodf(df, self.products_D)
        self.appendTodf(df, self.products_U)
        self.appendTodf(df, self.tags_D)
        self.appendTodf(df, self.tags_U)
        return df

    def appendTodf(self, df, Dict):
        for key in Dict:
            df.loc[-1] = [key, Dict[key]]
            df.index+=1
        
    def buildNodeList(self, remove = True):
        self.userNum = self.userCount+1
        for key in self.dict:
            if remove and not self.dict[key]:
                self.userNum -=1
                continue
            self.NodeList[key] = {}
            self.NodeList[key]['next_user'] = []
            self.NodeList[key]['next_pref'] = []
            self.NodeList[key]['next_prod'] = []
            self.NodeList[key]['next_tags'] = []
            self.NodeList[key]['Type'] = key.split('_')[0][:4]  
            self.NodeList[key]['Id'] = key
            for item in self.dict[key]:
                s = 'next_' + item[:4]
                self.NodeList[key][s].append(item)   
    
    def getCount(self, remove = True):
        if not remove:
            return [self.userCount+1, self.prefCount+1, self.prodUCount+1, self.prodDCount+1, self.tagUCount+1, self.tagDCount+1]
        return [self.userNum, self.prefCount+1, self.prodUCount+1, self.prodDCount+1, self.tagUCount+1, self.tagDCount+1]

    