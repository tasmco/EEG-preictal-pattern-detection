import os
import mne
import numpy as np
from mne.preprocessing import ICA
import scipy.stats
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

input_folder = r"C:\Users\XXX\splitted_segments"
output_folder = r"C:\Users\XXX\cleaned_segments"

l_freq, h_freq = 1.0, 10.0
n_components_ica = 0.99  
max_components_to_exclude = 5
kurt_threshold = 50

def detect_eog_components(ica, raw, eog_ch="FP1-F7"):
    """اكتشاف مركبات EOG عبر find_bads_eog."""
    eog_inds, _ = ica.find_bads_eog(raw, ch_name=eog_ch)
    return eog_inds

def compute_kurtosis(ica, raw):
    """حساب الكورتوسيس لكل مركبة في الإشارة."""
    sources = ica.get_sources(raw).get_data()  # (n_components, n_times)
    kurt_vals = [scipy.stats.kurtosis(comp, fisher=False) for comp in sources]
    return np.array(kurt_vals)

for fname in os.listdir(input_folder):
    if not fname.endswith('.edf'):
        continue

    file_path = os.path.join(input_folder, fname)
    print(f"\nProcessing file: {file_path}")
    try:
        raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
        
        # تهيئة meas_date لتجنب الخطأ
        raw.set_meas_date(None)
        
        # فلترة
        raw.filter(l_freq, h_freq, fir_design='firwin', verbose=False)

        ica = ICA(n_components=n_components_ica, method='fastica', random_state=42, max_iter=1000)
        ica.fit(raw)

        # اكتشاف مركبات EOG
        eog_inds = detect_eog_components(ica, raw, eog_ch="FP1-F7")

        # حساب الكورتوسيس
        kurt_vals = compute_kurtosis(ica, raw)
        bads_by_kurt = np.where(kurt_vals > kurt_threshold)[0]

        # تجميع المركبات (دون .tolist())
        candidate_bads = set(eog_inds) | set(bads_by_kurt)
        candidate_bads = sorted(candidate_bads)
        if len(candidate_bads) > max_components_to_exclude:
            candidate_bads = candidate_bads[:max_components_to_exclude]

        print(f"{fname}: Detected EOG components: {eog_inds}")
        print(f"{fname}: Components with kurtosis > {kurt_threshold}: {list(bads_by_kurt)}")
        print(f"{fname}: Final components to exclude: {candidate_bads}")

        ica.exclude = candidate_bads

        cleaned_raw = ica.apply(raw.copy())

        # مرة أخرى مسح meas_date قبل الحفظ
        cleaned_raw.set_meas_date(None)

        out_path = os.path.join(output_folder, fname.replace('.edf', '_cleaned.fif'))
        cleaned_raw.save(out_path, overwrite=True)
        print(f"{fname}: Saved cleaned segment to {out_path}")

    except Exception as e:
        print(f"Error processing {fname}: {e}")
