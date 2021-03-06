
import librosa
import librosa.display
import sklearn
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from librosa import*
import tqdm
from scipy.stats import kurtosis
from scipy.stats import skew

print(os.getcwd())

print(os.getcwd())

def extract_features(y,sr=22050,n_fft=1024,hop_length=512):
    features = {'centroid': librosa.feature.spectral_centroid(y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel(),
                'flux': librosa.onset.onset_strength(y=y, sr=sr).ravel(),
                'rmse': librosa.feature.rms(y, frame_length=n_fft, hop_length=hop_length).ravel(),
                'zcr': librosa.feature.zero_crossing_rate(y, frame_length=n_fft, hop_length=hop_length).ravel(),
                'contrast': librosa.feature.spectral_contrast(y, sr=sr).ravel(),
                'bandwidth': librosa.feature.spectral_bandwidth(y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel(),
                'flatness': librosa.feature.spectral_flatness(y, n_fft=n_fft, hop_length=hop_length).ravel(),
                'rolloff': librosa.feature.spectral_rolloff(y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()}

    # MFCC treatment
    mfcc = librosa.feature.mfcc(y, n_fft=n_fft, hop_length=hop_length, n_mfcc=20)
    for idx, v_mfcc in enumerate(mfcc):
        features['mfcc_{}'.format(idx)] = v_mfcc.ravel()

    # harmony and percu

    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Get statistics from the vectors
    def get_feature_stats(features):
        result = {}
        for k, v in features.items():
            #result['{}_max'.format(k)] = np.max(v)
            #result['{}_min'.format(k)] = np.min(v)
            result['{}_mean'.format(k)] = np.mean(v)
            result['{}_var'.format(k)] = np.var(v)
            #result['{}_kurtosis'.format(k)] = kurtosis(v)
            #result['{}_skew'.format(k)] = skew(v)
        return result

    dict_agg_features = get_feature_stats(features)
    dict_agg_features['tempo'] = librosa.beat.tempo(y=y,sr=sr,hop_length=hop_length)[0]

    return dict_agg_features



def make_train_data():
    os.chdir('Data/genres_original')
    arr_features=[]
    genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
    for idx,genre in (enumerate(genres)):
        for fname in os.listdir(genre):
            y, sr = librosa.load(genre+'/'+fname, duration=30)
            dict_features=extract_features(y=y,sr=sr)
            dict_features['label']=idx
            arr_features.append(dict_features)

    df=pd.DataFrame(data=arr_features)
    print(df.head())
    print(df.shape)
    os.chdir('..')
    df.to_csv('train_data.csv',index=False)


if __name__=='__main__':
    make_train_data()