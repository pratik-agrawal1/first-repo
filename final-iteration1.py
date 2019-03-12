import tkinter as tk
import time
import sqlite3
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    if width:
            entry.config(width=width)
    entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
    return entry

def run_bc():
    u = user.get()
    p = password.get()
    m = lab.get()
    l = level.get()
    root.destroy()
    conn = sqlite3.connect('fuckelab.db')
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--load-extension=C:/Users/91700/AppData/Local/Google/Chrome/User Data/Default/Extensions/mobdimfppndkappalbddccnhdndabecb/1.0.2_0')
    options.add_argument('--enable-extensions')
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.get("http://care.srmuniv.ac.in/ktrstudentskill/")
    driver.find_element_by_xpath("//input[@id='userid']").send_keys(u)
    driver.find_element_by_xpath("//input[@id='password']").send_keys(p)
    driver.find_element_by_xpath("//a[@id='login']").click()
    time.sleep(1)
    if m == 'c':
        driver.find_element_by_xpath("//a[@id='C']").click()
    elif m == 'cpp':
        driver.find_element_by_xpath("//a[@id='CPP']").click()
    elif m == 'java':
        driver.find_element_by_xpath("//a[@id='JAVA']").click()
    elif m == 'data-structure':
        driver.find_element_by_xpath("//a[@id='DATA-STRUCTURE']").click()
    elif m == 'python':
        driver.find_element_by_xpath("//a[@id='PYTHON']").click()
    queno = []
    filename = str(m) + str(l) + ".txt"
    for o in range(100):
        o = str(o)
        driver.get(
            "http://care.srmuniv.ac.in/ktrstudentskill/login/studentnew/code/" + m + "/" + m + ".code.php?id=" + l +"&value=" + o)
        try:
            if m!='java':
                try:
                    que = driver.find_element_by_xpath("//*[@id='nav-mobile1']/ul/li[2]/h6/b").text
                except NoSuchElementException:
                    continue
            else:
                try:
                    que = driver.find_element_by_xpath("//*[@id='nav-mobile1']/ul/li[2]").text
                except NoSuchElementException:
                    continue
            queque = que.split(": ")
            queno.append(queque[1])

        except TimeoutException:
            print("Loading took too much time!")
    ds1 = {}
    sub = 0
    if m == 'c':
        sub = 1
    elif m == 'cpp':
        sub = 2
    elif m == 'java':
        sub = 3
    elif m == 'data-structure':
        sub = 4
    elif m == 'python':
        sub = 8
    for q in queno:
        x = conn.execute("SELECT q_no FROM elab WHERE q_course=? AND q_name=?", (sub, q,))
        r = x.fetchall()
        if (len(r) > 0):
            for rows in r:
                ds1[q] = rows[0]
        else:
            print("\nSorry. Question name does not exist in the database.")

    if not os.path.exists(u):
        os.mkdir(u)
    os.chdir(u)
    fh = open(filename, "w")
    i = 1
    for k, v in ds1.items():
        fh.write("(" + str(i) + ") " + str(k) + " == " + str(v) + "\n")
        i += 1
    fh.close()


root = tk.Tk()
root.geometry('300x250')
root.title('Welcome to Elab')
parent = tk.Frame(root, padx=10, pady=10)
parent.pack(fill=tk.BOTH, expand=True)
lab = entry(parent, "Which Lab? ( lowercase ): ", 16)
level = entry(parent, "Choose Level: ",16)
user = entry(parent, "User Name : ", 16)
password = entry(parent, "Password :", 16, show="*")
b = tk.Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=run_bc)
b.pack(side=tk.BOTTOM)
lab.focus_set()
parent.mainloop()