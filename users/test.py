import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time



def run(duration,protocol_type,flag,src_bytes,dst_bytes,land,wrong_fragment,urgent,hot,num_failed_logins,logged_in,num_compromised,root_shell,su_attempted,num_root,num_file_creations,num_shells,num_access_files,is_guest_login,count,srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate,dst_host_count,dst_host_srv_count,dst_host_same_srv_rate,dst_host_diff_srv_rate,dst_host_same_src_port_rate,dst_host_srv_diff_host_rate,dst_host_serror_rate,dst_host_srv_serror_rate,dst_host_rerror_rate,dst_host_srv_rerror_rate):
    with open("../kddcup.names",'r') as f:
        print(f.read())


    cols="""duration,
    protocol_type,
    service,
    flag,
    src_bytes,
    dst_bytes,
    land,
    wrong_fragment,
    urgent,
    hot,
    num_failed_logins,
    logged_in,
    num_compromised,
    root_shell,
    su_attempted,
    num_root,
    num_file_creations,
    num_shells,
    num_access_files,
    num_outbound_cmds,
    is_host_login,
    is_guest_login,
    count,
    srv_count,
    serror_rate,
    srv_serror_rate,
    rerror_rate,
    srv_rerror_rate,
    same_srv_rate,
    diff_srv_rate,
    srv_diff_host_rate,
    dst_host_count,
    dst_host_srv_count,
    dst_host_same_srv_rate,
    dst_host_diff_srv_rate,
    dst_host_same_src_port_rate,
    dst_host_srv_diff_host_rate,
    dst_host_serror_rate,
    dst_host_srv_serror_rate,
    dst_host_rerror_rate,
    dst_host_srv_rerror_rate"""

    columns=[]
    for c in cols.split(','):
        if(c.strip()):
            columns.append(c.strip())

    columns.append('target')


    with open("../training_attack_types",'r') as f:
        print(f.read())

    attacks_types = {
        'normal': 'normal',
    'back': 'dos',
    'buffer_overflow': 'u2r',
    'ftp_write': 'r2l',
    'guess_passwd': 'r2l',
    'imap': 'r2l',
    'ipsweep': 'probe',
    'land': 'dos',
    'loadmodule': 'u2r',
    'multihop': 'r2l',
    'neptune': 'dos',
    'nmap': 'probe',
    'perl': 'u2r',
    'phf': 'r2l',
    'pod': 'dos',
    'portsweep': 'probe',
    'rootkit': 'u2r',
    'satan': 'probe',
    'smurf': 'dos',
    'spy': 'r2l',
    'teardrop': 'dos',
    'warezclient': 'r2l',
    'warezmaster': 'r2l',
    }

    path = "../kddcup.data_10_percent.gz"
    df = pd.read_csv(path,names=columns)


    df['Attack Type'] = df.target.apply(lambda r:attacks_types[r[:-1]])

    df['num_root'].corr(df['num_compromised'])
    df['srv_serror_rate'].corr(df['serror_rate'])
    df['srv_count'].corr(df['count'])
    df['srv_rerror_rate'].corr(df['rerror_rate'])
    df['dst_host_same_srv_rate'].corr(df['dst_host_srv_count'])
    df['dst_host_srv_serror_rate'].corr(df['dst_host_serror_rate'])
    df['dst_host_srv_rerror_rate'].corr(df['dst_host_rerror_rate'])
    df['dst_host_same_srv_rate'].corr(df['same_srv_rate'])
    df['dst_host_srv_count'].corr(df['same_srv_rate'])
    df['dst_host_same_src_port_rate'].corr(df['srv_count'])
    df['dst_host_serror_rate'].corr(df['serror_rate'])
    df['dst_host_serror_rate'].corr(df['srv_serror_rate'])
    df['dst_host_srv_serror_rate'].corr(df['serror_rate'])
    df['dst_host_srv_serror_rate'].corr(df['srv_serror_rate'])
    df['dst_host_rerror_rate'].corr(df['rerror_rate'])
    df['dst_host_rerror_rate'].corr(df['srv_rerror_rate'])
    df['dst_host_srv_rerror_rate'].corr(df['rerror_rate'])
    df['dst_host_srv_rerror_rate'].corr(df['srv_rerror_rate'])

    df_std = df.std()
    df_std = df_std.sort_values(ascending = True)
    pmap = {'icmp':0,'tcp':1,'udp':2}
    df['protocol_type'] = df['protocol_type'].map(pmap)

    fmap = {'SF':0,'S0':1,'REJ':2,'RSTR':3,'RSTO':4,'SH':5 ,'S1':6 ,'S2':7,'RSTOS0':8,'S3':9 ,'OTH':10}
    df['flag'] = df['flag'].map(fmap)

    df.drop('service',axis = 1,inplace= True)

    from sklearn.preprocessing import MinMaxScaler


    df = df.drop(['target',], axis=1)


    # Target variable and train set
    Y = df[['Attack Type']]
    X = df.drop(['Attack Type',], axis=1)


    sc = MinMaxScaler()
    X = sc.fit_transform(X)

    v=np.array([duration,protocol_type,flag,src_bytes,dst_bytes,land,wrong_fragment,urgent,hot,num_failed_logins,logged_in,num_compromised,root_shell,su_attempted,num_root,num_file_creations,num_shells,num_access_files,is_guest_login,count,srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate,dst_host_count,dst_host_srv_count,dst_host_same_srv_rate,dst_host_diff_srv_rate,dst_host_same_src_port_rate,dst_host_srv_diff_host_rate,dst_host_serror_rate,dst_host_srv_serror_rate,dst_host_rerror_rate,dst_host_srv_rerror_rate])

    X_transformed = sc.transform(v.reshape(1, -1))
    
    return X_transformed




    






