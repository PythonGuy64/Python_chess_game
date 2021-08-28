import os
import Classes_Echec as C

clear_screen = "cls" if os.name == "nt" else "clear"
dict_coordonees = {
    "a8": [0, 0], "b8": [0, 1], "c8": [0, 2], "d8": [0, 3], "e8": [0, 4], "f8": [0, 5], "g8": [0, 6], "h8": [0, 7],
    "a7": [1, 0], "b7": [1, 1], "c7": [1, 2], "d7": [1, 3], "e7": [1, 4], "f7": [1, 5], "g7": [1, 6], "h7": [1, 7],
    "a6": [2, 0], "b6": [2, 1], "c6": [2, 2], "d6": [2, 3], "e6": [2, 4], "f6": [2, 5], "g6": [2, 6], "h6": [2, 7],
    "a5": [3, 0], "b5": [3, 1], "c5": [3, 2], "d5": [3, 3], "e5": [3, 4], "f5": [3, 5], "g5": [3, 6], "h5": [3, 7],
    "a4": [4, 0], "b4": [4, 1], "c4": [4, 2], "d4": [4, 3], "e4": [4, 4], "f4": [4, 5], "g4": [4, 6], "h4": [4, 7],
    "a3": [5, 0], "b3": [5, 1], "c3": [5, 2], "d3": [5, 3], "e3": [5, 4], "f3": [5, 5], "g3": [5, 6], "h3": [5, 7],
    "a2": [6, 0], "b2": [6, 1], "c2": [6, 2], "d2": [6, 3], "e2": [6, 4], "f2": [6, 5], "g2": [6, 6], "h2": [6, 7],
    "a1": [7, 0], "b1": [7, 1], "c1": [7, 2], "d1": [7, 3], "e1": [7, 4], "f1": [7, 5], "g1": [7, 6], "h1": [7, 7]
}
dict_pieces_promotion = {
    "t": C.Tour, "c": C.Chevalier, "f": C.Fou, "r": C.Reine
}
bool_jeu = True

while bool_jeu:
    obj_game = C.Game()
    str_erreur = None
    int_nombre_espaces = 1
    input("\n Assurez-vous de mettre full screen (WinKey + Up) et appuyez sur Enter: ")
    obj_game.fn_generer_mvt_valides()

    while True:
        os.system(clear_screen)
        obj_game.fn_afficher_tableau()

        if str_erreur:
            print(f"\n{' ' * int_nombre_espaces}{str_erreur}")

        if obj_game.bool_echec:
            print(f"\n{' ' * int_nombre_espaces}Échec!")

        # Position =====================================================================================================
        str_position = input(f"\n{' ' * int_nombre_espaces}Entrez la position de la pièce à bouger (a1-h8): ").lower()
        list_position = dict_coordonees.get(str_position)

        if not list_position:
            if str_position == "reset":
                os.system(clear_screen)
                break

            str_erreur = "Valeur inexacte."
            continue

        int_y = list_position[0]
        obj_piece = obj_game.list_tab[int_y][list_position[1]]

        if str(obj_piece)[1] != obj_game.str_couleur_actuelle:
            str_erreur = "La position ne correspond pas à une pièce de votre couleur."
            continue

        if not obj_piece.list_mvt_valides:
            str_erreur = "Cette pièce n'a aucune possibilité de mouvement."
            continue

        # Destination ==================================================================================================
        print()

        if obj_game.str_couleur_actuelle == "n":
            print(" " * 102, end="")

        for i in range(len(obj_piece.list_mvt_valides)):
            for e in dict_coordonees:
                if dict_coordonees[e] == obj_piece.list_mvt_valides[i]:
                    if i != len(obj_piece.list_mvt_valides) - 1:
                        if i == 13:
                            print(f" {e},")

                            if obj_game.str_couleur_actuelle == "n":
                                print(" " * 102, end="")
                        else:
                            print(f" {e},", end="")
                    else:
                        print(f" {e}")

        str_destination = input(
            f"\n{' ' * int_nombre_espaces}Entrez la destination de la pièce à bouger (a1-h8): ").lower()
        list_destination = dict_coordonees.get(str_destination)

        if not list_destination:
            if str_destination == "reset":
                os.system(clear_screen)
                break

            str_erreur = "Valeur inexacte."
            continue

        if list_destination not in obj_piece.list_mvt_valides:
            str_erreur = "Mouvement invalide."
            continue

        # Exécution du mouvement =======================================================================================
        obj_game.fn_executer_mvt(obj_piece, list_destination)
        str_erreur = None
        obj_game.list_en_passant.clear()

        if isinstance(obj_piece, C.Pion):
            obj_piece.bool_premier_mvt = False

            if abs(obj_piece.int_y - int_y) == 2:
                obj_game.list_en_passant.extend(list_destination)
            elif obj_piece.int_y in (0, 7):
                while True:
                    os.system(clear_screen)
                    obj_game.fn_afficher_tableau()

                    if str_erreur:
                        print(f"\n{' ' * int_nombre_espaces}{str_erreur}")

                    str_promotion = input(
                        f"\n{' ' * int_nombre_espaces}Entrez la première lettre de la pièce en laquelle"
                        f"\n{' ' * int_nombre_espaces}vous voulez que votre pion soit promu (t/c/f/r): ").lower()
                    cls_piece_promue = dict_pieces_promotion.get(str_promotion)

                    if not cls_piece_promue:
                        str_erreur = "Valeur inexacte"
                        continue

                    obj_game.list_tab[obj_piece.int_y][obj_piece.int_x] = \
                        obj_game.list_pieces[obj_game.list_pieces.index(obj_piece)] = \
                        cls_piece_promue(list_destination, obj_piece.str_couleur)
                    str_erreur = None
                    break
        elif isinstance(obj_piece, (C.Tour, C.Roi)):
            obj_piece.bool_premier_mvt = False

        if obj_game.str_couleur_actuelle == "b":
            obj_game.str_couleur_actuelle = "n"
            int_nombre_espaces = 103
        else:
            obj_game.str_couleur_actuelle = "b"
            int_nombre_espaces = 1

        for y in range(8):
            for x in range(8):
                obj_game.list_tab_danger[y][x] = False

        obj_game.fn_generer_mvt_valides()

        # Analyse du jeu ===============================================================================================
        if obj_game.fn_game_over():
            os.system(clear_screen)
            obj_game.fn_afficher_tableau()

            if obj_game.bool_echec:
                print(f"\n{' ' * int_nombre_espaces}Échec et mat!")
            else:
                print(f"\n{' ' * 58}Match nul!")

            if input(f"\n{' ' * 58}Voulez-vous continuer? (o/n): ").lower() == "o":
                os.system(clear_screen)
            else:
                bool_jeu = False

            break

os.system("cls")
print("\n Au-revoir!")
input(" Appuyez sur Enter pour quitter: ")
