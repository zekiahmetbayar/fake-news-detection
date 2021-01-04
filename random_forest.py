import pickle
import pandas as pd
import numpy as np

from trnlp import TrnlpWord
from trnlp import SpellingCorrector
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split,KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

step0_accuracy = 0
step1_accuracy = 0

getbase_word = TrnlpWord()
corrector = SpellingCorrector()

def get_base_word(text):
    words = list()
    ret_text = " "
    words = text.split()
    
    for i in range(0,len(words)):
        
        getbase_word.setword(words[i])
        temp = words[i]
        words[i] = getbase_word.get_base 
        if words[i] == '':
            words[i] = temp
    
    return ret_text.join(words) + '\n'

def get_correct(text):
    words = list()
    true_words = list()
    ret_text = " "
    words = text.split()

    for i in range(0,len(words)):
        corrector.settext(words[i])
        true_words = corrector.correction(deasciifier=True)
        words[i] = true_words[0][0]
    
    return ret_text.join(words) + '\n'

def random_Forest(data_path,test_data,step):
    data = pd.read_csv(data_path, header=None, dtype=str)
    
    data['Label'] = data[1] # Label sütununu seç.
    data.drop([1], axis=1, inplace=True)

    tweets = np.array(data.drop(['Label'], axis = 1), dtype='<U13') # Metinlerin sütununu al
    tweet_Labels = np.array(data['Label']) # Label sütununu al

    tweets = tweets[1:] # Başlıkları sil
    tweet_Labels = tweet_Labels[1:] # Başlıkları sil

    kf = kf = KFold(n_splits=2)
    kf.get_n_splits(tweets)
    tweet_Labels = list(map(int, tweet_Labels)) # Label değerlerini integer'a çevir ve list haline getir

    # tweets_Train > Öğrenme verisi
    # tweets_Test > Test verisi
    # label_Train > Öğrenme verisi LABEL
    # label_Test > Test verisi LABEL

    tweets_Train, tweets_Test, label_Train, label_Test = train_test_split(tweets, tweet_Labels,test_size=0.30, random_state= 100)
    
    tweets_Train = list(tweets_Train) # Train verisi list haline geldi
    clean_tweets_Train = list()
    for train_tweet in tweets_Train:
        for train_tweet2 in train_tweet:
            clean_tweets_Train.append(train_tweet2) # Asıl verileri alır
            
    tweets_Test = list(tweets_Test)
    clean_tweets_Test = list()
    for test_tweet in tweets_Test:
        for test_tweet2 in test_tweet:
            clean_tweets_Test.append(test_tweet2) # Asıl verileri alır
            
    count_vect = CountVectorizer(lowercase=False)
    tweet_train_Counts = count_vect.fit_transform(clean_tweets_Train)
    tweet_test_Counts = count_vect.transform(clean_tweets_Test)

    test_input = test_data
    test_input_count = count_vect.transform(test_input)

    random_forestModel = RandomForestClassifier()
    random_forestModel.fit(tweet_train_Counts,label_Train) # Öğrenme aşaması
    label_Prediction = random_forestModel.predict(tweet_test_Counts) # Test verisi

    test_final_1 = random_forestModel.predict(test_input_count) # Test verisi
    acc = accuracy_score(label_Test,label_Prediction) # Karşılaştır

    if step == 0:
        global step0_accuracy 
        step0_accuracy = float("{0:.2f}".format(acc*100))
    
    if step == 1:
        global step1_accuracy
        step1_accuracy = float("{0:.2f}".format(acc*100))

    filename = 'finalized_model.sav'
    pickle.dump(random_forestModel, open(filename, 'wb'))

    return test_final_1

user_inp =  input('Dataset doğruluk oranlarını görmek için 0, Haberinizi test etmek için 1 tuşlaması yapınız !\nSeçiminiz : ')

if user_inp == '1':
    user_new = input('Test haberinizi giriniz ! \nHaber : ')
    user_new = get_correct(user_new)
    print('Mesajın doğrulaştırılmış hali : ' + user_new)
    user_new = get_base_word(user_new)
    print('Mesajın köklerine ayrılmış hali : ' + user_new)
    user_new = user_new.lower()
    print('Mesajın tekrar küçük harfe dönüştürülmüş hali : ' + user_new)
    test_data_list = [user_new]
    final = random_Forest('data.csv',test_data_list,0)

    if(final == 0):
        fake_final = random_Forest('fakedata.csv',test_data_list,1)

        if fake_final == 0:
            print('Karar : Bilinçsiz Yanlış !')

        if fake_final == 1:
            print('Karar : Bilinçli Yanlış !')
            
    else:
        fake_final = random_Forest('fakedata.csv',test_data_list,1)
        print('Karar : Haber doğru !')

if user_inp == '0':
    test_data_list = ['']
    zero_input = random_Forest('data.csv',test_data_list,0)
    print('Doğru/Yanlış haber ayırt etme doğruluğu : {} '.format(step0_accuracy))

    test_data_list = ['']
    zero_input = random_Forest('fakedata.csv',test_data_list,1)
    print('Bilinçli/Bilinçsiz haber ayırt etme doğruluğu : {} '.format(step1_accuracy))

if user_inp == 'q':
    exit 

