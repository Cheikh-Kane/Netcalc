

def ip_valid(adr):   #Vérification : exactement 4 octets, numériques, compris entre 0 et 255
    return len(adr) == 4 and all(octet.isdigit() for octet in adr) and all(0<=int(octet)<=255 for octet in adr)

def check_entier_positif(nbre):
    return nbre.isdigit() and int(nbre) > 0     #isdigit() => que des entiers positifs(ex: rejette '-5' ou '3.5')

def saisir_nbre_sous_reseau():
    while True:     #Saisie et validation du nombre de sous-réseau
        nbre_sous_reseau = input("Saisissez le nombre de sous-reseau: ")
        if check_entier_positif(nbre_sous_reseau):
            break
        print("Le nombre de sous reseau doit être un entier supérieur à 0!")
    return int(nbre_sous_reseau)

def saisir_hote_chaque_sous_reseau(nbre_sous_reseau):      #Saisie le nombre d'hotes de chaque sous-réseau
    nbre_hote_sr = []
    for i in range(nbre_sous_reseau):
        while True:
            saisie = input(f"Saisissez le nombre d'hôte du sous-reseau {i+1}: ")
            if check_entier_positif(saisie):
                nbre_hote_sr.append(int(saisie))
                break 
            print("Le nombre d'hôte doit être un entier supérieur à 0! ")
    return nbre_hote_sr     #Liste d'entiers(ex : [12,3,43,200])


def mask_en_decimal(cidr):   # Calcul du masque sous format decimal
    mask_decimal = []
    for octet in range(4):      #On remplit les 4 octets 1 à 1
        if (cidr >= 8 ):    #L'octet est entièrement dans le réseau(donc il vaut 255)
            mask_decimal.append(255)
            cidr -= 8
        elif(cidr > 0):     #L'octet est partiellement dans le réseau(déterminer la partie qui n'est pas dans le réseau)
            bits_hote = 8 - cidr       #Nbre de bits hote dans cet octet
            mask_decimal.append(256 - (2**bits_hote))
            cidr = 0
        else:       #L'octet est entiérement hote(donc il vaut 0)
            mask_decimal.append(0)
    return mask_decimal

def conv_mask_decimal_vers_binaire(adr): # Convertir une adresse de decimal vers binaire
    return [format(octet,'08b') for octet in adr]   #Convertis chaque octet en binaire et l'affiche sur 8 bits


def calcul_info_sous_reseau(add_ip, nbre_hote_voulu):
    #Etape 1 : calculer le nombre de bits hôte nécessaires
    nbre_adresse = int(nbre_hote_voulu) + 2      # +2 pour l'adresse réseau et l'adresse de diffusion
    nbre_bits_hostID =0
    while((2 ** nbre_bits_hostID) < nbre_adresse):
        nbre_bits_hostID += 1     

    #Etape 2 : déduire le CIDR et le nombre d'hôtes réel 
    CIDR = 32 - nbre_bits_hostID
    nbre_adr_utlisable = (2**nbre_bits_hostID) -2

    #Etape 3 : calculer le masque
    mask_decimal = mask_en_decimal(CIDR)
    mask_binaire = conv_mask_decimal_vers_binaire(mask_decimal)

    #Etape 4 : calculer l'adresse réseau (ET logique)
    reseau = []
    for i in range(4):
        reseau.append(add_ip[i] & mask_decimal[i])

    #Etape 5 : calculer l'adresse de diffusion (OU logique) 
    diffusion = []
    for i in range(4):
        diffusion.append(add_ip[i] | (255 - mask_decimal[i]))

    #Etape 6 : calculer la première adresse adresse utilisable
    premiere = reseau.copy()
    premiere[3] += 1
    #Etape 7 : calculer la dernière adresse utilisable
    derniere = diffusion.copy()
    for i in range(3, -1, -1):      #Parcourir de droite à gauche
        if derniere[i] > 0:         #et décrémenter le premier octet != 0
            derniere[i] -= 1
            break
    #Etape 8 : retourner un dictionnaire avec tous les paramétres réseaux
    return {
        "nbre_hote"             : nbre_hote_voulu,      "CIDR"                  : CIDR,
        "mask_decimal"          : mask_decimal,         "mask_binaire"          : mask_binaire,
        "reseau"                : reseau,               "diffusion"             : diffusion,
        "premiere"              : premiere,             "derniere"              : derniere,
        "nbre_adr_utilisable"   : nbre_adr_utlisable,
    }

def formater_liste(liste):
    return ".".join(map(str,liste))
def affichage_infos_sous_reseau(info):
        #Affichage des infos du sous-reseau
        print(f"Nombre d'hotes                 : {info['nbre_hote']}")
        print(f"CIDR                           : /{info['CIDR']}")
        print(f"Masque en decimal              : {formater_liste(info['mask_decimal'])}")
        print(f"Masque en binaire              : {'.'.join(info['mask_binaire'])}")  
        print(f"Adresse reseau                 : {formater_liste(info['reseau'])}")
        print(f"Adresse de diffusion           : {formater_liste(info['diffusion'])}")
        print(f"Premiere adresse utilisable    : {formater_liste(info['premiere'])}")
        print(f"Derniere adresse utilisable    : {formater_liste(info['derniere'])}")
        print(f"Plage des adresses utilisables : {formater_liste(info['premiere'])} à {formater_liste(info['derniere'])}")
        print(f"Nombre d'adresse utilisable    : {info['nbre_adr_utilisable']}\n\n")

def check_espace_adressage_suffisant(cidr, nbre_hote_sr):
    capacite_cidr = 2 ** (32 - cidr)
    som_bloc_adresse = 0 
    for hote in nbre_hote_sr:
        i = 0
        while(2 ** i) < (hote + 2):
            i += 1
        som_bloc_adresse += (2 ** i)
    return capacite_cidr >= som_bloc_adresse

def calcul_sous_reseau_suivant(diffusion_prec):
    reseau = diffusion_prec.copy()
    for i in range(3, -1, -1):      #On part de l'octet le plus à droite
        if reseau[i] < 255:
            reseau[i] += 1      #On peut incrémenter
            break
        else:
            reseau[i] = 0   #Incrémentation impossible: on met l'octet à 0 et on passe à l'octet suivant(de la droite vers la gauche)
    return reseau


def vlsm():
    while True:
        while True:
            try:
                adresse, cidr = input("\nSaisissez l'adresse à utiliser pour faire le découpage ainsi que le CIDR(Exemple de saisie valide: 12.14.10.0/24) : ").strip().split("/")                
                adresse = adresse.split(".")
                if ip_valid(adresse) and check_entier_positif(cidr) and int(cidr)<32:
                    break
                print("Format de l'adresse ou du CIDR invalide, veuillez reessayez")
            except:
                print("Saisie invalide(Exemple de saisie valide: 12.14.10.0/24), veuillez reessayer")
        adresse = [int(octet) for octet in adresse] 
        cidr = int(cidr)
        nbre_sous_reseau = saisir_nbre_sous_reseau()                        # Saisir le nombre de sous reseau pour le decoupage
        nbre_hote_sr = saisir_hote_chaque_sous_reseau(nbre_sous_reseau)     # Saisir le nbre d'hote de chaque sous reseau
        if check_espace_adressage_suffisant(cidr, nbre_hote_sr):    #Vérifier que le CIDR saisie par le user permet de couvrir tous les besoins
            break
        print("Le CIDR choisi ne permet pas de remplir les besoins de tous les sous-réseau, veuillez choisir un CIDR plus faible ou diminuer le nombre d'hotes des sous-réseaux")
    nbre_hote_sr = sorted(nbre_hote_sr,reverse=True)                    # Trier le nbre d'hote des sous != sous reseaux par ordre decroissant
    sous_reseau_actuel = adresse.copy()
    print("===================================== VLSM =====================================")
    for i, hote in enumerate(nbre_hote_sr):
        print(f"\n============================= Sous-reseau {i+1} ===============================")
        info = calcul_info_sous_reseau(sous_reseau_actuel,hote)
        affichage_infos_sous_reseau(info)
        sous_reseau_actuel = calcul_sous_reseau_suivant(info['diffusion'])

def reseau_simple():
    while True:     # Verifier que le format de l'adresse est valide(avec les fonction adr_est_entier, long_valid et octet_entre_0_255)
        add_ip = []
        add_ip = input("\nVeuillez saisir votre adresse réseau ou l'adresse d'un hôte de votre réseau: ").strip().split(".")
        if ip_valid(add_ip):
            break
        print("Format de l'adresse invalide, (exemple d'adresse valide: 192.168.1.4). Veuillez reessayer!")                    
    add_ip = [int(octet) for octet in add_ip]                           # Convertir chaque octet de l'adresse ip en entier(de base ce sont des chaines de caracteres)
    while True:
        nbre_hote = input("Combien d'hôtes voulez vous dans le reseau? :")
        if check_entier_positif(nbre_hote):
            break
        print("Le nombre d'hôtes doit être un entier supérieur à 0!")
    info = calcul_info_sous_reseau(add_ip, nbre_hote)
    print("\n====================== Infos de votre réseau =======================")
    affichage_infos_sous_reseau(info)


def main():
    print("Bienvenu sur Netcalc.")
    while True:     #Boucle : l'utilisateur peut faire plusieurs calculs de suite
        print("========================== MENU =======================")
        print("1 - Un sous-reseau(reseau simple)")
        print("2 - VLSM(plusieurs sous-reseaux de tailles differentes)")
        print("3 - Quitter")
        mode = input("Choisir un mode(1, 2 ou 3) : ").strip()
        if mode == "1":     #Un seul sous réseau
            reseau_simple()
        elif mode == "2":   #Enchainement VLSM
            vlsm()
        elif mode == '3':   #Quitter
            break
        else:
            print("Choix invalide, choisir entre 1, 2 et 3")
    print("Nous vous remercions d'avoir utiliser Netcalc, à bientôt")
if __name__ == "__main__":
    main()

