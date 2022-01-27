import pandas as pd
import oligomass as omass
import shortuuid as uid

class oligoOrder():
    def __init__(self, label_, seq_, amount_, units_):
        self.data = None
        self.order = None
        self.units = units_
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

            self.data['Mass, Da'] = [round(omass.oligoSeq(s).getMolMass(), 2) for s in seq_]
            self.data['Extinction'] = [omass.get_simple_ssdna_extinction(s, omass.get_extinction_dict()) for s in seq_]

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


    def create_order(self):
        return self.data


def test():

    print(uid.get_alphabet(), len(uid.get_alphabet()))
    for i in range(10):
        print(uid.uuid(name = 'oligos'))
        #print(uid.ShortUUID().random(length=5))

if __name__ == '__main__':
    test()