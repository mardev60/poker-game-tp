import unittest
from typing import List
from poker import Carte, Main, comparer_mains, nom_combinaison
from jeu_poker import JeuPoker, parser_carte

class TestPoker(unittest.TestCase):
    def test_creation_carte(self) -> None:
        carte: Carte = Carte('As', 'Coeur')
        self.assertEqual(carte.rang, 'As')
        self.assertEqual(carte.couleur, 'Coeur')
        self.assertEqual(carte.valeur, 12)
        
        carte2: Carte = Carte('2', 'Pique')
        self.assertEqual(carte2.rang, '2')
        self.assertEqual(carte2.couleur, 'Pique')
        self.assertEqual(carte2.valeur, 0)
    
    def test_comparaison_cartes(self) -> None:
        as_coeur: Carte = Carte('As', 'Coeur')
        roi_coeur: Carte = Carte('Roi', 'Coeur')
        as_pique: Carte = Carte('As', 'Pique')
        
        self.assertTrue(as_coeur > roi_coeur)
        self.assertFalse(roi_coeur > as_coeur)
        self.assertEqual(as_coeur, as_coeur)
        self.assertNotEqual(as_coeur, as_pique)
    
    def test_quinte_flush_royale(self) -> None:
        main: Main = Main([
            Carte('As', 'Coeur'),
            Carte('Roi', 'Coeur'),
            Carte('Dame', 'Coeur'),
            Carte('Valet', 'Coeur'),
            Carte('10', 'Coeur')
        ])
        
        self.assertTrue(main.est_quinte_flush_royale())
        self.assertEqual(main.evaluer()[0], 9)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Quinte Flush Royale")
    
    def test_quinte_flush(self) -> None:
        main: Main = Main([
            Carte('9', 'Pique'),
            Carte('8', 'Pique'),
            Carte('7', 'Pique'),
            Carte('6', 'Pique'),
            Carte('5', 'Pique')
        ])
        
        self.assertTrue(main.est_quinte_flush())
        self.assertFalse(main.est_quinte_flush_royale())
        self.assertEqual(main.evaluer()[0], 8)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Quinte Flush")
    
    def test_carre(self) -> None:
        main: Main = Main([
            Carte('7', 'Coeur'),
            Carte('7', 'Carreau'),
            Carte('7', 'Trèfle'),
            Carte('7', 'Pique'),
            Carte('9', 'Coeur')
        ])
        
        self.assertTrue(main.est_carre())
        self.assertEqual(main.evaluer()[0], 7)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Carré")
    
    def test_full(self) -> None:
        main: Main = Main([
            Carte('10', 'Coeur'),
            Carte('10', 'Carreau'),
            Carte('10', 'Pique'),
            Carte('4', 'Coeur'),
            Carte('4', 'Trèfle')
        ])
        
        self.assertTrue(main.est_full())
        self.assertEqual(main.evaluer()[0], 6)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Full")
    
    def test_couleur(self) -> None:
        main: Main = Main([
            Carte('As', 'Trèfle'),
            Carte('10', 'Trèfle'),
            Carte('7', 'Trèfle'),
            Carte('6', 'Trèfle'),
            Carte('2', 'Trèfle')
        ])
        
        self.assertTrue(main.est_couleur())
        self.assertEqual(main.evaluer()[0], 5)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Couleur")
    
    def test_quinte(self) -> None:
        main: Main = Main([
            Carte('9', 'Coeur'),
            Carte('8', 'Trèfle'),
            Carte('7', 'Pique'),
            Carte('6', 'Carreau'),
            Carte('5', 'Coeur')
        ])
        
        self.assertTrue(main.est_quinte())
        self.assertEqual(main.evaluer()[0], 4)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Quinte")
    
    def test_quinte_as_bas(self) -> None:
        main: Main = Main([
            Carte('As', 'Coeur'),
            Carte('2', 'Trèfle'),
            Carte('3', 'Pique'),
            Carte('4', 'Carreau'),
            Carte('5', 'Coeur')
        ])
        
        self.assertTrue(main.est_quinte())
        self.assertEqual(main.evaluer()[0], 4)
        self.assertEqual(main.get_valeur_quinte(), 3)
    
    def test_brelan(self) -> None:
        main: Main = Main([
            Carte('8', 'Coeur'),
            Carte('8', 'Carreau'),
            Carte('8', 'Pique'),
            Carte('Roi', 'Coeur'),
            Carte('3', 'Carreau')
        ])
        
        self.assertTrue(main.est_brelan())
        self.assertEqual(main.evaluer()[0], 3)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Brelan")
    
    def test_deux_paires(self) -> None:
        main: Main = Main([
            Carte('Valet', 'Coeur'),
            Carte('Valet', 'Trèfle'),
            Carte('4', 'Pique'),
            Carte('4', 'Coeur'),
            Carte('As', 'Carreau')
        ])
        
        self.assertTrue(main.est_deux_paires())
        self.assertEqual(main.evaluer()[0], 2)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Deux Paires")
    
    def test_paire(self) -> None:
        main: Main = Main([
            Carte('10', 'Coeur'),
            Carte('10', 'Trèfle'),
            Carte('Roi', 'Pique'),
            Carte('4', 'Coeur'),
            Carte('3', 'Carreau')
        ])
        
        self.assertTrue(main.est_paire())
        self.assertEqual(main.evaluer()[0], 1)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Paire")
    
    def test_carte_haute(self) -> None:
        main: Main = Main([
            Carte('As', 'Coeur'),
            Carte('Roi', 'Trèfle'),
            Carte('9', 'Pique'),
            Carte('7', 'Coeur'),
            Carte('2', 'Carreau')
        ])
        
        self.assertFalse(main.est_paire())
        self.assertFalse(main.est_brelan())
        self.assertFalse(main.est_quinte())
        self.assertFalse(main.est_couleur())
        self.assertEqual(main.evaluer()[0], 0)
        self.assertEqual(nom_combinaison(main.evaluer()[0]), "Carte Haute")
    
    def test_comparaison_mains(self) -> None:
        qfr: Main = Main([
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
        
        self.assertEqual(comparer_mains(qfr, carre), 1)
        self.assertEqual(comparer_mains(carre, qfr), -1)
        
        deux_paires1: Main = Main([
            Carte('Valet', 'Coeur'),
            Carte('Valet', 'Trèfle'),
            Carte('4', 'Pique'),
            Carte('4', 'Coeur'),
            Carte('As', 'Carreau')
        ])
        
        deux_paires2: Main = Main([
            Carte('Valet', 'Pique'),
            Carte('Valet', 'Carreau'),
            Carte('4', 'Trèfle'),
            Carte('4', 'Carreau'),
            Carte('Roi', 'Coeur')
        ])
        
        self.assertEqual(comparer_mains(deux_paires1, deux_paires2), 1)
        
        deux_paires3: Main = Main([
            Carte('Dame', 'Coeur'),
            Carte('Dame', 'Trèfle'),
            Carte('4', 'Pique'),
            Carte('4', 'Coeur'),
            Carte('2', 'Carreau')
        ])
        
        self.assertEqual(comparer_mains(deux_paires3, deux_paires2), 1)
    
    def test_egalite(self) -> None:
        main1: Main = Main([
            Carte('As', 'Coeur'),
            Carte('Roi', 'Trèfle'),
            Carte('9', 'Pique'),
            Carte('7', 'Coeur'),
            Carte('2', 'Carreau')
        ])
        
        main2: Main = Main([
            Carte('As', 'Pique'),
            Carte('Roi', 'Coeur'),
            Carte('9', 'Trèfle'),
            Carte('7', 'Pique'),
            Carte('2', 'Trèfle')
        ])
        
        self.assertEqual(comparer_mains(main1, main2), 0)
    
    def test_parser_carte(self) -> None:
        rang, couleur = parser_carte("As Coeur")
        self.assertEqual(rang, "As")
        self.assertEqual(couleur, "Coeur")
        
        rang, couleur = parser_carte("10C")
        self.assertEqual(rang, "10")
        self.assertEqual(couleur, "Coeur")
        
        rang, couleur = parser_carte("V♠")
        self.assertEqual(rang, "Valet")
        self.assertEqual(couleur, "Pique")
        
        rang, couleur = parser_carte("A Pique")
        self.assertEqual(rang, "As")
        self.assertEqual(couleur, "Pique")
        
        rang, couleur = parser_carte("K Trèfle")
        self.assertEqual(rang, "Roi")
        self.assertEqual(couleur, "Trèfle")
        
        rang, couleur = parser_carte("  Dame  Carreau  ")
        self.assertEqual(rang, "Dame")
        self.assertEqual(couleur, "Carreau")
    
    def test_parser_carte_invalide(self) -> None:
        with self.assertRaises(ValueError):
            parser_carte("")
        
        with self.assertRaises(ValueError):
            parser_carte("Z Coeur")
        
        with self.assertRaises(ValueError):
            parser_carte("As Jaune")
    
    def test_definir_main_joueur(self) -> None:
        jeu = JeuPoker()
        
        cartes: List[Carte] = [
            Carte('As', 'Coeur'),
            Carte('Roi', 'Coeur'),
            Carte('Dame', 'Coeur'),
            Carte('Valet', 'Coeur'),
            Carte('10', 'Coeur')
        ]
        
        jeu.definir_main_joueur(cartes)
        self.assertEqual(jeu.main_joueur.cartes[0].rang, 'As')
        self.assertEqual(jeu.main_joueur.cartes[0].couleur, 'Coeur')
        
        with self.assertRaises(ValueError):
            jeu.definir_main_joueur(cartes[:4])

if __name__ == '__main__':
    unittest.main() 