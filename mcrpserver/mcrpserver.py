# -*- coding: utf8 -*-

import locale
import tkFileDialog
import tkMessageBox
from Tkinter import *
from datetime import date
from os import startfile, mkdir, path, getenv
from ttk import *

from serial.tools import list_ports

from exporter import PDF
from server import *

locale.setlocale(locale.LC_ALL, '')

application_name = "MCRP server"
version = '2.1.1'


def receive_cb():
    data = Data()
    checksum = data.get(port_chooser.get())
    # checksum = data.open_file('TEST.txt')
    if not checksum:
        tkMessageBox.showerror('Error', 'An error has occurred while receiving data from the analyzer. '
                                        'Try choosing a different serial port and make sure the cable is connected.')
        return
    if checksum != int(data.raw[str(chr(0xfd))], 16):
        tkMessageBox.showerror('Error', 'The calculated checksum does not match the one received with the data. '
                                        'The serial cable may be damaged or too long.')
        return

    data.parse()

    pdf = PDF()

    if sedimentation_bool.get():
        data.data['sedimentation'] = float(sedimentation.get())
        sedimentation.delete(0, END)
        sedimentation_bool.set(0)
        sedimentation.config(state=DISABLED)

    data.data['first_name'] = unicode(first_name.get())
    data.data['last_name'] = unicode(last_name.get())
    data.data['sex'] = int(sex.get())
    data.data['ssn'] = unicode(ssn.get())
    data.data['custom_1'] = unicode(custom_1.get())
    data.data['phone_no'] = unicode(phone_no.get())
    data.data['email_address'] = unicode(email_address.get())
    data.data['custom_2'] = unicode(custom_2.get())
    data.data['address'] = unicode(address.get())
    data.data['date_of_birth'] = unicode(date_of_birth.get())
    data.data['custom_3'] = unicode(custom_3.get())

    pdf.generate(data.data, strings, signature.get())

    filename = tkFileDialog.asksaveasfilename(defaultextension=".pdf",
                                              filetypes=(('Portable Document Format', '.pdf'),),
                                              initialdir=day_path,
                                              initialfile=first_name.get() + ' ' + last_name.get())

    clear_fields()

    pdf.output(filename, 'F')
    startfile(filename)


def clear_fields():
    first_name.delete(0, END)
    last_name.delete(0, END)
    address.delete(0, END)
    ssn.delete(0, END)
    phone_no.delete(0, END)
    email_address.delete(0, END)
    date_of_birth.delete(0, END)
    custom_1.delete(0, END)
    custom_2.delete(0, END)
    custom_3.delete(0, END)
    custom_3.insert(0, date.today().strftime('%d.%m.%Y.'))

save_path = path.expanduser('~\\Documents\\Results')
day_path = path.expanduser(save_path + '\\' + date.today().isoformat())
appdata_path = getenv('APPDATA') + '\\' + application_name + '\\'
try:
    mkdir(save_path)
except OSError:
    pass
try:
    mkdir(day_path)
except OSError:
    pass
try:
    mkdir(appdata_path)
except OSError:
    pass

with open('r_values.txt', 'r') as f:
    strings = tuple(line.strip('\r\n').split(';') for line in f)

top = Tk()

com_ports = list(port[0] for port in list_ports.comports())
if not com_ports:
    top.withdraw()
    tkMessageBox.showerror('Error', 'No serial ports were found. '
                                    'If you are using a USB-serial converter, make sure it\'s plugged in.')
    sys.exit()

top.title("MCRP server")
top.minsize(350, 0)
top.resizable(True, False)
top.iconbitmap('icon.ico')


def about():
    about_w = Toplevel()
    about_w.iconbitmap('icon.ico')
    about_w.resizable(False, False)
    about_w.title('About...')
    about_gif = PhotoImage(file="about.gif")
    label = Label(about_w, image=about_gif)
    label.image = about_gif
    label.grid(column=0, row=0, rowspan=2, pady=24)
    msg = Message(about_w, text='MCRP server\n'
                                'version ' + version + '\n\n'
                                '© 2016 Đorđe Đukić\n'
                                'dj@mmcentar.com', aspect=300)
    msg.grid(column=1, row=0, padx=24, pady=24)
    button = Button(about_w, text='OK', command=about_w.destroy)
    button.grid(column=1, row=1)

menubar = Menu(top)
top.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Fajl', menu=filemenu, underline=0)
filemenu.add_command(label='Zatvori', command=top.quit)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Pomoć', menu=helpmenu, underline=0)
helpmenu.add_command(label='O programu', command=about)


receive_frame = LabelFrame(top, text="Primanje")
receive_frame.grid(column=0, row=0, padx=5, pady=5, sticky=N + S + E + W)

port_chooser = Combobox(receive_frame, state='readonly', values=com_ports)
port_chooser.set(com_ports[0])
port_chooser.grid(column=1, row=0, sticky=E + W, padx=5, pady=5)

Label(receive_frame, text='Komunikacioni port').grid(column=0, row=0, sticky=E)

r_button = Button(receive_frame, text='Primi podatke', command=receive_cb)
r_button.grid(column=2, row=0, padx=5, pady=5)


data_frame = LabelFrame(top, text="Lični podaci")
data_frame.grid(column=0, row=1, padx=5, pady=5, sticky=N + S + E + W)


sex_frame = Frame(data_frame)
sex_frame.grid(column=0, row=0, columnspan=4)

Label(sex_frame, text='Pol').grid(column=0, row=0)
sex = IntVar()
Radiobutton(sex_frame, text="Ž", variable=sex, value=2).grid(column=1, row=0)
Radiobutton(sex_frame, text="M", variable=sex, value=3).grid(column=2, row=0)


def labeled_entry(frame, label, l_column, l_row):
    Label(frame, text=label).grid(column=l_column, row=l_row, sticky=E)
    entry = Entry(frame)
    entry.grid(column=l_column + 1, row=l_row, sticky=E + W, padx=5, pady=5)
    return entry

first_name = labeled_entry(data_frame, 'First name', 0, 1)
last_name = labeled_entry(data_frame, 'Last name', 2, 1)
address = labeled_entry(data_frame, 'Address', 0, 2)
ssn = labeled_entry(data_frame, 'SS number', 2, 2)
phone_no = labeled_entry(data_frame, 'Telephone number', 0, 3)
email_address = labeled_entry(data_frame, 'E-mail address', 2, 3)
date_of_birth = labeled_entry(data_frame, 'Date of birth', 0, 4)
custom_1 = labeled_entry(data_frame, 'Custom info 1', 2, 4)
custom_2 = labeled_entry(data_frame, 'Custom info 2', 0, 5)
custom_3 = labeled_entry(data_frame, 'Custom info 3', 2, 5)
custom_3.insert(0, date.today().strftime('%Y-&m-&d'))


def sedimentation_cb():
    if sedimentation_bool.get() == 1:
        sedimentation.config(state=NORMAL)
    else:
        sedimentation.config(state=DISABLED)

sedimentation_bool = IntVar()
sedimentation_box = Checkbutton(data_frame, text='Sedimentation', var=sedimentation_bool, command=sedimentation_cb)
sedimentation_box.grid(column=0, row=6, sticky=E)
sedimentation = Entry(data_frame, state=DISABLED)
sedimentation.grid(column=1, row=6, sticky=E + W, padx=5, pady=5)


signature = IntVar()
signature_box = Checkbutton(data_frame, text='Signature line', var=signature)
signature_box.grid(column=2, row=6, columnspan=2)


top.columnconfigure(0, weight=1)
for y in range(2):
    top.rowconfigure(y, weight=y % 2)

for x in range(4):
    data_frame.columnconfigure(x, weight=x % 2)
for y in range(7):
    data_frame.rowconfigure(y, weight=1)

for x in range(3):
    receive_frame.columnconfigure(x, weight=1)
receive_frame.rowconfigure(0, weight=1)

top.mainloop()
