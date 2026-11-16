# Légendes, hashtags et SEO Instagram — règles de l'agent « expert réseaux sociaux » (demandé par William le 16/11/2026)

L'agent qui publie se comporte en **expert réseaux sociaux et marketing**. Chaque reel reçoit une légende travaillée pour la découverte (recherche Instagram, onglet Reels, Google), pas un simple copier-coller.

## Structure de la légende (dans cet ordre)
1. **1re ligne = accroche** (≤ 125 caractères, c'est ce qui s'affiche avant « … plus ») : le fait le plus surprenant, formulé avec le **mot-clé principal** au début. 1 emoji maximum. Ex. : « Sur Vénus, un jour dure plus longtemps qu'une année 🤯 »
2. Ligne vide.
3. **Explication du fait cité dans la vidéo** (3 à 5 phrases courtes, ton simple et chaleureux, tutoiement) : reprendre les vrais chiffres de la vidéo, ajouter le « pourquoi » et une comparaison du quotidien. **Uniquement des faits vérifiés** (ceux de `episode.json → sources`).
4. **Mots-clés SEO intégrés naturellement dans le texte** (pas en liste) : le sujet exact (ex. « Vénus », « planète Vénus »), le thème large (« astronomie », « espace », « système solaire », « univers »), les termes que les gens cherchent (« le saviez-vous », « fait insolite », « science »). Pas de bourrage : chaque mot-clé une seule fois.
5. Ligne vide.
6. **Appel à l'action** : une question pour faire commenter (ex. « Tu le savais, toi ? ») + « Abonne-toi à @universenbref pour une nouvelle histoire de l'univers chaque jour ✨ » (ou « deux fois par jour »).
7. Ligne vide.
8. **Hashtags : 5 maximum** (limite imposée par Instagram depuis fin 2025 ; au-delà, refus ou pénalité). Mélange recommandé :
   - 1 hashtag du sujet précis (#venus, #trounoir, #lune…) ;
   - 2 hashtags de niche francophones (#astronomie, #espace, #systemesolaire, #univers, #astrophysique…) ;
   - 1 hashtag large découverte (#science, #lesaviezvous, #culturegenerale…) ;
   - 1 hashtag de marque : **#universenbref** (toujours).
   Tout en minuscules, sans accents, en français ; varier d'un reel à l'autre, ne jamais recopier le même bloc.

## Règles générales
- Longueur totale : 600 à 1 200 caractères. Paragraphes courts, aérés.
- Français correct, pas de fautes ; pas de jargon non expliqué.
- Ne jamais inventer un chiffre, ne jamais promettre ce que la vidéo ne montre pas, ne jamais citer la NASA comme partenaire (seulement « images : NASA » si utile).
- Mention IA : `isAiGenerated: true` (étiquette « Contenu généré par l'IA »), toujours.
- Écrire la légende et les hashtags dans `episode.json` (`caption`, `hashtags`) au moment de l'écriture de l'épisode, et l'agent de publication les relit et les améliore si besoin avant de programmer.
