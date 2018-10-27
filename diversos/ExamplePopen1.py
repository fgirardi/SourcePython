import subprocess

def count_lines(website):
    args = ['curl', website]
    args2 = ['wc', '-l']
    process_curl = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
    process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,
                                  stdout=subprocess.PIPE, shell=False)
    # Allow process_curl to receive a SIGPIPE if process_wc exits. 
    process_curl.stdout.close()
    return process_wc.communicate()[0]

print (count_lines("www.google.com"))
