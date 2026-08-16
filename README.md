# Spot the Car

Jeu "devine la voiture" — zoom progressif sur une photo, 4 choix, plusieurs modes de jeu.
Packagé en app Android via Capacitor. Toutes les photos viennent de Wikimedia Commons
(voir `CREDITS_PHOTOS.txt`).

## Etat du projet

### Fait
- 5 modes de jeu : Jouer (classique), Mode Facile, Partie Rapide, Mort Subite, 2 Joueurs
- Catalogue de voitures avec photos embarquees localement (jouable 100% hors-ligne)
- Score sur 3 paliers (100 / 50 / 25 pts selon le zoom au moment de la bonne reponse),
  tableau recap detaille en fin de partie, meilleur score persistant par mode
- Icone et fond d'ecran d'accueil personnalises (branding "Yuna Studios")
- Orientation portrait verrouillee
- Pub interstitielle AdMob (ID de TEST Google) affichee avant l'ecran de score,
  une partie sur deux, avec consentement RGPD (UMP)
- Build automatique dans le cloud via GitHub Actions (APK debug + AAB release signe),
  sans rien installer sur le PC
- Outil local de calibrage des zooms (`www/zoom-editor.html`, non embarque dans l'app)

### A faire de ton cote avant une vraie publication

1. **Verification d'identite Google Play Console** -- en cours au moment de la redaction.
2. **Vrais ID AdMob** : cree l'app "Spot the Car" dans ta console AdMob
   (admob.google.com), recupere l'App ID (`ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY`)
   et l'ID du bloc interstitiel (`ca-app-pub-XXXXXXXXXXXXXXXX/ZZZZZZZZZZ`), et donne-les
   pour remplacer les ID de test dans `www/index.html`
   (constantes `ADMOB_APP_ID` / `ADMOB_INTERSTITIAL_ID`, `ADMOB_USE_TEST_IDS = false`)
   et dans `android/app/src/main/AndroidManifest.xml` (meta-data `APPLICATION_ID`).
3. **Fiche store Play Console** : description, categorie, captures d'ecran (l'icone
   512x512 est deja prete : `icon-512-playstore.png`), politique de confidentialite
   (obligatoire, meme simple, a heberger quelque part), questionnaire de classification
   par age.
4. **Upload de l'AAB signe** : workflow GitHub Actions "Build signed release AAB" ->
   telecharger l'artifact `spot-the-car-release-aab` -> uploader dans Play Console.

## Cle de signature (keystore) -- CRITIQUE

Le fichier `release.keystore` et son mot de passe (generes via le workflow
"Generate release keystore (one-off)") ne sont **jamais** dans ce depot -- ils sont
stockes uniquement comme secrets GitHub Actions chiffres
(`ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`,
`ANDROID_KEY_PASSWORD`).

**Tu dois avoir une copie de sauvegarde du fichier `release.keystore` et de son mot de
passe quelque part de sur (gestionnaire de mots de passe, cloud perso...).** Si tu la
perds, tu ne pourras plus jamais publier de mise a jour de cette app sur le Play Store.

## Ajouter de nouvelles voitures

1. Donner les liens Wikimedia Commons (pages `File:...`) des photos souhaitees.
2. Les photos sont telechargees, compressees (JPEG, 1000px de large, qualite 80) et
   creditees automatiquement dans `CREDITS_PHOTOS.txt`.
3. Calibrage du zoom, du nom et des mauvaises reponses via l'outil local
   `www/zoom-editor.html` (servi par un serveur local, jamais embarque dans l'app).
4. Export depuis l'outil -> integration dans le tableau `CARS` de `www/index.html`.

## Rebuild

- **APK debug** (test) : se declenche automatiquement a chaque push sur `main`
  (workflow "Build debug APK").
- **AAB release signe** : workflow "Build signed release AAB", a lancer manuellement
  depuis l'onglet Actions ("Run workflow").

Aucun logiciel Android (JDK, SDK) n'est necessaire en local -- tout se construit dans
le cloud via GitHub Actions.
