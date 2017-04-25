#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import argparse
import os
import os.path
import subprocess

import wx

def main():
    powerSettingDic = get_powercfg_setting()
    open_gui(powerSettingDic)


# powercfg /l
# 0        1     2                                     3
# 電源設定の GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (バランス) *
# 電源設定の GUID: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c  (高パフォーマンス)
# 電源設定の GUID: a1841308-3541-4fab-bc81-f71556f20b4a  (省電力)
#
# powercfg.exe -SETACTIVE 0c0eadf7-9b97-4475-903f-0c488ed5b568

def get_powercfg_setting():
    powerSettingDic = {}
    s = subprocess.check_output( "powercfg /l", shell=True ).decode('sjis')
    #s = subprocess.check_output( "powercfg /l", shell=True )
    #print (s)
    s1 = s.splitlines()

    for s2 in s1:
        if s2.find("電源設定の") > -1 :
            paramList = s2.split()

            if len(paramList)>4 and paramList[4] == "*":
                paramList[3] += "*"

            powerSettingDic[paramList[3]] = paramList[2]
            print ( paramList[3] + "=" + paramList[2] )

    return powerSettingDic



ACTIVE_KEY = ""

def open_gui(powerSettingDic):
    global ACTIVE_KEY

    def click_button_1(event):
        frame.SetStatusText("Click! button_1")
        print("button 1 is pressed.")

    def click_button_2(event):
        frame.SetStatusText("Click! button_2")

    def click_button(event):
        global ACTIVE_KEY
        press_ctrl_name = controlName[event.GetId()]
        print("Click " + str(event.GetId()) + " - " + press_ctrl_name + " - " + powerSettingDic[press_ctrl_name] )

        ACTIVE_KEY = press_ctrl_name
        set_active_color()

        cmd = "powercfg.exe -SETACTIVE " + powerSettingDic[press_ctrl_name]
        print ( "cmd: " + cmd )
        s = subprocess.check_output( cmd, shell=True ).decode('utf-8')

    def set_active_color():
        for k in powerSettingDic.keys():
            #print (k + "-" + ACTIVE_KEY)
            if ( k == ACTIVE_KEY ):
                wC[k].SetBackgroundColour("#FFBBBB")
            else:
                wC[k].SetBackgroundColour("#FFFFFF")

    wC = {}  # window control dictionary
    application = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, u"テストフレーム", size=(120,170))
    #frame.CreateStatusBar()

    panel = wx.Panel(frame, wx.ID_ANY)
    panel.SetBackgroundColour("#AFAFAF")

    # define control
    #wC['button_1'] = wx.Button(panel, wx.ID_ANY, u"ボタン１")
    #wC['button_2'] = wx.Button(panel, 3333     , u"ボタン２")
    #wC['button_3'] = wx.Button(panel, 4444     , u"ボタン３")

    # set event
    #wC['button_1'].Bind(wx.EVT_BUTTON, click_button_1)
    #frame.Bind(wx.EVT_BUTTON, click_button, wC['button_2'])
    #frame.Bind(wx.EVT_BUTTON, click_button, wC['button_3'])

    controlName = {}

    for k in sorted(powerSettingDic.keys()):
        #ctrlname = "btn_" + k
        wC[k] = wx.Button(panel, wx.ID_ANY, k)
        frame.Bind(wx.EVT_BUTTON, click_button, wC[k])
        controlName[ wC[k].GetId() ] = k   # e.g. controlName[3333] = "(省電力)"
        if k.find("*") > -1 and ACTIVE_KEY == "" :
            ACTIVE_KEY = k

    set_active_color()

    # define layout
    layout = wx.BoxSizer(wx.VERTICAL)

    for k in sorted(wC.keys()):
        layout.Add(wC[k], proportion=1, flag=wx.GROW)

    panel.SetSizer(layout)

    frame.Show()
    application.MainLoop()



main()
