# FlipBookLanguage
A language to generate Flipbooks

You can find the Language description and featues in ProjectReport.pdf

---

Requirements:
You must have python version 3.7+ installed.
---

*Steps to setup:*

1.> Run : pip3 install -r requirements.txt

*Steps to run:*

1.>  python3 main.py falling_apple.flip -o falling_apple.pdf -t pdf

*Usage:*

1.> python main.py *input-file* -o *output-file* [-d *int*] [-r *int*] [-l *int*] [-t *pdf or gif*]

*Options:*

 -o output file
 
 -t pdf/gif format (default pdf)
 
 -d duration between frames in gif (default 400)
 
 -l looping enabled in gif , 0 for disable, 1 for enabled, (default enabled)
 
 -r resolution in pdf (default 100)

