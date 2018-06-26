import wx
import pymysql


# 用户操作界面
#建一个窗口类MyFrame1继承wx.Frame
class MyFrame1(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,id=wx.ID_ANY, title=u"银行存取款系统", pos=wx.DefaultPosition, size=wx.Size(600,300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Center() #居中显示

        # 小构件，如按钮，文本框等被放置在面板窗口。 wx.Panel类通常是被放在一个wxFrame对象中。这个类也继承自wxWindow类。
        self.m_panel1 = wx.Panel(self)
        # 标签，一行或多行的只读文本，Wx.StaticText(parent, id, label, position, size, style)
     



        self.m_button1 = wx.Button(self.m_panel1, wx.ID_ANY, u"查询余额", (130, 90), wx.DefaultSize,
                                   style=wx.BORDER_MASK)
        self.m_button2 = wx.Button(self.m_panel1, wx.ID_ANY, u"取款", (250, 90), wx.DefaultSize,
                                   style=wx.BORDER_MASK)
        self.m_button3 = wx.Button(self.m_panel1, wx.ID_ANY, u"存款", (370, 90), wx.DefaultSize,
                                   style=wx.BORDER_MASK)

        self.m_button4 = wx.Button(self.m_panel1, wx.ID_ANY, u"退卡", (250, 160), wx.DefaultSize,
                                   style=wx.BORDER_MASK)

                                   


        # 按钮绑定对话框的弹出
        # 在创建应用程序时，Bind函数可以将按钮的动作与特定的函数绑定，当按钮上有动作时，这个函数就会启动，从而处理响应的事件。
        # 个Button被单击发生了EVT_BUTTON事件
        self.m_button1.Bind(wx.EVT_BUTTON, MyDialog1(None).OnClick)
        self.m_button2.Bind(wx.EVT_BUTTON, MyDialog2(None).OnClick)
        self.m_button3.Bind(wx.EVT_BUTTON, MyDialog3(None).OnClick)

        self.m_button4.Bind(wx.EVT_BUTTON, self.onExit)
    # “退出”选项的事件处理器
    def onExit(self, event):
        wx.Exit()

# 查询余额
class MyDialog1(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"查询余额", pos=wx.DefaultPosition, size=wx.Size(500, 400),
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.Center()
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')

        wx.StaticText(self.panel, -1, "银行账户名：", (20, 20))
        self.t1 = wx.TextCtrl(self.panel, pos=(90, 20), size=(120, 25))

        wx.StaticText(self.panel, -1, "密码：", (20, 70))
        self.t2 = wx.TextCtrl(self.panel, pos=(90, 70), size=(120, 25) ,style=wx.TE_PASSWORD)

        wx.StaticText(self.panel, wx.ID_ANY, "账号", (20, 120))
        wx.StaticText(self.panel, wx.ID_ANY, "用户名", (140, 120))
        wx.StaticText(self.panel, wx.ID_ANY, "余额", (260, 120))

    def OnClick(self, event):
        dialog = MyDialog1(None)
        btn = wx.Button(parent=dialog.panel, label="查询", pos=(240, 20), size=(70, 25))
        btn.Bind(wx.EVT_BUTTON, dialog.find)
        dialog.ShowModal()

    def find(self, event):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ydj', db='test', charset='utf8')
        cursor = db.cursor()
        accountname = self.t1.GetValue()
        passwd = self.t2.GetValue()
        try:
            sql = "SELECT * FROM userinfoes WHERE account='%s' and password='%s'"%(accountname,passwd)
            j=cursor.execute(sql)
            rs = cursor.fetchall()
            if j!=1:
                dia4 = wx.MessageDialog(None, '账户名或密码错误', 'error', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
                dia4.ShowModal()  # 显示对话框
            else:
                h = 120
                for i in rs:
                    h = h + 40
                    u_account=i[0]
                    u_name=i[2]
                    u_balance=i[3]
           
                    wx.StaticText(self.panel, wx.ID_ANY, str(u_account), (20, h))
                    wx.StaticText(self.panel, wx.ID_ANY, str(u_name), (140, h))
                    wx.StaticText(self.panel, wx.ID_ANY, str(u_balance), (260, h))
        except:
            db.rollback()
        finally:
            cursor.close()
            db.close()

# 取款
class MyDialog2(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"取款界面", pos=wx.DefaultPosition, size=wx.Size(400, 400),
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.Center()
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')

        wx.StaticText(self.panel, -1, "请输入银行账号：", (20, 20))
        self.t1 = wx.TextCtrl(self.panel, pos=(140, 20), size=(120, 25))

        wx.StaticText(self.panel, -1, "请输入密码", (20, 70))
        self.t2 = wx.TextCtrl(self.panel, pos=(140,70), size=(120, 25), style=wx.TE_PASSWORD)

        wx.StaticText(self.panel, -1, "请输入金额：", (20, 120))
        self.t3 = wx.TextCtrl(self.panel, pos=(140,120), size=(120, 25))


        wx.StaticText(self.panel, wx.ID_ANY, "账号", (20, 160))
        wx.StaticText(self.panel, wx.ID_ANY, "账户名", (140, 160))
        wx.StaticText(self.panel, wx.ID_ANY, "取款金额", (260, 160))

    def OnClick(self, e):
        dialog22 = MyDialog2(None)
        btn = wx.Button(parent=dialog22.panel, label="确定", pos=(140, 280), size=(70, 25))
        btn.Bind(wx.EVT_BUTTON, dialog22.withdraw)
        dialog22.ShowModal()

    def withdraw(self, e):
        M_balance=0
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ydj', db='test', charset='utf8')
        cursor = db.cursor()
        accountname = self.t1.GetValue()
        passwd = self.t2.GetValue() 
        money = self.t3.GetValue()
        M_balance = float(money)
        if M_balance%100!=0:
                        
            dial = wx.MessageDialog(None, '请输入100的倍数', 'error', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
            dial.ShowModal()  # 显示对话框
        else:
            sql = "SELECT * FROM userinfoes WHERE account='%s' and password='%s'"%(accountname,passwd)
            j = cursor.execute(sql)
            k = cursor.fetchall()
            if j!=1:
                dia4 = wx.MessageDialog(None, '账户名或密码错误请重新输入', 'error', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
                dia4.ShowModal()  # 显示对话框
            else:  
                for i in k:
                    u_balance=i[3]              
                if u_balance-M_balance >= 0:  
                    sq1 = "UPDATE userinfoes SET balance='%0.2f' WHERE account='%s'"%(u_balance-M_balance,accountname)  
                    try:  
                        cursor.execute(sq1)  
                        db.commit()  
                        dial = wx.MessageDialog(None, '成功取款', '结果', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
                        dial.ShowModal()  # 显示对话框
                        sql= "SELECT * FROM userinfoes WHERE account='%s'"%(accountname)
                        cursor.execute(sql)  
                        k = cursor.fetchall()
                        h=180
                        for i in k:

                            u_name=i[2]
                            u_account=i[0]
                            wx.StaticText(self.panel, wx.ID_ANY, str(u_account), (20, h)) 
                            wx.StaticText(self.panel, wx.ID_ANY, str(u_name), (140, h))
                            wx.StaticText(self.panel, wx.ID_ANY, str(money), (260, h))       
                    except:  
                        db.rollback()
                    finally:
                        cursor.close()
                        db.close()
                else:  
                    dia2 = wx.MessageDialog(None, '你的余额不够', '结果', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
                    dia2.ShowModal()  # 显示对话框
# 存款
class MyDialog3(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"存款界面", pos=wx.DefaultPosition, size=wx.Size(400, 400),
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.Center()
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')

        wx.StaticText(self.panel, -1, "请输入银行账号：", (20, 20))
        self.t1 = wx.TextCtrl(self.panel, pos=(140, 20), size=(120, 25))

        wx.StaticText(self.panel, -1, "请输入金额：", (20, 70))
        self.t2 = wx.TextCtrl(self.panel, pos=(140,70), size=(120, 25))


        wx.StaticText(self.panel, wx.ID_ANY, "账号", (20, 120))
        wx.StaticText(self.panel, wx.ID_ANY, "账户名", (140, 120))
        wx.StaticText(self.panel, wx.ID_ANY, "存款金额", (260, 120))

    def OnClick(self, e):
        dialog22 = MyDialog3(None)
        btn = wx.Button(parent=dialog22.panel, label="确定", pos=(140, 280), size=(70, 25))
        btn.Bind(wx.EVT_BUTTON, dialog22.deposite)
        dialog22.ShowModal()

    def deposite(self, e):
        M_balance=0
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ydj', db='test', charset='utf8')
        cursor = db.cursor()
        accountname = self.t1.GetValue()
        money = self.t2.GetValue()
        M_balance = float(money)

        if M_balance%100!=0:
                        
            dial = wx.MessageDialog(None, '请输入100的倍数', 'error', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
            dial.ShowModal()  # 显示对话框
        else:
            sq1= "UPDATE userinfoes SET balance=balance+'%0.2f' WHERE account='%s'"%(M_balance,accountname)  
           
            try:  
                j=cursor.execute(sq1)  
                db.commit()
                if j!=1:
                    dia4 = wx.MessageDialog(None, '账户不存在', 'error', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
                    dia4.ShowModal()  # 显示对话框
                else:  
                    dial = wx.MessageDialog(None, '存款成功', '结果', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
                    dial.ShowModal()  # 显示对话框
                    sql= "SELECT * FROM userinfoes WHERE account='%s'"%(accountname)
                    cursor.execute(sql)  
                    k = cursor.fetchall()
                    h=150
                    for i in k:

                        u_name=i[2]
                        u_account=i[0]
                        wx.StaticText(self.panel, wx.ID_ANY, str(u_account), (20, h)) 
                        wx.StaticText(self.panel, wx.ID_ANY, str(u_name), (140, h))
                        wx.StaticText(self.panel, wx.ID_ANY, str(money), (260, h))
            except:  
                db.rollback()  
                dia2 = wx.MessageDialog(None, '存款失败', '结果', wx.YES_NO)  # 创建一个带按钮的对话框, 语法是(self, 内容, 标题, ID) 
                dia2.ShowModal()  # 显示对话框 


        


