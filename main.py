#-*-coding:utf-8-*-
import wx
import uibase
import os
import sqlite3
import pm25

class SqliteData:
    def __init__(self):
        path = os.getcwd() + "./data/city.db"
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()
        self.curs.execute('CREATE TABLE if not exists pm_data(city_py TEXT  UNIQUE, city_zh TEXT)')
        self.conn.commit()
        
    def PushInto(self, city, cityname):
        try:
            self.curs.execute('insert into pm_data values (?,?)', [city, cityname])
            self.conn.commit()
        except sqlite3.IntegrityError:
            #print "same city", city, cityname
            return
        
    def GetCityList(self):
        rs = self.curs.execute("select * from pm_data")
        city_py = []
        city_zh = []
        for r in rs:
            city_py.append(r[0])
            city_zh.append(r[1])
           
        return city_py, city_zh 
        
class MainFrame(uibase.MainFrameBase):
    def __init__(self, parent):
        uibase.MainFrameBase.__init__(self, parent)
        self.sq = SqliteData()
        self.city_py,self.city_zh = self.sq.GetCityList()
       
        for i in  range(0, len(self.city_py)):
            self.m_choiceCity.Append(self.city_zh[i])
            
        self.m_choiceCity.Select(0)
        
    def OnCityChange( self, event ):
        data = pm25.GetPM25(self.city_py[self.m_choiceCity.GetSelection()])
        s = data['area']
        s += str("\n  pm2.5: ")
        s += str(data['pm2_5'])
        s += str("\n  ��������: ")
        s += str(data['quality'])
        s += str('\n')
        self.m_textCtrlInfo.AppendText(s)
        
    def OnClose( self, event ):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    
    frame = MainFrame(None)
    frame.Show()
    
    app.MainLoop()