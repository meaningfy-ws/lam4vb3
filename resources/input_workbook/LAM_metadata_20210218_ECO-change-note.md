# Changes to the LAM data delivered on 19/02/2021
* Delivered file - LAM_metadata_20210218_OP
* Renamed into - LAM_metadata_20210218_ECO

### Known changes, repeated by past example

* LAM property classification - URIs prefixes: chnage "lamd:clas_" into "lamd:class_"; correspondingly references in LAM properties are updated as well
* LAM class classification - URIs prefixes: change "class_classif:clc_" changed into "lamd:class_"
* Celex class classification - URIs prefixes: change "celex_classif:clc_" into "celexd:class_"
* Celex sector 4 Code: change 5 to 4
* LAM property mappings: recreated the table: 149 instead of 116 rows
* lam class classification:  - add column parent (holding URI) + parent code instead of having parent column with conde values and no parent URI
* celex class classification: add column parent (holding URI) + parent code instead of having parent column with conde values and no parent URI
* celex class codes: remove the "/" slash characters and replace by "_" undescore (1_/AFI/DCL, 1_/PRO, 1_/TXT)

### Code changes

* Changed some columns from simple into multi-line columns (CDM_CLASS, DN_CLASS, AU, FM)
* Added two annotation columns (ANN_TOD(IF), ANN_COD(IF)) ; a bunch are still unused
* Need information which columns have been added, in order to indicate them to the script 

### Issues during transformation:
* Exception: Could not create triples for the cell at row 58 and column DN_CLASS. ValueError: Can't split 'celex:c_5_M_OJC'; 
  Reason: using celex: prefix instead of celexd: prefix. 
  Solution: manually replaced 22 values.

* Exception: Could not create triples for the cell at row 72 and column CDM_CLASS. ValueError: Can't split 'resource_legal'
 Reason: non URI or non cdm: values used 
 Solution: Set cdm:resource_legal value (in CDM_CLASS column) for 11 LAM classes: (lamd:c_073, lamd:c_255, lamd:c_256, lamd:c_257, lamd:c_258, lamd:c_259, lamd:c_260, lamd:c_261, lamd:c_262, lamd:c_263, lamd:c_264)

* Exception: Could not create triples for the cell at row 117 and column CDM_CLASS. ValueError: "cdm: arrangement_institutional" and "cdm: resolution_other_ep" does not look like a valid URI, cannot serialize this. Did you want to urlencode it?
 Solution: manually fixed the URI exception (lamd:c_118, lamd:c_119, lamd:c_139)

* Exception: Could not create triples for the cell at row 125 and column AU. ValueError: "[Member state]/+[National central banks]" does not look like a valid URI, cannot serialize this. Did you want to urlencode it?
 Solution: manually changed
  "country" -> "Y" at lamd:c_233
  remove "/" at lamc:c_126
  
* Exception: Could not create triples for the cell at row 175 and column CDM_CLASS. ValueError: "cdm:resource_legal cdm:act_preparatory cdm:act_other_ec cdm:work" does not look like a valid URI, cannot serialize this. Did you want to urlencode it?
  Reason1: spaces instead of new line between multiple values.
  Reason2: The CDM_Class columns, did not support multiple values.
  Reason3: Strange new line characters identified, different from the standard line break `\n`
  Solution: manually delete extra spaces and insert new lines where needed in columns AU and CDM_CLASS for (lamd:c_175, lamd:c_176, lamd:c_180, lamd:c_182, lamd:c_183, lamd:c_184, lamd:c_185)
  
  
* Exception: Could not create triples for the cell at row 182 and column ANN_COD(DD).  ValueError: "fd_365:DATADOPT fd_340:DATTRANS" does not look like a valid URI, cannot serialize this. Did you want to urlencode it?
  Reason2: The CDM_Class columns, did not support multiple values.
  Reason3: Strange new line characters identified, different from the standard line break `\n`
  Solution: manually delete extra spaces and insert new lines where needed for (lamd:c_183)
  
* Exception: Could not create triples for the cell at row 124 and column ANN_TOD(IF). ValueError: "fd_335: APPLICATION" does not look like a valid URI, cannot serialize this. Did you want to urlencode it?
  Solution: manually delete extra spaces and insert new lines where needed
  
* Exception: Could not create triples for the cell at row 103 and column CC.
  Solution: manually delete extra spaces and insert new lines where needed .
  
* Exception: Could not create triples for the cell at row 106 and column CT. 
  Solution: manually delete extra spaces and insert new lines where needed for (, lamd:c_106, lamd:c_107, lamd:c_156, lamd:c_157, lamd:c_158, lamd:c_185, lamd:c_187, lamd:c_188, lamd:c_189, lamd:c_190, lamd:c_195, lamd:c_199, lamd:c_200, lamd:c_204, ) 
  
* Exception:  erovoc: prefix is nto defined does not exist, 
  Solution: manually replaced by eurovoc:

* Exception: Could not create triples for the cell at row 179 and column DC. ValueError: "eurovoc:2380 (or NT)" does not look like a valid URI, cannot serialize this. Did you want to urlencode it?
  Solution: remove or transform nto comment "(or NT)".
  
* Exception: Could not create triples for the cell at row 180 and column DC. ValueError: "country or region" does not look like a valid URI, cannot serialize this. Did you want to urlencode it? 
  Solution: manually fix.
  
* Exception: Could not create triples for the cell at row 260 and column DC. ValueError: "eurovoc: Y " does not look like a valid URI, cannot serialize this. Did you want to urlencode it?  
  Solution: manually fix for (lamd:c_021, lamd:c_022, lamd:c_023, lamd:c_024, lamd:c_025, lamd:c_026, lamd:c_032, lamd:c_037, lamd:c_045, lamd:c_046, lamd:c_081, lamd:c_099, lamd:c_100, lamd:c_101, lamd:c_102, lamd:c_103, lamd:c_104, lamd:c_105, lamd:c_108, lamd:c_110, lamd:c_111, lamd:c_112, lamd:c_134, lamd:c_140, lamd:c_146, lamd:c_169, lamd:c_170, lamd:c_178, lamd:c_179, lamd:c_193, lamd:c_224, lamd:c_225, lamd:c_226, lamd:c_227, lamd:c_229, lamd:c_230, lamd:c_242, lamd:c_243 )
