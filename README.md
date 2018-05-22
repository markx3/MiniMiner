# Mini Miner
Solves hackattic's MiniMiner problem in playground mode!

A JSON is received from the endpoint with two attributes:
`block` and `difficulty`. The `block` attribute contains
`data`, which houses arbitrary data and `nonce`. MiniMiner's goal is to
find a `nonce` value that causes the SHA256 hash of `block` to
start with `difficulty` zero bits. That is, if `difficulty` is
4, the hash should start with at least 4 zero bits.

## How to run
To run Mini Miner you should have an access token from hackattic. Go to
[hackattic](https://hackattic.com/) and sign up! Once you've got your token,
input it to `constants.py`.
If you're running python 3.3+, you're good to go! Else, you should
install python's latest version. If you're on a Mac, use `brew install python`.
On debian-based distros, use `sudo apt install python3.6`.

### Running tests
To run tests, run `python3.6 test_miniminer.py`.

### Running Mini Miner
To run Mini Miner, run `python3.6 miniminer.py`.
