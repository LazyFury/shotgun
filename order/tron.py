import requests

# https://apilist.tronscanapi.com/api/block
hash_code = "b257aedf5e38bf4da96290ac6fad346721a20133002d2ca66d41bf96c58fde08"
result = requests.get("https://apilist.tronscanapi.com/api/transaction-info?hash=" + hash_code,headers={
    "TRON-PRO-API-KEY":"2f64932f-7d07-4735-a93a-8aa1fdf6594c"
})
print(result.text)
