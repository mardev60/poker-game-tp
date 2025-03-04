# Projet Poker

Ce projet implémente un jeu de poker en Python, avec les règles standard du poker à 5 cartes.

## Structure du projet

- `poker.py` : Contient les classes et fonctions de base pour représenter les cartes, les mains de poker et les règles d'évaluation.
- `test_poker.py` : Tests unitaires pour vérifier que les règles du poker sont correctement implémentées.
- `jeu_poker.py` : Interface en ligne de commande pour jouer au poker contre l'ordinateur.

## Règles du Poker

### Cartes
- 52 cartes : 4 couleurs (Cœur, Carreau, Trèfle, Pique) et 13 rangs (2, 3, 4, 5, 6, 7, 8, 9, 10, Valet, Dame, Roi, As)
- Une main de poker est composée de 5 cartes

### Types de mains (du plus fort au plus faible)

1. **Quinte Flush Royale** (Royal Flush)
   - Une suite de As, Roi, Dame, Valet, 10 de la même couleur
   - Exemple : As♥ Roi♥ Dame♥ Valet♥ 10♥

2. **Quinte Flush** (Straight Flush)
   - Cinq cartes de la même couleur qui se suivent
   - Exemple : 9♠ 8♠ 7♠ 6♠ 5♠
   - L'As peut former une quinte basse : As, 2, 3, 4, 5

3. **Carré** (Four of a Kind)
   - Quatre cartes de même rang
   - Exemple : 7♥ 7♦ 7♠ 7♣ 9♥
   - En cas d'égalité : le carré le plus élevé gagne

4. **Full** (Full House)
   - Un brelan (trois cartes de même rang) et une paire
   - Exemple : 10♥ 10♦ 10♠ 4♣ 4♥
   - En cas d'égalité : comparer d'abord le brelan, puis la paire

5. **Couleur** (Flush)
   - Cinq cartes de la même couleur (non consécutives)
   - Exemple : As♣ 10♣ 7♣ 6♣ 2♣
   - En cas d'égalité : comparer la carte la plus haute, puis la suivante, etc.

6. **Quinte** (Straight)
   - Cinq cartes qui se suivent (pas de la même couleur)
   - Exemple : 9♥ 8♣ 7♠ 6♦ 5♥
   - L'As peut former une quinte haute (10, V, D, R, A) ou basse (A, 2, 3, 4, 5)
   - En cas d'égalité : la quinte avec la carte la plus haute gagne

7. **Brelan** (Three of a Kind)
   - Trois cartes de même rang
   - Exemple : 8♥ 8♦ 8♠ K♣ 3♦
   - En cas d'égalité : le brelan le plus élevé gagne

8. **Deux Paires** (Two Pair)
   - Deux paires de cartes de même rang
   - Exemple : J♥ J♣ 4♠ 4♥ A♦
   - En cas d'égalité : comparer la paire la plus haute, puis la seconde paire, puis la carte restante

9. **Paire** (One Pair)
   - Deux cartes de même rang
   - Exemple : 10♥ 10♣ K♠ 4♥ 3♦
   - En cas d'égalité : comparer la paire, puis les cartes restantes par ordre décroissant

10. **Carte Haute** (High Card)
    - Aucune combinaison ci-dessus
    - En cas d'égalité : comparer la carte la plus haute, puis la suivante, etc.

## Comment jouer

Pour jouer au poker contre l'ordinateur, exécutez le fichier `jeu_poker.py` :

```bash
python jeu_poker.py
```

Le jeu vous distribuera 5 cartes et vous pourrez choisir lesquelles échanger. L'ordinateur fera de même, puis les mains seront comparées pour déterminer le gagnant.

## Tests

Pour exécuter les tests unitaires :

```bash
python test_poker.py
```

## Fonctionnalités

- Implémentation complète des règles du poker à 5 cartes
- Évaluation et comparaison des mains selon les règles standard
- Interface en ligne de commande pour jouer contre l'ordinateur
- Tests unitaires pour vérifier la correction des règles

## Auteur

Ce projet a été réalisé dans le cadre d'un TP de programmation. 