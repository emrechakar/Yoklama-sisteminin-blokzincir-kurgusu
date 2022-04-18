from hashlib import sha256
import PyPDF2
import json
from datetime import datetime
class Block:
    def __init__(self, index, previous_hash, current_transactions,
timestamp, nonce):
     self.index = index
     self.previous_hash = previous_hash
     self.current_transactions = current_transactions
     self.timestamp = timestamp
     self.nonce = nonce
     self.hash = self.compute_hash()
    def compute_hash(self):
     block_string = json.dumps(self.__dict__, sort_keys=True)
     first_hash = sha256(block_string.encode()).hexdigest()
     second_hash = sha256(first_hash.encode()).hexdigest()
     return second_hash
    def __str__(self):
     return str(self.__dict__)
class BlockChain:
    def __init__(self):
     self.chain = []
     self.transactions = []
     self.genesis_block()
    def __str__(self):
     return str(self.__dict__)
    def genesis_block(self):
     genesis_block = Block('Genesis', 0x0, [3, 4, 5, 6, 7],
    'datetime.now().timestamp()', 0)
     genesis_block.hash = genesis_block.compute_hash()
     self.chain.append(genesis_block.hash)
     self.transactions.append(str(genesis_block.__dict__))
    def getLastBlock(self):
        return self.chain[-1]
    def proof_of_work(self, block: Block):
        difficulty = 1

        block.nonce = 0
        computed_hash = block.compute_hash()
        while not (computed_hash.endswith('0' * difficulty) and ('34' *
      difficulty) in computed_hash):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    def add(self, data):
        block = Block(len(self.chain), self.chain[-1], data,
'datetime.now().timestamp()', 0)
        block.hash = self.proof_of_work(block)
        self.chain.append(block.hash)
        self.transactions.append(block.__dict__)
        return json.loads(str(block.__dict__).replace('\'', '\"'))
    def getTransactions(self, id):
        labels = ['Ogrenci', 'Ogretmen']
        while True:
            try:
                if id == 'all':
                    for i in range(len(self.transactions) - 1):
                        print('{}:\n{}\n'.format(labels[i],
self.transactions[i + 1]))
                    break
                elif type(id) == int:
                    print(self.transactions[id])
                    break
            except Exception as e:
                print(e)
'''
 Block Template
'''
ogrenci_new_transaction = {
 'timestamp': '', # datetime.now().timestamp(),
 'product_id': 1,
 'ogrenci_numarasi': 195509018,
 'sistem': 'yoklama sistemi', 
 'kurum': 'fırat üniversitesi adli bilişim mühendisliği',
 'ogrenci_adi': 'Emre Çakar',
 ### CHANGEABLE KEYS
 'mesaj': '', #'yoklama girisi basariyla gerceklesti.'
 'digital_signature': '', #kabul edildi ya da reddedildi
 'flagged': '' #Evet için 'E', hayır için 'H'
}
ogretmen_new_transaction = {
 'timestamp': '', # datetime.now().timestamp(),
 'product_id': 1,
 'ogretmen_kullanici_numarasi': 3401238045,
 'sistem': 'yoklama sistemi', 
 'kurum': 'fırat üniversitesi adli bilişim mühendisliği',
 'ogretmen': 'Mehmet demirkol',
 ### CHANGEABLE KEYS
 'mesaj': '', #'yoklama girisi basariyla gerceklesti'
 'digital_signature': '', #kabul edildi ya da reddedildi
 'flagged': '' #Evet için 'E', hayır için 'H'
}

'''
 DATA BLOCKS
'''
ogrenci = {
 'transactions': []
}
ogretmen = {
 'transactions': []
}

def ogrenciBlockProcess():

    print('\nOgrenci Blok Prosesi Icin Bilgi Girisi', end='\n')
    message = ''
    while len(message) < 1:
        message = input('Bir Mesaj Giriniz: ')
    digital_signature = ''
    while not (digital_signature == 'kabul edildi' or digital_signature ==
    'reddedildi'):
        digital_signature = input('Ogrenci Bilgi Durumu nihai durumu ("kabul edildi" ya da "reddedildi"): ')
    if digital_signature == 'reddedildi':
        return False
    flagged = ''

    while not (flagged == 'E' or flagged == 'H'):
        flagged = input('Yoklama girisi basariyla gerceklesti mi ? (Evet icin "E", Hayir icin "H"): ')
    ogrenci_new_transaction["timestamp"] = datetime.now().timestamp()
    ogrenci_new_transaction["mesaj"] = message
    ogrenci_new_transaction["digital_signature"] = digital_signature
    ogrenci_new_transaction["flagged"] = flagged
    return ogrenci_new_transaction
def ogretmenBlockProcess():
    print('\Ogretmen Blok Prosesi Icin Bilgi Girisi', end='\n')
    message = ''
    while len(message) < 1:
        message = input('Bir Mesaj Giriniz: ')
        digital_signature = ''
    while not (digital_signature == 'kabul edildi' or digital_signature ==
'reddedildi'):
        digital_signature = input('Sistem Bilgisi nihai durumu ("kabul edildi" ya da "reddedildi"): ')
    if digital_signature == 'reddedildi':
        return False
    flagged = ''
    while not (flagged == 'E' or flagged == 'H'):
        flagged = input('Yoklama girisi basariyla gerceklesti mi? (Evet icin "E", Hayir icin "H"): ')
    ogretmen_new_transaction["timestamp"] = datetime.now().timestamp()
    ogretmen_new_transaction["mesaj"] = message
    ogretmen_new_transaction["digital_signature"] = digital_signature
    ogretmen_new_transaction["flagged"] = flagged
    return ogretmen_new_transaction

def main():
    print('Butun Blok Zinciri Sisteminin Baslatilmasi...', end='\n')
    B = BlockChain()
    ogrenciBlock = ogrenciBlockProcess()
    if ogrenciBlock == False:
        print('ogrenci Blok Prosesi Reddedildi')
        exit()
    ogrenci['transactions'].append(ogrenciBlock)
    a = B.add(ogrenci)
    print('ogrenci Blogu Eklendi')
    print(a)
    ogretmenBlock = ogretmenBlockProcess()
    if ogretmenBlock == False:
        print('ogretmen Blok Prosesi Reddedildi')
        exit()
    ogretmen['transactions'].append(ogretmenBlock)
    b = B.add(ogretmen)
    print('ogretmen Blogu Eklendi')
    print(b)


    print('Bloklara Kaydedilen Butun Transfer Degerlerinin Ozeti',end='\n')
    B.getTransactions('all')
if __name__ == '__main__':
    main()