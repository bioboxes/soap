# Soap Assembler

Signature: `soap:[(Id,fastq)],[(Id,fragment_size)] -> fasta`

## Quickstart

1. git clone https://github.com/bioboxes/soap
2. cd soap
3. docker build -t soap .
4. sudo docker run -v /path/to/your/assembler.yaml:/bbx/input/assembler.yaml -v /path/to/reads.fastq.gz:/home/input/reads.fastq.gz -v /path/to/output:/bbx/output ray

#### Example assembler.yaml:
```YAML
---
version: 0.9.0
arguments:
    fastq:
      - id: "pe" 
        path: "/dckr/mnt/input/reads.fastq.gz"
        type: single
    fragment_size:
      - id: "pe"
        value: 123
```

## Required
* assembler.yaml : Please see https://github.com/bioboxes/rfc/issues/90 for current definition.
* gzipped reads with the path provided in assembler.yaml
* mount your output directory to /bbx/output
* mount your assembler.yaml to /bbx/input/assembler.yaml


####!Note this is not meant for production, it is a showcase for
* checking a provided yaml against a rx schema
* provide different parameters for an assembler (paired,single,fragment_size)
