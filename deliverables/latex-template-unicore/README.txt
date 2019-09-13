EU latex template
==================================
This system, implemented as a Makefile, creates an EU deliverable document from
Latex source files. Before using it, please set the PDFVIEWER variable to your
favorite PDF viewer. To generate a PDF simply run

         make all

To clean the directory run

         make clean

Please modify the following files:

frontpages.tex:         cover sheet information such as deliverable title
executive-summary.tex:  the deliverable's executive summary text
authors.tex:            list of authors and institutions
content.tex:            main content
glossary.tex:           glossary terms

That's it!
