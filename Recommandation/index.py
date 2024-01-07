from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
import math
import re
import chardet
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from flask_cors import CORS
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
sns.set_style("darkgrid")

# sử dụng thuật toán lọc cộng tác SVD để đề xuất và dự đoán các đánh giá cho người dùng và sản phẩm phim trong hệ thống gợi ý
# Thiết lập Cross-Origin Resource Sharing (CORS) để cho phép các yêu cầu từ trang web chạy ở http://localhost:3000
app = Flask(__name__)

CORS(app, origins=['http://localhost:3000'])

@app.route('/', methods = ['GET', 'POST']) 
def home(): 
    if(request.method == 'GET'): 
  
        data = "hello world"
        return jsonify({'data': data}) 

@app.route('/recommend/<name_film>', methods=['GET'])
def recommend_movie(name_film):
    try:
        movie_title_req = name_film
        # Tiền xử lý dữ liệu:
        df1 = pd.read_csv('./dataset/combined_data_1.txt', header = None, names = ['Cust_Id', 'Rating'], usecols = [0,1])

        df1['Rating'] = df1['Rating'].astype(float)

        print('Dataset 1 shape: {}'.format(df1.shape))
        print('-Dataset examples-')
        print(df1.iloc[::5000000, :])

        # Tải ít dữ liệu hơn để tăng tốc

        df = df1
        df.index = np.arange(0,len(df))
        print('Full dataset shape: {}'.format(df.shape))
        print('-Dataset examples-')
        print(df.iloc[::5000000, :])

        # xóa dữ liệu
        df_nan = pd.DataFrame(pd.isnull(df.Rating))
        df_nan = df_nan[df_nan['Rating'] == True]
        df_nan = df_nan.reset_index()

        movie_np = []
        movie_id = 1

        for i,j in zip(df_nan['index'][1:],df_nan['index'][:-1]):
            # numpy approach
            temp = np.full((1,i-j-1), movie_id)
            movie_np = np.append(movie_np, temp)
            movie_id += 1

        # Tính đến bản ghi cuối cùng và độ dài tương ứng
        # numpy approach    
        last_record = np.full((1,len(df) - df_nan.iloc[-1, 0] - 1),movie_id)
        movie_np = np.append(movie_np, last_record)

        print('Movie numpy: {}'.format(movie_np))
        print('Length: {}'.format(len(movie_np)))

        # remove those Movie ID rows
        df = df[pd.notnull(df['Rating'])]

        df['Movie_Id'] = movie_np.astype(int)
        df['Cust_Id'] = df['Cust_Id'].astype(int)
        print('-Dataset examples-')
        print(df.iloc[::5000000, :])

        f = ['count','mean']

        df_movie_summary = df.groupby('Movie_Id')['Rating'].agg(f)
        df_movie_summary.index = df_movie_summary.index.map(int)
        movie_benchmark = round(df_movie_summary['count'].quantile(0.7),0)
        drop_movie_list = df_movie_summary[df_movie_summary['count'] < movie_benchmark].index

        print('Movie minimum times of review: {}'.format(movie_benchmark))

        df_cust_summary = df.groupby('Cust_Id')['Rating'].agg(f)
        df_cust_summary.index = df_cust_summary.index.map(int)
        cust_benchmark = round(df_cust_summary['count'].quantile(0.7),0)
        drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index

        print('Customer minimum times of review: {}'.format(cust_benchmark))

        print('Original Shape: {}'.format(df.shape))
        df = df[~df['Movie_Id'].isin(drop_movie_list)]
        df = df[~df['Cust_Id'].isin(drop_cust_list)]
        print('After Trim Shape: {}'.format(df.shape))
        print('-Data Examples-')
        print(df.iloc[::5000000, :])

        df_p = pd.pivot_table(df,values='Rating',index='Cust_Id',columns='Movie_Id')

        # Use detected encoding in pd.read_csv
        # df_title = pd.read_csv('./dataset/movie_titles.csv', encoding=result['encoding'], header=None, names=['Movie_Id', 'Year', 'Name'])
        df_title = pd.read_csv('a.csv', header = None, names = ['Movie_Id', 'Year', 'Name'],usecols = [0,1,2])
        df_title.set_index('Movie_Id', inplace = True)
        print("For movie ({})".format(movie_title_req))
        print("- Top 10 movies recommended based on Pearsons'R correlation - ")
        i = int(df_title.index[df_title['Name'] == movie_title_req][0])
        target = df_p[i]
        similar_to_target = df_p.corrwith(target)
        corr_target = pd.DataFrame(similar_to_target, columns=['PearsonR'])
        corr_target.dropna(inplace=True)
        corr_target = corr_target.sort_values('PearsonR', ascending=False)
        corr_target.index = corr_target.index.map(int)
        corr_target = corr_target.join(df_title).join(df_movie_summary)[['PearsonR', 'Name', 'count', 'mean']]
        recommendations = corr_target[corr_target['count'] > 0][:10].to_dict(orient='records')
        print(recommendations)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)