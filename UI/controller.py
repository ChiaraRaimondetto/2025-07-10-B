import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.categoria = None
        self.start=None
        self.end=None

    def handleCreaGrafo(self, e):
        d_min=self._view._dp1.value
        d_max=self._view._dp2.value
        if d_min and d_max and self.categoria:
            n,a=self._model.buildGraph(d_min,d_max,self.categoria)
            if n and a:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato con {n} nodi e {a} archi"))
            else:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Non siamo riusciti a creare il grafo"))
                self._view.update_page()
                return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare tutti i valori in input"))
            self._view.update_page()
            return
        self.fillDDStart()
        self.fillDDEnd()
        self._view.update_page()


    def handleBestProdotti(self, e):
        prodotti=self._model.bestProdotti()
        if prodotti:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Ecco la lista dei 5 prodotti più venduti:"))

            for p in prodotti:
                self._view.txt_result.controls.append(ft.Text(f"{p[0]} with score {p[1]}"))
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non siamo riusciti a trovare i prodotti piuù venduti"))
            self._view.update_page()
            return
        self._view.update_page()





    def handleCercaCammino(self, e):
        lun=self._view._txtInLun.value
        if lun and self.start and self.end:
            try:
                intLun=int(lun)
                cammin,pesi=self._model.bestPath(self.start,self.end,intLun)
                if cammin and pesi:
                    self._view.txt_result.controls.clear()
                    self._view.txt_result.controls.append(ft.Text(f"Cammino creato! Lunghezza: {len(cammin)} Peso: {pesi}"))
                    for c in cammin:
                        self._view.txt_result.controls.append(
                            ft.Text(f"{c.product_name}"))
                else:
                    self._view.txt_result.controls.clear()
                    self._view.txt_result.controls.append(ft.Text(f"Non siamo riusciti a creare il cammino"))
                    self._view.update_page()
                    return

            except ValueError:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Inserire un valore intero"))
                self._view.update_page()
                return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire e selezionare i valori in input"))
            self._view.update_page()
            return
        self._view.update_page()


    def fillDDCategorie(self):
        categorie=self._model.getCategorie()
        for c in categorie:
            self._view._ddcategory.options.append(ft.dropdown.Option(data=c,text=c.category_name,on_click=self.readcategoria))
    def readcategoria(self,e):
        if e.control.data is None:
            self.categoria=None
        else:
            self.categoria=e.control.data
    def fillDDStart(self):
        nodi=self._model.getNodi()
        for n in nodi:
            self._view._ddProdStart.options.append(ft.dropdown.Option(data=n,text=n.product_name,on_click=self.readStart))

    def fillDDEnd(self):
        nodi = self._model.getNodi()
        for n in nodi:
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(data=n, text=n.product_name, on_click=self.readEnd))

    def readStart(self, e):
        if e.control.data is None:
            self.start= None
        else:
            self.start = e.control.data

    def readEnd(self, e):
        if e.control.data is None:
            self.end = None
        else:
            self.end = e.control.data

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
