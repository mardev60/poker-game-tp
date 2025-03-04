import random
from typing import List, Optional, Union, Literal, Tuple, Dict
from poker import Carte, Main, comparer_mains, nom_combinaison, RANGS, COULEURS

class JeuPoker:
    def __init__(self) -> None:
        self.jeu: List[Carte] = self.creer_jeu()
        self.main_joueur: Optional[Main] = None
        self.main_ordi: Optional[Main] = None
    
    def creer_jeu(self) -> List[Carte]:
        return [Carte(rang, couleur) for couleur in COULEURS for rang in RANGS]
    
    def melanger(self) -> None:
        random.shuffle(self.jeu)
    
    def distribuer_main(self) -> Main:
        if len(self.jeu) < 5:
            self.jeu = self.creer_jeu()
            self.melanger()
        
        cartes: List[Carte] = []
        for _ in range(5):
            cartes.append(self.jeu.pop())
        
        return Main(cartes)
    
    def nouvelle_partie(self) -> None:
        self.jeu = self.creer_jeu()
        self.melanger()
        self.main_ordi = self.distribuer_main()
    
    def definir_main_joueur(self, cartes: List[Carte]) -> None:
        if len(cartes) != 5:
            raise ValueError("une main doit contenir exactement 5 cartes")
        self.main_joueur = Main(cartes)
    
    def echanger_cartes_joueur(self, indices: List[int]) -> None:
        if not indices or not self.main_joueur:
            return
        
        cartes: List[Carte] = list(self.main_joueur.cartes)
        for i in sorted(indices, reverse=True):
            if 0 <= i < 5:
                cartes.pop(i)
                cartes.insert(i, self.jeu.pop())
        
        self.main_joueur = Main(cartes)
    
    def echanger_cartes_ordi(self) -> None:
        if not self.main_ordi:
            return
            
        main: Main = self.main_ordi
        eval_main: int = main.evaluer()[0]
        cartes: List[Carte] = list(main.cartes)
        
        if eval_main >= 4:
            return
        
        indices_a_changer: List[int] = []
        
        if eval_main == 3:
            valeurs: Dict[int, List[int]] = {}
            for i, carte in enumerate(cartes):
                valeurs[carte.valeur] = valeurs.get(carte.valeur, []) + [i]
            
            for val, indices in valeurs.items():
                if len(indices) == 3:
                    continue
                indices_a_changer.extend(indices)
        
        elif eval_main == 2:
            valeurs: Dict[int, List[int]] = {}
            for i, carte in enumerate(cartes):
                valeurs[carte.valeur] = valeurs.get(carte.valeur, []) + [i]
            
            for val, indices in valeurs.items():
                if len(indices) == 1:
                    indices_a_changer.extend(indices)
        
        elif eval_main == 1:
            valeurs: Dict[int, List[int]] = {}
            for i, carte in enumerate(cartes):
                valeurs[carte.valeur] = valeurs.get(carte.valeur, []) + [i]
            
            for val, indices in valeurs.items():
                if len(indices) == 1:
                    indices_a_changer.extend(indices)
        
        else:
            for i, carte in enumerate(cartes):
                if carte.valeur < 10:
                    indices_a_changer.append(i)
        
        for i in sorted(indices_a_changer, reverse=True):
            cartes.pop(i)
            cartes.insert(i, self.jeu.pop())
        
        self.main_ordi = Main(cartes)
    
    def determiner_gagnant(self) -> Literal["joueur", "ordinateur", "égalité"]:
        if not self.main_joueur or not self.main_ordi:
            raise ValueError("les mains ne sont pas initialisées")
            
        resultat: int = comparer_mains(self.main_joueur, self.main_ordi)
        
        if resultat > 0:
            return "joueur"
        elif resultat < 0:
            return "ordinateur"
        else:
            return "égalité"

def afficher_main(main: Main, cacher: bool = False) -> str:
    if cacher:
        return "? ? ? ? ?"
    
    return str(main)

def afficher_resultat(jeu: JeuPoker) -> None:
    if not jeu.main_joueur or not jeu.main_ordi:
        raise ValueError("les mains ne sont pas initialisées")
        
    print("\nresultat final:")
    print(f"votre main: {afficher_main(jeu.main_joueur)} - {nom_combinaison(jeu.main_joueur.evaluer()[0])}")
    print(f"main de l'ordinateur: {afficher_main(jeu.main_ordi)} - {nom_combinaison(jeu.main_ordi.evaluer()[0])}")
    
    gagnant: str = jeu.determiner_gagnant()
    if gagnant == "joueur":
        print("vous avez gagné!")
    elif gagnant == "ordinateur":
        print("l'ordinateur a gagné!")
    else:
        print("egalité!")

def parser_carte(texte: str) -> Tuple[str, str]:
    texte = texte.strip()
    
    parties = texte.split()
    if len(parties) == 2:
        rang, couleur = parties
    else:
        if len(texte) < 2:
            raise ValueError(f"format de carte invalide: {texte}")
        rang = texte[:-1]
        couleur_abbr = texte[-1]
        
        conversion_couleur = {
            'C': 'Coeur', 'H': 'Coeur', '♥': 'Coeur',
            'K': 'Carreau', 'D': 'Carreau', '♦': 'Carreau',
            'T': 'Trèfle', 'S': 'Trèfle', '♣': 'Trèfle',
            'P': 'Pique', 'S': 'Pique', '♠': 'Pique'
        }
        
        if couleur_abbr in conversion_couleur:
            couleur = conversion_couleur[couleur_abbr]
        else:
            raise ValueError(f"Couleur non reconnue: {couleur_abbr}")
    
    conversion_rang = {
        'A': 'As', 'J': 'Valet', 'V': 'Valet', 
        'Q': 'Dame', 'D': 'Dame', 
        'K': 'Roi', 'R': 'Roi'
    }
    
    if rang in conversion_rang:
        rang = conversion_rang[rang]
    
    if rang not in RANGS:
        raise ValueError(f"Rang non valide: {rang}")
    
    if couleur not in COULEURS:
        raise ValueError(f"Couleur non valide: {couleur}")
    
    return rang, couleur

def saisir_carte() -> Carte:
    while True:
        try:
            texte = input("Entrez une carte (ex: AC, 10C, VP): ")
            rang, couleur = parser_carte(texte)
            return Carte(rang, couleur)
        except ValueError as e:
            print(f"Erreur: {e}")
            print("Formats acceptés: 'AC', '10C', 'VP', etc.")

def jouer() -> None:
    jeu: JeuPoker = JeuPoker()
    
    while True:
        jeu.nouvelle_partie()
        
        print("\nNouvelle partie de poker!")
        print("Veuillez entrer votre main de 5 cartes:")
        
        cartes_joueur: List[Carte] = []
        for i in range(5):
            print(f"Carte {i+1}/5:")
            carte = saisir_carte()
            cartes_joueur.append(carte)
        
        try:
            jeu.definir_main_joueur(cartes_joueur)
            print(f"\nVotre main: {afficher_main(jeu.main_joueur)}")
            print(f"Main de l'ordinateur: {afficher_main(jeu.main_ordi)}")
            
            afficher_resultat(jeu)
            
            print("\nVoulez-vous jouer une autre partie? (oui/non)")
            if input("> ").strip().lower() != "oui":
                break
        except ValueError as e:
            print(f"Erreur: {e}")
    
    print("Merci d'avoir joué!")

if __name__ == "__main__":
    jouer()