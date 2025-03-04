import unittest
from typing import List
from poker import Carte, Main, comparer_mains, nom_combinaison
from jeu_poker import JeuPoker, parser_carte, afficher_main, afficher_resultat
import io
import sys
from unittest.mock import patch

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
        
        rang, couleur = parser_carte("VP")
        self.assertEqual(rang, "Valet")
        self.assertEqual(couleur, "Pique")
        
        rang, couleur = parser_carte("KT")
        self.assertEqual(rang, "Roi")
        self.assertEqual(couleur, "Trèfle")
    
    def test_parser_carte_invalide(self) -> None:
        with self.assertRaises(ValueError):
            parser_carte("Z")
        
        with self.assertRaises(ValueError):
            parser_carte("AZ")
        
        with self.assertRaises(ValueError):
            parser_carte("1C")
    
    def test_definir_main_joueur(self) -> None:
        jeu = JeuPoker()
        cartes = [
            Carte('As', 'Coeur'),
            Carte('Roi', 'Coeur'),
            Carte('Dame', 'Coeur'),
            Carte('Valet', 'Coeur'),
            Carte('10', 'Coeur')
        ]
        
        jeu.definir_main_joueur(cartes)
        self.assertEqual(jeu.main_joueur.cartes[0].rang, 'As')
        
        with self.assertRaises(ValueError):
            jeu.definir_main_joueur(cartes[:4])

    def test_creer_jeu(self) -> None:
        jeu = JeuPoker()
        cartes = jeu.creer_jeu()
        
        self.assertEqual(len(cartes), 52)
        
        # Vérifier que toutes les combinaisons sont présentes
        for couleur in ['Coeur', 'Carreau', 'Trèfle', 'Pique']:
            for rang in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']:
                self.assertTrue(any(c.rang == rang and c.couleur == couleur for c in cartes))
    
    def test_melanger(self) -> None:
        jeu = JeuPoker()
        jeu_original = jeu.creer_jeu().copy()
        jeu.melanger()

        self.assertNotEqual([str(c) for c in jeu_original], [str(c) for c in jeu.jeu])
        
        self.assertEqual(len(jeu.jeu), 52)
    
    def test_distribuer_main(self) -> None:
        jeu = JeuPoker()
        main = jeu.distribuer_main()
        
        self.assertEqual(len(main.cartes), 5)
        
        self.assertEqual(len(jeu.jeu), 47)
        
        jeu.jeu = jeu.jeu[:3]  # Ne garder que 3 cartes
        main = jeu.distribuer_main()
        
        self.assertEqual(len(jeu.jeu), 47)
    
    def test_nouvelle_partie(self) -> None:
        jeu = JeuPoker()
        jeu.nouvelle_partie()
        
        self.assertIsNotNone(jeu.main_ordi)
        self.assertEqual(len(jeu.main_ordi.cartes), 5)
        
        self.assertEqual(len(jeu.jeu), 47)
    
    def test_echanger_cartes_joueur(self) -> None:
        jeu = JeuPoker()
        cartes_joueur = [
            Carte('As', 'Coeur'),
            Carte('Roi', 'Coeur'),
            Carte('Dame', 'Coeur'),
            Carte('Valet', 'Coeur'),
            Carte('10', 'Coeur')
        ]
        jeu.definir_main_joueur(cartes_joueur)
        
        cartes_originales = [str(c) for c in jeu.main_joueur.cartes]
        
        jeu.echanger_cartes_joueur([1, 3])
        
        cartes_nouvelles = [str(c) for c in jeu.main_joueur.cartes]
        self.assertNotEqual(cartes_originales[1], cartes_nouvelles[1])
        self.assertNotEqual(cartes_originales[3], cartes_nouvelles[3])
        
        self.assertEqual(cartes_originales[0], cartes_nouvelles[0])
    
    def test_echanger_cartes_ordi_carte_haute(self) -> None:
        jeu = JeuPoker()
        cartes_ordi = [
            Carte('As', 'Coeur'),
            Carte('Roi', 'Trèfle'),
            Carte('9', 'Pique'),
            Carte('7', 'Coeur'),
            Carte('2', 'Carreau')
        ]
        jeu.main_ordi = Main(cartes_ordi)
        
        cartes_originales = [str(c) for c in jeu.main_ordi.cartes]
        
        jeu.echanger_cartes_ordi()
        
        cartes_nouvelles = [str(c) for c in jeu.main_ordi.cartes]
        self.assertNotEqual(cartes_originales[4], cartes_nouvelles[4])
    
    def test_echanger_cartes_ordi_paire(self) -> None:
        jeu = JeuPoker()
        cartes_ordi = [
            Carte('10', 'Coeur'),
            Carte('10', 'Trèfle'),
            Carte('Roi', 'Pique'),
            Carte('4', 'Coeur'),
            Carte('3', 'Carreau')
        ]
        jeu.main_ordi = Main(cartes_ordi)
        
        cartes_originales = [str(c) for c in jeu.main_ordi.cartes]
        
        jeu.echanger_cartes_ordi()
        
        cartes_nouvelles = [c.rang for c in jeu.main_ordi.cartes]
        self.assertEqual(cartes_nouvelles.count('10'), 2)
    
    def test_echanger_cartes_ordi_bonne_main(self) -> None:
        jeu = JeuPoker()
        cartes_ordi = [
            Carte('9', 'Coeur'),
            Carte('8', 'Trèfle'),
            Carte('7', 'Pique'),
            Carte('6', 'Carreau'),
            Carte('5', 'Coeur')
        ]
        jeu.main_ordi = Main(cartes_ordi)
        
        cartes_originales = [str(c) for c in jeu.main_ordi.cartes]
        
        jeu.echanger_cartes_ordi()
        
        cartes_nouvelles = [str(c) for c in jeu.main_ordi.cartes]
        self.assertEqual(cartes_originales, cartes_nouvelles)
    
    def test_determiner_gagnant(self) -> None:
        jeu = JeuPoker()
        
        jeu.main_joueur = Main([
            Carte('As', 'Coeur'),
            Carte('Roi', 'Coeur'),
            Carte('Dame', 'Coeur'),
            Carte('Valet', 'Coeur'),
            Carte('10', 'Coeur')
        ])
        
        jeu.main_ordi = Main([
            Carte('7', 'Coeur'),
            Carte('7', 'Carreau'),
            Carte('7', 'Trèfle'),
            Carte('7', 'Pique'),
            Carte('9', 'Coeur')
        ])
        
        self.assertEqual(jeu.determiner_gagnant(), "joueur")
        
        jeu.main_joueur, jeu.main_ordi = jeu.main_ordi, jeu.main_joueur
        
        self.assertEqual(jeu.determiner_gagnant(), "ordinateur")
        
        jeu.main_joueur = Main([
            Carte('As', 'Coeur'),
            Carte('Roi', 'Trèfle'),
            Carte('9', 'Pique'),
            Carte('7', 'Coeur'),
            Carte('2', 'Carreau')
        ])
        
        jeu.main_ordi = Main([
            Carte('As', 'Pique'),
            Carte('Roi', 'Coeur'),
            Carte('9', 'Trèfle'),
            Carte('7', 'Pique'),
            Carte('2', 'Trèfle')
        ])
        
        self.assertEqual(jeu.determiner_gagnant(), "égalité")
        
        jeu.main_joueur = None
        with self.assertRaises(ValueError):
            jeu.determiner_gagnant()
        
    def test_afficher_main(self) -> None:
        main = Main([
            Carte('As', 'Coeur'),
            Carte('Roi', 'Coeur'),
            Carte('Dame', 'Coeur'),
            Carte('Valet', 'Coeur'),
            Carte('10', 'Coeur')
        ])
        
        self.assertEqual(afficher_main(main), "As♥ Roi♥ Dame♥ Valet♥ 10♥")
        
        self.assertEqual(afficher_main(main, True), "? ? ? ? ?")
    
    def test_afficher_resultat(self) -> None:
        jeu = JeuPoker()
        
        jeu.main_joueur = Main([
            Carte('As', 'Coeur'),
            Carte('Roi', 'Coeur'),
            Carte('Dame', 'Coeur'),
            Carte('Valet', 'Coeur'),
            Carte('10', 'Coeur')
        ])
        
        jeu.main_ordi = Main([
            Carte('7', 'Coeur'),
            Carte('7', 'Carreau'),
            Carte('7', 'Trèfle'),
            Carte('7', 'Pique'),
            Carte('9', 'Coeur')
        ])
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        afficher_resultat(jeu)
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("votre main: As♥ Roi♥ Dame♥ Valet♥ 10♥ - Quinte Flush Royale", output)
        self.assertIn("7♥", output)
        self.assertIn("7♦", output)
        self.assertIn("7♣", output)
        self.assertIn("7♠", output)
        self.assertIn("9♥", output)
        self.assertIn("Carré", output)
        self.assertIn("vous avez gagné!", output)
    
    
    @patch('builtins.input', side_effect=['AC', '10C', 'VC', 'RC', 'DC', 'non'])
    def test_integration_partie_complete(self, mock_input) -> None:
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        from jeu_poker import jouer
        
        jouer()
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Nouvelle partie de poker!", output)
        self.assertIn("Veuillez entrer votre main de 5 cartes:", output)
        self.assertIn("As♥", output)
        self.assertIn("10♥", output)
        self.assertIn("Valet♥", output)
        self.assertIn("Roi♥", output)
        self.assertIn("Dame♥", output)
        self.assertIn("resultat final:", output)
        self.assertIn("Merci d'avoir joué!", output)

if __name__ == '__main__':
    unittest.main() 