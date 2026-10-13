import pymupdf, re, json, os

pdf_path = r'c:\Users\abdal\Desktop\RE4E\CCNA 1 Examen final du cours ITNv7 Questions et Réponses.pdf'
doc = pymupdf.open(pdf_path)

# Manual overrides / image transcriptions for questions where answers are visual or require precise structuring
IMAGE_SOLUTIONS = {
    (2, 3): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p02_xref50.png",
        "image_description": "Schéma de mise en correspondance avec lignes reliant les termes aux définitions.",
        "correct_answers": [
            "Dimensionnement des messages ➔ Processus consistant à décomposer un message long en parties distinctes avant de les envoyer sur le réseau",
            "Encapsulation des messages ➔ Processus consistant à placer un format de message à l'intérieur d'un autre",
            "Codage des messages ➔ Processus permettant de convertir des informations dans un format acceptable pour la transmission"
        ],
        "matching_pairs": {
            "Dimensionnement des messages": "Processus consistant à décomposer un message long en parties distinctes avant de les envoyer sur le réseau",
            "Encapsulation des messages": "Processus consistant à placer un format de message à l'intérieur d'un autre",
            "Codage des messages": "Processus permettant de convertir des informations dans un format acceptable pour la transmission"
        }
    },
    (13, 27): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p14_xref81.png",
        "topology_image": "extracted_images/p13_xref78.png",
        "image_description": "Schéma VLSM avec lignes reliant les réseaux aux sous-réseaux appropriés.",
        "correct_answers": [
            "Réseau A (100 hôtes) ➔ 192.168.0.0 /25",
            "Réseau B (50 hôtes) ➔ 192.168.0.128 /26",
            "Réseau C (25 hôtes) ➔ 192.168.0.192 /27",
            "Réseau D (2 hôtes) ➔ 192.168.0.224 /30"
        ],
        "matching_pairs": {
            "Réseau A (100 hôtes)": "192.168.0.0 /25",
            "Réseau B (50 hôtes)": "192.168.0.128 /26",
            "Réseau C (25 hôtes)": "192.168.0.192 /27",
            "Réseau D (2 hôtes)": "192.168.0.224 /30"
        }
    },
    (17, 33): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p18_xref90.png",
        "image_description": "Méthodes de transmission cut-through et store-and-forward avec leurs caractéristiques.",
        "correct_answers": [
            "cut-through ➔ A une faible latence",
            "cut-through ➔ Peut transférer des trames incomplètes",
            "cut-through ➔ Démarre la transmission lorsque l'adresse de destination est reçue",
            "store-and-forward ➔ Stocke toujours la trame entière",
            "store-and-forward ➔ Vérifie le CRC avant d'effectuer la transmission",
            "store-and-forward ➔ Vérifie la longueur de la trame avant d'effectuer la transmission"
        ],
        "categories": {
            "cut-through": [
                "A une faible latence",
                "Peut transférer des trames incomplètes",
                "Démarre la transmission lorsque l'adresse de destination est reçue"
            ],
            "store-and-forward": [
                "Stocke toujours la trame entière",
                "Vérifie le CRC avant d'effectuer la transmission",
                "Vérifie la longueur de la trame avant d'effectuer la transmission"
            ]
        }
    },
    (19, 35): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p19_xref93.png",
        "image_description": "Classification des caractéristiques entre Adresse IP et Adresse MAC.",
        "correct_answers": [
            "Adresse IP ➔ contenu dans l'en-tête de couche 3",
            "Adresse IP ➔ séparés en une partie réseau et un identifiant unique",
            "Adresse IP ➔ 32 ou 128 bits",
            "Adresse MAC ➔ contenu dans l'en-tête de couche 2",
            "Adresse MAC ➔ séparés en OUI et un identifiant unique",
            "Adresse MAC ➔ 48 bits"
        ],
        "categories": {
            "Adresse IP": [
                "contenu dans l'en-tête de couche 3",
                "séparés en une partie réseau et un identifiant unique",
                "32 ou 128 bits"
            ],
            "Adresse MAC": [
                "contenu dans l'en-tête de couche 2",
                "séparés en OUI et un identifiant unique",
                "48 bits"
            ]
        }
    },
    (22, 42): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p22_xref101.png",
        "image_description": "Mise en relation des types d'adresses IP spéciales avec leurs exemples.",
        "correct_answers": [
            "Adresse de bouclage ➔ 127.0.0.1",
            "Adresse expérimentale ➔ 240.2.6.255",
            "À une adresse publique ➔ 198.133.219.2",
            "Adresse link-local ➔ 169.254.1.5"
        ],
        "matching_pairs": {
            "Adresse de bouclage": "127.0.0.1",
            "Adresse expérimentale": "240.2.6.255",
            "À une adresse publique": "198.133.219.2",
            "Adresse link-local": "169.254.1.5"
        }
    },
    (34, 67): {
        "type": "image_choice",
        "has_image": True,
        "image_file": "extracted_images/p35_xref132.png",
        "image_description": "Photos de connecteurs réseau : LC (fibre), BNC (coaxial), SC (fibre), RJ-45 (paire torsadée).",
        "correct_answers": [
            "Connecteur RJ-45 (connecteur modulaire 8P8C pour câble à paires torsadées Ethernet)"
        ]
    },
    (39, 80): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p40_xref144.png",
        "image_description": "Association des champs d'en-tête réseau aux couches OSI 2, 3 et 4.",
        "correct_answers": [
            "Couche 2 ➔ En-tête 802.2",
            "Couche 2 ➔ Séquence de contrôle de trame (FCS)",
            "Couche 2 ➔ Adresse MAC de destination",
            "Couche 3 ➔ TTL",
            "Couche 3 ➔ Adresse IP source",
            "Couche 4 ➔ Numéro d’accusé de réception",
            "Couche 4 ➔ Numéro du port de destination"
        ],
        "categories": {
            "Couche 2": ["En-tête 802.2", "Séquence de contrôle de trame (FCS)", "Adresse MAC de destination"],
            "Couche 3": ["TTL", "Adresse IP source"],
            "Couche 4": ["Numéro d’accusé de réception", "Numéro du port de destination"]
        }
    },
    (41, 82): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p41_xref147.png",
        "image_description": "Différence entre réseau peer-to-peer et application peer-to-peer.",
        "correct_answers": [
            "réseau peer to peer ➔ Aucun serveur dédié n'est requis",
            "réseau peer to peer ➔ Les rôles de client et de serveur sont définis en fonction de chaque requête",
            "Application peer-to-peer ➔ Nécessite une interface utilisateur spécifique",
            "Application peer-to-peer ➔ Un service en tâche de fond est requis"
        ],
        "categories": {
            "réseau peer to peer": [
                "Aucun serveur dédié n'est requis",
                "Les rôles de client et de serveur sont définis en fonction de chaque requête"
            ],
            "Application peer-to-peer": [
                "Nécessite une interface utilisateur spécifique",
                "Un service en tâche de fond est requis"
            ]
        }
    },
    (43, 86): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p43_xref153.png",
        "image_description": "Composants de structure d'une adresse IPv6 unicast globale.",
        "correct_answers": [
            "Cette partie de l'adresse est utilisée par une entreprise pour identifier les sous-réseaux ➔ ID de sous-réseau",
            "Cette partie de l'adresse est l'équivalent de la partie hôte d'une adresse IPv4 ➔ ID d'interface",
            "Cette partie réseau de l'adresse est attribuée par le fournisseur d'accès Internet ➔ Préfixe de routage global"
        ],
        "matching_pairs": {
            "Cette partie de l'adresse est utilisée par une entreprise pour identifier les sous-réseaux": "ID de sous-réseau",
            "Cette partie de l'adresse est l'équivalent de la partie hôte d'une adresse IPv4": "ID d'interface",
            "Cette partie réseau de l'adresse est attribuée par le fournisseur d'accès Internet": "Préfixe de routage global"
        }
    },
    (47, 97): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p48_xref164.png",
        "image_description": "Éléments sur diagrammes de topologie physique vs logique.",
        "correct_answers": [
            "Diagramme de topologie physique ➔ Emplacement d'un ordinateur de bureau dans une salle de classe",
            "Diagramme de topologie physique ➔ Chemin de câbles reliant les salles aux armoires de câblage",
            "Diagramme de la topologie logique ➔ Adresse IP d'un serveur"
        ],
        "categories": {
            "Diagramme de topologie physique": [
                "Emplacement d'un ordinateur de bureau dans une salle de classe",
                "Chemin de câbles reliant les salles aux armoires de câblage"
            ],
            "Diagramme de la topologie logique": [
                "Adresse IP d'un serveur"
            ]
        }
    },
    (54, 113): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p54_xref180.png",
        "image_description": "Association des mécanismes de fiabilité TCP avec leurs définitions.",
        "correct_answers": [
            "Nombre d'octets qu'un périphérique de destination peut accepter et traiter en une seule fois ➔ taille de fenêtre",
            "Reçu par un expéditeur avant de transmettre plus de segments dans une session ➔ acknowledgment",
            "Méthode de gestion des segments de données perdues ➔ retransmission",
            "Utilisé pour identifier les segments de données manquants ➔ numéros d'ordre"
        ],
        "matching_pairs": {
            "Nombre d'octets qu'un périphérique de destination peut accepter et traiter en une seule fois": "taille de fenêtre",
            "Reçu par un expéditeur avant de transmettre plus de segments dans une session": "acknowledgment",
            "Méthode de gestion des segments de données perdues": "retransmission",
            "Utilisé pour identifier les segments de données manquants": "numéros d'ordre"
        }
    },
    (56, 116): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p56_xref185.png",
        "image_description": "Classification des protocoles applicatifs selon la couche 4 (TCP vs UDP).",
        "correct_answers": [
            "TCP ➔ FTP",
            "TCP ➔ HTTP",
            "TCP ➔ SMTP",
            "UDP ➔ DHCP",
            "UDP ➔ TFTP"
        ],
        "categories": {
            "TCP": ["FTP", "HTTP", "SMTP"],
            "UDP": ["DHCP", "TFTP"]
        }
    },
    (56, 117): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p57_xref188.png",
        "image_description": "Fonctions de pare-feu et types de protection.",
        "correct_answers": [
            "filtrage des paquets ➔ empêche l'accès selon l'adresse IP ou MAC",
            "Filtrage des URL ➔ empêche l'accès aux sites Web",
            "Filtrage dynamique de paquets (SPI) ➔ empêche les sessions entrantes non sollicitées",
            "Filtrage des applications ➔ empêche l'accès par numéro de port"
        ],
        "matching_pairs": {
            "filtrage des paquets": "empêche l'accès selon l'adresse IP ou MAC",
            "Filtrage des URL": "empêche l'accès aux sites Web",
            "Filtrage dynamique de paquets (SPI)": "empêche les sessions entrantes non sollicitées",
            "Filtrage des applications": "empêche l'accès par numéro de port"
        }
    },
    (61, 127): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p62_xref202.png",
        "image_description": "Rôle des champs d'en-tête et de fin de trame de liaison de données.",
        "correct_answers": [
            "Ce champ vérifie si la trame a été endommagée pendant la transmission ➔ Détection des erreurs",
            "Ce champ permet de diriger la trame vers sa destination ➔ Adressage",
            "Ce champ indique le début d'une trame ➔ Début de trame",
            "Ce champ permet d'identifier le protocole de couche 3 grâce à la procédure LLC ➔ type"
        ],
        "matching_pairs": {
            "Ce champ vérifie si la trame a été endommagée pendant la transmission": "Détection des erreurs",
            "Ce champ permet de diriger la trame vers sa destination": "Adressage",
            "Ce champ indique le début d'une trame": "Début de trame",
            "Ce champ permet d'identifier le protocole de couche 3 grâce à la procédure LLC": "type"
        }
    },
    (64, 24): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p65_xref209.png",
        "image_description": "Éléments sur diagrammes de topologie physique vs logique (anglais/français).",
        "correct_answers": [
            "physical topology diagram ➔ location of a desktop PC in a classroom",
            "physical topology diagram ➔ path of cables that connect rooms to wiring closets",
            "logical topology diagram ➔ IP address of a server"
        ],
        "categories": {
            "physical topology diagram": [
                "location of a desktop PC in a classroom",
                "path of cables that connect rooms to wiring closets"
            ],
            "logical topology diagram": [
                "IP address of a server"
            ]
        }
    },
    (66, 58): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p66_xref212.png",
        "image_description": "Menaces de sécurité physique et environnementale réseau.",
        "correct_answers": [
            "maintenance threats ➔ poor handling of key electrical components (electrostatic discharge), lack of critical spare parts, poor cabling, and poor labeling",
            "environmental threats ➔ temperature extremes (too hot or too cold) or humidity extremes (too wet or too dry)",
            "hardware threats ➔ physical damage to servers, routers, switches, cabling plant, and workstations",
            "electrical threats ➔ voltage spikes, insufficient supply voltage (brownouts), unconditioned power (noise), and total power loss"
        ],
        "matching_pairs": {
            "maintenance threats": "poor handling of key electrical components (electrostatic discharge), lack of critical spare parts, poor cabling, and poor labeling",
            "environmental threats": "temperature extremes (too hot or too cold) or humidity extremes (too wet or too dry)",
            "hardware threats": "physical damage to servers, routers, switches, cabling plant, and workstations",
            "electrical threats": "voltage spikes, insufficient supply voltage (brownouts), unconditioned power (noise), and total power loss"
        }
    },
    (70, 147): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p72_xref226.png",
        "topology_image": "extracted_images/p71_xref223.png",
        "image_description": "Attribution VLSM pour 4 réseaux (A: 100 hôtes, B: 50 hôtes, C: 25 hôtes, D: 2 hôtes).",
        "correct_answers": [
            "Network A (100 hôtes) ➔ 192.168.0.0 /25",
            "Network B (50 hôtes) ➔ 192.168.0.128 /26",
            "Network C (25 hôtes) ➔ 192.168.0.192 /27",
            "Network D (2 hôtes) ➔ 192.168.0.224 /30"
        ],
        "matching_pairs": {
            "Network A (100 hôtes)": "192.168.0.0 /25",
            "Network B (50 hôtes)": "192.168.0.128 /26",
            "Network C (25 hôtes)": "192.168.0.192 /27",
            "Network D (2 hôtes)": "192.168.0.224 /30"
        }
    },
    (73, 151): {
        "type": "matching",
        "has_image": True,
        "image_file": "extracted_images/p73_xref230.png",
        "image_description": "Modèles de réseau pair-à-pair : peer-to-peer network vs peer-to-peer application.",
        "correct_answers": [
            "peer-to-peer network ➔ no dedicated server is required",
            "peer-to-peer network ➔ client and server roles are set on a per request basis",
            "peer-to-peer application ➔ requires a specific user interface",
            "peer-to-peer application ➔ a background service is required"
        ],
        "categories": {
            "peer-to-peer network": [
                "no dedicated server is required",
                "client and server roles are set on a per request basis"
            ],
            "peer-to-peer application": [
                "requires a specific user interface",
                "a background service is required"
            ]
        }
    },
    (74, 159): {
        "type": "multiple_choice",
        "has_image": True,
        "image_file": "extracted_images/p74_xref233.png",
        "image_description": "Topologie LAN avec switch, routeur R1, hôtes A, B, C sur un segment et D sur un autre.",
        "correct_answers": [
            "uniquement les hôtes B, C et le routeur R1"
        ],
        "explanation": "La requête ARP est une diffusion (broadcast de couche 2). Le commutateur la propage sur tous les ports du réseau local (reçue par B, C et R1). Le routeur R1 arrête la diffusion et ne la transmet pas à l'autre réseau (hôte D ne la reçoit pas)."
    }
}

IMAGE_EXHIBITS = {
    (7, 16): "extracted_images/p07_xref62.png",
    (10, 23): "extracted_images/p10_xref69.png",
    (12, 26): "extracted_images/p12_xref75.png",
    (13, 27): "extracted_images/p13_xref78.png",
    (21, 39): "extracted_images/p21_xref98.png",
    (25, 47): "extracted_images/p25_xref108.png",
    (27, 51): "extracted_images/p27_xref113.png",
    (30, 58): "extracted_images/p30_xref120.png",
    (33, 65): "extracted_images/p33_xref127.png",
    (37, 72): "extracted_images/p37_xref137.png",
    (42, 84): "extracted_images/p42_xref150.png",
    (49, 100): "extracted_images/p49_xref167.png",
    (51, 103): "extracted_images/p51_xref172.png",
    (54, 112): "extracted_images/p54_xref179.png",
    (58, 119): "extracted_images/p58_xref191.png",
    (60, 125): "extracted_images/p60_xref196.png",
    (61, 127): "extracted_images/p61_xref199.png",
    (71, 147): "extracted_images/p71_xref223.png",
    (74, 159): "extracted_images/p74_xref233.png"
}

def clean_text(s):
    if not s:
        return ""
    s = s.replace('\u200b', '').replace('\xa0', ' ')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def is_header_or_footer(text):
    t = text.strip()
    patterns = [
        r'^CCNA 1 Examen final',
        r'^CCNA 1 ITN \(Version 7\.00\)',
        r'^https?://ccnareponses\.com',
        r'^\d{1,2}/\d{1,2}/\d{4}',
        r'^\d{1,2}/\d{1,2}$',
        r'^(Copy Link|Facebook|Twitter|WhatsApp|Contents)$',
        r'^Updated:',
        r'^\d+\s+commentaires',
        r'^CCNA 1$',
        r'^Français$',
        r'^i\d+v\d+n\d+.*\.png',
        r'^Abonnez-vous à CCNA Réponses',
        r'^Recevez toute l’actualité',
        r"^J'accepte que mes données",
        r'^Votre e-mail',
        r"^S’A B ON N ER"
    ]
    for p in patterns:
        if re.search(p, t):
            return True
    return False

lines = []
for p_idx, page in enumerate(doc):
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                spans = l['spans']
                txt = ' '.join(s['text'].strip() for s in spans if s['text'].strip())
                txt = clean_text(txt)
                if not txt or is_header_or_footer(txt):
                    continue
                is_red = any(s['color'] == 0xff0000 for s in spans)
                lines.append({
                    'text': txt,
                    'is_red': is_red,
                    'page': p_idx + 1
                })

raw_questions = []
current = None

for l in lines:
    m = re.match(r'^(\d{1,3})\.\s+(.*)$', l['text'])
    is_real_question = False
    if m:
        num = int(m.group(1))
        # Check if this is the accidental split on port 67 on page 67
        prev_text = ""
        if current:
            if current['lines']:
                prev_text = current['lines'][-1]['text']
            else:
                prev_text = current['title_start']
                
        if prev_text.strip().endswith('destination de') and num == 67:
            # continuation of previous question
            is_real_question = False
            l['text'] = f"67. {m.group(2)}"
        else:
            is_real_question = True

    if is_real_question:
        if current:
            raw_questions.append(current)
        current = {
            'num': int(m.group(1)),
            'title_start': m.group(2),
            'page': l['page'],
            'lines': []
        }
    else:
        if current:
            current['lines'].append(l)

if current:
    raw_questions.append(current)

print(f'Total questions cleanly segmented: {len(raw_questions)}')

processed_dataset = []

for idx, q in enumerate(raw_questions, 1):
    q_num = q['num']
    page = q['page']
    
    manual = IMAGE_SOLUTIONS.get((page, q_num))
    if not manual:
        for k, v in IMAGE_SOLUTIONS.items():
            if k[1] == q_num and abs(k[0] - page) <= 1:
                manual = v
                break

    title_parts = [q['title_start']]
    options = []
    correct_answers = []
    explanation_parts = []
    in_explanation = False
    
    # Check if title_start already completed the question
    ts = q['title_start'].strip()
    in_options = bool(re.search(r'(\?|\:|\))\s*$', ts) and not ts.endswith('de'))

    for l in q['lines']:
        t = l['text']
        is_red = l['is_red']
        
        # Explanation check
        exp_m = re.match(r'^(Explique\s*:|Explication\s*:|Expliquer\s*:|Explications\s*:)\s*(.*)$', t, re.IGNORECASE)
        if exp_m:
            in_explanation = True
            if exp_m.group(2).strip():
                explanation_parts.append(exp_m.group(2).strip())
            continue
            
        if in_explanation:
            explanation_parts.append(t)
            continue
            
        if is_red:
            in_options = True
            options.append(t)
            correct_answers.append(t)
            continue
            
        if not in_options:
            if re.search(r'(\?|\:|\))\s*$', t) or len(title_parts) >= 3 or t.endswith('(Choisissez deux réponses.)') or t.endswith('(Choisissez trois réponses.)'):
                title_parts.append(t)
                in_options = True
            elif any(t.startswith(prefix) for prefix in ['À ', 'Le ', 'La ', 'Les ', 'Un ', 'Une ', 'Des ', 'De ', 'Dans ', 'Pour ', 'Il ', 'Elle ', 'Ce ', 'Cette ']) and len(' '.join(title_parts)) > 35:
                in_options = True
                options.append(t)
            else:
                title_parts.append(t)
        else:
            options.append(t)

    full_question = clean_text(' '.join(title_parts))
    full_explanation = clean_text(' '.join(explanation_parts)) if explanation_parts else None

    item_type = "single_choice"
    has_image = False
    image_file = IMAGE_EXHIBITS.get((page, q_num), None)
    image_desc = None
    matching_pairs = None
    categories = None

    if manual:
        item_type = manual.get('type', 'matching')
        has_image = manual.get('has_image', False)
        image_file = manual.get('image_file', image_file)
        image_desc = manual.get('image_description')
        correct_answers = manual.get('correct_answers', correct_answers)
        matching_pairs = manual.get('matching_pairs')
        categories = manual.get('categories')
        if manual.get('explanation'):
            full_explanation = manual['explanation']
    else:
        if len(correct_answers) > 1:
            item_type = "multiple_choice"
        elif len(correct_answers) == 1:
            item_type = "single_choice"
            
    if image_file:
        has_image = True

    clean_correct = [clean_text(a) for a in correct_answers if clean_text(a)]
    clean_opts = [clean_text(o) for o in options if clean_text(o)]

    item = {
        "id": idx,
        "original_number": q_num,
        "page": page,
        "question": full_question,
        "type": item_type,
        "options": clean_opts,
        "correct_answers": clean_correct,
        "explanation": full_explanation,
        "has_image": has_image,
        "image_file": image_file,
        "image_description": image_desc
    }
    if matching_pairs:
        item["matching_pairs"] = matching_pairs
    if categories:
        item["categories"] = categories

    processed_dataset.append(item)

out_file = r'c:\Users\abdal\Desktop\RE4E\data\ccna1_exam.json'
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(processed_dataset, f, ensure_ascii=False, indent=2)

print(f'Successfully built dataset with {len(processed_dataset)} questions!')
no_ans = [q for q in processed_dataset if not q['correct_answers']]
print(f'Questions with 0 answers: {len(no_ans)}')
for q in processed_dataset:
    if not q['correct_answers']:
        print(f"Missing answer: ID {q['id']}, Q{q['original_number']}, P{q['page']}: {q['question'][:50]}")
