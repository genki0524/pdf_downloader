import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import urllib.request as rq
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Pdf_batch_acquisition:
    def __init__(self,url,storage_directory):
        self.user = ""
        self.password = ""
        self.url = url
        self.storage_directory = storage_directory

    def set_user_and_password(self,user,password):
        self.user = user
        self.password = password
    
    def set_basic_auth(uri,user,passwd):
        pass_mgr = rq.HTTPPasswordMgrWithDefaultRealm()
        pass_mgr.add_password(realm=None,uri=uri,user=user,passwd=passwd)
        auth_header = rq.HTTPBasicAuthHandler(pass_mgr)
        opener = rq.build_opener(auth_header)
        rq.install_opener(opener)
    
    def replace_invalid_chars(self,filename):
        invalid_chars = {'\\', '/', ':', '*', '?', '"', '<', '>', '|', ' '}
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def set_pdf_list_and_save_path_list(self):
        if (self.user != "") and (self.password != ""): 
            res = requests.get(self.url,auth=(self.user,self.password))
        else : res = requests.get(self.url)

        soup = BeautifulSoup(res.content.decode("utf-8", "ignore"),"html.parser")
        tags = soup.select("a[href]")
        
        link_list = [tag.get("href") for tag in tags]

        pdf_list = [link for link in link_list if link.endswith("pdf")]

        abs_pdf_list = [urljoin(self.url,pdf) for pdf in pdf_list]

        filename_list = []
        
        for tag in tags:
            if tag.get("href").endswith("pdf"):
                filename = self.replace_invalid_chars(tag.text)
                filename_list.append(filename + ".pdf")
        
        savepath_list = []
        for filename in filename_list:
            savepath_list.append(os.path.join(self.storage_directory,filename))
        
        return abs_pdf_list,savepath_list
    

    def set_basic_auth(self,uri,user,passwd):
        pass_mgr = rq.HTTPPasswordMgrWithDefaultRealm()
        pass_mgr.add_password(realm=None,uri=uri,user=user,passwd=passwd)
        auth_header = rq.HTTPBasicAuthHandler(pass_mgr)
        opener = rq.build_opener(auth_header)
        rq.install_opener(opener)

    def download_pdf(self):
        abs_pdf_list, savepath_list = self.set_pdf_list_and_save_path_list()

        if (self.user != "") and (self.password != ""): 
            cnt = 0
            for (pdf_link,save_path) in zip(abs_pdf_list,savepath_list):
                cnt +=1
                self.set_basic_auth(pdf_link,self.user,self.password)
                rq.urlretrieve(pdf_link,save_path)
                print("{0}".format(cnt)+"番目終了")
                time.sleep(5)
        else:
            cnt = 0
            for (pdf_link,save_path) in zip(abs_pdf_list,savepath_list):
                cnt +=1
                rq.urlretrieve(pdf_link,save_path)
                print("{0}".format(cnt)+"番目終了")
                time.sleep(5)



