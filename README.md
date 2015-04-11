# Soap Assembler

Signature: `soap:[fastq A],[fragment_size B] -> contigs C, scaffolds D`

## Quickstart

1. git clone https://github.com/bioboxes/soap
2. cd soap
3. docker build -t soap .
4. sudo docker run -v /path/to/your/assembler.yaml:/bbx/input/biobox.yaml -v /path/to/reads.fastq.gz:/bbx/input/test1/reads.fastq.gz -v /path/to/output:/bbx/output ray default

#### Example biobox.yaml:
```YAML
---
version: 0.9.0
arguments:
    - fastq:
      - id: "pe" 
        value: "/bbx/input/test1/reads.fastq.gz"
        type: single
    - fragment_size:
      - id: "pe"
        value: 123
```

## Required
* biobox.yaml : Please see https://github.com/bioboxes/rfc/issues/90 for current definition.
* gzipped reads with the path provided in biobox.yaml
* mount your input files to /bbx/input. 
* mount your output directory to /bbx/output
* mount your biobox.yaml to /bbx/input/biobox.yaml
* "default" task at the end of your docker run command

####!Note this is not meant for production, it is a showcase for
* checking a provided yaml against a json-schema schema
* provide different parameters for an assembler (paired,single,fragment_size)
