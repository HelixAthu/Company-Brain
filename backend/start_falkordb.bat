@echo off
echo Starting FalkorDB Container on port 6379...
docker run -p 6379:6379 -it --name falkordb-devtrace -d falkordb/falkordb:latest
echo FalkorDB container launched!
