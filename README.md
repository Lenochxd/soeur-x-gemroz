# Analyse de la vidéo teaser

Ce projet analyse les frames d'une vidéo teaser postée sur Twitter par Ptite Soeur et Gemroz, pour décrypter un message caché. 

**Frame random**

![Frame random](example.png)

**Image Finale**

Méthode 1: Garder les pixels les plus lumineux

|           Frames twitter            |           Frames instagram            |         Frames des deux          |
| :---------------------------------: | :-----------------------------------: | :------------------------------: |
| ![Image Finale](output/output-TWITTER.png) | ![Image Finale](output/output-INSTAGRAM.png) | ![Image Finale](output/output-BOTH.png) |

Méthode 2: Garder les pixels les plus lumineux ou sombres en fonction de leur luminosité

|           Frames twitter            |           Frames instagram            |         Frames des deux          |
| :---------------------------------: | :-----------------------------------: | :------------------------------: |
| ![Image Finale](output/output-nobg-TWITTER.png) | ![Image Finale](output/output-nobg-INSTAGRAM.png) | ![Image Finale](output/output-nobg-BOTH.png) |

Méthode 3: Garder la couleur moyenne de chaque pixel

|           Frames twitter            |           Frames instagram            |         Frames des deux          |
| :---------------------------------: | :-----------------------------------: | :------------------------------: |
| ![Image Finale](output/output-avg-TWITTER.png) | ![Image Finale](output/output-avg-INSTAGRAM.png) | ![Image Finale](output/output-avg-BOTH.png) |

## Contexte
Ptite Soeur et Gemroz ont posté [un teaser sur Twitter](https://twitter.com/PRXPVNE/status/1800230037611753785). À la fin de la vidéo, un message caché est présent mais indescriptible directement. 

Mon thread twitter expliquant plus en détails [juste ici](https://twitter.com/LenochJ/status/1800313166775427112)

![code](https://i.imgur.com/9rkTIQx.png)

## Méthode
Pour décrypter ce message :
1. Extraction des frames de la fin de la vidéo avec Shotcut.
2. Utilisation de Python et de la librairie PILLOW pour analyser chaque pixel de chaque frame.
3. Conservation uniquement des pixels les plus lumineux.
4. Création d'une seule image lisible en output.


\
\
\
J'ai fait webdeck aussi: https://github.com/Lenochxd/WebDeck \
super projet 👍

\
<a href="https://ko-fi.com/lenoch" target="_blank"><img height="35" style="height:46px;" src="https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0" alt="Buy Me a Coffee at ko-fi.com"/>
^^