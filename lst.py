from pathlib import Path
import re
import fitz
import pandas as pd
import os

# Returns list of tuples: (date, dataframe)
# input_dir = Path.cwd() / 'Data'
# files = sorted(list(input_dir.glob("*.pdf*")), reverse=True)  # Sort for consistency
# files = files[:10]  # Limit to the first 3 files for testing

def vege_table():
    input_dir = Path.cwd() / 'data'
    files = sorted(list(input_dir.glob("*.pdf*")), reverse=True)  # Sort for consistency
    files = files[:10]  # Limit to the first 3 files for testing

    cwd = os.getcwd()
    # print(os.listdir(os.path.join(cwd, "data")))
    
    # print("vege table files:")
    # print(files)

    result = []
    columns = ['Veg', 'Rate','w-Ptth-Yesterday','','w-ptth-Today','','w-dbll-Yesterday','','w-dbll-Today',
        '','r-ptth-yesterday','','r-ptth-today','','r-dbll-yesterday','','r-dbll-today','',
        'r-nara-yesterday','','r-nara-today','']

    for file in files:
        doc = fitz.open(file)
        data = []
        target_y = 105   
        row_spacing = 13.5
        tolerance = 5

        while target_y <= 220:  
            page = doc.load_page(1)
            blocks = page.get_text("dict")["blocks"]
            row = [] 
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            bbox = span["bbox"]  
                            y0 = bbox[1]  
                            if target_y - tolerance <= y0 <= target_y + tolerance:
                                row.append(text)
            if row:
                data.append(row)
            target_y += row_spacing

        if data:
            df = pd.DataFrame(data)
            df.columns = columns[:len(df.columns)]
            df = df.drop([''], axis=1, errors='ignore')
            date = int(re.search(r'\d{8}', str(file)).group())
            result.append((date, df))
    return result

def oth_table():
    input_dir = Path.cwd() / 'data'
    files = sorted(list(input_dir.glob("*.pdf*")), reverse=True)  # Sort for consistency
    files = files[:10]  # Limit to the first 3 files for testing

    result = []
    columns = ['Oth', 'Rate','w-Ptth-Yesterday','','w-ptth-Today','','w-dbll-Yesterday','','w-dbll-Today',
        '','r-ptth-yesterday','','r-ptth-today','','r-dbll-yesterday','','r-dbll-today','',
        'r-nara-yesterday','','r-nara-today','']

    for file in files:
        doc = fitz.open(file)
        data = []
        target_y = 237   
        row_spacing = 13.5
        tolerance = 5

        while target_y <= 420:  
            page = doc.load_page(1)
            blocks = page.get_text("dict")["blocks"]
            row = [] 
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            bbox = span["bbox"]  
                            y0 = bbox[1]  
                            if target_y - tolerance <= y0 <= target_y + tolerance:
                                row.append(text)
            if row:
                data.append(row)
            target_y += row_spacing

        if data:
            df = pd.DataFrame(data)
            df.columns = columns[:len(df.columns)]
            df = df.drop([''], axis=1, errors='ignore')
            date = int(re.search(r'\d{8}', str(file)).group())
            result.append((date, df))

    return result

def fruits_table():
    input_dir = Path.cwd() / 'data'
    files = sorted(list(input_dir.glob("*.pdf*")), reverse=True)  # Sort for consistency
    files = files[:10]  # Limit to the first 3 files for testing

    result = []
    columns = ['Oth', 'Rate','w-Ptth-Yesterday','','w-ptth-Today','','w-dbll-Yesterday','','w-dbll-Today',
        '','r-ptth-yesterday','','r-ptth-today','','r-dbll-yesterday','','r-dbll-today','',
        'r-nara-yesterday','','r-nara-today','']

    for file in files:
        doc = fitz.open(file)
        data = []
        target_y = 434   
        row_spacing = 13.5
        tolerance = 5

        while target_y <= 490:  
            page = doc.load_page(1)
            blocks = page.get_text("dict")["blocks"]
            row = [] 
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            bbox = span["bbox"]  
                            y0 = bbox[1]  
                            if target_y - tolerance <= y0 <= target_y + tolerance:
                                row.append(text)
            if row:
                data.append(row)
            target_y += row_spacing

        if data:
            df = pd.DataFrame(data)
            df.columns = columns[:len(df.columns)]
            df = df.drop([''], axis=1, errors='ignore')
            date = int(re.search(r'\d{8}', str(file)).group())
            result.append((date, df))

    return result

def rice_table():
    input_dir = Path.cwd() / 'data'
    files = sorted(list(input_dir.glob("*.pdf*")), reverse=True)  # Sort for consistency
    files = files[:10]  # Limit to the first 3 files for testing

    result = []
    columns = ['Oth', 'Rate','w-Ptth-Yesterday','','w-ptth-Today','','w-mrndgmll-Yesterday','','w-mrndgmll-Today',
        '','r-ptth-yesterday','','r-ptth-today','','r-dbll-yesterday','','r-dbll-today','',
        'r-nara-yesterday','','r-nara-today','']

    for file in files:
        doc = fitz.open(file)
        data = []
        target_y = 525   
        row_spacing = 13.5
        tolerance = 5

        while target_y <= 610:  
            page = doc.load_page(1)
            blocks = page.get_text("dict")["blocks"]
            row = [] 
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            bbox = span["bbox"]  
                            y0 = bbox[1]  
                            if target_y - tolerance <= y0 <= target_y + tolerance:
                                row.append(text)
            if row:
                data.append(row)
            target_y += row_spacing

        if data:
            df = pd.DataFrame(data)
            df.columns = columns[:len(df.columns)]
            df = df.drop([''], axis=1, errors='ignore')
            date = int(re.search(r'\d{8}', str(file)).group())
            result.append((date, df))

    return result

def fish_table():
    input_dir = Path.cwd() / 'data'
    files = sorted(list(input_dir.glob("*.pdf*")), reverse=True)  # Sort for consistency
    files = files[:10]  # Limit to the first 3 files for testing

    result = []
    columns = ['Fish', 'Rate', 'w-plygd-Yesterday', '', 'w-plygd-Today', '', 
                'w-neg-Yesterday', '', 'w-neg-Today', '', 'r-neg-yesterday', '', 
                'r-neg-today', '', 'r-nara-yesterday', '', 'r-nara-today', '']

    for file in files:
        doc = fitz.open(file)
        data = []
        target_y = 642  
        row_spacing = 13.5  
        tolerance = 5

        while target_y <= 725:  
            page = doc.load_page(1)
            blocks = page.get_text("dict")["blocks"]
            row = [] 
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            bbox = span["bbox"]  
                            y0 = bbox[1]  
                            if target_y - tolerance <= y0 <= target_y + tolerance:
                                row.append(text)
            if row:
                data.append(row)
            target_y += row_spacing

        if data:
            df = pd.DataFrame(data)
            df.columns = columns[:len(df.columns)]
            df = df.drop([''], axis=1, errors='ignore')
            date = int(re.search(r'\d{8}', str(file)).group())
            result.append((date, df))

    return result