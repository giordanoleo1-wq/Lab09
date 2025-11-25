from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO

class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        # TODO: Aggiungere eventuali altri attributi

        # Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        """
            Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.
            --> Ogni Tour ha un set di Attrazione.
            --> Ogni Attrazione ha un set di Tour.
        """

        # TODO
        relazioni = TourDAO.get_tour_attrazioni()

        if relazioni is None:
            return


        for riga in relazioni:
            id_tour = riga['id_tour']
            id_attrazione = riga['id_attrazione']

            tour = self.tour_map[id_tour]
            attrazione = self.attrazioni_map[id_attrazione]

            #si crei la relazione bidirezionale

            tour.attrazioni.add(attrazione)
            attrazione.tour.add(tour)



    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        :param id_regione: id della regione
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        # TODO
        #si filtrino solo i tour della regione scelta dall'utente

        tour_regione = [tour for tour in self.tour_map.values() if tour.id_regione == id_regione]

        #inizializzo la ricorsione
        self._ricorsione(start_index=0, pacchetto_parziale=[], durata_corrente=0,
                         costo_corrente=0.0, valore_corrente=0,attrazioni_usate=set(),
                         lista_tour = tour_regione, max_giorni = max_giorni, max_budget = max_budget)

        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list,
                    durata_corrente: int, costo_corrente: float,
                    valore_corrente: int, attrazioni_usate: set,
                    lista_tour: list, max_giorni: int, max_budget: float):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno

        #caso migliore trovato
        if valore_corrente > self._valore_ottimo:
            self._valore_ottimo = valore_corrente
            self._pacchetto_ottimo = pacchetto_parziale.copy() #copy.deepcopy(pacchetto_parziale)
            self._costo = costo_corrente

        #ciclo sui tour che sono disponibili
        for i in range(start_index, len(lista_tour)):
            tour = lista_tour[i]

            #VINCOLI

            #vincolo sulla durata

            if max_giorni is not None:
                if durata_corrente + tour.durata_giorni > max_giorni:
                    continue

            #vincolo sul costo

            if max_budget is not None:
                if costo_corrente + float(tour.costo) > max_budget:
                    continue

            #vincolo affinchè le attrazioni siano uniche

            if tour.attrazioni.intersection(attrazioni_usate):
                continue

            # SCELTA DEL TOUR

            valore_tour = 0
            for a in tour.attrazioni:
                valore_tour += a.valore_culturale

            nuovo_valore = valore_tour + valore_corrente

            pacchetto_parziale.append(tour)
            nuove_attrazioni = attrazioni_usate.copy()
            nuove_attrazioni.update(tour.attrazioni)

            #RICORSIONE
            self._ricorsione(i+1,pacchetto_parziale,durata_corrente + tour.durata_giorni,
                             costo_corrente + float(tour.costo), nuovo_valore,nuove_attrazioni,
                             lista_tour, max_giorni, max_budget)

            #backtracking
            pacchetto_parziale.pop()
















