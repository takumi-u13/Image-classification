# Image-classification
<h2>実行方法</h2>
#ローカルのリポジトリで下記のコマンドを実行
docker build .
docker run -v <ローカルのリポジトリのパス>:/work/ -p 5000:5000 <image id>
