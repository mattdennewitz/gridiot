.phony: create destroy

WIT=./quickwit-v0.8.2/quickwit

create:
	$(WIT) index create --index-config ./schema.yaml

destroy:
	$(WIT) index delete --index players

recycle: destroy create

ingest:
	$(WIT) index ingest --index players --input-path ./*.ndjson

status:
	$(WIT) index describe --index players

query:
	$(WIT) index search --index players --query $(query)
