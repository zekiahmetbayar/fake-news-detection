from string import digits
from trnlp import TrnlpWord
from trnlp import SpellingCorrector
import pandas as pd 
import csv,os,string,re
import logging
import emoji

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('log')
handler.setLevel(logging.DEBUG)

# logging format oluşturun
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# handler’i logger a kaydedin
logger.addHandler(handler)

getbase_word = TrnlpWord()
corrector = SpellingCorrector()

stopwords = ["ama", "ancak", "arada", "ayrıca", "bana", "bazı", "belki", "ben", "beni", "benim", "beri", "bile", "bir", "birçok",
    "biri", "birkaç", "biz", "bize", "bizi", "bizim","böyle", "böylece", "bu","buna", "bundan", "bunlar", "bunları", "bunların", 
    "bunu", "bunun", "burada", "çok", "çünkü", "da", "daha", "de","değildir","diğer", "diye", "dolayı", "dolayısıyla", "edecek", 
    "eden", "ederek", "edilecek", "ediliyor", "edilmesi", "ediyor", "eğer", "etmesi", "etti", "ettiği", "ettiğini", "gibi","göre", 
    "halen", "hangi", "hatta", "hem", "henüz", "her", "herhangi", "herkesin", "hiç", "hiçbir", "için", "ile", "ilgili", "ise", "işte",
    "itibaren", "itibariyle", "kadar", "karşın", "kendi", "kendilerine", "kendini", "kendisi", "kendisine", "kendisini", "ki",
    "kim", "kimse", "mı", "mi", "mu", "mü", "nasıl", "ne", "neden", "nedenle", "o", "olan", "olarak", "oldu", "olduğu", 
    "olduğunu", "olduklarını", "olmadı", "olmadığını", "olmak", "olması", "olmayan", "olmaz", "olsa", "olsun", "olup", "olur",
    "olursa", "oluyor", "ona", "onlar", "onları", "onların", "onu", "onun", "öyle", "oysa", "pek", "rağmen", "sadece", "siz",
    "şey", "şöyle", "şu", "şunları", "tarafından", "üzere", "var", "vardı", "ve", "veya", "ya", "yani", "yapacak", "yapılan",
    "yapılması", "yapıyor", "yapmak", "yaptı", "yaptığı", "yaptığını", "yaptıkları", "yerine", "yine", "yoksa", "zaten"]

def main():
    select_text_column('output')
    search_keywords()
    clean_data('output','final')

def select_text_column(csv_name):
    logger.info('Tweet dosyası okunuyor...')
    df = pd.read_csv(str(csv_name)+'.csv')

    logger.info('Text sütunu ayırılıyor...')
    tweets = df.loc[:, "text"]

    logger.info('Ayırılan sütun dosyaya yazılıyor...')
    filename = 'output.csv'
    tweets.to_csv(filename, index = False)

def search_keywords():
    tweets = list()
    clean_tweets = list()

    logger.info('Keyword taraması için dosya okunuyor...')
    with open('output.csv') as cleantweets:
        tweets = cleantweets.readlines()
        keyword_list = ["recep", "tayyip", "erdoğan", "akp", "bakan", "albayrak", "selçuk",
                        "siyaset", "siyasi", "meclis", "milletvekili", "mv.",
                        "saray", "emine"]

        logger.info('Keyword içeren tweetler ayırılıyor...')
        for i in tweets:
            for j in keyword_list:
                if j in i.lower():
                    clean_tweets.append(i)
    
    logger.info('Keyword içeren tweetler dosyaya yazılıyor...')
    with open('output.csv','w') as new:
        for i in range(len(clean_tweets)):
            new.write(clean_tweets[i])

def strip_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text

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

def clean_data(inp,output):
    with open(inp + '.csv') as tweetsfile:
        tweets_List = list()
        tweets_List = tweetsfile.readlines()
        for i in range(0,len(tweets_List)):

            logger.info('Linkler temizleniyor...')
            unlink = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweets_List[i])
            tweets_List[i] = unlink # Linkleri temizler.

            logger.info('Rakamlar temizleniyor...')
            remove_digits = str.maketrans('', '', digits)
            tweets_List[i] = tweets_List[i].translate(remove_digits) # Rakamları temizler

            logger.info('Noktalama işaretleri metinden çıkarılıyor...')
            tweets_List[i] = tweets_List[i].translate(str.maketrans('', '', string.punctuation)) # Noktalama işaretlerini temizler.

            logger.info('N karakterden az kelimeler siliniyor...')
            shortword = re.compile(r'\W*\b\w{1,3}\b')
            tweets_List[i] = shortword.sub('', tweets_List[i]) # N karakterden az kelimeleri temizler
            tweets_List[i] = tweets_List[i].lower()
            
            logger.info('Özel durumlar metinlerden siliniyor...')
            tweets_List[i] = tweets_List[i].replace('•', '')
            tweets_List[i] = tweets_List[i].replace('❞', '')
            tweets_List[i] = tweets_List[i].replace('❝', '')
            tweets_List[i] = tweets_List[i].replace('fotohaber', '')
            tweets_List[i] = tweets_List[i].replace('sporhaber', '')
            tweets_List[i] = tweets_List[i].replace('son', '')
            tweets_List[i] = tweets_List[i].replace('dakika', '')
            tweets_List[i] = tweets_List[i].replace('’', '')
            tweets_List[i] = tweets_List[i].replace('₺', '')
            tweets_List[i] = tweets_List[i].replace('”', '')
            tweets_List[i] = tweets_List[i].replace('“', '')
            tweets_List[i] = tweets_List[i].replace('✘', '')
            tweets_List[i] = tweets_List[i].replace("'", '')
            
            logger.info('Emojiler metinlerden siliniyor...')
            tweets_List[i] = strip_emoji(tweets_List[i])

            logger.info('Yanlış yazılan kelimeler düzeltiliyor...')
            tweets_List[i] = get_correct(tweets_List[i])

            logger.info('Kelimeler köklerine ayrılıyor...')
            tweets_List[i] = get_base_word(tweets_List[i])
            tweets_List[i] = tweets_List[i].lower()
            tweets_List[i] = tweets_List[i].replace('i̇', 'i')
            tweets_List[i] = tweets_List[i].replace("'", '')

        logger.info('Durak kelimeler metinden çıkarılıyor...')
        for i in tweets_List:
            for j in stopwords:
                if i == j:
                    index = tweets_List.index(i)
                    tweets_List.pop(index)

        print("İşlem başarıyla tamamlandı.\nToplam veri sayısı : {} ".format(len(tweets_List)))

        logger.info('Temizlenmiş metin dosyaya yazılıyor...')
        with open(output + '.csv','w') as new_tweetsfile:
            for i in range(len(tweets_List)):
                new_tweetsfile.write(tweets_List[i])
        
main()