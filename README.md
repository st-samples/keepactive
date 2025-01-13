Projects currently in my releases

PDF Decrypt Tool 
I made this app to remove security from PDFs easily. It is made for Windows and helps when a PDF is password-protected or has electronic signature error messages. It works for individual files or an entire folder.

Essentially, it runs a PDF through qpdf --decrypt and then uses pdftocairo from the poppler library to reprocess the PDF, copying it with security features removed.

Bulk Word to PDF Converter 
This is a Windows app that converts an entire folder of .doc and .docx files to PDF. This is my primary method of doing these conversions in bulk, and it can be much faster than using Acrobat to do the same task.

The downside is you need Microsoft Office and Adobe Acrobat installed, as it uses Word to silently pass the files to Acrobat for conversion. Acrobat has a built-in tool for this, but I found it to be buggy and unreliable when converting more than a handful of documents.

Keep Active 
I am going to continue working on little projects and updating this site. My current project is an app to take bloated PDFs and reprocess them to quickly reduce file sizes. I think I will be using command-line utilities to deconstruct and reconstruct the PDFs. I also plan to add a feature to set a page size so that it can standardize PDFs at the same time.

Feel free to reach out and say hi if you have a project you want to discuss or if you have any questions about mine