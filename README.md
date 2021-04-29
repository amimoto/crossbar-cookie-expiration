# Crossbar Cookie Expiration Test

## Running

Clone the repo then run:

```bash
./run-test.sh
```

This should:

1. Build an image named `temp/crossbar-cookies`
2. Spin it up under then local name `test-cookies`
   - This will also map the current directory to `/node`
3. Runs the command `/node/run-server-and-test.sh` on the server
   - This run `crossbar start`
   - Waits 10 seconds
   - Runs `python test-case.py` which demonstrates the issue


