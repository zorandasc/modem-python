from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure

import threading
from collections import deque
from ipaddress import ip_address
import datetime
import time



matplotlib.use("TkAgg")


# self represents the current object. This is a common first parameter for any method of a class.
# As you suggested, it's similar to Java's this.

# parent represents a widget to act as the parent of the current object.
# All widgets in tkinter except the root window require a parent(sometimes also called a master)

# controller represents some other object that is designed to act as a
# common point of interaction for several pages of widgets.
# It is an attempt to decouple the pages.
# That is to say, each page doesn't need to know about the other pages.
# If it wants to interact with another page, such as causing it to be visible,
# it can ask the controller to make it visible.

options = Options()
options.add_argument('--headless')
options.add_argument("--disable-setuid-sandbox")
options.add_argument('--no-sandbox')
# ovim komentovanjem cemo ugasiti sve crom procese nakon gasenja aplikacije
options.add_argument('--disable-gpu')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--no-proxy-server')
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--disable-default-apps")
options.add_argument("--enable-precise-memory-info")
options.add_argument('disable-notifications')
options.add_argument("--disable-default-apps")
options.add_argument("--disable-impl-side-painting")
options.add_argument("--disable-seccomp-filter-sandbox")
options.add_argument("--disable-breakpad")
options.add_argument("--disable-client-side-phishing-detection")
options.add_argument("--disable-cast")
options.add_argument("--disable-cast-streaming-hw-encoding")
options.add_argument("--disable-cloud-import")
options.add_argument("--disable-popup-blocking")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-session-crashed-bubble")
options.add_argument("--disable-ipv6")
options.add_argument('--disable-application-cache')
options.add_argument('--incognito')


style.use("ggplot")


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.tk_setPalette(background="dark sea green")
        self.graf_colors = {"facecolor": "#8fbc8f", "ticscolor": "black"}

        

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.browser = None
        self.canvas = None
        self.eth = []

        self.title('Modem Troughput Monitoring Aplication')
        self.frames = {}

        pageList = [StartPage, ModemHG8245H5, GrafHG8245H5,
                    ModemHG8245H, GrafHG8245H, ModemZTE_H267N, GrafZTE_H267N]
        geometryList = ['950x500', '650x450', '900x650',
                        '650x450', '900x650', '650x450', '900x650']

        for F, geometry in zip(pageList, geometryList):
            frame = F(parent=container, controller=self)
            self.frames[F] = (frame, geometry)
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, cont):
        frame, geometry = self.frames[cont]
        self.geometry(geometry)
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Zatvori", "Da li želite da zatvorite?"):
            if self.browser is not None:
                self.browser.close()
                self.browser.quit()
            if self.canvas is not None:
                self.canvas.get_tk_widget().destroy()
            plt.close("all")
            self.quit()
            self.destroy()

    def change_colors(self, tema):

        if tema == "Fresh Lime":
            self.tk_setPalette(background="dark sea green")
            self.graf_colors["facecolor"] = "#8fbc8f"
            self.graf_colors["ticscolor"] = "black"
            text_color = "black"
            bg = "#000000"
            fg = '#b7f731'
        if tema == "Dark Orange":
            self.tk_setPalette(background="gray7")
            self.graf_colors["facecolor"] = "#121212"
            self.graf_colors["ticscolor"] = "orange"
            text_color = 'orange2'
            bg = 'OrangeRed3'
            fg = 'mint cream'
        if tema == "Bubble Gum":
            self.tk_setPalette(background="Indian red")
            self.graf_colors["facecolor"] = "#cd5c5c"
            self.graf_colors["ticscolor"] = "#121212"
            text_color = "black"
            bg = 'light sky blue'
            fg = 'gray7'

        for key in self.frames:
            frame = self.frames[key][0]
            frame.repaint_gui(bg, fg, text_color)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.OptionList = [
            "Home Router ZTE: H267N",
            "Home Router Huawei:  HG8245H5",
            "Home Router Huawei:  HG8245H"
        ]

        self.setGui()

    def setGui(self):

            left = tk.Frame(self)
            self.right = tk.Frame(self)
            self.bottom = tk.Frame(self)
            self.copy_frame = tk.Frame(self)
            self.copy_frame.columnconfigure(0, weight=1)
            self.copy_frame.rowconfigure(0, weight=1)

            self.copy_frame.pack(
                side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            self.bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            self.btn_prihvati = tk.Button(self, text="PRIHVATI",
                                          font=('Tempus Sans ITC', 10, "bold"),
                                          width=12, cursor="hand2", relief=tk.RIDGE, command=self.prihvati)
            self.btn_prihvati.configure(
                bg='#000000', fg='#b7f731', padx=20, pady=20)
            self.btn_prihvati.pack(
                in_=self.bottom, side=tk.LEFT, padx=20, pady=20)

            color_label = tk.Label(self, text="Teme",
                                   font=('Tempus Sans ITC', 10, "bold"), pady=20)
            color_label.pack(in_=self.bottom, side=tk.LEFT, padx=(20, 5))
            self.color_variable = tk.StringVar(self)
            self.color_variable.set("Fresh Lime")
            self.color_variable.trace("w", self.color_callback)
            self.color_option = tk.OptionMenu(
                self, self.color_variable, "Fresh Lime", "Dark Orange", "Bubble Gum")
            self.color_option.config(
                bg='#000000', fg='#b7f731', font=('Tempus Sans ITC', 10))
            self.color_option.pack(in_=self.bottom, side=tk.LEFT, pady=20)

            copyright_label = tk.Label(self, font=(
                'Verdana', 10), text=u"\u00A9 Copyright 2020 Nazor Sicda INC. All rights reserved.")
            copyright_label.grid(in_=self.copy_frame, row=0, column=0)

            self.next_btn = None
            self.next_bg = '#000000'
            self.next_fg = '#b7f731'

            self.label2 = tk.Label(
                self, text="MOLIM VAS IZABERITE ROUTER", font=('Tempus Sans ITC', 14, 'bold'))
            self.label2.grid(in_=self.right, row=0, column=0, pady=20)

            self.variable = tk.StringVar(self)
            self.variable.set("IZBORNIK")
            # w ako se upisuje u variablu
            self.variable.trace("w", self.callback)

            self.opt = tk.OptionMenu(self, self.variable, *self.OptionList)
            self.opt.config(font=('Tempus Sans ITC', 10, "bold"),
                            bg='#000000', fg='#b7f731', disabledforeground="gray", width=30, cursor="", padx=20, pady=20, state="disabled")
            self.opt['menu'].config(font=('Helvetica', (12)), activebackground='#b7f731',
                                    activeforeground='black')
            self.opt.grid(in_=self.right, row=1, column=0, padx=10)

            self.text2 = tk.Text(self, height=30, width=65)
            scroll = tk.Scrollbar(self, command=self.text2.yview)
            self.text2.configure(yscrollcommand=scroll.set)
            self.text2.tag_configure('bold_italics', font=(
                'Arial', 12, 'bold', 'italic'))
            self.text2.tag_configure('big', font=('Verdana', 20, 'bold'))
            self.text2.tag_configure('color',
                                     foreground='black',
                                     font=('Tempus Sans ITC', 12, 'bold'))
            self.text2.insert(
                tk.END, '\n     Terms and conditions \n', 'big')

            quote = """
            These terms and conditions ("Terms", "Agreement")
            are an agreement between Application Developer
            ("Application Developer", "us", "we" or "our") and you
            ("User", "you" or "your").This Agreement sets forth the
            general terms and conditions of your use of the
            Modem Troughput Monitoring Application (MTM)
            application and any of its products or services
            (collectively, "Application" or "Services").

            MTM Application

            The purpose of this experimental application is to 
            provide insight into the total traffic that is 
            generated while sending and receiving content. 
            Quantitative estimation of total traffic this 
            application realizes by visual representation of 
            the current bit rate on the selected interface 
            (wireless or wire standard), of the corresponding 
            home router (modem).
            The significance of this application is that the 
            insight into the amount of user traffic is realized 
            at the point of convergence of the home network, 
            that is, at the place where the network of users 
            is connected to the network of the operator and 
            not on the individual device of the user.

            Recommendations

            If the application is running for the first time 
            on the computer, the Internet connection of the 
            computer is required, due to the need to obtain or 
            update the appropriate driver (a utility required 
            for the smooth operation of the application). 
            For the normal operation of the application, 
            no internet connection is necessary.
            Due to the experimental nature of the application, 
            irregularities in its operation are not impossible. 
            Here, in particular, should be noted the case where 
            MEASURED INTERFACE and CONNECTED INTERFACE 
            (the interface of connecting the router and the computer 
            on which the application is located), selected as WIFI. 
            Because in the case of severe congestion of the wifi 
            link, this combination of interfaces can lead to 
            application failure (eg. timeout error). This scenario 
            is possible due to the shared nature (shered enviroment) 
            of WIFI technology and the lack of any particular 
            priority of this application over any other 
            application or other user traffic.

            Legal Statement

            You are about to log on to a proprietary computer
            system where access is provided,by the Owner of the
            computer system, only to authorized users. If you
            are not authorized to use this system, please refrain
            from doing so. All activities on this system are being
            logged. Unauthorized access to this system may be
            subjected to legal action, and/or prosecution.

            Backups

            We are not responsible for Content residing in the
            Application. In no event shall we be held liable for
            any loss of any Content.It is your sole responsibility
            to maintain appropriate backup of your Content.
            Notwithstanding the foregoing, on some occasions and
            in certain circumstances, with absolutely no obligation,
            we may be able to restore some or all of your data that
            has been deleted as of a certain date and time when we
            may have backed up data for our own purposes. We make
            no guarantee that the data you need will be available.


            Links to other applications

            Although this Application may link to other applications,
            we are not, directly or indirectly, implying any approval,
            association, sponsorship, endorsement, or affiliation with
            any linked application, unless specifically stated herein.
            We are not responsible for examining or evaluating, and we
            do not warrant the offerings of, any businesses or
            individuals or the content of their applications. We do
            not assume any responsibility or liability for the actions,
            products, services, and content of any other third-parties.
            You should carefully review the legal statements and other
            conditions of use of any mobile application which you
            access through a link from this Application. Your linking
            to any other off-site applications is at your own risk.

            Prohibited uses

            The author of this application is not responsible for
            any damages resulting from the use of this application
            in a non-expert and harmful manner.In addition to other
            terms as set forth in the Agreement, you are prohibited
            from using the Application or its Content: (a) for any
            unlawful purpose; (b) to solicit others to perform or
            participate in any unlawful acts; (c) to violate any
            international, federal,provincial or state regulations,
            rules, laws, or local ordinances; (d) to infringe upon
            or violate our intellectual property rights or the
            intellectual property rights of others; (e) to harass, abuse,
            insult, harm, defame, slander, disparage, intimidate, or
            discriminate based on gender, sexual orientation, religion,
            ethnicity, race, age, national origin, or disability; (f)
            to submit false or misleading information; (g) to upload or
            transmit viruses or any other type of malicious code that
            will or may be used in any way that will affect the
            functionality or operation of the Service or of any related
            application, other applications, or the Internet; (h) to
            collect or track the personal information of others; (i) to
            spam, phish, pharm, pretext, spider, crawl, or scrape; (j)
            for any obscene or immoral purpose; or (k) to interfere
            with or circumvent the security features of the Service
            or any related application, other applications, or the
            Internet. We reserve the right to terminate your use of
            the Service or any related application for violating any
            of the prohibited uses.

            Intellectual property rights

            This Agreement does not transfer to you any intellectual
            property owned by Application Developer or third-parties,
            and all rights, titles, and interests in and to such property
            will remain (as between the parties) solely with Application
            Developer. All trademarks, service marks, graphics and logos
            used in connection with our Application or Services, are
            trademarks or registered trademarks of Application
            Developer or Application Developer licensors. Other
            trademarks, service marks, graphics and logos used in
            connection with our Application or Services may be the
            trademarks of other third-parties. Your use of our
            Application and Services grants you no right or license to
            reproduce or otherwise use any Application Developer or
            third-party trademarks.

            Guarantees and warranties

            To the maximum extent allowed by law, this app disclaims
            all warranties and representations of any kind, including
            without limitation the implied warranties of
            merchantability, fitness for a particular purpose,
            and noninfringement, whether express, implied, or
            statutory. This app provides no guarantees that the
            services or network will function without interruption
            or errors and provides the services, and any related
            content or products subject to these public network
            terms on an “as is” basis.

            Dispute resolution

            The formation, interpretation, and performance of this
            Agreement and any disputes arising out of it shall be
            governed by the substantive and procedural laws of
            Bosnia and Herzegovina without regard to its rules on
            conflicts or choice of law and, to the extent applicable,
            the laws of Bosnia and Herzegovina. The exclusive
            jurisdiction and venue for actions related to the subject
            matter hereof shall be the state and federal courts located
            in Bosnia and Herzegovina, and you hereby submit to the
            personal jurisdiction of such courts. You hereby waive
            any right to a jury trial in any proceeding arising out
            of or related to this Agreement. The United Nations
            Convention on Contracts for the International Sale of
            Goods does not apply to this Agreement.

            Changes and amendments

            We reserve the right to modify this Agreement or its
            policies relating to the Application or Services at any
            time, effective upon posting of an updated version of
            this Agreement in the Application. Continued use of
            the Application after any such changes shall constitute
            your consent to such changes. Policy was created with
            https://www.WebsitePolicies.com

            Acceptance of these terms

            You acknowledge that you have read this Agreement and
            agree to all its terms and conditions. By using the
            Application or its Services you agree to be bound by
            this Agreement. If you do not agree to abide by the
            terms of this Agreement, you are not authorized to
            use or access the Application and its Services.
            By clicking PRIHVATI buttton you affirm that you have
            read, understand, and agree to be bound by these Terms.
            """
            self.text2.insert(tk.END, quote, 'color')
            self.text2.pack(in_=left, side=tk.LEFT)
            scroll.pack(in_=left, side=tk.RIGHT, fill=tk.Y)
            self.text2.configure(state="disabled")

    def callback(self, *args):
        if self.next_btn:
            self.next_btn.destroy()
        self.next_btn = self.create_button(self.variable.get())
        self.next_btn.configure(
            bg=self.next_bg, fg=self.next_fg, cursor="hand2", font=('Tempus Sans ITC', 10, "bold"), padx=20, pady=20)
        self.next_btn.pack(in_=self.bottom, side=tk.RIGHT, padx=20, pady=20)

    def create_button(self, arg):
        return {
            "Home Router ZTE: H267N": tk.Button(
                self, text="NASTAVI >>", font=('Tempus Sans ITC', 10, "bold"), relief=tk.RIDGE, command=lambda: self.controller.show_frame(ModemZTE_H267N)),
            "Home Router Huawei:  HG8245H5": tk.Button(
                self, text="NASTAVI >>", font=('Tempus Sans ITC', 10, "bold"), relief=tk.RIDGE, command=lambda: self.controller.show_frame(ModemHG8245H5)),
            "Home Router Huawei:  HG8245H": tk.Button(
                self, text="NASTAVI >>", font=('Tempus Sans ITC', 10, "bold"), relief=tk.RIDGE, command=lambda: self.controller.show_frame(ModemHG8245H)),
        }[arg]

    def prihvati(self):
        self.opt.configure(state="normal", cursor="hand2")

    def color_callback(self, *args):
        # promjeni teme na svim objektima
        self.controller.change_colors(self.color_variable.get())

    def repaint_gui(self, bg, fg, text_color):
        # promjeni temu na ovom objektu
         self.next_bg = bg
         self.next_fg = fg

         self.color_option.configure(bg=bg, fg=fg)
         self.btn_prihvati.configure(bg=bg, fg=fg)
         self.text2.tag_configure('color', foreground=text_color)
         if self.next_btn:
             self.next_btn.configure(bg=bg, fg=fg)
         self.opt.config(bg=bg, fg=fg)
         self.opt['menu'].config(activebackground=bg,
                                 activeforeground=fg)

# abstract class
class Modem(tk.Frame):
    global options

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.browser = None

        self.ip_gateway_text = tk.StringVar()
        self.username_text = tk.StringVar()
        self.password_text = tk.StringVar()
        self.alert_text = tk.StringVar()
        self.alert_text.set("NOT CONNECTED.")

        self.set_default()
        self.setGui()

    def setGui(self):

        self.top = tk.Frame(self)
        self.top1 = tk.Frame(self)
        self.bottom = tk.Frame(self)
        self.bottom1 = tk.Frame(self)

        self.top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.top1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom1.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        label1 = tk.Label(self, text="IME MODELA: ", font=(
            'Tempus Sans ITC', 20, "bold"), padx=20, pady=20)
        label1.grid(in_=self.top, row=0, column=0)

        self.label2 = tk.Label(self, text="MODEM GENERICKI",
                               font=('Tempus Sans ITC', 20, "bold"), fg="blue", pady=20)
        self.label2.grid(in_=self.top, row=0, column=1, columnspan=5)

        ip_gateway_label = tk.Label(self,
                                    text="IP GATEWAY: ", font=('Tempus Sans ITC', 12, "bold"), pady=10)
        ip_gateway_label.grid(in_=self.top1, row=1, column=1)

        self.ip_gateway_entry = tk.Entry(
            self, textvariable=self.ip_gateway_text, font=("bold", 14), bg="white", fg="blue")
        self.ip_gateway_entry.grid(
            in_=self.top1, row=1, column=2, columnspan=4)

        username_label = tk.Label(self, text="KORISNICKO IME: ",
                                  font=('Tempus Sans ITC', 12, "bold"), pady=10)
        username_label.grid(in_=self.top1, row=2, column=1)

        self.username_entry = tk.Entry(self,
                                       textvariable=self.username_text, font=("bold", 14), bg="white", fg="blue")
        self.username_entry.grid(
            in_=self.top1, row=2, column=2, columnspan=4)

        password_label = tk.Label(
            self, text="KORISNICKA SIFRA: ", font=('Tempus Sans ITC', 12, "bold"), pady=10)
        password_label.grid(in_=self.top1, row=3, column=1)

        self.password_entry = tk.Entry(self,
                                       textvariable=self.password_text, font=("bold", 14), bg="white", fg="blue", show="*")
        self.password_entry.grid(
            in_=self.top1, row=3, column=2, columnspan=4)

        self.btn_def = tk.Button(
            self, text="PODESI", padx=20, pady=20, width=8, cursor="hand2", bg='#000000', fg='#b7f731', relief=tk.RIDGE, command=self.set_default, font=('Tempus Sans ITC', 10, "bold"))
        self.btn_def.grid(in_=self.top1, row=1, rowspan=3,
                          column=0, pady=20, padx=20)

        self.btn_connect = tk.Button(
            self, text="POVEŽI SE",
            width=8, cursor="hand2", bg='#000000', fg='#b7f731', padx=20, pady=20, command=self.start, relief=tk.RIDGE, font=('Tempus Sans ITC', 10, "bold"))
        self.btn_connect.grid(in_=self.bottom, row=0,
                              column=0, pady=20, padx=20)

        label3 = tk.Label(self, text="STATUS",
                          font=('Tempus Sans ITC', 12, "bold"), padx=20, pady=20)

        label3.grid(in_=self.bottom, row=0, column=1, sticky=tk.W)

        self.alert_entry = tk.Entry(self,
                                    textvariable=self.alert_text, font=("bold", 12), fg="blue", width=40, state="readonly")
        self.alert_entry.grid(in_=self.bottom, row=0,
                              column=2, columnspan=6, sticky=tk.W)

        self.progress = Progressbar(
            self, orient=tk.HORIZONTAL, length=370, mode='indeterminate')

        self.btn_back = tk.Button(
            self, text="<<NATRAG",
            width=8, cursor="hand2", bg='#000000', fg='#b7f731', padx=20, pady=20,  command=self.back, relief=tk.RIDGE, font=('Tempus Sans ITC', 10, "bold"))
        self.btn_back.pack(in_=self.bottom1, side=tk.LEFT, pady=20, padx=20)

        self.btn_next = tk.Button(
            self, text="NASTAVI>>",
            width=8,  state="disable", cursor="", bg='#000000', fg='#b7f731', padx=20, pady=20, command=self.startGraph, relief=tk.RIDGE, font=('Tempus Sans ITC', 10, "bold"))
        self.btn_next.pack(in_=self.bottom1, side=tk.RIGHT, pady=20, padx=20)

    def set_default(self):

        self.ip_gateway_text.set("192.168.100.1") if self.ip_gateway_text.get(
        ) == "" else self.ip_gateway_text.set("")

        self.username_text.set("telecomadmin") if self.username_text.get(
        ) == "" else self.username_text.set("")

        self.password_text.set("admintelecom") if self.password_text.get(
        ) == "" else self.password_text.set("")

    def start(self):

        #ISPITAJ VALIDNOST IP ADRESE USERNAM I PASSWORDA
        try:
            ip_address(self.ip_gateway_text.get())
        except ValueError:
            messagebox.showinfo(
                "IP GATEWAY", "Unesena IP adresa rutera nije validna.")
            return

        if self.username_text.get() == "":
            messagebox.showinfo("KORISNICKO IME", "Unesite korisnicko ime.")
            return

        if self.password_text.get() == "":
            messagebox.showinfo("KORISNICKA SIFRA",
                                "Unesite korisnicku sifru.")
            return
        #POKRENI KONEKCIJU U THREDU
        self.thred()

    def thred(self):
        def real_thred():

            self.alert_entry.grid_forget()
            self.progress.grid(in_=self.bottom, row=0, column=2)

            #STARTUJ PROGRES BAR
            self.progress.start()

            #CEKAJ DOK KONEKLKCIJA NE ZAVRSI
            #A ONDA PODESI ALERT SA REZULTATOM KONEKCIJE
            self.alert_text.set(self.connect())

            #YAUSRAVI PROGRES BAR
            self.progress.stop()
            self.progress.grid_forget()

            # AKO KONEKCIJA NIJE USPIJESNA
            if self.alert_text.get() != "KONEKCIJA USPOSTAVLJENA":
                if self.browser is not None:
                    self.browser.close()
                    self.browser.quit()
                    self.browser = None
                self.alert_entry.configure(fg="red1")
            else:
                # AKO JE KONEKCIJA USPIJESNA
                self.btn_next.configure(state="normal", cursor="hand2")
                self.alert_entry.configure(fg="dark green")

                self.btn_def.configure(state="disable", cursor="")
                self.ip_gateway_entry.configure(state="disable")
                self.username_entry.configure(state="disable")
                self.password_entry.configure(state="disable")
                self.btn_connect.configure(state="disable", cursor="")

            #POSALJI BROWSER OBJEKAT KONTROLERU ZA DALJE GRAF OBKEKTE
            self.controller.browser = self.browser

            #PRIKAYI STATUS KONEKCIJE
            self.alert_entry.grid(in_=self.bottom, row=0,
                                  column=2, columnspan=6, sticky=tk.W)
            #VELIKI PROBLEMA AKO SE NE IZADJE IZ THREDA
            #RAM MEMORIJA SE NPRESTANO UVECAVALA SA
            #NEZAVRSENIM THREADOM

            return

        self.t1 = threading.Thread(target=real_thred)
        self.t1.start()

    # abstract method

    def connect(self):
        pass

    # abstract method
    def startGraph(self):
        pass

    def back(self):
        self.disconnect()
        self.controller.show_frame(StartPage)

    def disconnect(self):

        if self.browser is not None:
            self.browser.close()
            self.browser.quit()
            self.browser = None
            self.controller.browser = self.browser

        self.alert_entry.configure(fg="blue")
        self.alert_text.set("NOT CONNECTED.")

        self.btn_next.configure(state="disable", cursor="")
        self.btn_connect.configure(state="normal", cursor="hand2")
        self.btn_def.configure(state="normal", cursor="hand2")

        self.ip_gateway_entry.configure(state="normal")
        self.username_entry.configure(state="normal")
        self.password_entry.configure(state="normal")

    def repaint_gui(self, bg, fg, text_color):
        self.btn_def.configure(bg=bg, fg=fg)
        self.btn_connect.configure(bg=bg, fg=fg)
        self.btn_next.configure(bg=bg, fg=fg)
        self.btn_back.configure(bg=bg, fg=fg)
        self.label2.configure(fg=text_color)


# abstract class
class Graf(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.canvas = None
        self.toolbar = None

        self.OVERHEAD = False

        #OVO POTRBNO ZA GUI
        self.interf = [
            ("WIFI", 0),
            ("ETH1", 1),
            ("ETH2", 2),
            ("ETH3", 3),
            ("ETH4", 4),
        ]

        # BROJ ODMJERAKA U DEQUE I NA X-OSI
        self.max_x = 20

        self.eth = []

        # self.f = Figure(figsize= (5, 5), dpi = 100)
        self.f = Figure()
        self.a = self.f.add_subplot(111)

        self.xList = deque([0]*self.max_x, maxlen=self.max_x)
        self.downList = deque([0]*self.max_x, maxlen=self.max_x)
        self.upList = deque([0]*self.max_x, maxlen=self.max_x)

        self.monitoring = tk.IntVar()
        self.monitored = tk.IntVar()
        self.setGui()
        self.clearCounters()

    def setGui(self):

        self.top = tk.Frame(self)
        self.top1 = tk.Frame(self)
        self.top2 = tk.Frame(self)
        self.top3 = tk.Frame(self)
        self.bottom = tk.Frame(self)

        self.top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.top3.pack(in_=self.top, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.top1.pack(in_=self.top, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.top2.pack(in_=self.top, side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.btn_back = tk.Button(
            self, text="<<",
            width=4, cursor="hand2", relief=tk.RIDGE, bg='#000000', fg='#b7f731', pady=15, command=self.back, font=('Tempus Sans ITC', 10, "bold"))
        self.btn_back.grid(in_=self.top3, row=0, column=0, padx=10, pady=20)

        label3 = tk.Label(self, text="POVEZNI INTERFEJS: ",
                          font=('Tempus Sans ITC', 12, "bold"), padx=10)
        label3.grid(in_=self.top1, row=0, column=1, pady=(20, 0))

        self.monitoringBtns = list()

        for idx, (inter, val) in enumerate(self.interf):
            item = tk.Radiobutton(self, text=inter, padx=20, variable=self.monitoring,
                                  font=("bold", 10), borderwidth=2, bg='#000000', fg='#b7f731',
                                  selectcolor="#323232", highlightcolor="blue", takefocus="blue",
                                  command=self.show_monitoring, value=val)
            self.monitoringBtns.append(item)
            item.grid(in_=self.top1, row=0, pady=(20, 0), column=idx+2)

        label4 = tk.Label(self, text="MJERENI INTERFEJS: ",
                          font=('Tempus Sans ITC', 12, "bold"), padx=10, pady=10)
        label4.grid(in_=self.top1, row=1, column=1, sticky=tk.W)

        self.monitoredBtns = list()

        for idx, (inter, val) in enumerate(self.interf):
            item = tk.Radiobutton(self, text=inter, padx=20, variable=self.monitored,
                                  font=("bold", 10), borderwidth=2, bg='#000000', fg='#b7f731',
                                  selectcolor="#323232", highlightcolor="blue", takefocus="blue",
                                  command=self.set_monitored, value=val)
            self.monitoredBtns.append(item)
            item.grid(in_=self.top1, row=1, column=idx+2)

        self.btn_start_graf = tk.Button(
            self, text="START GRAF",
            width=8, cursor="", relief=tk.RIDGE, bg='#000000', fg='#b7f731', disabledforeground="gray", padx=20, command=self.start_grafh, font=('Tempus Sans ITC', 10, "bold"))
        self.btn_start_graf.grid(
            in_=self.top2, row=0, column=7, padx=20, pady=(20, 5))

        self.btn_stop_graf = tk.Button(
            self, text="STOP GRAF", relief=tk.RIDGE,
            width=8, cursor="", bg='#000000', fg='#b7f731', state="disable", disabledforeground="gray", padx=20, command=self.stop_grafh, font=('Tempus Sans ITC', 10, "bold"))
        self.btn_stop_graf.grid(in_=self.top2, row=1,
                                column=7, padx=20)

    def show_monitoring(self):
        pass

    def set_monitored(self):
        pass

    # VRATI SVE NA DEFAULT
    def clearCounters(self):
        self.monitoring.set(7)
        self.monitored.set(7)

        self.OVERHEAD = False
        # IZABRANI MONITORED INTERFACE

        self.down_owerhead = 0

        self.staribajt_down = 0
        self.staribajt_up = 0
        self.novibajt_down = 0
        self.novibajt_up = 0
        self.browserbajt = 0

        # OVO JE BITNO KOD DIJELJENA PRVOG ODMJERKA KOJI JE ODUZET SA 0
        # PA CE ZA PRVI BITI: NOVI_BAJT-0/ datetime.timedelta(days=1)
        self.xtimestara = datetime.datetime.now()-datetime.timedelta(days=1)

        self.xList.clear()
        self.downList.clear()
        self.upList.clear()

    def start_grafh(self):
        # DOBAVI BROWSER OBJEKAT IZ CONTROLERA DOBIJEN IZ PRETHODNOG PAGEA
        self.browser = self.controller.browser

        #DOBAVI ETH INTERFACE IZ CONTROLERA DOBIJEN IZ PRETHODNOG PAGEA
        self.eth = self.controller.eth

        self.wait = WebDriverWait(self.browser, 10)

        # GET IZABRANI MONITORED
        self.index = self.monitored.get()

        if self.monitoring.get() == 7:
            messagebox.showinfo("MONITORING INTERFACE",
                                "IZABERITE INTERFEJS NA MODEMU SA KOJIM STE POVEZANI!")
            return

        if self.index == 7:
            messagebox.showinfo("MONITORED INTERFACE",
                                "IZABERITE INTERFEJS KOJI ŽELITE DA POSMATRATE.")
            return

        # AKO SU NA ISTOM ADD OVERHEAD
        if self.monitoring.get() == self.index:
            self.OVERHEAD = True

            # AKO SU JOS NA ISTOM WIFI PRIKAZI UPOZORENJE
            if self.index == 0:
                messagebox.showwarning(
                    "UPOZORENJE", """            ZBOG DIJELJENOG OKRUŽENJA WIFI TEHNOLOGIJE, OVA
            KOMBINACIJA INTERFEJSA, MOŽE DOVESTI DO ISPADA 
            APLIKACIJE, POSEBNO U SLUČAJU IZRAZITOG ZAGUŠENJA 
            LINKA.""")

        # INDEX ODREDJUJE ETHERNET ILI WIFI
        if self.index == 0:
            self.getBajtRates = self.getWlanInfo
        else:
            self.getBajtRates = self.getEthInfo

        # TOOGLE STARTGRAF I STOPGRAF BUTTONS
        self.btn_start_graf.configure(state="disabled", cursor="")
        self.btn_stop_graf.configure(state="normal", cursor="hand2")

        # OBOJI GRAFOVE
        #--------------------------------------------------------
        # ZA IVICE GRAFA
        self.f.patch.set_facecolor(self.controller.graf_colors["facecolor"])
        self.a.tick_params(
            axis='x', colors=self.controller.graf_colors["ticscolor"])
        self.a.tick_params(
            axis='y', colors=self.controller.graf_colors["ticscolor"])
        self.a.yaxis.label.set_color(self.controller.graf_colors["ticscolor"])
        # ZA BACKGROUND GRAFA
        # self.a.set_facecolor('xkcd:salmon')

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas._tkcanvas.pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)

        self.ani = animation.FuncAnimation(
            self.f, self.animate, interval=4000)

    def stop_grafh(self):

        self.a.clear()

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        if self.toolbar is not None:
            self.toolbar.destroy()
            self.toolbar = None
        self.clearCounters()

        # TOOGLE STARTGRAF I STOPGRAF
        self.btn_start_graf.configure(state="normal", cursor="hand2")
        self.btn_stop_graf.configure(state="disabled", cursor="")

    # abstract method
    def getEthInfo(self):
        pass

    # abstract method
    def getWlanInfo(self):
        pass

    def calculate_overhead(self):
        if self.OVERHEAD:
            return self.browser.execute_script("""
                return performance.getEntries()
                    .filter(e => e.entryType==='navigation' || e.entryType==='resource')
                    .reduce((acc, e) => acc + e.transferSize, 0)
                """)
        return 0

    def calculateBitRate(self):
        # NOVO VRIJEME
        xtime = datetime.datetime.now()
        self.xList.append(xtime.strftime('%H:%M:%S'))

        # VREMENSKA RAZLIKA IZMEDJU DVA BAJT OCITAVANJA
        timediffer = (xtime-self.xtimestara).total_seconds()

        # RAZLIKA APSOLUTNIH VRIJEDNOSTI BAJTA-OVERHEAD
        self.bajtdiffer_down = (
            self.novibajt_down-self.staribajt_down)-self.size
        self.bajtdiffer_up = (self.novibajt_up-self.staribajt_up)

        # REZULTAT=BITSKA BRZINA (kbit)
        self.result_down = (((self.bajtdiffer_down * 8) /
                             (timediffer))/1024)
        self.result_up = (
            ((self.bajtdiffer_up*8)/(timediffer))/1024)

        self.downList.append(self.result_down)
        self.upList.append(self.result_up)

        # SACUVAJ STARE VRIJEDNOSTI I STARO VRIJEME
        self.staribajt_down = self.novibajt_down
        self.staribajt_up = self.novibajt_up
        self.xtimestara = xtime
        return

    def plotBitRate(self):
        self.a.clear()

        label_down = self.eth[self.index]["name"]+"[down]: " + \
            "{:.2f}".format(self.result_down)+"kbit/s."
        label_up = self.eth[self.index]["name"]+"[up]: " + \
            "{:.2f}".format(self.result_up)+"kbit/s."

        self.a.plot_date(self.xList, self.downList, "g", label=label_down)

        self.a.plot_date(self.xList, self.upList, "r", label=label_up)
        self.a.set_xticklabels(self.xList, rotation=35, ha="right")
        self.a.set_ylabel('kbit/s')
        self.a.legend(bbox_to_anchor=(0, 1.02, 1, .102),
                      loc=3, ncol=2, borderaxespad=0)
        # self.a.legend()
        # self.a.set_title("Bit Rate [kbit/s]")
        return

    def animate(self, i):

        # DOBAVI (NETWORK REQUEST)
        self.getBajtRates()
        # SRACUNAJ (CALCULATE)
        self.calculateBitRate()
        # PLOTIRAJ (PLOT)
        self.plotBitRate()

    # abstract method
    def back(self):
        pass

    def repaint_gui(self, bg, fg, text_color):
        self.btn_back.configure(bg=bg, fg=fg)
        self.btn_stop_graf.configure(bg=bg, fg=fg)
        self.btn_start_graf.configure(bg=bg, fg=fg)
        for btn in self.monitoredBtns:
            btn.configure(bg=bg, fg=fg, selectcolor=bg)
        for btn in self.monitoringBtns:
            btn.configure(bg=bg, fg=fg, selectcolor=bg)


class ModemHG8245H5(Modem):
    global options

    def __init__(self, parent, controller):

        super().__init__(parent, controller)
        self.label2.configure(text="HUAWEI HG8245H5")

        self.controller = controller

        self.eth = [
            {
                "name": "WIFI",
                "down": "/html/body/div[11]/div[2]/table/tbody/tr[3]/td[7]",
                "up": "/html/body/div[11]/div[2]/table/tbody/tr[3]/td[3]"},
            {
                "name": "ETH1",
                'down': '/html/body/div[6]/table/tbody/tr[3]/td[7]',
                'up': '/html/body/div[6]/table/tbody/tr[3]/td[5]'},
            {
                "name": "ETH2",
                'down': '/html/body/div[6]/table/tbody/tr[4]/td[7]',
                'up': '/html/body/div[6]/table/tbody/tr[4]/td[5]'},
            {
                "name": "ETH3",
                'down': '/html/body/div[6]/table/tbody/tr[5]/td[7]',
                'up': '/html/body/div[6]/table/tbody/tr[5]/td[5]'},
            {
                "name": "ETH4",
                'down': '/html/body/div[6]/table/tbody/tr[6]/td[7]',
                'up': '/html/body/div[6]/table/tbody/tr[6]/td[5]'},
        ]

    def connect(self):

        #PROVJERA VERZIJA CROME DRIVERA
        try:
            CHROMEDRIVER_PATH = ChromeDriverManager().install()
        except Exception as e:
            return "Neuspješno osvježavanje drajvera. Provjerite vašu internet konekciju. " +str(e)


        self.browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

        wait = WebDriverWait(self.browser, 10)
        self.browser.get("http://"+self.ip_gateway_text.get()+"/")

        try:
            assert "HG8245H5" in self.browser.page_source
        except AssertionError:
            return "Niste na HG8245H5 ruteru, ili provjerite gateway IP adresu."

        username = wait.until(
            EC.presence_of_element_located((By.ID, "txt_Username")))

        username.send_keys(self.username_text.get())

        password = wait.until(
            EC.presence_of_element_located((By.ID, "txt_Password")))

        password.send_keys(self.password_text.get())

        login = wait.until(EC.element_to_be_clickable((By.ID, "loginbutton")))

        login.click()

        try:
            assert "Incorrect User Name/Password combination. Please try again." not in self.browser.page_source
        except AssertionError:
            return "Neispravna kombinacija korisničko ime/šifra. Pokušajte ponovo."

        sys_info = wait.until(
            EC.element_to_be_clickable((By.ID, "name_Systeminfo")))
        sys_info.click()

        #PROVJERA VERZIJE SOFTVERA NA MODEMU

        deviceinfo = wait.until(
            EC.element_to_be_clickable((By.ID, "name_deviceinfo")))
        deviceinfo.click()

        wait.until(
            EC.frame_to_be_available_and_switch_to_it('menuIframe'))

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="td5_2"]')))
        try:
            assert "V5R019C00S100" in self.browser.page_source
            self.controller.eth = self.eth
            return "KONEKCIJA USPOSTAVLJENA"
        except AssertionError:
            pass

        return "NEPODRAZANA VERZIJA"

    def startGraph(self):
        self.controller.show_frame(GrafHG8245H5)


class GrafHG8245H5(Graf):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def getEthInfo(self):

        self.browser.switch_to.default_content()
        try:
            ethinfo = self.wait.until(
                EC.element_to_be_clickable((By.ID, "name_ethinfo")))
            ethinfo.click()

            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it('menuIframe'))

            html_down = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["down"])))
            self.novibajt_down = int(html_down.get_attribute("innerHTML"))

            html_up = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["up"])))
            self.novibajt_up = int(html_up.get_attribute("innerHTML"))

            self.size = self.calculate_overhead()

        except StaleElementReferenceException as e:
            #print("STALEELEMENT ERROR OCURED"+str(e))
            pass
        except WebDriverException as e:
            #print("WEBDRIVER: "+str(e))
            pass

        except TimeoutException as e:
            messagebox.showerror("ERROR", "TIMEOUT ERROR OCURED: \n" + str(e))
            self.stop_grafh()

    def getWlanInfo(self):

        self.browser.switch_to.default_content()

        try:
            wlaninfo = self.wait.until(
                EC.element_to_be_clickable((By.ID, "name_wlaninfo")))
            wlaninfo.click()

            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it("menuIframe"))

            html_down = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["down"])))
            self.novibajt_down = int(
                html_down.get_attribute("innerHTML").split("&")[0])

            html_up = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["up"])))
            self.novibajt_up = int(
                html_up.get_attribute("innerHTML").split("&")[0])

            self.size = self.calculate_overhead()

        except StaleElementReferenceException as e:
            #print("STALEELEMENT ERROR OCURED"+str(e))
            pass
        except WebDriverException as e:
            #print("WEBDRIVER: "+str(e))
            pass

        except TimeoutException as e:
            messagebox.showerror("ERROR", "TIMEOUT ERROR OCURED: \n" + str(e))
            self.stop_grafh()

    def back(self):
        self.stop_grafh()
        self.controller.show_frame(ModemHG8245H5)


class ModemHG8245H(Modem):
    global options

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.controller = controller

        self.label2.configure(text="HUAWEI HG8245H")

        self.eth_v17 = [
            {
                "name": "WIFI",
                "down": "/html/body/div[10]/div[2]/table/tbody/tr[3]/td[7]",
                "up": "/html/body/div[10]/div[2]/table/tbody/tr[3]/td[3]"},
            {
                "name": "ETH1",
                'down': '/html/body/div[5]/table/tbody/tr[3]/td[7]',
                'up': '/html/body/div[5]/table/tbody/tr[3]/td[5]'},
            {
                "name": "ETH2",
                'down': '/html/body/div[5]/table/tbody/tr[4]/td[7]',
                'up': '/html/body/div[5]/table/tbody/tr[4]/td[5]'},
            {
                "name": "ETH3",
                'down': '/html/body/div[5]/table/tbody/tr[5]/td[7]',
                'up': '/html/body/div[5]/table/tbody/tr[5]/td[5]'},
            {
                "name": "ETH4",
                'down': '/html/body/div[5]/table/tbody/tr[6]/td[7]',
                'up': '/html/body/div[5]/table/tbody/tr[6]/td[5]'}, ]

        self.eth_v15 = [
            {
                "name": "WIFI",
                "down": "/html/body/div[3]/table[1]/tbody/tr[3]/td[7]",
                "up": "/html/body/div[3]/table[1]/tbody/tr[3]/td[3]"},
            {
                "name": "ETH1",
                'down': '/html/body/div[3]/table[2]/tbody/tr[3]/td[7]',
                'up': '/html/body/div[3]/table[2]/tbody/tr[3]/td[5]'},
            {
                "name": "ETH2",
                'down': '/html/body/div[3]/table[2]/tbody/tr[4]/td[7]',
                'up': '/html/body/div[3]/table[2]/tbody/tr[4]/td[5]'},
            {
                "name": "ETH3",
                'down': '/html/body/div[3]/table[2]/tbody/tr[5]/td[7]',
                'up': '/html/body/div[3]/table[2]/tbody/tr[5]/td[5]'},
            {
                "name": "ETH4",
                'down': '/html/body/div[3]/table[2]/tbody/tr[6]/td[7]',
                'up': '/html/body/div[3]/table[2]/tbody/tr[6]/td[5]'}, ]

    def connect(self):

        #PROVJERA VERZIJA CROME DRIVERA
        try:
            CHROMEDRIVER_PATH = ChromeDriverManager().install()
        except Exception:
            return "Neuspješno osvježavanje drajvera. Provjerite vašu internet konekciju."

        self.browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
        wait = WebDriverWait(self.browser, 10)
        self.browser.get("http://"+self.ip_gateway_text.get()+"/")

        try:
            assert "HG8245H" in self.browser.page_source
        except AssertionError:
            return "Niste na HG8245H ruteru, ili provjerite gateway IP adresu."

        # ovaj dole try je potreban ako se kacimo na H5 a greskom izaberemo H router. pa ce
        # prvi assert proci, posto je  "HG8245H" in "HG8245H5"
        try:
            username = wait.until(
                EC.presence_of_element_located((By.ID, "txt_Username")))

            username.send_keys(self.username_text.get())

            password = wait.until(
                EC.presence_of_element_located((By.ID, "txt_Password")))

            password.send_keys(self.password_text.get())

            login = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="button"]')))

            login.click()

        except Exception:
            return "Niste na HG8245H ruteru, ili provjerite gateway IP adresu."

        try:
            assert "Incorrect account/password combination. Please try again." not in self.browser.page_source
        except AssertionError:
            return "Neispravna kombinacija korisničko ime/šifra. Pokušajte ponovo."

        #PROVJERA VERZIJE SOFTVERA NA MODEMU
        wait.until(
            EC.frame_to_be_available_and_switch_to_it('frameContent'))

        try:
            assert "V3R017C10S122" in self.browser.page_source
            self.controller.eth = self.eth_v17
            return "KONEKCIJA USPOSTAVLJENA"
        except AssertionError:
            pass
        try:
            assert "V3R015C10S150" in self.browser.page_source
            self.controller.eth = self.eth_v15
            return "KONEKCIJA USPOSTAVLJENA"
        except AssertionError:
            pass

        return "NEPODRZANA SOFTVERSKA VERZIJA"

    def startGraph(self):

        self.controller.show_frame(GrafHG8245H)


class GrafHG8245H(Graf):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def back(self):
        self.stop_grafh()
        self.controller.show_frame(ModemHG8245H)

    def getEthInfo(self):

        self.browser.switch_to.default_content()
        try:
            ethinfo = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[1]/ul/li[5]/div')))
            ethinfo.click()

            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it('frameContent'))

            html_down = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["down"])))
            self.novibajt_down = int(html_down.get_attribute("innerHTML"))

            html_up = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["up"])))
            self.novibajt_up = int(html_up.get_attribute("innerHTML"))

            self.size = self.calculate_overhead()

        except StaleElementReferenceException as e:
            #print("STALEELEMENT ERROR OCURED"+str(e))
            pass
       
        except WebDriverException as e:
            #print("WEBDRIVER: "+str(e))
            pass

        except TimeoutException as e:
            messagebox.showerror("ERROR", "TIMEOUT ERROR OCURED: \n" + str(e))
            self.stop_grafh()

        return

    def getWlanInfo(self):

        self.browser.switch_to.default_content()
        try:
            wlaninfo = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[1]/ul/li[3]')))
            wlaninfo.click()

            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it('frameContent'))

            html_down = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["down"])))
            self.novibajt_down = int(
                html_down.get_attribute("innerHTML").split("&")[0])

            html_up = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["up"])))
            self.novibajt_up = int(
                html_up.get_attribute("innerHTML").split("&")[0])

            self.size = self.calculate_overhead()
        
        except StaleElementReferenceException as e:
            #print("STALEELEMENT ERROR OCURED"+str(e))
            pass
        except WebDriverException as e:
            #print("WEBDRIVER: "+str(e))
            pass
        except TimeoutException as e:
            messagebox.showerror("ERROR", "TIMEOUT ERROR OCURED: \n" + str(e))
            self.stop_grafh()
        return


class ModemZTE_H267N(Modem):
    global options

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label2.configure(text="ModemZTE_H267N")

        self.controller = controller

        self.eth = [
            {
                "name": "WIFI",
                "down": "//*[@id='TotalBytesSent:0']",
                "up": "//*[@id='TotalBytesReceived:0']"},
            {
                "name": "ETH1",
                'down': '//*[@id="BytesSent:0"]',
                'up': '//*[@id="BytesReceived:0"]'},
            {
                "name": "ETH2",
                'down': '//*[@id="BytesSent:1"]',
                'up': '//*[@id="BytesReceived:1"]'},
            {
                "name": "ETH3",
                'down': '//*[@id="BytesSent:2"]',
                'up': '//*[@id="BytesReceived:2"]'},
            {
                "name": "ETH4",
                'down': '//*[@id="BytesSent:3"]',
                'up': '//*[@id="BytesReceived:3"]'}, ]


    def set_default(self):
        self.alert_text.set("NOT CONNECTED.")

        self.ip_gateway_text.set("192.168.1.1") if self.ip_gateway_text.get(
        ) == "" else self.ip_gateway_text.set("")

        self.username_text.set("admin") if self.username_text.get(
        ) == "" else self.username_text.set("")

        self.password_text.set("admin") if self.password_text.get(
        ) == "" else self.password_text.set("")


    def connect(self):
        #PROVJERA VERZIJA CROME DRIVERA
        try:
            CHROMEDRIVER_PATH = ChromeDriverManager().install()
        except Exception:
            return "Neuspješno osvježavanje drajvera. Provjerite vašu internet konekciju."

        
        self.browser = webdriver.Chrome(
            CHROMEDRIVER_PATH, options=options)
        wait = WebDriverWait(self.browser, 10)
        self.browser.get("http://"+self.ip_gateway_text.get()+"/")

        try:
            assert "ZXHN H267N" in self.browser.page_source
        except AssertionError:
            return "Niste na ZXHN H267N ruteru, ili provjerite gateway IP adresu."

        # U SLUCAJU DA JE VEC LOGOVAN IZLOGUJ
        try:
            assert "Welcome to ZXHN H267N. Please login." in self.browser.page_source
        except AssertionError:

            logout = wait.until(
                EC.element_to_be_clickable((By.ID, "LogOffLnk")))
            logout.click()

        username = wait.until(
            EC.presence_of_element_located((By.ID, "Frm_Username")))
        username.send_keys(self.username_text.get())

        password = wait.until(
            EC.presence_of_element_located((By.ID, "Frm_Password")))
        password.send_keys(self.password_text.get())

        login = wait.until(
            EC.element_to_be_clickable((By.ID, 'LoginId')))
        login.click()

        try:
            assert "Username or password is error." not in self.browser.page_source
        except AssertionError:
            return "Neispravna kombinacija korisničko ime/šifra. Pokušajte ponovo."

        local_network = wait.until(
            EC.element_to_be_clickable((By.ID, "mmLocalnet")))
        local_network.click()

        wlan_network = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='WLANStatus']")))
        wlan_network.click()

        #OVO JE BITNOKOD MODEM SOFTVARE VERZIAJ
        self.controller.eth = self.eth

        return "KONEKCIJA USPOSTAVLJENA"

    def startGraph(self):
        self.controller.show_frame(GrafZTE_H267N)


class GrafZTE_H267N(Graf):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        #POSTO KOD ZTE NEMA OVERHEDAD
        self.size=0

    def back(self):
        self.stop_grafh()
        self.controller.show_frame(ModemZTE_H267N)

    def getEthInfo(self):

        try:
            html_down = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["down"])))
            self.novibajt_down = int(html_down.get_attribute("innerHTML"))

            html_up = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["up"])))
            self.novibajt_up = int(html_up.get_attribute("innerHTML"))

            btn_eth_refresh = self.wait.until(
                EC.element_to_be_clickable((By.ID, "LANStatus_Btn_refresh")))
            btn_eth_refresh.click()

        except StaleElementReferenceException as e:
            #print("STALEELEMENT ERROR OCURED"+str(e))
            pass
        except WebDriverException as e:
            #print("WEBDRIVER: "+str(e))
            pass

        except TimeoutException as e:
            messagebox.showerror("ERROR", "TIMEOUT ERROR OCURED: \n" + str(e))
            self.stop_grafh()
        return

    def getWlanInfo(self):

        try:
            html_down = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["down"])))
            self.novibajt_down = int(
                html_down.get_attribute("innerHTML"))

            html_up = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.eth[self.index]["up"])))
            self.novibajt_up = int(
                html_up.get_attribute("innerHTML"))

            btn_wlan_refresh = self.wait.until(
                EC.element_to_be_clickable((By.ID, "WLANStatus_Btn_refresh")))
            btn_wlan_refresh.click() 

        except StaleElementReferenceException as e:
            #print("STALEELEMENT ERROR OCURED"+str(e))
            pass
        except WebDriverException as e:
            #print("WEBDRIVER: "+str(e))
            pass

        except TimeoutException as e:
            messagebox.showerror("ERROR", "TIMEOUT ERROR OCURED: \n" + str(e))
            self.stop_grafh()
        return


app = MainApp()
#app.iconbitmap(r'.\\Eye.ico')
app.mainloop()
