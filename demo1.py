import wx
import pymysql
import menu



#建一个窗口类MyFrame1继承wx.Frame
class MyFrame1(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,id=wx.ID_ANY, title=u"银行存取款系统", pos=wx.DefaultPosition, size=wx.Size(600,300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.m_panel1 = wx.Panel(self)
        self.m_staticText1 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"请输入银行账号(不超过10位)", (20, 70))
        self.m_staticText2 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"请输入密码：(密码为6位)", (20, 110))

        self.m_staticText3 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"请确认密码",(20,140))
        self.m_staticText4 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"请输入姓名：",(20,170))
        self.t1 = wx.TextCtrl(self.m_panel1, pos=(180, 70), size=(300, 25))
        self.t2 = wx.TextCtrl(self.m_panel1,-1,u'', pos=(180, 110), size=(300, 25), style=wx.TE_PASSWORD)
        self.t3 = wx.TextCtrl(self.m_panel1,-1,u'', pos=(180, 140), size=(300, 25), style=wx.TE_PASSWORD)
        self.t4 = wx.TextCtrl(self.m_panel1,-1,u'', pos=(180, 170), size=(300, 25))


        self.m_button1 = wx.Button(self.m_panel1, wx.ID_ANY, u"确认", (50, 220), size = (70,25))
        self.m_button2 = wx.Button(self.m_panel1, wx.ID_ANY, u"返回登录", (400, 220), size = (70,25))
        self.m_button3 = wx.Button(self.m_panel1, wx.ID_ANY, u"取消", (220, 220), size = (70,25))
        

        # 按钮绑定对话框的弹出
        # 在创建应用程序时，Bind函数可以将按钮的动作与特定的函数绑定，当按钮上有动作时，这个函数就会启动，从而处理响应的事件。
        # 个Button被单击发生了EVT_BUTTON事件
        self.m_button1.Bind(wx.EVT_BUTTON, self.check)

        self.m_button2.Bind(wx.EVT_BUTTON, self.menu)

        self.m_button3.Bind(wx.EVT_BUTTON, self.onExit)
    # “退出”选项的事件处理器
    def onExit(self, event):
        wx.Exit()

    def menu(self,event):
        menu.MyFrame(None).Show()


    def check(self, event):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ydj', db='test', charset='utf8')
        cursor = db.cursor()

        accountname = self.t1.GetValue()
        passwd1 = self.t2.GetValue()
        passwd2 = self.t3.GetValue()
        username=self.t4.GetValue()
        #查询输入的密码是否与用户匹配
        if len(passwd1)!=6 :
            dial = wx.MessageDialog(None, '密码长度不对!', 'error', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID)
            dial.ShowModal()
        elif passwd1!=passwd2:
            dia2 = wx.MessageDialog(None, '两次密码不一样', 'error', wx.YES_NO)  
            dia2.ShowModal()
        elif len(accountname)>10:
            dia3 = wx.MessageDialog(None, '银行账户名长度错误', 'error', wx.YES_NO)  
            dia3.ShowModal()

        else:            
            userinfoes = "SELECT * FROM userinfoes WHERE account='%s'"%accountname #查询该用户是否存在  
            j = cursor.execute(userinfoes) #满足此条件的数据条数  
            if j==1:  
                dia3 = wx.MessageDialog(None, '该账户已存在', 'error', wx.YES_NO)  
                dia3.ShowModal() 
            else:
                sql = "INSERT INTO userinfoes(account,password,pname,balance)VALUES('%s','%s','%s','%f')" % (accountname,passwd1,username,0)  
                try: 
                    cursor.execute(sql)
                    db.commit()  
                    dia4 = wx.MessageDialog(None, '注册成功', '结果', wx.YES_NO)  
                    dia4.ShowModal()   
                except: 
                    db.rollback()


 




        


