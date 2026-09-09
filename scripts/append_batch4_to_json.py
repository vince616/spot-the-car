# -*- coding: utf-8 -*-
import json

PATH = r"C:\Users\vincent.krief\Downloads\spot-the-car-app\scripts\cars.json"

with open(PATH, encoding="utf-8") as f:
    cars = json.load(f)

NEW = [
    {"name": "Kia Picanto", "url": "assets/cars/kia-picanto.jpg",
     "wikiFile": "Kia%20Picanto,%20Auto%202024,%20Zurich%20(PANA0815).jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Hyundai Inster", "Dacia Spring", "Toyota Yaris"],
     "slug": "kia-picanto"},
    {"name": "Subaru Impreza (2002)", "url": "assets/cars/subaru-impreza-gde.jpg",
     "wikiFile": "2001-2002%20Subaru%20Impreza%20(GDE%20MY02)%20RS%20sedan%20(2011-06-15)%2001.jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Audi A4", "Alfa Romeo Giulia", "BMW 323i (E21)"],
     "slug": "subaru-impreza-gde"},
    {"name": "Renault Vel Satis", "url": "assets/cars/renault-vel-satis.jpg",
     "wikiFile": "Renault%20Vel%20Satis%203.0%20dCi%20V6%20%E2%80%93%20Frontansicht,%205.%20Mai%202012,%20Ratingen.jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Renault Avantime", "Mercedes-Benz Classe C", "Renault Espace III"],
     "slug": "renault-vel-satis"},
    {"name": "Renault Avantime", "url": "assets/cars/renault-avantime.jpg",
     "wikiFile": "2002%20Renault%20Avantime%20Privilege%203.0%20Front.jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Renault Vel Satis", "Renault Espace III", "Citroen C4 Picasso"],
     "slug": "renault-avantime"},
    {"name": "Maserati GranTurismo (2023)", "url": "assets/cars/maserati-granturismo.jpg",
     "wikiFile": "Maserati%20GranTurismo%20Trofeo%201X7A0828.jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Aston Martin DB12", "Bentley Continental GT", "Porsche 911 Carrera S"],
     "slug": "maserati-granturismo"},
    {"name": "BMW X6 (E71)", "url": "assets/cars/bmw-x6-e71.jpg",
     "wikiFile": "BMW%20X6%20xDrive30d%20(E71)%20%E2%80%93%20Frontansicht,%2026.%20M%C3%A4rz%202011,%20D%C3%BCsseldorf.jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Range Rover Sport SVR", "Jaguar F-Pace", "Porsche Macan Electrique (2024)"],
     "slug": "bmw-x6-e71"},
    {"name": "Renault Clio II RS", "url": "assets/cars/renault-clio-ii-rs.jpg",
     "wikiFile": "Clio%20RS%202.2.jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Peugeot 208 GTi", "Volkswagen Golf R", "Renault Twingo III"],
     "slug": "renault-clio-ii-rs"},
    {"name": "Renault Clio VI", "url": "assets/cars/renault-clio-vi.jpg",
     "wikiFile": "Renault%20Clio%20TCe%20115%20Techno%20(VI)%20%E2%80%93%20h%2017032026.jpg",
     "anchorX": 50.0, "anchorY": 50.0, "maxScale": 2.6,
     "distractors": ["Peugeot 208 (Mk2)", "Renault Captur", "Citroën C3 III"],
     "slug": "renault-clio-vi"},
]

cars.extend(NEW)

with open(PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(cars, f, ensure_ascii=False, indent=2)

print(f"cars.json now has {len(cars)} entries (+{len(NEW)})")
