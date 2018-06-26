import wx #导入wxpyhton，pyhton自带的GUI库
import pymysql #用于操作数据库
import demo
import demo1





class MyFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,id=wx.ID_ANY, title=u"银行存取款系统", pos=wx.DefaultPosition, size=wx.Size(300,250),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Center()
        self.m_panel1 = wx.Panel(self)
        self.m_staticText1 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"账  户：", (20, 70))
        self.m_staticText2 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"密  码：", (20, 110))

        self.m_staticText3 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"欢迎使用银行存取款系统",(80,20))
        self.t1 = wx.TextCtrl(self.m_panel1, pos=(90, 70), size=(120, 25))
        self.t2 = wx.TextCtrl(self.m_panel1,-1,u'', pos=(90, 110), size=(120, 25), style=wx.TE_PASSWORD)

        self.m_button1 = wx.Button(self.m_panel1, wx.ID_ANY, u"登  录", (50, 160), size = (70,25))
        self.m_button2 = wx.Button(self.m_panel1, wx.ID_ANY, u"注册", (160, 160), size = (70,25))

        self.m_button1.Bind(wx.EVT_BUTTON, self.check)
        self.m_button2.Bind(wx.EVT_BUTTON, self.eroll)

    def check(self, event):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ydj', db='test', charset='utf8')
        cursor = db.cursor()

        accountname = self.t1.GetValue()
        passwd = self.t2.GetValue()
        #查询输入的密码是否与用户匹配

        sql = "SELECT * FROM userinfoes WHERE account='%s' and password='%s'"%(accountname,passwd)

        j = cursor.execute(sql) #满足该条件的数据条数 
        if j ==1:     
            demo.MyFrame1(None).Show()
            cursor.close()
            db.close()
        else:
            dial = wx.MessageDialog(None, '账户或密码错误!', '结果', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID)
            dial.ShowModal()
    def eroll(self,event):
        demo1.MyFrame1(None).Show()
