import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True, help="Pushover Token.", type=str)  
    l = parser.parse_args() 
    
    token = l.token
    if token.startswith('"') and token.endswith('"'):
        token = l.token[1:-1]
        print (token)
    print (l.token)