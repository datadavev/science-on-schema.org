# Validation

## About

This directory holds work related to graph validation.  The focus is on using the
W3C SHACL Recommendation (https://www.w3.org/TR/shacl/).

Contents:

* `/SHACL` contains SHACL shape graphs
* `/vocabularies`: contains the schema.org vocabulary and may include others as needed
* `/data`: contains example data graphs
* `/test`: Python code for running tests 


In general, the tests apply SHACL shape graphs against data graphs and compare with
an expected outcome. 






At present we have worked up some examples around the Google Developers guidance at
https://developers.google.com/search/docs/data-types/dataset#dataset.   However,
example focused on the Science on Schema, FAIR Data, DataONE or other community
principles would be welcome.  

## Resources

If you are looking for tools test SHACL shapes with you should look at the 
W3C Implementation Report (https://w3c.github.io/data-shapes/data-shapes-test-suite/).  
Two of the higer ranking tools are pySHACL (https://github.com/RDFLib/pySHACL)
and TopBraid (https://github.com/TopQuadrant/shacl)

