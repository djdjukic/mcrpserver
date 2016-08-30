# -*- coding: utf8 -*-

from fpdf import FPDF
from datetime import date
import locale


class PDF(FPDF):
    def __init__(self):
        super(PDF, self).__init__('P', 'mm', 'A4')
        self.add_font('DejaVu Sans', '', 'font/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu Sans', 'B', 'font/DejaVuSans-Bold.ttf', uni=True)
        self.add_font('DejaVu Sans', 'EL', 'font/DejaVuSans-ExtraLight.ttf', uni=True)

    def header(self):
        self.image('logo.png', 10, 10, 48)
        self.set_font('DejaVu Sans', 'EL', 11)
        self.cell(50)
        self.multi_cell(80, 5.5, 'LABORATORY\\HOSPITAL NAME\nADDITIONAL INFO\nADDRESS')
        self.set_xy(-80, 10)
        self.cell(70, 16, 'LABORATORY ANALYSIS', 1, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-16)
        self.set_font('DejaVu Sans', 'EL', 8)
        self.multi_cell(0, 4, 'PHONE 1\nPHONE 2\nPHONE 3')
        self.set_y(-15)
        self.cell(0, 10, 'Page: ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        self.set_y(-15)
        self.cell(0, 10, 'E-mail: jsmith@example.com', 0, 0, 'R')

    def generate(self, data, strings, signature):
        self.alias_nb_pages()
        self.add_page()

        self.set_font('DejaVu Sans', 'B', 14)
        self.cell(0, 20, 'IZVEŠTAJ', 0, 1, 'C')

        self.set_font('DejaVu Sans', '', 10)

        self.cell(50, 8, 'First name: ' + data['first_name'], 1, 0)
        self.cell(0, 8, 'Last name: ' + data['last_name'], 1, 1)
        if data['sex'] == 3:
            self.cell(50, 8, 'Sex: M', 1, 0)
        else:
            self.cell(50, 8, 'Sex: F', 1, 0)
        self.cell(90, 8, 'SS number: ' + data['jmbg'], 1, 0)
        self.cell(0, 8, 'Custom info 1: ' + data['custom_1'], 1, 1)
        self.cell(50, 8, 'Tel.: ' + data['phone_no'], 1, 0)
        self.cell(90, 8, 'E-mail: ' + data['email_address'], 1, 0)
        self.cell(0, 8, 'Custom info 2: ' + data['custom_2'], 1, 1)
        self.cell(80, 8, 'Address: ' + data['address'], 1, 0)
        self.cell(60, 8, u'Date of birth: ' + data['date_of_birth'], 1, 0)
        self.cell(0, 8, 'Custom info 3: ' + data['custom_3'], 1, 1)

        for item in strings:
            if item[0] == 'labels':
                self.set_font('DejaVu Sans', 'B', 10)
                self.cell(50, 8, item[1], 1, 0, 'C')
                self.cell(30, 8, item[2], 1, 0, 'C')
                self.cell(30, 8, item[4], 1, 0, 'C')
                self.cell(0, 8, item[3], 1, 1, 'C')
                self.set_font('DejaVu Sans', '', 10)
            elif item[0] == 'title':
                self.set_font('DejaVu Sans', 'B', 10)
                self.cell(0, 8, item[1], 0, 1)
                self.set_font('DejaVu Sans', '', 10)
            elif item[0] in data:
                self.cell(50, 8, item[1], 1, 0)
                if item[0] == 'crp' and data[item[0]] < 2:
                    self.cell(30, 8, '< 2', 1, 0, 'R')
                else:
                    self.cell(30, 8, locale.format('%.'+item[5]+'f', data[item[0]]), 1, 0, 'R')
                self.cell(30, 8, item[4], 1, 0)
                self.cell(0, 8, item[data['sex']], 1, 1, 'C')

        self.cell(0, 8, '', 0, 1)
        self.cell(120, 6, 'Location,', 0, 0)
        self.cell(80, 6, 'Analyzed by:', 0, 1)
        self.cell(120, 6, 'Date: ' + date.today().strftime('%d.%m.%Y.'), 0, 0)

        if signature:
            self.set_font('DejaVu Sans', '', 8)
            self.cell(0, 10, '________________________________________________', 0, 1, 'R')
            self.cell(0, 6, 'M.P.', 0, 0, 'C')
        else:
            self.cell(80, 6, 'NAME OF TECHNICIAN', 0, 1)
            self.set_font('DejaVu Sans', '', 8)
            self.cell(0, 18, 'This is a computer-generated document and does not require a signature.', 0, 1)
