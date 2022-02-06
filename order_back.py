import pandas as pd
#import oligomass as omass
import shortuuid as uid
import os
from os import walk
from oligoMass import molmassOligo as mmo

def compare_files_hash(hash, path='data'):
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
    ctrl = False
    for file in files:
        if file.find('_') != -1:
            if hash == file[0: file.find('_')]:
                ctrl = True
                break
    return ctrl

class oligoOrder():
    def __init__(self, label_, seq_, amount_, units_, user_):
        self.label = label_
        self.seq = seq_
        self.amount = amount_
        self.units = units_
        self.data = pd.DataFrame()
        self.order = None
        self.units = units_
        self.user = user_
        self.msg_equal_seq = ''
        self.date = pd.to_datetime('today')
        self.__set_data(label_, seq_, amount_)

    def __set_data(self, label_, seq_, amount_):
        label_ = label_.split('\n')
        seq_ = seq_.split('\n')
        amount_ = amount_.split('\n')

        if len(label_) == len(seq_) and len(label_) > 0 and seq_[0] != '':
            if len(amount_) != len(seq_):
                amount_ = [amount_[0] for s in seq_]

            self.data = pd.DataFrame({'Name': label_})
            self.data['Sequence'] = seq_

            if amount_[0] == '':
                self.data['Amount'] = [1 for i in range(len(seq_))]
            else:
                self.data['Amount'] = amount_

            masses, exts = [], []
            for s in seq_:
                try:
                    mass = mmo.oligoNASequence(s).getAvgMass()
                    ext = mmo.dna.get_simple_ssdna_extinction(s, mmo.dna.get_extinction_dict())
                    masses.append(mass)
                    exts.append(ext)
                except Exception as e:
                    masses.append('error seq')
                    exts.append('error seq')
                    print(e)

            self.data['Mass, Da'] = masses#[round(omass.oligoSeq(s).getMolMass(), 2) for s in seq_]
            self.data['Extinction'] = exts#[omass.get_simple_ssdna_extinction(s, omass.get_extinction_dict()) for s in seq_]

            uid_list = []
            for l, s, index in zip(label_, seq_, range(len(label_))):
                name = str(self.date) + l + s + str(index)
                uid_list.append(uid.uuid(name=name))

            self.data['UID'] = uid_list

            self.data = self.data.set_index('UID')

            #print(self.data)

        else:
            if len(label_) != len(seq_):
                self.msg_equal_seq = 'WARNING: label not equal sequence'
            elif seq_[0] == '':
                self.msg_equal_seq = 'WARNING: sequences is empty'
            elif amount_[0] == '':
                self.msg_equal_seq = 'WARNING: change amounts'

    def create_data_hash(self):
        hash1 = uid.uuid(name=self.label)
        hash2 = uid.uuid(name=self.seq)
        hash3 = uid.uuid(name=self.amount)
        hash4 = uid.uuid(name=self.units)
        return uid.uuid(name=hash1 + hash2 + hash3 + hash4)

    def create_order(self):
        return self.data

    def create_send_df(self):
        df = pd.DataFrame(self.data)
        if not self.data.empty:
            self.date = pd.to_datetime('today')
            df['DateTime'] = [str(self.date) for i in range(self.data.shape[0])]
            df['Units'] = [self.units for i in range(self.data.shape[0])]
            df['Customer'] = [self.user for i in range(self.data.shape[0])]
        return df


def test():

    print(uid.get_alphabet(), len(uid.get_alphabet()))
    for i in range(10):
        print(uid.uuid(name = 'oligos'))
        #print(uid.ShortUUID().random(length=5))


def test2():
    print(compare_files_hash('BVptoUTNMgE95FumhQ3MpL'))

if __name__ == '__main__':
    test2()