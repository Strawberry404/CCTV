# Rapport Technique: Système d'Analyse de Vidéosurveillance CCTV

## Table des Matières

1. [Introduction](#1-introduction)
   - [1.1 Contexte](#11-contexte)
   - [1.2 Objectifs Principaux](#12-objectifs-principaux)
   - [1.3 Portée](#13-portée)
   - [1.4 Références](#14-références)
2. [Analyse des besoins](#2-analyse-des-besoins)
   - [2.1 Besoins Fonctionnels](#21-besoins-fonctionnels)
   - [2.2 Besoins Non Fonctionnels](#22-besoins-non-fonctionnels)
   - [2.3 Diagramme de cas d'utilisation](#23-diagramme-de-cas-dutilisation)
3. [Conception du système](#3-conception-du-système)
   - [3.1 Modèles](#31-modèles)
   - [3.2 Front-end](#32-front-end)
   - [3.3 Contrôleurs](#33-contrôleurs)
   - [3.4 Services](#34-services)
   - [3.5 Service IA](#35-service-ia)
4. [Conception base de données](#4-conception-base-de-données)
5. [Implémentation](#5-implémentation)
   - [5.1 Technologies utilisées](#51-technologies-utilisées)
   - [5.2 Structure du code](#52-structure-du-code)
6. [Manuel](#6-manuel)

## 1. Introduction

### 1.1 Contexte

Dans le domaine de la sécurité et de la surveillance, l'utilisation de caméras de vidéosurveillance (CCTV) est devenue omniprésente. Cependant, l'analyse manuelle des heures de vidéos de surveillance présente plusieurs défis majeurs:

- **Volume de données**: Les systèmes CCTV génèrent d'énormes quantités de données vidéo, souvent 24 heures sur 24, 7 jours sur 7.
- **Ressources humaines limitées**: L'examen manuel de ces vidéos nécessite un personnel considérable.
- **Fatigue attentionnelle**: Les opérateurs humains peuvent manquer des événements critiques en raison de la fatigue ou de l'inattention.
- **Temps de réaction**: L'analyse rétrospective manuelle ne permet pas une réponse en temps opportun aux incidents.

Ces défis ont créé un besoin croissant de solutions automatisées capables d'analyser efficacement les vidéos de surveillance, d'identifier les événements pertinents, et de réduire le temps nécessaire pour passer en revue les enregistrements. C'est dans ce contexte que notre système d'analyse CCTV a été développé.

### 1.2 Objectifs Principaux

Le système d'analyse CCTV a été conçu avec les objectifs suivants:

1. **Automatiser la détection d'événements**: Identifier automatiquement les mouvements, les objets et les comportements dans les vidéos de surveillance en utilisant des techniques avancées de vision par ordinateur et d'intelligence artificielle.

2. **Réduire le temps d'analyse**: Générer des résumés vidéo concis contenant uniquement les segments pertinents, permettant aux utilisateurs de visualiser rapidement les événements importants sans avoir à parcourir des heures d'enregistrement.

3. **Offrir une sensibilité configurable**: Permettre aux utilisateurs d'ajuster les paramètres de détection selon leurs besoins spécifiques, de la détection ultra-sensible pour ne manquer aucun mouvement à des réglages plus conservateurs pour réduire les faux positifs.

4. **Faciliter l'investigation**: Fournir un système de catégorisation et d'organisation des événements détectés pour faciliter les investigations ultérieures.

5. **Fournir une solution extensible**: Créer une architecture modulaire permettant l'ajout de nouvelles fonctionnalités et l'amélioration des algorithmes existants.

### 1.3 Portée

Le système d'analyse CCTV couvre les aspects suivants:

**Inclus dans la portée:**
- Traitement des fichiers vidéo préenregistrés au format standard (MP4, AVI, etc.)
- Détection de mouvements avec sensibilité configurable
- Détection et classification d'objets (personnes, véhicules, etc.)
- Suivi d'objets à travers les séquences vidéo
- Analyse d'événements (mouvements inhabituels, stationnement prolongé, etc.)
- Génération de clips vidéo des événements détectés
- Fusion des clips en une vidéo récapitulative
- Génération de rapports détaillés au format JSON

**Exclus de la portée:**
- Traitement en temps réel des flux de caméras en direct
- Reconnaissance faciale ou identification des individus
- Intégration directe avec des systèmes d'alarme ou de notification
- Analyses prédictives des comportements futurs
- Interface utilisateur graphique avancée (actuellement interface en ligne de commande)
- Stockage à long terme ou archivage des données d'événements
- Fonctionnalités multi-utilisateurs ou gestion des droits d'accès

### 1.4 Références

Le développement de ce système s'appuie sur diverses technologies, bibliothèques et recherches dans le domaine de la vision par ordinateur et de l'analyse vidéo:

1. **Bibliothèques et Frameworks**:
   - OpenCV: https://opencv.org/
   - FFmpeg: https://ffmpeg.org/
   - YOLOv8: https://github.com/ultralytics/ultralytics

2. **Documents Techniques**:
   - CONFIGURATION.md: Guide de configuration du système
   - USAGE.md: Instructions d'utilisation
   - TROUBLESHOOTING.md: Guide de dépannage

3. **Articles et Publications**:
   - Redmon, J., & Farhadi, A. (2018). YOLOv3: An Incremental Improvement.
   - Bewley, A., et al. (2016). Simple Online and Realtime Tracking.
   - KaewTraKulPong, P., & Bowden, R. (2002). An improved adaptive background mixture model for real-time tracking.

## 2. Analyse des besoins

### 2.1 Besoins Fonctionnels

Le système d'analyse CCTV doit répondre aux besoins fonctionnels suivants:

#### BF1: Détection de mouvement
- **BF1.1**: Le système doit détecter les changements significatifs entre les images consécutives.
- **BF1.2**: Le système doit permettre l'ajustement du seuil de sensibilité pour la détection de mouvement.
- **BF1.3**: Le système doit filtrer les micro-mouvements non significatifs (comme les variations d'éclairage).

#### BF2: Détection et classification d'objets
- **BF2.1**: Le système doit identifier et classifier les objets d'intérêt dans les vidéos (personnes, véhicules, etc.).
- **BF2.2**: Le système doit associer un score de confiance à chaque détection.
- **BF2.3**: Le système doit permettre la filtration des objets par catégorie.

#### BF3: Suivi d'objets
- **BF3.1**: Le système doit suivre les objets détectés à travers les séquences vidéo.
- **BF3.2**: Le système doit gérer l'occlusion temporaire des objets.
- **BF3.3**: Le système doit attribuer des identifiants uniques aux objets suivis.

#### BF4: Analyse d'événements
- **BF4.1**: Le système doit identifier des comportements spécifiques (arrêt prolongé, mouvement rapide, etc.).
- **BF4.2**: Le système doit évaluer l'importance de chaque événement détecté.
- **BF4.3**: Le système doit associer les événements aux objets concernés.

#### BF5: Génération de clips vidéo
- **BF5.1**: Le système doit extraire des segments vidéo pour chaque événement détecté.
- **BF5.2**: Le système doit inclure un buffer temporel avant et après l'événement.
- **BF5.3**: Le système doit fusionner les événements proches temporellement.

#### BF6: Fusion de clips
- **BF6.1**: Le système doit permettre la fusion de tous les clips d'événements en une seule vidéo récapitulative.
- **BF6.2**: Le système doit organiser chronologiquement les clips dans la vidéo fusionnée.

#### BF7: Génération de rapports
- **BF7.1**: Le système doit produire un rapport détaillé des événements détectés au format JSON.
- **BF7.2**: Le système doit fournir des statistiques sur les types d'objets détectés.

### 2.2 Besoins Non Fonctionnels

#### BNF1: Performance
- **BNF1.1**: Le système doit traiter les vidéos à une vitesse d'au moins 10 images par seconde sur un matériel standard.
- **BNF1.2**: Le système doit optimiser l'utilisation de la mémoire pour gérer de longues séquences vidéo.
- **BNF1.3**: Le système doit permettre le saut de frames pour accélérer le traitement.

#### BNF2: Fiabilité
- **BNF2.1**: Le système doit gérer les erreurs de lecture de fichiers vidéo.
- **BNF2.2**: Le système doit créer des journaux d'erreurs détaillés.
- **BNF2.3**: Le système doit reprendre le traitement après une interruption.

#### BNF3: Configurabilité
- **BNF3.1**: Le système doit permettre l'ajustement de tous les paramètres de détection.
- **BNF3.2**: Le système doit supporter différentes configurations pour différents environnements.
- **BNF3.3**: Le système doit pouvoir charger des configurations à partir de fichiers externes.

#### BNF4: Maintenabilité
- **BNF4.1**: Le code doit être modulaire et bien documenté.
- **BNF4.2**: Les composants doivent être faiblement couplés pour faciliter les modifications.
- **BNF4.3**: Le système doit suivre les bonnes pratiques de développement Python.

#### BNF5: Compatibilité
- **BNF5.1**: Le système doit fonctionner sur les systèmes d'exploitation Windows, Linux et macOS.
- **BNF5.2**: Le système doit supporter les formats vidéo courants (MP4, AVI, MOV).
- **BNF5.3**: Le système doit être compatible avec Python 3.8 et versions ultérieures.

### 2.3 Diagramme de cas d'utilisation

Le diagramme de cas d'utilisation ci-dessous illustre les interactions principales entre l'utilisateur et le système d'analyse CCTV:

```
+--------------------------------------------------+
|                    Système CCTV                   |
+--------------------------------------------------+
|                                                  |
|  +---------------+       +--------------------+  |
|  | Configurer    |       | Traiter vidéo de   |  |
|  | paramètres    |------>| surveillance       |  |
|  +---------------+       +--------------------+  |
|         ^                         |              |
|         |                         v              |
|  +------+--------+       +--------------------+  |
|  | Ajuster       |       | Détecter mouvements|  |
|  | sensibilité   |       | et objets          |  |
|  +---------------+       +--------------------+  |
|                                    |              |
|                                    v              |
|                          +--------------------+  |
|                          | Analyser événements|  |
|                          +--------------------+  |
|                                    |              |
|                                    v              |
|                          +--------------------+  |
|                          | Générer clips      |  |
|  +---------------+       | d'événements       |  |
|  | Visualiser    |<------+--------------------+  |
|  | événements    |                |              |
|  +---------------+                v              |
|         ^                +--------------------+  |
|         |                | Fusionner clips en |  |
|         +----------------| vidéo récapitulative  |
|                          +--------------------+  |
|                                    |              |
|                                    v              |
|                          +--------------------+  |
|  +---------------+       | Générer rapport    |  |
|  | Consulter     |<------| d'analyse          |  |
|  | rapport       |       +--------------------+  |
|  +---------------+                               |
|                                                  |
+--------------------------------------------------+
```

## 3. Conception du système

### 3.1 Modèles

Le système utilise plusieurs structures de données pour représenter les événements détectés et les segments vidéo. Les principaux modèles de données sont:

#### 3.1.1 Modèle Event

La classe `Event` représente un événement détecté dans la vidéo:

```python
@dataclass
class Event:
    type: str                  # Type d'événement (mouvement, objet détecté, etc.)
    timestamp: float           # Timestamp en secondes dans la vidéo
    frame_idx: int             # Index de la frame où l'événement a été détecté
    score: float               # Score de confiance/importance (0-1)
    confidence: float          # Niveau de confiance de la détection
    object_id: Optional[int]   # ID de l'objet concerné (si applicable)
    bbox: Optional[List[float]]  # Coordonnées du rectangle englobant [x1,y1,x2,y2]
    metadata: Dict[str, Any]   # Métadonnées supplémentaires
```

Cette structure permet de stocker toutes les informations pertinentes sur un événement détecté, y compris son type, sa position temporelle dans la vidéo, et des données contextuelles.

#### 3.1.2 Modèle VideoSegment

La classe `VideoSegment` représente un segment de vidéo correspondant à un ou plusieurs événements:

```python
@dataclass
class VideoSegment:
    start_time: float         # Temps de début du segment (secondes)
    end_time: float           # Temps de fin du segment (secondes)
    start_frame: int          # Frame de début
    end_frame: int            # Frame de fin
    duration: float           # Durée du segment (secondes)
    events: List[Event]       # Liste des événements contenus dans ce segment
    output_file: Optional[Path]  # Chemin du fichier clip généré
    
```

Cette structure permet de définir précisément les segments vidéo à extraire et à associer aux événements détectés.

#### 3.1.3 Configurations

Le système utilise également des classes de configuration pour paramétrer chaque composant:

- `MotionDetectorConfig`: Configuration pour la détection de mouvement
- `ObjectDetectorConfig`: Configuration pour la détection d'objets
- `ObjectTrackerConfig`: Configuration pour le suivi d'objets
- `EventAnalyzerConfig`: Configuration pour l'analyse d'événements
- `VideoExporterConfig`: Configuration pour l'exportation vidéo

Exemple de configuration ultra-sensible pour la détection de mouvement:

```python
motion_cfg = MotionDetectorConfig(
    min_area=100,        # Surface minimale (pixels) pour considérer un mouvement
    var_threshold=15,    # Seuil de variance pour la détection
)
```

### 3.2 Front-end

Le système actuel utilise principalement une interface en ligne de commande (CLI) plutôt qu'une interface graphique complète. Cette approche privilégie la flexibilité et l'intégration à d'autres systèmes.

#### 3.2.1 Interface de ligne de commande

L'interface principale est définie dans le script `cctv_analysis_pipeline.py` qui expose les fonctionnalités suivantes:

```
usage: cctv_analysis_pipeline.py [-h] [-o OUTPUT] [--skip-frames SKIP_FRAMES] [--merge] [--merged-output MERGED_OUTPUT] video

CCTV Analysis with Ultra-Sensitive Detection and Highlight Merging

positional arguments:
  video                 Path to source video file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output folder for highlights and summary (default: highlights)
  --skip-frames SKIP_FRAMES
                        Process every Nth frame (default: 1, meaning process all frames)
  --merge               Merge all highlight clips into a single video
  --merged-output MERGED_OUTPUT
                        Output file for merged highlights (default: output/merged_highlights.mp4)
```

Cette interface permet aux utilisateurs de spécifier:
- Le fichier vidéo à analyser
- Le dossier de sortie pour les clips d'événements
- La fréquence d'échantillonnage des frames
- L'option de fusionner automatiquement les clips
- Le nom du fichier de sortie pour la vidéo fusionnée

#### 3.2.2 Sorties visuelles

Bien que le système n'offre pas d'interface graphique, il génère plusieurs types de sorties visuelles:

1. **Clips vidéo individuels**: Chaque événement détecté génère un clip vidéo (`highlight_X.mp4`).
2. **Vidéo récapitulative**: Fusion de tous les clips en une seule vidéo (`merged_highlights.mp4`).
3. **Rapports JSON**: Informations détaillées sur les événements détectés.

### 3.3 Contrôleurs

Le système est conçu selon une architecture en pipeline, où chaque étape de traitement est encapsulée dans un composant distinct. Le flux de contrôle principal est orchestré par la fonction `process_cctv_video()` dans le module `pipeline.py`.

#### 3.3.1 Orchestrateur principal

Le contrôleur principal gère l'enchaînement des opérations:

```python
def process_cctv_video(
    video_path: str,
    *,
    motion_cfg: MotionDetectorConfig = MotionDetectorConfig(),
    objdet_cfg: ObjectDetectorConfig = ObjectDetectorConfig(),
    tracker_cfg: ObjectTrackerConfig = ObjectTrackerConfig(),
    event_cfg: EventAnalyzerConfig = EventAnalyzerConfig(),
    export_cfg: VideoExporterConfig = VideoExporterConfig(),
    skip_frames: int = 2,
) -> Dict[str, Any]:
    """End‑to‑end CCTV analysis pipeline."""

    # 1 ▸ Extract frames & timestamps
    frames, timestamps, fps = video_utils.extract_frames(
        video_path, skip_frames=skip_frames
    )

    # 2 ▸ Motion detection
    motion = MotionDetector(motion_cfg)
    motion_data = motion.detect_motion(frames)

    # 3 ▸ Object detection
    detector = ObjectDetector(objdet_cfg)
    detections = detector.detect_objects(frames)
    
    # 4 ▸ Object tracking
    tracker = ObjectTracker(tracker_cfg)
    tracked_history = defaultdict(list)
    for idx, frame_det in enumerate(filtered):
        tracks = tracker.track_objects([frame_det], timestamps[idx : idx + 1])
        
    # 5 ▸ Event analysis
    analyzer = EventAnalyzer(event_cfg)
    events = analyzer.analyze_events(
        motion_data, tracked_history, timestamps, fps
    )

    # 6 ▸ Highlight export
    exporter = VideoExporter(export_cfg)
    segments = exporter.create_highlights(
        video_path, events, timestamps, "highlights"
    )

    # Génération du rapport
    report = {
        "total_video_duration": timestamps[-1] if timestamps else 0,
        "total_events": len(events),
        "highlight_count": len(segments),
        "class_counts": detector.get_detection_summary(filtered)["class_counts"],
    }

    return {"segments": segments, "events": events, "report": report}
```

#### 3.3.2 Mode Ultra-sensible

Le script `cctv_analysis_pipeline.py` fournit également une fonction spéciale pour créer des configurations ultra-sensibles, adaptées à la détection d'événements subtils:

```python
def create_ultra_sensitive_configs():
    """Create configurations with extremely low thresholds for maximum event detection."""
    # Ultra-sensitive motion detection
    motion_cfg = MotionDetectorConfig(
        min_area=100,  # Even lower minimum area
        var_threshold=15,  # Even lower variance threshold
    )
    
    # Ultra-sensitive object detection
    objdet_cfg = ObjectDetectorConfig(
        confidence_threshold=0.3,  # Even lower confidence threshold
    )
    
    # Plus d'autres configurations...
    
    return motion_cfg, objdet_cfg, tracker_cfg, event_cfg, export_cfg
```

#### 3.3.3 Fusion de vidéos

La fonction `merge_highlights()` contrôle le processus de fusion des clips individuels en une vidéo récapitulative:

```python
def merge_highlights(input_dir: str, output_file: str) -> bool:
    """Merge all highlight videos in the input directory into a single output file using FFmpeg."""
    # Recherche des clips vidéo
    video_files = glob.glob(os.path.join(input_dir, "highlight_*.mp4"))
    
    # Tri chronologique des clips
    video_files.sort(key=lambda x: int(os.path.basename(x).split("_")[1]))
    
    # Création d'un fichier de liste pour FFmpeg
    list_file = "filelist.txt"
    with open(list_file, "w") as f:
        for video_file in video_files:
            f.write(f"file '{video_file}'\n")
    
    # Exécution de FFmpeg pour la fusion
    cmd = [
        ffmpeg_exe,
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-y",
        output_file
    ]
    
    # Exécution de la commande
    subprocess.run(cmd, check=True)
```

### 3.4 Services

Le système est composé de plusieurs services spécialisés, chacun responsable d'une étape spécifique du traitement vidéo.

#### 3.4.1 Service de détection de mouvement

Le `MotionDetector` est responsable de l'identification des changements significatifs entre les frames consécutives:

```python
class MotionDetector:
    def __init__(self, config: MotionDetectorConfig):
        self.config = config
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=self.config.history,
            varThreshold=self.config.var_threshold
        )
        
    def detect_motion(self, frames: List[np.ndarray]) -> List[Dict]:
        motion_data = []
        for frame in frames:
            # Application du soustracteur de fond
            fg_mask = self.bg_subtractor.apply(frame)
            
            # Recherche des contours de mouvement
            contours, _ = cv2.findContours(
                fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            # Filtrage par taille minimale
            motion_regions = [
                cv2.boundingRect(c) for c in contours 
                if cv2.contourArea(c) > self.config.min_area
            ]
            
            motion_data.append({
                "regions": motion_regions,
                "motion_score": len(motion_regions) / self.config.normalization_factor
            })
            
        return motion_data
```

#### 3.4.2 Service de détection d'objets

Le `ObjectDetector` utilise le modèle YOLOv8 pour identifier et classifier les objets dans chaque frame:

```python
class ObjectDetector:
    def __init__(self, config: ObjectDetectorConfig):
        self.config = config
        # Chargement du modèle YOLOv8
        self.model = YOLO(self.config.model_path)
        
    def detect_objects(self, frames: List[np.ndarray]) -> List[List[Dict]]:
        all_detections = []
        for frame in frames:
            # Exécution de l'inférence YOLOv8
            results = self.model(
                frame, 
                conf=self.config.confidence_threshold,
                classes=self.config.relevant_classes
            )
            
            # Conversion des résultats en format standard
            frame_detections = []
            for detection in results[0].boxes.data:
                x1, y1, x2, y2, conf, cls = detection
                frame_detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "class": self.model.names[int(cls)],
                    "class_id": int(cls)
                })
                
            all_detections.append(frame_detections)
            
        return all_detections
```

#### 3.4.3 Service de suivi d'objets

Le `ObjectTracker` assure le suivi des objets détectés à travers les frames:

```python
class ObjectTracker:
    def __init__(self, config: ObjectTrackerConfig):
        self.config = config
        self.next_object_id = 0
        self.objects = {}  # Dictionnaire des objets actuellement suivis
        self.disappeared = {}  # Compteur des frames depuis la dernière détection
        
    def track_objects(self, detections: List[List[Dict]], timestamps: List[float]) -> Dict[int, Dict]:
        tracked_objects = {}
        
        for frame_idx, frame_dets in enumerate(detections):
            # Calcul des correspondances entre détections et objets suivis
            # en utilisant l'IoU (Intersection over Union)
            matches, unmatched_dets, unmatched_objs = self._match_detections(frame_dets)
            
            # Mise à jour des objets correspondants
            for obj_id, det_idx in matches:
                self._update_object(obj_id, frame_dets[det_idx], timestamps[frame_idx])
                tracked_objects[obj_id] = self.objects[obj_id]
                
            # Enregistrement des nouvelles détections
            for det_idx in unmatched_dets:
                obj_id = self._register_object(frame_dets[det_idx], timestamps[frame_idx])
                tracked_objects[obj_id] = self.objects[obj_id]
                
            # Gestion des objets non détectés
            for obj_id in unmatched_objs:
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.config.max_disappeared:
                    self._deregister_object(obj_id)
                    
        return tracked_objects
```

#### 3.4.4 Service d'analyse d'événements

Le `EventAnalyzer` identifie les événements significatifs à partir des données de mouvement et de suivi d'objets:

```python
class EventAnalyzer:
    def __init__(self, config: EventAnalyzerConfig):
        self.config = config
        
    def analyze_events(
        self, 
        motion_data: List[Dict], 
        tracked_objects: Dict[int, List[Dict]], 
        timestamps: List[float],
        fps: float
    ) -> List[Event]:
        events = []
        
        # Détection d'événements basés sur le mouvement
        motion_events = self._analyze_motion_events(motion_data, timestamps)
        events.extend(motion_events)
        
        # Détection d'événements basés sur les objets
        object_events = self._analyze_object_events(tracked_objects, timestamps, fps)
        events.extend(object_events)
        
        # Filtrage des événements par score
        filtered_events = self._filter_events(events)
        
        return filtered_events
        
    def _analyze_motion_events(self, motion_data, timestamps):
        # Logique de détection des événements de mouvement
        # ...
        
    def _analyze_object_events(self, tracked_objects, timestamps, fps):
        # Logique de détection des événements liés aux objets
        # (changements de vitesse, stationnement, etc.)
        # ...
        
    def _filter_events(self, events):
        # Filtrage des événements par score d'importance
        filtered = [e for e in events if e.score >= 0.05]
        filtered.sort(key=lambda ev: ev.score, reverse=True)
        return filtered[:40]  # Retourne les 40 événements les plus importants
```

#### 3.4.5 Service d'exportation vidéo

Le `VideoExporter` génère des clips vidéo pour chaque événement détecté:

```python
class VideoExporter:
    def __init__(self, config: VideoExporterConfig):
        self.config = config
        
    def create_highlights(
        self, 
        source_video: str, 
        events: List[Event], 
        timestamps: List[float],
        output_dir: str
    ) -> List[VideoSegment]:
        # Création du dossier de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        # Regroupement des événements proches temporellement
        grouped_events = self._group_events(events)
        
        segments = []
        for idx, event_group in enumerate(grouped_events):
            # Détermination des temps de début et fin du segment
            start_time = min(e.timestamp for e in event_group) - self.config.buffer_seconds
            end_time = max(e.timestamp for e in event_group) + self.config.buffer_seconds
            
            # Ajustement pour rester dans les limites de la vidéo
            start_time = max(0, start_time)
            end_time = min(timestamps[-1], end_time)
            
            # Conversion en indices de frames
            start_frame = self._find_nearest_frame(timestamps, start_time)
            end_frame = self._find_nearest_frame(timestamps, end_time)
            
            # Création du segment
            segment = VideoSegment(
                start_time=start_time,
                end_time=end_time,
                start_frame=start_frame,
                end_frame=end_frame,
                duration=end_time - start_time,
                events=event_group,
                output_file=Path(output_dir) / f"highlight_{idx}.mp4"
            )
            
            # Extraction du clip vidéo
            self._extract_video_segment(
                source_video, 
                str(segment.output_file), 
                segment.start_time, 
                segment.duration
            )
            
            segments.append(segment)
            
        return segments
        
    def _group_events(self, events):
        # Regroupement des événements proches temporellement
        # ...
        
    def _extract_video_segment(self, source_video, output_file, start_time, duration):
        # Extraction du segment vidéo en utilisant FFmpeg
        # ...
```

### 3.5 Service IA

Le service d'intelligence artificielle est principalement basé sur le modèle YOLOv8 pour la détection et la classification d'objets.

#### 3.5.1 Modèle YOLOv8

YOLOv8 (You Only Look Once, version 8) est un réseau de neurones convolutifs de pointe pour la détection d'objets en temps réel. Ce modèle offre un excellent compromis entre vitesse et précision.

Caractéristiques principales:
- Détection en une seule passe (contrairement aux approches en deux étapes)
- Architecture basée sur CSPDarknet53 pour l'extraction de caractéristiques
- Capacité à détecter multiples classes d'objets simultanément
- Haute précision pour la localisation des objets (boîtes englobantes)

Le système utilise spécifiquement la version légère `yolov8n.pt` (YOLOv8 nano) qui est optimisée pour les performances sur du matériel standard tout en maintenant une précision acceptable.

#### 3.5.2 Paramètres de détection

L'intégration du modèle YOLOv8 est configurée avec les paramètres suivants:

```python
objdet_cfg = ObjectDetectorConfig(
    model_path="yolov8n.pt",  # Chemin vers le modèle pré-entraîné
    confidence_threshold=0.3,  # Seuil de confiance (ultra-sensible)
    relevant_classes=[0, 1, 2, 3, 5, 7],  # IDs des classes pertinentes
)
```

Les classes standard de COCO détectées incluent:
- Personnes (ID 0)
- Véhicules (voitures, camions, motos, etc.)
- Animaux domestiques courants
- Objets du quotidien

#### 3.5.3 Post-traitement des détections

Après la détection initiale par YOLOv8, plusieurs étapes de post-traitement sont appliquées:

1. **Filtrage par classe**: Seules les classes spécifiées comme pertinentes sont conservées.
2. **Filtrage par confiance**: Les détections avec un score de confiance inférieur au seuil défini sont éliminées.
3. **Suivi d'objets**: Les détections sont associées à travers les frames pour créer des trajectoires cohérentes.
4. **Analyse comportementale**: Les trajectoires sont analysées pour identifier des comportements spécifiques (arrêt prolongé, accélération soudaine, etc.).

#### 3.5.4 Pipeline d'IA complet

Le pipeline d'intelligence artificielle complet comprend:

1. **Prétraitement**: Extraction et normalisation des frames vidéo
2. **Détection de mouvement**: Identification des zones de changement dans l'image
3. **Détection d'objets**: Application du modèle YOLOv8 pour identifier les objets
4. **Suivi d'objets**: Association des détections à travers le temps
5. **Analyse d'événements**: Identification de comportements d'intérêt
6. **Scoring**: Attribution d'un score d'importance à chaque événement
7. **Filtrage**: Sélection des événements les plus significatifs

Cette approche multi-niveaux permet d'atteindre un haut niveau de sensibilité tout en maintenant un taux raisonnable de faux positifs.

## 4. Conception base de données

Le système d'analyse CCTV n'utilise pas de base de données relationnelle traditionnelle, mais s'appuie sur une organisation structurée de fichiers pour stocker les données générées.

### 4.1 Organisation des fichiers

```
CCTV/
├── data/                  # Vidéos sources à analyser
│   ├── video1.mp4
│   └── video2.mp4
├── highlights/            # Clips vidéo des événements individuels
│   ├── highlight_0.mp4
│   ├── highlight_1.mp4
│   ├── ...
│   ├── sensitive_summary.json  # Résumé global de l'analyse
│   └── events_detail.json      # Détails sur tous les événements
└── output/                # Vidéos récapitulatives fusionnées
    └── merged_highlights.mp4
```

### 4.2 Structure des fichiers JSON

#### 4.2.1 Fichier sensitive_summary.json

Ce fichier contient un résumé global de l'analyse vidéo:

```json
{
  "total_video_duration": 3600.5,     // Durée totale en secondes
  "total_events": 42,                // Nombre total d'événements détectés
  "highlight_count": 15,             // Nombre de clips générés
  "class_counts": {                  // Distribution des classes d'objets
    "person": 26,
    "car": 14,
    "dog": 2
  }
}
```

#### 4.2.2 Fichier events_detail.json

Ce fichier contient des informations détaillées sur chaque événement détecté:

```json
[
  {
    "type": "movement",            // Type d'événement
    "timestamp": 127.5,            // Position temporelle (secondes)
    "frame_idx": 3825,             // Index de la frame
    "score": 0.87,                 // Score d'importance (0-1)
    "confidence": 0.92,            // Confiance de la détection
    "metadata": {                  // Métadonnées spécifiques
      "motion_intensity": 0.45,
      "region": [120, 340, 210, 480]
    }
  },
  {
    "type": "object_detected",
    "timestamp": 143.2,
    "frame_idx": 4296,
    "score": 0.95,
    "confidence": 0.88,
    "object_id": 12,               // ID de l'objet suivi
    "bbox": [250, 180, 320, 380],  // Boîte englobante [x1,y1,x2,y2]
    "metadata": {
      "class": "person",
      "velocity": 2.3,
      "direction": [1.2, -0.5]
    }
  },
  // ... autres événements
]
```

### 4.3 Modèle de données logique

Bien que le système n'utilise pas de base de données relationnelle, on peut représenter conceptuellement les relations entre les entités principales:

#### 4.3.1 Entité Video

Représente une vidéo source analysée.
- **Attributs**: path, duration, fps, frame_count
- **Relation 1:N avec Event**: Une vidéo contient plusieurs événements

#### 4.3.2 Entité Event

Représente un événement détecté dans une vidéo.
- **Attributs**: type, timestamp, frame_idx, score, confidence, metadata
- **Relation N:1 avec Video**: Un événement appartient à une vidéo
- **Relation N:1 avec Object**: Un événement peut être associé à un objet
- **Relation N:1 avec Segment**: Un événement appartient à un segment vidéo

#### 4.3.3 Entité Object

Représente un objet détecté et suivi dans la vidéo.
- **Attributs**: object_id, class, trajectory
- **Relation 1:N avec Event**: Un objet peut générer plusieurs événements

#### 4.3.4 Entité Segment

Représente un segment vidéo extrait.
- **Attributs**: start_time, end_time, duration, output_file
- **Relation 1:N avec Event**: Un segment contient plusieurs événements

### 4.4 Persistance et évolutivité

Le système actuel est conçu pour des analyses ponctuelles plutôt que pour le stockage à long terme. Pour une utilisation à plus grande échelle, plusieurs améliorations pourraient être envisagées:

1. **Intégration d'une base de données NoSQL**: MongoDB ou ElasticSearch pour stocker les événements et les métadonnées
2. **Stockage des vidéos dans un système de fichiers distribué**: Pour gérer de grandes quantités de données vidéo
3. **Indexation des événements**: Pour permettre des recherches rapides par type, timestamp, objet, etc.
4. **Versionnement des analyses**: Pour suivre l'évolution des résultats avec différents paramètres

## 5. Implémentation

### 5.1 Technologies utilisées

Le système d'analyse CCTV est construit sur un ensemble de technologies modernes pour le traitement vidéo et l'intelligence artificielle:

#### 5.1.1 Python

- **Version**: Python 3.8 ou supérieure
- **Rôle**: Langage de programmation principal pour l'ensemble du système
- **Avantages**: Écosystème riche pour le traitement d'image et l'IA, lisibilité du code, développement rapide

#### 5.1.2 OpenCV

- **Version**: OpenCV 4.x
- **Rôle**: Bibliothèque de vision par ordinateur pour le traitement d'images et la détection de mouvement
- **Fonctionnalités utilisées**:
  - Lecture et manipulation de vidéos
  - Soustraction d'arrière-plan (BackgroundSubtractorMOG2)
  - Détection de contours
  - Opérations morphologiques pour le filtrage

#### 5.1.3 YOLOv8

- **Version**: YOLOv8 (nano)
- **Rôle**: Modèle de deep learning pour la détection et classification d'objets
- **Caractéristiques**:
  - Taille du modèle: ~6.5 Mo (version nano)
  - Classes: 80 catégories standard COCO
  - Précision: mAP 37.3% (COCO val2017)
  - Vitesse: ~500 FPS sur GPU, ~40 FPS sur CPU standard

#### 5.1.4 FFmpeg

- **Version**: FFmpeg intégré via imageio_ffmpeg
- **Rôle**: Traitement et manipulation de fichiers vidéo
- **Utilisations**:
  - Extraction de segments vidéo
  - Fusion de clips en une vidéo continue
  - Conversion de formats si nécessaire

#### 5.1.5 NumPy

- **Rôle**: Traitement numérique efficace pour les opérations sur les images et les matrices
- **Utilisations**:
  - Manipulation des arrays d'images
  - Calculs vectorisés pour le traitement d'images
  - Analyse statistique des mouvements et trajectoires

#### 5.1.6 Dataclasses

- **Rôle**: Structures de données typées et lisibles pour les modèles
- **Avantages**:
  - Typage des attributs pour une meilleure fiabilité
  - Génération automatique des méthodes standard
  - Documentation intégrée des structures de données

### 5.2 Structure du code

L'organisation du code suit une architecture modulaire avec séparation claire des responsabilités:

```
CCTV/
├── src/
│   └── cctv_analyzer/            # Package principal
│       ├── core/                 # Composants essentiels
│       │   ├── motion_detector.py
│       │   ├── object_detector.py
│       │   ├── object_tracker.py
│       │   ├── event_analyzer.py
│       │   ├── video_exporter.py
│       │   └── video_utils.py
│       ├── models/               # Structures de données
│       │   └── event_models.py
│       ├── config.py             # Configurations
│       ├── pipeline.py           # Orchestration du pipeline
│       └── __init__.py
├── cctv_analysis_pipeline.py     # Script principal
├── requirements.txt              # Dépendances
├── setup.py                      # Installation du package
└── USAGE.md, CONFIGURATION.md    # Documentation
```

#### 5.2.1 Structure des modules

Chaque module du système suit une structure cohérente:

1. **Classes de configuration**: Définition des paramètres configurables avec valeurs par défaut
2. **Classe principale**: Implémentation de la fonctionnalité principale du module
3. **Méthodes publiques**: Interface bien définie pour l'intégration avec les autres modules
4. **Méthodes privées**: Fonctionnalités internes utilisées par les méthodes publiques

Exemple de structure de module (motion_detector.py):

```python
"""Module de détection de mouvement."""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MotionDetectorConfig:
    """Configuration pour la détection de mouvement."""
    history: int = 50
    var_threshold: float = 25.0
    min_area: int = 300
    normalization_factor: float = 100.0

class MotionDetector:
    """Détecte les mouvements dans une séquence vidéo."""
    
    def __init__(self, config: MotionDetectorConfig):
        """Initialise le détecteur avec la configuration spécifiée."""
        self.config = config
        self.bg_subtractor = self._create_background_subtractor()
    
    def detect_motion(self, frames: List[np.ndarray]) -> List[Dict]:
        """Méthode publique principale pour détecter le mouvement."""
        # ...
        
    def _create_background_subtractor(self):
        """Méthode privée pour créer le soustracteur d'arrière-plan."""
        # ...
        
    def _process_frame(self, frame):
        """Méthode privée pour traiter une frame individuelle."""
        # ...
```

#### 5.2.2 Patterns de conception utilisés

Le système implémente plusieurs patterns de conception logicielle:

1. **Pattern Pipeline**: Chaîne de traitement où la sortie d'un composant devient l'entrée du suivant
2. **Pattern Strategy**: Configuration flexible de chaque composant via des classes de configuration
3. **Pattern Factory**: Création d'objets complexes (comme les événements) à partir de données brutes
4. **Pattern Façade**: Interface simplifiée exposée par le module pipeline

#### 5.2.3 Gestion des erreurs

Le système implémente une gestion robuste des erreurs:

1. **Validation des entrées**: Vérification des paramètres et des données en entrée
2. **Exceptions typées**: Utilisation d'exceptions spécifiques pour les différents types d'erreurs
3. **Journalisation**: Enregistrement détaillé des erreurs et avertissements
4. **Graceful degradation**: Continuation partielle du traitement en cas d'erreur non critique

Exemple de gestion d'erreur:

```python
try:
    # Traitement principal
    results = process_cctv_video(video_path, ...)
    
except FileNotFoundError:
    print(f"Erreur: Fichier vidéo non trouvé: {video_path}")
    return 1
    
except Exception as e:
    print(f"Erreur lors du traitement de la vidéo: {e}")
    # Journalisation détaillée de l'erreur
    log.error(f"Détails de l'erreur: {traceback.format_exc()}")
    return 1
```

## 6. Manuel

### 6.1 Installation

Pour installer le système d'analyse CCTV, suivez ces étapes:

1. **Prérequis**:
   - Python 3.8 ou supérieur
   - Pip (gestionnaire de paquets Python)
   - Environnement virtuel (recommandé)

2. **Installation des dépendances**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Installation du package**:
   ```bash
   pip install -e .
   ```

### 6.2 Utilisation basique

Pour analyser une vidéo avec les paramètres par défaut:

```bash
python cctv_analysis_pipeline.py data/ma_video.mp4
```

Les clips des événements détectés seront enregistrés dans le dossier `highlights/`.

### 6.3 Options de configuration

Le système offre plusieurs options de configuration:

```bash
python cctv_analysis_pipeline.py data/ma_video.mp4 \
    --output mon_dossier_highlights \
    --skip-frames 2 \
    --merge \
    --merged-output output/ma_video_resume.mp4
```

Options disponibles:
- `--output` ou `-o`: Dossier de sortie pour les clips et rapports
- `--skip-frames`: Traiter une frame sur N (pour accélérer l'analyse)
- `--merge`: Fusionner tous les clips en une seule vidéo
- `--merged-output`: Nom du fichier de sortie pour la vidéo fusionnée

### 6.4 Configuration avancée

Pour une configuration plus fine, modifiez les valeurs des classes de configuration dans votre code:

```python
from src.cctv_analyzer.config import MotionDetectorConfig, ObjectDetectorConfig

# Configuration personnalisée pour la détection de mouvement
motion_cfg = MotionDetectorConfig(
    min_area=200,         # Taille minimale pour considérer un mouvement
    var_threshold=20.0    # Seuil de variance plus bas = plus sensible
)

# Configuration personnalisée pour la détection d'objets
objdet_cfg = ObjectDetectorConfig(
    confidence_threshold=0.4,  # Seuil de confiance
    relevant_classes=[0, 1, 2] # Uniquement personnes (0), vélos (1), voitures (2)
)

# Traitement avec configurations personnalisées
results = process_cctv_video(
    "data/ma_video.mp4",
    motion_cfg=motion_cfg,
    objdet_cfg=objdet_cfg
)
```

### 6.5 Mode ultra-sensible

Pour une détection maximale des événements, même subtils:

```bash
python cctv_analysis_pipeline.py data/ma_video.mp4 --merge
```

Le script principal utilise automatiquement des configurations ultra-sensibles qui:
- Détectent des mouvements plus petits (min_area=100)
- Utilisent un seuil de confiance plus bas pour la détection d'objets (0.3)
- Permettent un suivi d'objets plus souple
- Considèrent plus d'événements comme significatifs

### 6.6 Interprétation des résultats

#### 6.6.1 Fichiers de sortie

Après l'analyse, vous trouverez:
- Des clips vidéo individuels dans le dossier `highlights/`
- Un fichier `sensitive_summary.json` avec le résumé de l'analyse
- Un fichier `events_detail.json` avec les détails de chaque événement
- Si demandé, une vidéo fusionnée dans le dossier `output/`

#### 6.6.2 Rapport d'analyse

Le rapport JSON contient des informations utiles:
- Durée totale de la vidéo
- Nombre total d'événements détectés
- Nombre de clips générés
- Distribution des classes d'objets détectés

### 6.7 Dépannage

#### 6.7.1 Problèmes courants

1. **Aucun événement détecté**:
   - Vérifiez que la vidéo contient effectivement du mouvement
   - Essayez de diminuer les seuils de sensibilité
   - Vérifiez que le format vidéo est supporté

2. **Trop d'événements détectés**:
   - Augmentez les seuils de sensibilité
   - Limitez les classes d'objets pertinentes
   - Utilisez un filtre spatial pour ignorer certaines zones de l'image

3. **Erreurs de lecture vidéo**:
   - Vérifiez que le fichier vidéo n'est pas corrompu
   - Convertissez la vidéo vers un format standard avec FFmpeg
   - Vérifiez les codecs vidéo installés

#### 6.7.2 Journalisation

Le système utilise le module `logging` de Python pour enregistrer les informations de diagnostic:

```bash
# Activer la journalisation détaillée
export PYTHONVERBOSE=1
python cctv_analysis_pipeline.py data/ma_video.mp4
```

Les messages de journal incluent:
- Informations sur les étapes de traitement
- Avertissements pour les situations non optimales
- Erreurs pour les problèmes empêchant l'analyse

### 6.8 Exemples d'utilisation

#### 6.8.1 Analyse d'une vidéo de parking

```bash
python cctv_analysis_pipeline.py data/parking_surveillance.mp4 \
    --output parking_highlights \
    --merge \
    --merged-output output/parking_resume.mp4
```

Cette commande va:
1. Analyser la vidéo `parking_surveillance.mp4`
2. Détecter les mouvements et objets (véhicules, personnes)
3. Générer des clips pour chaque événement dans `parking_highlights/`
4. Créer une vidéo récapitulative `parking_resume.mp4`

#### 6.8.2 Analyse accélérée d'une longue vidéo

```bash
python cctv_analysis_pipeline.py data/surveillance_24h.mp4 \
    --skip-frames 5 \
    --merge
```

Cette commande va:
1. Analyser la vidéo en traitant une frame sur 5 (accélération x5)
2. Générer des clips pour les événements détectés
3. Fusionner les clips en une vidéo récapitulative

