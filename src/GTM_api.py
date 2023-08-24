import os
import csv
import qrcode
import random
import string
from tqdm import tqdm
from PIL import Image
from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from email.mime.base import MIMEBase
from email import encoders
import requests