from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

##############################################################

URL_LOGIN = 'https://www.immortalnight.com/authenticate.php'
payload = {
    'username' : 'webscraper',
    'password' : '.d4v1sEmm4'
}

URL_HAPM = 'http://www.immortalnight.com/stocks.php?action=hist&s=HAPM'
URL_LTHD = 'http://www.immortalnight.com/stocks.php?action=hist&s=LHDC'
URL_LALT = 'http://www.immortalnight.com/stocks.php?action=hist&s=LLTX'
URL_THCM = 'http://www.immortalnight.com/stocks.php?action=hist&s=THCF'
URL_PWDI = 'http://www.immortalnight.com/stocks.php?action=hist&s=PWDI'
URL_BDAL = 'http://www.immortalnight.com/stocks.php?action=hist&s=BDAL'
URL_GGHG = 'http://www.immortalnight.com/stocks.php?action=hist&s=GGHG'
URL_SBHI = 'http://www.immortalnight.com/stocks.php?action=hist&s=SBHI'
URL_HSEM = 'http://www.immortalnight.com/stocks.php?action=hist&s=HSEM'



class Stock_URL:
    def GetData(self, url):
        with requests.Session() as session:
            post = session.post(URL_LOGIN, data=payload)
            URL = session.get(url)
    
        soup = BeautifulSoup(URL.text, 'html.parser')
        data_tables = soup.find('table', attrs={'class':'table'})
        rows = data_tables.find_all('tr')
        col_data = [None] * (len(rows)-2)
        for j in range(len(rows)-2):
            col_data[j] = rows[(len(rows)-1)-(j)].find_all('td')[2].text.translate({ord(c): None for c in '!@#$'})
            col_data[j] = float(col_data[j])
        return(col_data)            


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.hold_graph = tk.IntVar()
        self.fig_num = 1
        self.bought_for = tk.DoubleVar()
        root.geometry("760x120+800+20")
        self.pack()
        self.create_widgets()


    def create_widgets(self):

        #####################GRAPH BUTTONS########################

        self.HAPM_btn = tk.Button(self, text="HAPM", bg="#D32F2F", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_HAPM))
        self.LTHD_btn = tk.Button(self, text="LTHD", bg="#C2185B", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_LTHD))
        self.LALT_btn = tk.Button(self, text="LALT", bg="#7B1FA2", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_LALT))
        self.THCM_btn = tk.Button(self, text="THCM", bg="#512DA8", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_THCM))
        self.PWDI_btn = tk.Button(self, text="PWDI", bg="#303F9F", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_PWDI))
        self.BDAL_btn = tk.Button(self, text="BDAL", bg="#1976D2", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_BDAL))
        self.GGHG_btn = tk.Button(self, text="GGHG", bg="#0288D1", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_GGHG))
        self.SBHI_btn = tk.Button(self, text="SBHI", bg="#0097A7", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_SBHI))
        self.HSEM_btn = tk.Button(self, text="HSEM", bg="#00796B", fg="white", height=40, width=10, command=lambda:self.GraphData(URL_HSEM))
        
        ########################################################


        self.boughtfor_ent = tk.Entry(self, textvariable=self.bought_for)
        self.price_lbl = tk.Label(self, text="(Optional) Enter Share Price Bought At")
        self.holdgraph_cbtn = tk.Checkbutton(self, text="Hold Graphs", variable=self.hold_graph)
        self.quit = tk.Button(self, text="QUIT", fg="red", command=lambda:self.End())


        ####################PACK########################

        self.holdgraph_cbtn.pack(side=tk.TOP)
        self.price_lbl.pack(side=tk.TOP)
        self.boughtfor_ent.pack(side=tk.TOP)
        self.HAPM_btn.pack(side=tk.LEFT)
        self.LTHD_btn.pack(side=tk.LEFT)
        self.LALT_btn.pack(side=tk.LEFT)
        self.THCM_btn.pack(side=tk.LEFT)
        self.PWDI_btn.pack(side=tk.LEFT)
        self.BDAL_btn.pack(side=tk.LEFT)
        self.GGHG_btn.pack(side=tk.LEFT)
        self.SBHI_btn.pack(side=tk.LEFT)
        self.HSEM_btn.pack(side=tk.LEFT)
        self.quit.pack(side=tk.BOTTOM)

        #################################################


    def SwitchStatement(self, argument):
        switch_urls = {
            URL_HAPM: "Hemoglobin Artificial Plasma Makers",
            URL_LTHD: "Let Them Hang Dry Cleaners",
            URL_LALT: "Leather And Lace Textiles",
            URL_THCM: "Top Hat Coffin Makers",
            URL_PWDI: "Pearly Whites Dental Implants",
            URL_BDAL: "Bleed em Dry Attorneys at Law",
            URL_GGHG: "Ghastly Ghouls Halloween Gear",
            URL_SBHI: "Stone Butchers Headstones Inc",
            URL_HSEM: "Holy Silver Explosive Manufacturers"
        }
        return(switch_urls.get(argument, "Oops"))

    def GraphData(self, url):
        if(self.hold_graph.get()==0):
            for i in range(self.fig_num):
                plt.close(i+1)
            self.fig_num = 1
        else:
            self.fig_num += 1

        plt.figure(self.fig_num)
        URL = Stock_URL()
        x = list(range(0, 49))
        y = URL.GetData(url)
        fit = np.polyfit(x,y,1)
        fit_fn = np.poly1d(fit)

        if(self.bought_for.get() > 0.0):
            bought_price = [self.bought_for.get()]*49
            plt.plot(x, y, 'r', x, fit_fn(x), '--k', x, bought_price, '--g')
        else:
            plt.plot(x, y, 'r', x, fit_fn(x), '--k')

        plt.ylabel('PRICE')
        plt.xlabel('TIME')
        plt.title(self.SwitchStatement(url))

        plt.show()

    def End(self):
        for i in range(self.fig_num):
            plt.close(i+1)
        self.master.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
