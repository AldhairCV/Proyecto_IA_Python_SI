
# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys

cred = credentials.Certificate("firebase_key.json")  # 👈 Se usa el archivo JSON aquí
firebase_admin.initialize_app(cred)

db = firestore.client()

