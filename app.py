from flask import Flask, render_template, url_for, request, redirect, abort
from werkzeug.utils import secure_filename
import os
from nltk.tokenize import sent_tokenize as tokenize
from underthesea import sent_tokenize as vn_tokenize
from underthesea import word_tokenize
from googletrans import Translator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from time import time
import concurrent.futures


app = Flask(__name__)

app.config["TEXT_UPLOAD"] = "D:/Năm 3_HK 2/NLP/NLP_project/static/cache"

@app.route('/', methods = ["POST", "GET"])
def hello():
   EL = []
   VN = []

   if request.method == "POST":
      if request.files:
         files = request.files.getlist("file[]")
         if len(files) == 2:
            for file in files:
               file_name = secure_filename(file.filename)
               file.save(os.path.join(app.config["TEXT_UPLOAD"], file_name))
               f = open(os.path.join(app.config["TEXT_UPLOAD"], file_name), mode='rt', encoding='utf-8')
               if 'el' in file.filename:
                  for line in f:
                     EL += tokenize(line.replace('\n', ""), language='english')
                  f.close()
                  os.remove(os.path.join(app.config["TEXT_UPLOAD"], file_name))
               if 'vn' in file.filename:
                  for line in f:
                     VN += vn_tokenize(line.replace('\n', ""))
                  f.close()
                  os.remove(os.path.join(app.config["TEXT_UPLOAD"], file_name))

            def pre_translate(EL, VN):
               data = [[EL[i], []] for i in range(len(EL))]
               EL_len, VN_len = len(EL), len(VN)
               translator = Translator(service_urls=['translate.google.com'])
               start = time()
               def translate(sentence):
                  translation = translator.translate(sentence, src='en', dest='vi')
                  return translation.text
               with concurrent.futures.ThreadPoolExecutor() as executor:
                  translations = executor.map(translate, EL)
               print("Translation time: " + str(time() - start))
               translations = [word_tokenize(translation, format="text") for translation in translations]
               VN_sentences = [word_tokenize(sent, format = "text") for sent in VN ]
               VN_sentences += translations
               VN_sentences = CountVectorizer().fit_transform(VN_sentences)
               similarity_scores = cosine_similarity(VN_sentences[VN_len:], VN_sentences[:VN_len])
               similarity_scores = [similarity_score.flatten() for similarity_score in similarity_scores]

               check_list = [-1]*VN_len
               top, bot = -1, VN_len
               def max_indexes(cur_el_index):
                  max_value = np.max(similarity_scores[cur_el_index])
                  if max_value < .3:
                     return []
                  return list(np.where(similarity_scores[cur_el_index] + .05 >= max_value)[0])
               for i in range(int(EL_len/2)):
                  max_indexes_top = max_indexes(i)
                  if max_indexes_top != []:
                     for index in max_indexes_top:
                        if check_list[index] == -1 and abs(index - top + 1) <= 15:
                           check_list[index] = i
                           data[i][1].append(VN[index])
                           if index > top:
                              top = index
                           else:
                              top += 1
                           break
                     else:
                        top += 1
                  max_indexes_bot = max_indexes(EL_len-i-1)
                  if max_indexes_bot != []:
                     for index in max_indexes_bot[::-1]:
                        if check_list[index] == -1 and abs(index - bot + 1) <= 15:
                           check_list[index] = EL_len - i - 1
                           data[EL_len-i-1][1].append(VN[index])
                           if index < bot:
                              bot = index
                           else:
                              bot -= 1
                           break
                     else:
                        bot -= 1

               # sort check_list >>>
               VN_satisfied_indexes = [check_list[i] for i in range(VN_len) if check_list[i] != -1]
               VN_satisfied_indexes.sort()
               j = 0
               for i in range(VN_len):
                  if check_list[i] != -1:
                     check_list[i] = VN_satisfied_indexes[j]
                     j += 1

               if check_list[0] == -1:
                  data[0][1].append(VN[0])
                  check_list[0] = 0

               if check_list[VN_len - 1] == -1:
                  data[EL_len - 1][1].append(VN[-1])
                  check_list[VN_len - 1] = EL_len - 1

               for i in range(int(VN_len)):
                  if check_list[i] == -1:
                     for j in range(i-1, -1, -1):
                        if check_list[j] != -1 and check_list[j] < EL_len - 1:
                           data[check_list[j] + 1][1].append(VN[i])
                           check_list[i] = check_list[j] + 1
                           break
                  if check_list[VN_len - i - 1] == -1:
                     for j in range(VN_len - i, VN_len):
                        if check_list[j] != -1:
                           data[check_list[j] - 1][1].append(VN[VN_len - i - 1])
                           check_list[VN_len - i - 1] = check_list[j] - 1
                           break

               # for i in range(int(VN_len/2) + 1):
               #    if check_list[i] == -1:
               #       for j in range(i-1, -1, -1):
               #          if check_list[j] != -1:
               #             data[check_list[j] + 1][1].append(VN[i])
               #             check_list[i] = check_list[j] + 1
               #             break
               #    if check_list[VN_len - i - 1] == -1:
               #       for j in range(VN_len - i, VN_len):
               #          if check_list[j] != -1:
               #             data[check_list[j] - 1][1].append(VN[VN_len - i - 1])
               #             check_list[VN_len - i - 1] = check_list[j] - 1
               #             break

               return data

            data = pre_translate(EL, VN)

            return render_template('index.html', data = data)

         else:
            return "Files aren't correct", 400

         return redirect(request.url)

   return render_template('index.html', data = [])

if __name__ == "__main__":
   app.run(debug=True)