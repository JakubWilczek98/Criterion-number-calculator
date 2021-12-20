class Case_4():
    def __init__(self, material, temp_plynu, temp_powierzchni, predkosc_charakterystyczna, wymiar_charakterystyczny, mycursor):
        self.przysp_ziemskie = 9.81
        self.material = material
        self.temp_plynu = temp_plynu
        self.temp_powierzchni = temp_powierzchni
        self.temp_charakterystyczna = round((temp_powierzchni + temp_plynu)/2)
        self.predkosc_charakterystyczna = predkosc_charakterystyczna
        self.wymiar_charakterystyczny = wymiar_charakterystyczny
        self.mycursor = mycursor


    def liczba_Prandtla(self):
        selection = 'SELECT liczba_prandtla FROM {} WHERE temperatura = {}'.format(self.material, self.temp_charakterystyczna)
        self.mycursor.execute(selection)
        myresult = self.mycursor.fetchall()
        self.liczba_Prandtla = [i[0] for i in myresult][0]
        return self.liczba_Prandtla

    def liczba_Reynoldsa(self):
        selection = 'SELECT wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}'.format(self.material, self.temp_charakterystyczna)
        self.mycursor.execute(selection)
        myresult = self.mycursor.fetchall()
        wsp_lepkosci_kinematycznej = ([i[0] for i in myresult][0]) / 10 ** 6
        self.liczba_Reynoldsa = (self.predkosc_charakterystyczna * self.wymiar_charakterystyczny) / wsp_lepkosci_kinematycznej
        return self.liczba_Reynoldsa

    def liczba_Grashofa(self):
        if self.material == 'water':
            selection = 'SELECT wspl_lepkosci_kinematycznej, wspl_rozszerzalnosci FROM {} WHERE temperatura = {}'.format(
                self.material, self.temp_charakterystyczna)
            self.mycursor.execute(selection)
            myresult = self.mycursor.fetchall()
            wsp_lepkosci_kinematycznej = ([i[0] for i in myresult][0]) / 10 ** 6
            wsp_rozszerzalnosci = ([i[1] for i in myresult][0]) / 10 ** 4
            liczba_Grashofa = ((wsp_rozszerzalnosci * self.przysp_ziemskie * self.wymiar_charakterystyczny ** 3) / wsp_lepkosci_kinematycznej ** 2) * (
                                      self.temp_powierzchni - self.temp_plynu)
        elif self.material == 'dry_air':
            selection = 'SELECT wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}'.format(self.material,
                                                                                                   self.temp_charakterystyczna)
            self.mycursor.execute(selection)
            myresult = self.mycursor.fetchall()
            wsp_lepkosci_kinematycznej = ([i[0] for i in myresult][0]) / 10 ** 6
            wsp_rozszerzalnosci = 1 / 373
            self.liczba_Grashofa = ((wsp_rozszerzalnosci * self.przysp_ziemskie * self.wymiar_charakterystyczny ** 3) / wsp_lepkosci_kinematycznej ** 2) * (
                           self.temp_powierzchni - self.temp_plynu)
        return self.liczba_Grashofa

    def liczba_Rayleigha(self):
        self.liczba_Rayleigha = self.liczba_Grashofa * self.liczba_Prandtla
        return self.liczba_Rayleigha

    def liczba_Nusselta(self):
        if self.liczba_Rayleigha < 0.001:
            C = 0.5
            n = 0
        elif self.liczba_Rayleigha >= 0.001 and self.liczba_Rayleigha < 500:
            C = 1.18
            n = 1 / 8
        elif self.liczba_Rayleigha >= 500 and self.liczba_Rayleigha < 20 * 10 ** 6:
            C = 0.54
            n = 1 / 4
        elif self.liczba_Rayleigha > 20 * 10 ** 6 and self.liczba_Rayleigha < 10 ** 13:
            C = 0.135
            n = 1 / 3
        self.liczba_Nusselta = C * (self.liczba_Rayleigha) ** (n)
        return self.liczba_Nusselta
