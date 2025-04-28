import os
import pandas as pd
import mne

# التحقق من تثبيت edfio
try:
    import edfio
except ImportError as e:
    raise ImportError("For exporting to EDF, please install edfio:\n    pip install edfio\n    or\n    conda install -c conda-forge edfio") from e

# إعداد مسارات المصدر والوجهة
source = r"C:\Users\XXX\orginal_dataset"        # مجلد ملفات EEG الأصلية
destination = r"C:\Users\XXX\splitted_segments"   # مجلد حفظ الملفات المستقطعة
csv_file = r"C:\Users\XXX\seizure_recordings.csv"  # ملف CSV الذي يحتوي على معلومات النوبات

# مدة الفترة المطلوبة قبل بداية النوبة (ثوانٍ)
pre_duration = 30  # 30 ثانية قبل النوبة

# التأكد من وجود مجلد الوجهة
if not os.path.exists(destination):
    os.makedirs(destination)

# قراءة ملف CSV باستخدام pandas
df = pd.read_csv(csv_file)

# حلقة لقراءة كل صف من ملف CSV
for idx, row in df.iterrows():
    file_name = row['File_Name']          # اسم ملف EEG، مثل "chb05_06.edf"
    seizure_start = row['Seizure_Start']    # زمن بداية النوبة (بالثواني)
    seizure_number = row['Seizure_Number']  # رقم النوبة في الملف
    # حساب زمن بداية المقطع المطلوب (30 ثانية قبل بداية النوبة)
    preictal_start = seizure_start - pre_duration
    preictal_end = seizure_start  # ينتهي عند بداية النوبة

    # الحصول على المسار الكامل للملف الأصلي
    file_path = os.path.join(source, file_name)
    
    # التحقق من وجود الملف
    if not os.path.isfile(file_path):
        print(f"File {file_path} not found. Skipping...")
        continue

    # قراءة ملف EDF باستخدام MNE
    try:
        raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue

    # قص المقطع المطلوب (الفترة قبل النوبة)
    try:
        raw_crop = raw.copy().crop(tmin=preictal_start, tmax=preictal_end)
    except Exception as e:
        print(f"Error cropping {file_path}: {e}")
        continue

    # بناء اسم الملف الناتج مع إضافة اللاحقة المناسبة
    base_name = os.path.splitext(file_name)[0]
    output_file = f"{base_name}_seizure{seizure_number}_preictal.edf"
    output_path = os.path.join(destination, output_file)
    
    # حفظ المقطع المستقطع بصيغة EDF باستخدام الدالة export()
    try:
        raw_crop.export(output_path, fmt='edf', overwrite=True)
        print(f"Saved preictal segment to {output_path}")
    except Exception as e:
        print(f"Error exporting {output_path}: {e}")
