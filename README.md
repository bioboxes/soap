# Soap Assembler

Signature: `soap:[fastq A],[fragment_size B] -> contigs C, scaffolds D`

## Quickstart

1. git clone https://github.com/bioboxes/soap
2. cd soap
3. docker build -t soap .
4. sudo docker run -v /path/to/your/assembler.yaml:/bbx/input/assembler.yaml -v /path/to/reads.fastq.gz:/bbx/input/test1/reads.fastq.gz -v /path/to/output:/bbx/output ray

#### Example assembler.yaml:
```YAML
---
version: 0.9.0
arguments:
    - fastq:
      - id: "pe" 
        value: "/test1/reads.fastq.gz"
        type: single
    - fragment_size:
      - id: "pe"
        value: 123
```

## Required
* assembler.yaml : Please see https://github.com/bioboxes/rfc/issues/90 for current definition.
* gzipped reads with the path provided in assembler.yaml
* mount your input files to /bbx/input. The path provided in assembler.yaml is relative to /bbx/input
  * Example: When you mount your file to /bbx/input/test1/reads.fastq.gz then you have to provide the path
    "/test1/reads.fastq.gz" in the yaml file.
* mount your output directory to /bbx/output
* mount your assembler.yaml to /bbx/input/assembler.yaml


####!Note this is not meant for production, it is a showcase for
* checking a provided yaml against a rx schema
* provide different parameters for an assembler (paired,single,fragment_size)
