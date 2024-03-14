echo "Getting 'input.txt' from the char-rnn Repo and saving it as 'data/shakespeare.txt'"
if [ ! -d "data" ]; then
    echo "data directory does not exist. Creating it."
    mkdir -p "data"
fi
curl "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt" > data/shakespeare.txt
echo "Finished Data Downloading."