from typing import List, Tuple, Dict

COULEURS: List[str] = ['Coeur', 'Carreau', 'Trèfle', 'Pique']
RANGS: List[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
VALEURS: Dict[str, int] = {rang: i for i, rang in enumerate(RANGS)}

class Carte:
    def __init__(self, rang: str, couleur: str) -> None:
        self.rang: str = rang
        self.couleur: str = couleur
        self.valeur: int = VALEURS[rang]
    
    def __str__(self) -> str:
        symboles: Dict[str, str] = {'Coeur': '♥', 'Carreau': '♦', 'Trèfle': '♣', 'Pique': '♠'}
        return f"{self.rang}{symboles[self.couleur]}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __lt__(self, autre: 'Carte') -> bool:
        return self.valeur < autre.valeur
    
    def __eq__(self, autre: object) -> bool:
        if not isinstance(autre, Carte):
            return NotImplemented
        return self.valeur == autre.valeur and self.couleur == autre.couleur

class Main:
    def __init__(self, cartes: List[Carte]) -> None:
        if len(cartes) != 5:
            raise ValueError("Une main doit contenir exactement 5 cartes")
        self.cartes: List[Carte] = sorted(cartes, reverse=True, key=lambda carte: carte.valeur)
    
    def __str__(self) -> str:
        return " ".join(str(carte) for carte in self.cartes)
    
    def evaluer(self) -> Tuple[int, List[int]]:
        if self.est_quinte_flush_royale():
            return (9, [])
        elif self.est_quinte_flush():
            return (8, [self.get_valeur_quinte()])
        elif self.est_carre():
            valeurs = self.get_valeurs_par_groupes()
            return (7, [valeurs[0][0], valeurs[1][0]])
        elif self.est_full():
            valeurs = self.get_valeurs_par_groupes()
            return (6, [valeurs[0][0], valeurs[1][0]])
        elif self.est_couleur():
            return (5, [carte.valeur for carte in self.cartes])
        elif self.est_quinte():
            return (4, [self.get_valeur_quinte()])
        elif self.est_brelan():
            valeurs = self.get_valeurs_par_groupes()
            return (3, [valeurs[0][0]] + [valeurs[1][0], valeurs[2][0]])
        elif self.est_deux_paires():
            valeurs = self.get_valeurs_par_groupes()
            return (2, [valeurs[0][0], valeurs[1][0], valeurs[2][0]])
        elif self.est_paire():
            valeurs = self.get_valeurs_par_groupes()
            return (1, [valeurs[0][0]] + [v[0] for v in valeurs[1:]])
        else:
            return (0, [carte.valeur for carte in self.cartes])
    
    def get_valeurs_par_groupes(self) -> List[Tuple[int, int]]:
        valeurs: Dict[int, int] = {}
        for carte in self.cartes:
            valeurs[carte.valeur] = valeurs.get(carte.valeur, 0) + 1
        
        groupes: List[Tuple[int, int]] = []
        for val, count in sorted(valeurs.items(), key=lambda x: (-x[1], -x[0])):
            groupes.append((val, count))
        
        return groupes
    
    def est_meme_couleur(self) -> bool:
        return len(set(carte.couleur for carte in self.cartes)) == 1
    
    def est_quinte(self) -> bool:
        valeurs: List[int] = sorted([carte.valeur for carte in self.cartes])
        if valeurs == [0, 1, 2, 3, 12]:
            return True
        
        return valeurs == list(range(min(valeurs), max(valeurs) + 1))
    
    def get_valeur_quinte(self) -> int:
        valeurs: List[int] = sorted([carte.valeur for carte in self.cartes])
        if valeurs == [0, 1, 2, 3, 12]:
            return 3
        return max(carte.valeur for carte in self.cartes)
    
    def est_quinte_flush(self) -> bool:
        return self.est_meme_couleur() and self.est_quinte()
    
    def est_quinte_flush_royale(self) -> bool:
        return (self.est_meme_couleur() and 
                sorted([carte.valeur for carte in self.cartes]) == [8, 9, 10, 11, 12])
    
    def est_carre(self) -> bool:
        groupes = self.get_valeurs_par_groupes()
        return len(groupes) >= 1 and groupes[0][1] == 4
    
    def est_full(self) -> bool:
        groupes = self.get_valeurs_par_groupes()
        return len(groupes) >= 2 and groupes[0][1] == 3 and groupes[1][1] == 2
    
    def est_couleur(self) -> bool:
        return self.est_meme_couleur() and not self.est_quinte()
    
    def est_brelan(self) -> bool:
        groupes = self.get_valeurs_par_groupes()
        return len(groupes) >= 3 and groupes[0][1] == 3 and groupes[1][1] == 1
    
    def est_deux_paires(self) -> bool:
        groupes = self.get_valeurs_par_groupes()
        return len(groupes) >= 3 and groupes[0][1] == 2 and groupes[1][1] == 2
    
    def est_paire(self) -> bool:
        groupes = self.get_valeurs_par_groupes()
        return len(groupes) >= 4 and groupes[0][1] == 2 and groupes[1][1] == 1

def comparer_mains(main1: Main, main2: Main) -> int:
    eval1 = main1.evaluer()
    eval2 = main2.evaluer()
    
    if eval1[0] > eval2[0]:
        return 1
    elif eval1[0] < eval2[0]:
        return -1
    
    for v1, v2 in zip(eval1[1], eval2[1]):
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    
    return 0

def nom_combinaison(rang: int) -> str:
    noms: Dict[int, str] = {
        0: "Carte Haute",
        1: "Paire",
        2: "Deux Paires",
        3: "Brelan",
        4: "Quinte",
        5: "Couleur",
        6: "Full",
        7: "Carré",
        8: "Quinte Flush",
        9: "Quinte Flush Royale"
    }
    return noms.get(rang, "Inconnu")

if __name__ == "__main__":
    jeu: List[Carte] = [Carte(rang, couleur) for couleur in COULEURS for rang in RANGS]
    
    quinte_flush_royale: Main = Main([
        Carte('As', 'Coeur'),
        Carte('Roi', 'Coeur'),
        Carte('Dame', 'Coeur'),
        Carte('Valet', 'Coeur'),
        Carte('10', 'Coeur')
    ])
    
    carre: Main = Main([
        Carte('7', 'Coeur'),
        Carte('7', 'Carreau'),
        Carte('7', 'Trèfle'),
        Carte('7', 'Pique'),
        Carte('9', 'Coeur')
    ])
    
    print(f"Quinte Flush Royale: {quinte_flush_royale}")
    print(f"Type: {nom_combinaison(quinte_flush_royale.evaluer()[0])}")
    
    print(f"Carré: {carre}")
    print(f"Type: {nom_combinaison(carre.evaluer()[0])}")
    
    resultat: int = comparer_mains(quinte_flush_royale, carre)
    if resultat > 0:
        print("La Quinte Flush Royale gagne")
    elif resultat < 0:
        print("Le Carré gagne")
    else:
        print("Égalité")