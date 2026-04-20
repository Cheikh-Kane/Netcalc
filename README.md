

# Netcalc
Calculatrice réseau IPv4 en Python — sans bibliothèque spécialisée

Netcalc est un programme en ligne de commande qui calcule automatiquement
toutes les informations utiles d'un réseau IPv4, y compris le découpage
en sous-réseaux via la technique VLSM.


# Fonctionnalités


- Calcul du masque (décimal et binaire) à partir du nombre d'hôtes
- Calcul de l'adresse réseau
- Calcul de l'adresse de diffusion
- Calcul de la plage d'adresses utilisables
- Découpage VLSM
- Validation complète des entrées utilisateur


# Utilisation



bash
python calculatrice_reseau.py



1 - Un sous-réseau (réseau simple) 

2 - VLSM (plusieurs sous-réseaux de tailles différentes)

3 - Quitter



# Exemple — Réseau simple

Adresse IP     : 192.168.1.10

Hôtes requis   : 50

========== Résultas ==========

CIDR                       : /26

Masque en décimal          : 255.255.255.192

Masque en binaire          : 11111111.11111111.11111111.11000000

Adresse réseau             : 192.168.1.0

Adresse de diffusion       : 192.168.1.63

Première adresse utilisable: 192.168.1.1

Dernière adresse utilisable: 192.168.1.62

Plage utilisable           : 192.168.1.1 à 192.168.1.62

Nombre d'hôtes utilisables : 62




# Exemple — VLSM



Adresse de base : 192.168.10.0/24

Sous-réseaux    : 50 hôtes, 20 hôtes, 5 hôtes

========== Résultats ==========

Sous-réseau 1 → 192.168.10.0/26   (62 hôtes)

Sous-réseau 2 → 192.168.10.64/27  (30 hôtes)

Sous-réseau 3 → 192.168.10.96/29  (6 hôtes)









# Structure du code


Fonction	| Rôle 

ip_valid()	| Valide le format d'une adresse ip

check_entier_positif()	| Vérifie qu'une saisie est un entier > 0

saisir_nbre_sous_reseau()	| Demande et vérifie la saisie du nombre de sous-réseau pour le VLSM

saisir_hote_chaque_sous_reseau()	| Demande et vérifie le nombre d'hôtes de chaque sous-réseau

mask_en_decimal()	| Calcule le masque à partir du CIDR 

conv_mask_decimal_vers_binaire() 	| Convertit le masque en binaire 

calcul_info_sous_reseau()	| Calcule toutes les infos d'un sous-réseau 


reseau_simple()		| Traitement pour un réseau simple 


check_espace_adressage_suffisant()	| Vérifie que le CIDR couvre tous les besoins VLSM 

calcul_sous_reseau_suivant()	| Calcule l'adresse du prochain sous-réseau 

vlsm()	| Orchestre le découpage VLSM 

formater_liste()	| Formate une liste d'entiers en adresse lisible 


affichage_infos_sous_reseau()	| Affiche toutes les infos d'un sous-réseau

main()	| Menu principal 







# Documentation



Un document pédagogique complète accompagne ce projet.
Il couvre les concepts réseau, les formules, le code commenté et des exercices corrigés.
[documentation_Netcalc](./documentation_Netcalc.pdf)





# Auteur



Serigne Cheikh Mbacké Kane 

Étudiant en Systèmes, Réseaux et Télécommunications (SRT)
